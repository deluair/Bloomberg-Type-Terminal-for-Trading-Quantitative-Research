"""
Yahoo Finance data feed for real market data.
"""
import asyncio
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Callable
import pandas as pd
import numpy as np
from ..models.base import MarketData, AssetClass, DataFrequency, MarketDataFeed


class YahooMarketData(MarketData):
    """Extended market data model for Yahoo Finance."""
    bid: Optional[float] = None
    ask: Optional[float] = None
    last: Optional[float] = None
    volume: int = 0
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None


class YahooFinanceFeed(MarketDataFeed):
    """Yahoo Finance market data feed that provides real market data."""
    
    def __init__(
        self,
        symbols: Optional[List[str]] = None,
        update_interval: float = 60.0,  # Update every minute for real data
    ):
        """Initialize the Yahoo Finance feed.
        
        Args:
            symbols: List of symbols to track
            update_interval: Time between updates in seconds
        """
        self.symbols = symbols or ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"]
        self.update_interval = update_interval
        
        # Cache for storing latest data
        self._latest_data: Dict[str, YahooMarketData] = {}
        
        # Subscriptions
        self._subscribers: Dict[str, Set[Callable[[MarketData], None]]] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None
    
    def get_real_time_data(self, symbols: List[str]) -> Dict[str, YahooMarketData]:
        """Fetch real-time data from Yahoo Finance."""
        try:
            tickers = yf.Tickers(' '.join(symbols))
            data = {}
            
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    hist = ticker.history(period='2d', interval='1m')
                    
                    if hist.empty:
                        continue
                    
                    # Get latest data point
                    latest = hist.iloc[-1]
                    previous_close = info.get('previousClose', latest['Close'])
                    
                    # Calculate change
                    current_price = latest['Close']
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
                    
                    # Estimate bid/ask from spread (typical spread is 0.1-0.5% for liquid stocks)
                    spread_pct = 0.002  # 0.2% spread estimate
                    spread = current_price * spread_pct
                    bid = current_price - spread/2
                    ask = current_price + spread/2
                    
                    data[symbol] = YahooMarketData(
                        symbol=symbol,
                        timestamp=datetime.now(),
                        asset_class=AssetClass.EQUITY,
                        exchange=info.get('exchange', 'NASDAQ'),
                        currency=info.get('currency', 'USD'),
                        bid=bid,
                        ask=ask,
                        last=current_price,
                        open=latest['Open'],
                        high=latest['High'],
                        low=latest['Low'],
                        close=current_price,
                        volume=int(latest['Volume']),
                        change=change,
                        change_percent=change_percent,
                        market_cap=info.get('marketCap'),
                        pe_ratio=info.get('trailingPE')
                    )
                    
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {e}")
                    continue
                    
            return data
            
        except Exception as e:
            print(f"Error fetching Yahoo Finance data: {e}")
            return {}
    
    async def _update_loop(self):
        """Main update loop for fetching real-time data."""
        while self._running:
            try:
                # Fetch data for all subscribed symbols
                all_symbols = set()
                for symbols in self._subscribers.keys():
                    all_symbols.add(symbols)
                
                if all_symbols:
                    # Convert set to list for API call
                    symbol_list = list(all_symbols)
                    new_data = self.get_real_time_data(symbol_list)
                    
                    # Update cache and notify subscribers
                    for symbol, market_data in new_data.items():
                        self._latest_data[symbol] = market_data
                        
                        # Notify subscribers
                        if symbol in self._subscribers:
                            for callback in self._subscribers[symbol]:
                                try:
                                    if asyncio.iscoroutinefunction(callback):
                                        await callback(market_data)
                                    else:
                                        callback(market_data)
                                except Exception as e:
                                    print(f"Error in callback: {e}")
                
                # Wait before next update
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                print(f"Error in update loop: {e}")
                await asyncio.sleep(self.update_interval)
    
    async def connect(self) -> None:
        """Start the data feed."""
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._update_loop())
    
    async def subscribe(
        self,
        symbols: List[str],
        fields: List[str],
        callback: Optional[Callable[[MarketData], None]] = None
    ) -> None:
        """Subscribe to market data.
        
        Args:
            symbols: List of symbols to subscribe to
            fields: List of fields to subscribe to (ignored - Yahoo provides all fields)
            callback: Optional callback function to receive updates
        """
        for symbol in symbols:
            if symbol not in self._subscribers:
                self._subscribers[symbol] = set()
            if callback:
                self._subscribers[symbol].add(callback)
    
    def get_latest_data(self, symbol: str) -> Optional[YahooMarketData]:
        """Get the latest cached data for a symbol."""
        return self._latest_data.get(symbol)
    
    def get_latest_price(self, symbol: str) -> Optional[float]:
        """Get the latest price for a symbol."""
        data = self._latest_data.get(symbol)
        return data.last if data else None
    
    async def get_historical_data(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        frequency: DataFrequency = DataFrequency.DAILY,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Get historical market data from Yahoo Finance."""
        try:
            # Convert frequency to Yahoo Finance format
            freq_map = {
                DataFrequency.MINUTE: '1m',
                DataFrequency.HOUR: '1h',
                DataFrequency.DAILY: '1d',
                DataFrequency.WEEKLY: '1wk',
                DataFrequency.MONTHLY: '1mo',
            }
            
            interval = freq_map.get(frequency, '1d')
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(start=start, end=end, interval=interval)
            
            if hist.empty:
                return []
            
            result = []
            for date, row in hist.iterrows():
                result.append({
                    'symbol': symbol,
                    'timestamp': date.to_pydatetime(),
                    'open': row['Open'],
                    'high': row['High'],
                    'low': row['Low'],
                    'close': row['Close'],
                    'volume': int(row['Volume']),
                })
            
            return result
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return []
    
    async def close(self) -> None:
        """Stop the data feed."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None 