"""
Example script demonstrating the use of the simulation market data feed.
"""
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Add the project root to the Python path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from bloomberg_terminal.data.feeds.simulation_feed import SimulationFeed


class MarketDataPrinter:
    """Simple class to print market data updates."""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
    
    def __call__(self, data: Any) -> None:
        """Print market data update."""
        print(f"\n{self.symbol} Update:")
        print(f"  Time:    {data.timestamp}")
        print(f"  Bid/Ask: {data.bid:.2f} / {data.ask:.2f}")
        print(f"  Last:    {data.last:.2f}")
        print(f"  Volume:  {data.volume:,}")
        
        if data.bids and data.asks:
            print("\n  Order Book:")
            print("  --------")
            print("  Bids (Price x Size)")
            for price, size in sorted(data.bids.items(), reverse=True)[:5]:
                print(f"  {price:.2f} x {size:,}")
            
            print("\n  Asks (Price x Size)")
            for price, size in sorted(data.asks.items())[:5]:
                print(f"  {price:.2f} x {size:,}")


async def run_simulation() -> None:
    """Run the simulation example."""
    print("Starting market data simulation...")
    
    # Create and start the simulation feed
    symbols = ["AAPL", "MSFT", "GOOGL"]
    feed = SimulationFeed(symbols=symbols, update_interval=2.0)  # 2-second updates
    
    # Create and register callbacks
    printers = {symbol: MarketDataPrinter(symbol) for symbol in symbols}
    
    # Subscribe to all symbols
    for symbol, printer in printers.items():
        await feed.subscribe([symbol], ["BID", "ASK", "LAST"], printer)
    
    # Start the feed
    await feed.connect()
    
    # Get some historical data
    print("\nFetching historical data...")
    end = datetime.utcnow()
    start = end - timedelta(days=30)
    
    for symbol in symbols:
        print(f"\nHistorical data for {symbol}:")
        historical = await feed.get_historical_data(
            symbol=symbol,
            start=start,
            end=end,
            frequency="DAILY"
        )
        
        # Print the first 5 days
        for i, data in enumerate(historical[:5]):
            print(f"  {data['timestamp'].strftime('%Y-%m-%d')}: "
                  f"O:{data['open']:.2f} H:{data['high']:.2f} "
                  f"L:{data['low']:.2f} C:{data['close']:.2f} "
                  f"V:{data['volume']:,}")
    
    # Run for a while to see real-time updates
    print("\nStarting real-time updates (press Ctrl+C to stop)...")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping simulation...")
    finally:
        await feed.close()


if __name__ == "__main__":
    asyncio.run(run_simulation())
