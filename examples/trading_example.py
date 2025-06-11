"""Example: submit orders through SimulationOrderManager and observe fills."""
import asyncio
from datetime import datetime, timedelta

import sys
from pathlib import Path

# Allow running example directly
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from bloomberg_terminal.data.feeds.simulation_feed import SimulationFeed
from bloomberg_terminal.trading.oms.simulation_oms import SimulationOrderManager
from bloomberg_terminal.trading.models.orders import Order, OrderSide, OrderType


async def main() -> None:
    feed = SimulationFeed(update_interval=1.0)
    oms = SimulationOrderManager(feed)

    # Simple listener to print executions
    async def print_exec(execution):
        print(
            f"EXEC -> {execution.symbol} {execution.side} {execution.quantity} @ {execution.price} "
            f"({execution.execution_time.strftime('%H:%M:%S')})"
        )

    oms.add_execution_callback(lambda exe: asyncio.create_task(print_exec(exe)))

    # Submit a market BUY and a limit SELL
    market_buy = Order(
        symbol="AAPL",
        side=OrderSide.BUY,
        quantity=100,
        order_type=OrderType.MARKET,
    )
    limit_sell = Order(
        symbol="AAPL",
        side=OrderSide.SELL,
        quantity=100,
        order_type=OrderType.LIMIT,
        limit_price=market_buy.limit_price or 0  # placeholder
    )

    await oms.submit_order(market_buy)
    await oms.submit_order(limit_sell)

    # Let simulation run for 10 seconds
    try:
        await asyncio.sleep(10)
    finally:
        await feed.close()
        print("Positions:", oms.positions)
        print("Cash:", oms.cash)


if __name__ == "__main__":
    asyncio.run(main())
