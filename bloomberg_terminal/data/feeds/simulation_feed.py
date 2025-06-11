"""
Simulation market data feed for testing and development.
"""
import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Callable
import numpy as np
import pandas as pd
from ..models.base import MarketData, AssetClass, DataFrequency, MarketDataFeed


class SimulationMarketData(MarketData):
    """Extended market data model for simulation."""
    bid: Optional[float] = None
    ask: Optional[float] = None
    last: Optional[float] = None
    volume: int = 0
    open_interest: Optional[int] = None
    
    # For order book simulation
    bids: Optional[Dict[float, int]] = None  # price -> size
    asks: Optional[Dict[float, int]] = None  # price -> size


class SimulationFeed(MarketDataFeed):
    """Simulation market data feed that generates realistic market data."""
    
    def __init__(
        self,
        symbols: Optional[List[str]] = None,
        initial_prices: Optional[Dict[str, float]] = None,
        volatility: float = 0.02,  # Daily volatility (2%)
        tick_size: float = 0.01,
        lot_size: int = 100,
        update_interval: float = 1.0,  # seconds
    ):
        """Initialize the simulation feed.
        
        Args:
            symbols: List of symbols to simulate
            initial_prices: Optional dict of {symbol: price} for initial prices
            volatility: Daily price volatility (standard deviation of returns)
            tick_size: Minimum price movement
            lot_size: Standard lot size
            update_interval: Time between updates in seconds
        """
        self.symbols = symbols or ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
        self.volatility = volatility
        self.tick_size = tick_size
        self.lot_size = lot_size
        self.update_interval = update_interval
        
        # Initialize price data
        self._prices = initial_prices or {
            sym: round(random.uniform(100, 500), 2) for sym in self.symbols
        }
        
        # Subscriptions
        self._subscribers: Dict[str, Set[Callable[[MarketData], None]]] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        # Market hours simulation
        self.market_open = datetime.utcnow().replace(hour=13, minute=30, second=0, microsecond=0)  # 9:30 AM ET
        self.market_close = datetime.utcnow().replace(hour=20, minute=0, second=0, microsecond=0)  # 4:00 PM ET
    
    def _generate_market_data(self, symbol: str) -> SimulationMarketData:
        """Generate a new market data point for the given symbol."""
        current_price = self._prices[symbol]
        
        # Generate price movement using geometric brownian motion
        dt = self.update_interval / (6.5 * 60 * 60)  # Trading day in hours
        drift = 0.0  # No drift for now
        shock = random.gauss(0, 1) * self.volatility * np.sqrt(dt)
        
        new_price = current_price * np.exp(drift + shock)
        
        # Round to nearest tick
        new_price = round(new_price / self.tick_size) * self.tick_size
        
        # Update price
        self._prices[symbol] = new_price
        
        # Generate order book
        spread = self.tick_size * random.randint(1, 5)  # 1-5 ticks spread
        bid = new_price - spread/2
        ask = new_price + spread/2
        
        # Generate random sizes
        bid_size = random.randint(1, 20) * self.lot_size
        ask_size = random.randint(1, 20) * self.lot_size
        
        # Generate order book levels (5 levels)
        bids = {}
        asks = {}
        
        for i in range(5):
            price_level = bid - i * self.tick_size
            size = max(1, int(bid_size * (0.5 ** i) * random.uniform(0.8, 1.2)))
            bids[round(price_level, 2)] = size
            
            price_level = ask + i * self.tick_size
            size = max(1, int(ask_size * (0.5 ** i) * random.uniform(0.8, 1.2)))
            asks[round(price_level, 2)] = size
        
        return SimulationMarketData(
            symbol=symbol,
            timestamp=datetime.utcnow(),
            asset_class=AssetClass.EQUITY,
            exchange="SIM",
            currency="USD",
            bid=bid,
            ask=ask,
            last=new_price,
            volume=random.randint(100, 10000),
            bids=bids,
            asks=asks,
        )
    
    async def connect(self) -> None:
        """Start the simulation."""
        if self._running:
            return
            
        self._running = True
        self._task = asyncio.create_task(self._run())
    
    async def _run(self) -> None:
        """Main simulation loop."""
        while self._running:
            now = datetime.utcnow()
            
            # Only generate data during market hours
            if (now.weekday() < 5 and  # Monday-Friday
                self.market_open.time() <= now.time() <= self.market_close.time()):
                
                for symbol in self._subscribers.keys():
                    data = self._generate_market_data(symbol)
                    await self._notify_subscribers(data)
            
            await asyncio.sleep(self.update_interval)
    
    async def _notify_subscribers(self, data: MarketData) -> None:
        """Notify all subscribers of new market data."""
        if data.symbol not in self._subscribers:
            return
            
        for callback in list(self._subscribers[data.symbol]):
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                print(f"Error in subscriber callback: {e}")
    
    async def subscribe(
        self,
        symbols: List[str],
        fields: List[str],
        callback: Optional[Callable[[MarketData], None]] = None
    ) -> None:
        """Subscribe to market data.
        
        Args:
            symbols: List of symbols to subscribe to
            fields: List of fields to subscribe to (ignored in simulation)
            callback: Optional callback function to receive updates
        """
        for symbol in symbols:
            if symbol not in self._subscribers:
                self._subscribers[symbol] = set()
            if callback:
                self._subscribers[symbol].add(callback)
    
    async def get_historical_data(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        frequency: DataFrequency = DataFrequency.DAILY,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate historical market data."""
        # Convert frequency to pandas frequency string
        freq_map = {
            DataFrequency.TICK: '1s',
            DataFrequency.SECOND: '1s',
            DataFrequency.MINUTE: '1min',
            DataFrequency.HOUR: '1h',
            DataFrequency.DAILY: '1D',
            DataFrequency.WEEKLY: '1W',
            DataFrequency.MONTHLY: '1M',
            DataFrequency.QUARTERLY: '3M',
            DataFrequency.YEARLY: '1Y',
        }
        
        # Generate date range
        dates = pd.date_range(start, end, freq=freq_map[frequency])
        
        # Generate random walk
        n = len(dates)
        if n == 0:
            return []
            
        # Start with initial price if available, otherwise random
        initial_price = self._prices.get(symbol, random.uniform(100, 500))
        
        # Generate random returns
        if frequency == DataFrequency.TICK or frequency == DataFrequency.SECOND:
            vol = self.volatility / np.sqrt(6.5 * 60 * 60)  # Scale volatility to per-second
        elif frequency == DataFrequency.MINUTE:
            vol = self.volatility / np.sqrt(6.5 * 60)  # Scale volatility to per-minute
        elif frequency == DataFrequency.HOUR:
            vol = self.volatility / np.sqrt(6.5)  # Scale volatility to per-hour
        else:
            vol = self.volatility  # Daily or lower frequency
        
        # Generate random walk
        returns = np.random.normal(0, vol, n-1)
        prices = [initial_price]
        
        for r in returns:
            prices.append(prices[-1] * (1 + r))
        
        # Round to tick size
        prices = [round(p / self.tick_size) * self.tick_size for p in prices]
        
        # Create result
        result = []
        for i, (date, price) in enumerate(zip(dates, prices)):
            # Add some noise to OHLC
            o = price * random.uniform(0.995, 1.005)
            h = max(o, price * random.uniform(1.0, 1.01))
            l = min(o, price * random.uniform(0.99, 1.0))
            c = price * random.uniform(0.995, 1.005)
            
            # Round to 2 decimal places
            o, h, l, c = [round(p, 2) for p in [o, h, l, c]]
            
            result.append({
                'symbol': symbol,
                'timestamp': date.to_pydatetime(),
                'open': o,
                'high': h,
                'low': l,
                'close': c,
                'volume': random.randint(1000, 1000000),
            })
        
        return result
    
    async def close(self) -> None:
        """Stop the simulation."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
