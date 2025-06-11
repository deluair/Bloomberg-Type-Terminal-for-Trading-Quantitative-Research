"""Minimal event-driven backtesting engine skeleton.

Provides just enough structure to plug trading strategies and run against the
`SimulationFeed` + `SimulationOrderManager` without any real broker.
"""
from __future__ import annotations

import asyncio
import logging
from collections import deque
from datetime import datetime
from decimal import Decimal
from typing import Deque, Dict, List, Protocol, Union

from ...data.feeds.simulation_feed import SimulationFeed, SimulationMarketData
from ...trading.oms.simulation_oms import SimulationOrderManager
from ...trading.models.orders import Order, OrderSide, OrderType

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# ---------------------------------------------------------------------------
# Interfaces
# ---------------------------------------------------------------------------


class Strategy(Protocol):
    """Any strategy must implement *on_tick* and optionally *on_start/stop*."""

    async def on_start(self, engine: "BacktestEngine") -> None:
        ...

    async def on_tick(self, tick: SimulationMarketData, engine: "BacktestEngine") -> None:
        ...

    async def on_stop(self, engine: "BacktestEngine") -> None:
        ...


# ---------------------------------------------------------------------------
# Backtest Engine
# ---------------------------------------------------------------------------


class BacktestEngine:
    """Extremely small event-driven backtester."""

    def __init__(self, symbols: List[str], strategy: Strategy, *, update_interval: float = 1.0) -> None:
        self.symbols = symbols
        self.strategy = strategy
        self.feed = SimulationFeed(symbols=symbols, update_interval=update_interval)
        self.oms = SimulationOrderManager(self.feed)
        self._running: bool = False
        self._tick_q: Deque[SimulationMarketData] = deque()

    # ---------------------------------------------------------------------
    # Control helpers
    # ---------------------------------------------------------------------

    async def start(self) -> None:
        if self._running:
            return
        self._running = True

        await self.feed.connect()
        for sym in self.symbols:
            await self.feed.subscribe([sym], ["BID", "ASK", "LAST"], self._on_tick)

        await self.strategy.on_start(self)

        # Main loop: process ticks as they arrive
        try:
            while self._running:
                while self._tick_q:
                    tick = self._tick_q.popleft()
                    await self.strategy.on_tick(tick, self)
                await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            pass
        finally:
            await self.strategy.on_stop(self)
            await self.feed.close()

    async def stop(self) -> None:
        self._running = False

    # ---------------------------------------------------------------------
    # Callbacks / order helpers
    # ---------------------------------------------------------------------

    async def _on_tick(self, data: SimulationMarketData):
        self._tick_q.append(data)

    # Convenience wrappers around OMS
    async def send_order(
        self,
        symbol: str,
        side: OrderSide,
        qty: Union[int, Decimal],
        order_type: OrderType = OrderType.MARKET,
        **kwargs,
    ) -> str:
        order = Order(symbol=symbol, side=side, quantity=Decimal(str(qty)), order_type=order_type, **kwargs)
        return await self.oms.submit_order(order)

    # ---------------------------------------------------------------------
    # PnL snapshot
    # ---------------------------------------------------------------------

    def portfolio_value(self) -> Decimal:  # noqa: D401
        value = self.oms.cash
        for sym, pos in self.oms.positions.items():
            mid = Decimal(str(self.feed._prices.get(sym, 0)))
            value += pos * mid
        return value
