"""
Simulation-based Order Management System (OMS) implementation.
This OMS interacts with the `SimulationFeed` to provide realistic order routing,
matching, execution, and P&L tracking entirely offline.
"""
from __future__ import annotations

import asyncio
import logging
import random
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set

from ...data.feeds.simulation_feed import SimulationMarketData
from ...data.models.base import MarketData
from ..models.orders import (
    Order,
    OrderExecution,
    OrderSide,
    OrderStatus,
    OrderType,
)
from .base import BaseOrderManager

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# ---------------------------------------------------------------------------
# Simulation OMS
# ---------------------------------------------------------------------------


class SimulationOrderManager(BaseOrderManager):
    """A fully-featured Order Management System for the simulation environment."""

    def __init__(
        self,
        data_feed: Any,
        *,
        default_slippage: float = 0.0005,  # 5 bps
        default_commission: float = 0.0005,  # 5 bps
        limit_fill_probability: float = 0.9,
    ) -> None:
        super().__init__()
        self.data_feed = data_feed
        self.default_slippage = Decimal(str(default_slippage))
        self.default_commission = Decimal(str(default_commission))
        self.limit_fill_probability = limit_fill_probability

        # Internal state
        self._symbols: Set[str] = set()
        self._initialized_feed: bool = False
        self._order_counter: int = 0
        self._executions: Dict[str, List[OrderExecution]] = {}

        # Portfolio state
        self.positions: Dict[str, Decimal] = {}
        self.cash: Decimal = Decimal("1000000")  # 1m starting cash.

    # ---------------------------------------------------------------------
    # Market-data handling
    # ---------------------------------------------------------------------

    async def _ensure_feed_subscription(self, symbol: str) -> None:
        """Subscribe to market-data for *symbol* if not already."""
        if symbol in self._symbols:
            return

        self._symbols.add(symbol)
        await self.data_feed.subscribe([symbol], ["BID", "ASK", "LAST"], self._on_market_data)
        if not self._initialized_feed:
            await self.data_feed.connect()
            self._initialized_feed = True

    async def _on_market_data(self, data: MarketData) -> None:  # noqa: D401
        """Callback triggered on each new `SimulationMarketData` tick."""
        if not isinstance(data, SimulationMarketData):
            return

        symbol = data.symbol
        # Attempt to match any active orders for this symbol
        await self._match_open_orders(symbol, data)

    # ---------------------------------------------------------------------
    # Order matching helpers
    # ---------------------------------------------------------------------

    async def _match_open_orders(self, symbol: str, mkt: SimulationMarketData) -> None:
        """Try to fill open orders against the latest market-data."""
        open_orders = [
            o
            for o in self._orders.values()
            if o.symbol == symbol and o.is_active and o.remaining_quantity > 0
        ]

        for order in open_orders:
            if order.order_type == OrderType.MARKET:
                await self._fill_market_order(order, mkt)
            elif order.order_type == OrderType.LIMIT:
                await self._fill_limit_order(order, mkt)
            elif order.order_type == OrderType.STOP:
                await self._fill_stop_order(order, mkt)
            elif order.order_type == OrderType.STOP_LIMIT:
                await self._fill_stop_limit_order(order, mkt)

    # ---- Individual order-type handlers ---------------------------------

    async def _fill_market_order(self, order: Order, mkt: SimulationMarketData) -> None:
        """Fill market order immediately with slippage."""
        price = Decimal(str(mkt.ask if order.side == OrderSide.BUY else mkt.bid))
        if price <= 0:
            return  # can't price
        slp = (1 + self.default_slippage) if order.side == OrderSide.BUY else (1 - self.default_slippage)
        await self._execute_order(order, price * Decimal(str(slp)), order.remaining_quantity)

    async def _fill_limit_order(self, order: Order, mkt: SimulationMarketData) -> None:
        if order.limit_price is None:
            return
        ask = Decimal(str(mkt.ask)) if mkt.ask else None
        bid = Decimal(str(mkt.bid)) if mkt.bid else None
        if order.side == OrderSide.BUY and ask is not None and ask <= order.limit_price:
            if random.random() < self.limit_fill_probability:
                await self._execute_order(order, ask, order.remaining_quantity)
        elif order.side == OrderSide.SELL and bid is not None and bid >= order.limit_price:
            if random.random() < self.limit_fill_probability:
                await self._execute_order(order, bid, order.remaining_quantity)

    async def _fill_stop_order(self, order: Order, mkt: SimulationMarketData) -> None:
        if order.stop_price is None:
            return
        last = Decimal(str(mkt.last)) if mkt.last else None
        if last is None:
            return
        if order.side == OrderSide.BUY and last >= order.stop_price:
            await self._execute_order(order, last, order.remaining_quantity)
        elif order.side == OrderSide.SELL and last <= order.stop_price:
            await self._execute_order(order, last, order.remaining_quantity)

    async def _fill_stop_limit_order(self, order: Order, mkt: SimulationMarketData) -> None:
        if order.limit_price is None or order.stop_price is None:
            return
        last = Decimal(str(mkt.last)) if mkt.last else None
        if last is None:
            return
        ask = Decimal(str(mkt.ask)) if mkt.ask else None
        bid = Decimal(str(mkt.bid)) if mkt.bid else None
        if order.side == OrderSide.BUY and last >= order.stop_price and ask is not None and ask <= order.limit_price:
            await self._execute_order(order, ask, order.remaining_quantity)
        elif order.side == OrderSide.SELL and last <= order.stop_price and bid is not None and bid >= order.limit_price:
            await self._execute_order(order, bid, order.remaining_quantity)

    # ---------------------------------------------------------------------
    # Execution and bookkeeping
    # ---------------------------------------------------------------------

    async def _execute_order(self, order: Order, price: Decimal, qty: Decimal) -> None:
        """Mark an *order* as executed for *qty* at *price*. Handles P&L."""
        qty = min(qty, order.remaining_quantity)
        notional = price * qty
        commission = notional * self.default_commission

        # Update order fields
        order.filled_quantity += qty
        order.avg_fill_price = (
            price if order.avg_fill_price is None else (
                (order.avg_fill_price * (order.filled_quantity - qty) + price * qty) / order.filled_quantity
            )
        )
        order.status = OrderStatus.FILLED if order.remaining_quantity == 0 else OrderStatus.PARTIALLY_FILLED
        order.updated_at = datetime.utcnow()

        # Portfolio adjustments
        pos_delta = qty if order.side == OrderSide.BUY else -qty
        self.positions[order.symbol] = self.positions.get(order.symbol, Decimal("0")) + pos_delta
        cash_delta = -notional if order.side == OrderSide.BUY else notional
        self.cash += cash_delta - commission

        # Build execution object
        exec_msg = OrderExecution(
            execution_id=f"exec_{uuid.uuid4().hex}",
            order_id=order.order_id or order.client_order_id,
            client_order_id=order.client_order_id,
            symbol=order.symbol,
            side=order.side,
            price=price,
            quantity=qty,
            execution_time=datetime.utcnow(),
            commission=commission,
            commission_asset="USD",
            is_maker=False,
        )
        self._executions.setdefault(order.order_id, []).append(exec_msg)

        # Fire notifications
        await self._notify_order_status(order)
        await self._notify_execution(exec_msg)

        logger.info(
            "EXEC | %s | %s %s @ %s (filled %.2f/%.2f)",
            order.order_id,
            order.side,
            order.symbol,
            price,
            order.filled_quantity,
            order.quantity,
        )

    # ---------------------------------------------------------------------
    # BaseOrderManager abstract-method overrides
    # ---------------------------------------------------------------------

    async def submit_order(self, order: Order) -> str:
        if not order.order_id:
            self._order_counter += 1
            order.order_id = f"SIM{self._order_counter:08d}"
        self._orders[order.client_order_id] = order
        await self._notify_order_status(order)
        await self._ensure_feed_subscription(order.symbol)
        return order.order_id

    async def cancel_order(self, order_id: str) -> bool:
        for o in self._orders.values():
            if o.order_id == order_id and o.is_active:
                o.status = OrderStatus.CANCELED
                o.updated_at = datetime.utcnow()
                await self._notify_order_status(o)
                return True
        return False

    async def replace_order(self, order_id: str, **changes) -> Optional[Order]:
        order = next((o for o in self._orders.values() if o.order_id == order_id), None)
        if order is None or not order.is_active:
            return None
        # Apply changes
        for k, v in changes.items():
            if hasattr(order, k):
                setattr(order, k, v)
        order.status = OrderStatus.PENDING_REPLACE
        order.updated_at = datetime.utcnow()
        await self._notify_order_status(order)
        return order

    async def get_order(self, order_id: str) -> Optional[Order]:
        return next((o for o in self._orders.values() if o.order_id == order_id), None)

    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        return [
            o for o in self._orders.values() if o.is_active and (symbol is None or o.symbol == symbol)
        ]

    async def get_executions(
        self,
        order_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[OrderExecution]:
        if order_id:
            execs = self._executions.get(order_id, [])
        else:
            # Flatten all executions
            execs = [e for lst in self._executions.values() for e in lst]
        if start_time:
            execs = [e for e in execs if e.execution_time >= start_time]
        if end_time:
            execs = [e for e in execs if e.execution_time <= end_time]
        return execs
