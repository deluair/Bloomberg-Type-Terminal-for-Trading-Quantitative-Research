"""
Base models and interfaces for market data.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field


class AssetClass(str, Enum):
    """Supported asset classes."""
    EQUITY = "EQUITY"
    FIXED_INCOME = "FIXED_INCOME"
    FX = "FX"
    COMMODITY = "COMMODITY"
    CRYPTO = "CRYPTO"
    DERIVATIVE = "DERIVATIVE"


class DataFrequency(str, Enum):
    """Data frequency types."""
    TICK = "TICK"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"


class MarketData(BaseModel):
    """Base class for all market data models."""
    symbol: str = Field(..., description="Unique identifier for the security")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the data point")
    asset_class: AssetClass = Field(..., description="Asset class of the security")
    exchange: Optional[str] = Field(None, description="Exchange where the security is traded")
    currency: str = Field("USD", description="Currency of the price")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        extra = "allow"  # Allow extra fields for flexibility


class MarketDataFeed(ABC):
    """Abstract base class for market data feeds."""
    
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the data feed."""
        pass
    
    @abstractmethod
    async def subscribe(self, symbols: List[str], fields: List[str]) -> None:
        """Subscribe to market data for given symbols and fields.
        
        Args:
            symbols: List of symbols to subscribe to
            fields: List of fields to subscribe to (e.g., ['BID', 'ASK', 'LAST'])
        """
        pass
    
    @abstractmethod
    async def get_historical_data(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        frequency: DataFrequency = DataFrequency.DAILY,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Retrieve historical market data.
        
        Args:
            symbol: Security symbol
            start: Start datetime
            end: End datetime
            frequency: Data frequency
            **kwargs: Additional parameters specific to the data feed
            
        Returns:
            List of market data points
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the connection to the data feed."""
        pass
