"""
Order models and related enums for the trading system.
"""
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal


class OrderSide(str, Enum):
    """Order side (buy or sell)."""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Order types."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"
    ICEBERG = "ICEBERG"
    TWAP = "TWAP"
    VWAP = "VWAP"


class TimeInForce(str, Enum):
    """Time in force for orders."""
    DAY = "DAY"  # Good for the day
    GTC = "GTC"  # Good Till Canceled
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill
    GTD = "GTD"  # Good Till Date
    OPG = "OPG"  # At the Opening
    CLS = "CLS"  # At the Close


class OrderStatus(str, Enum):
    """Order status."""
    NEW = "NEW"
    PENDING_NEW = "PENDING_NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    DONE_FOR_DAY = "DONE_FOR_DAY"
    CANCELED = "CANCELED"
    PENDING_CANCEL = "PENDING_CANCEL"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    PENDING_REPLACE = "PENDING_REPLACE"
    REPLACED = "REPLACED"
    STOPPED = "STOPPED"
    SUSPENDED = "SUSPENDED"
    CALCULATED = "CALCULATED"
    HELD = "HELD"


class Order(BaseModel):
    """Base order model."""
    # Required fields
    symbol: str = Field(..., description="Trading symbol")
    side: OrderSide = Field(..., description="Buy or sell")
    quantity: Decimal = Field(..., gt=0, description="Order quantity")
    order_type: OrderType = Field(..., description="Order type")
    
    # Optional fields with defaults
    limit_price: Optional[Decimal] = Field(None, description="Limit price for limit orders")
    stop_price: Optional[Decimal] = Field(None, description="Stop price for stop orders")
    time_in_force: TimeInForce = Field(TimeInForce.DAY, description="Time in force")
    
    # Order metadata
    client_order_id: str = Field(default_factory=lambda: f"order_{datetime.utcnow().timestamp()}",
                               description="Client-assigned order ID")
    order_id: Optional[str] = Field(None, description="Exchange-assigned order ID")
    status: OrderStatus = Field(OrderStatus.NEW, description="Current order status")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Order creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    
    # Execution details
    filled_quantity: Decimal = Field(Decimal(0), description="Filled quantity")
    avg_fill_price: Optional[Decimal] = Field(None, description="Average fill price")
    
    # Additional parameters
    params: Dict[str, Any] = Field(default_factory=dict, description="Additional order parameters")
    
    class Config:
        json_encoders = {
            Decimal: lambda v: str(v),
            datetime: lambda v: v.isoformat(),
        }
    
    @validator('quantity', 'limit_price', 'stop_price', 'filled_quantity', 'avg_fill_price', pre=True)
    def parse_decimal(cls, v):
        """Parse string numbers to Decimal."""
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        if isinstance(v, str):
            return Decimal(v)
        return v
    
    @property
    def is_active(self) -> bool:
        """Check if the order is still active."""
        return self.status in [
            OrderStatus.NEW,
            OrderStatus.PARTIALLY_FILLED,
            OrderStatus.PENDING_NEW,
            OrderStatus.PENDING_CANCEL,
            OrderStatus.PENDING_REPLACE,
        ]
    
    @property
    def remaining_quantity(self) -> Decimal:
        """Calculate remaining quantity to be filled."""
        return self.quantity - self.filled_quantity
    
    def update_status(self, status: OrderStatus, **kwargs) -> None:
        """Update order status and related fields."""
        self.status = status
        self.updated_at = datetime.utcnow()
        
        # Update relevant fields based on status
        if status == OrderStatus.FILLED:
            self.filled_quantity = self.quantity
        
        # Update any provided fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class OrderExecution(BaseModel):
    """Order execution details."""
    execution_id: str
    order_id: str
    client_order_id: str
    symbol: str
    side: OrderSide
    price: Decimal
    quantity: Decimal
    execution_time: datetime
    exchange_order_id: Optional[str] = None
    commission: Optional[Decimal] = None
    commission_asset: Optional[str] = None
    trade_id: Optional[str] = None
    is_maker: bool = False
    
    class Config:
        json_encoders = {
            Decimal: lambda v: str(v),
            datetime: lambda v: v.isoformat(),
        }


class OrderBookUpdate(BaseModel):
    """Order book update message."""
    symbol: str
    bids: List[List[Decimal]]  # [price, quantity, count?]
    asks: List[List[Decimal]]  # [price, quantity, count?]
    timestamp: datetime
    
    class Config:
        json_encoders = {
            Decimal: lambda v: str(v),
            datetime: lambda v: v.isoformat(),
        }
