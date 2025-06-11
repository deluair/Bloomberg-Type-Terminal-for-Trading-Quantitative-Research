"""
Base classes for Order Management System (OMS).
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Callable, Any, Set
from datetime import datetime
import asyncio
from decimal import Decimal

from ...data.models.base import MarketData
from ..models.orders import Order, OrderStatus, OrderExecution, OrderBookUpdate


class OrderListener(ABC):
    """Interface for order event listeners."""
    
    @abstractmethod
    async def on_order_status(self, order: Order) -> None:
        """Called when an order status changes."""
        pass
    
    @abstractmethod
    async def on_execution(self, execution: OrderExecution) -> None:
        """Called when an order is executed."""
        pass
    
    @abstractmethod
    async def on_order_book_update(self, update: OrderBookUpdate) -> None:
        """Called when the order book is updated."""
        pass


class BaseOrderManager(ABC):
    """Base class for order management systems."""
    
    def __init__(self):
        self._listeners: Set[OrderListener] = set()
        self._order_callbacks: Dict[str, List[Callable[[Order], None]]] = {}
        self._execution_callbacks: List[Callable[[OrderExecution], None]] = []
        self._order_book_callbacks: List[Callable[[OrderBookUpdate], None]] = []
        self._orders: Dict[str, Order] = {}
        self._executions: Dict[str, List[OrderExecution]] = {}
    
    def add_listener(self, listener: OrderListener) -> None:
        """Add an order event listener."""
        self._listeners.add(listener)
    
    def remove_listener(self, listener: OrderListener) -> None:
        """Remove an order event listener."""
        self._listeners.discard(listener)
    
    def add_order_callback(
        self, 
        order_id: str, 
        callback: Callable[[Order], None]
    ) -> None:
        """Add a callback for a specific order."""
        if order_id not in self._order_callbacks:
            self._order_callbacks[order_id] = []
        self._order_callbacks[order_id].append(callback)
    
    def add_execution_callback(
        self, 
        callback: Callable[[OrderExecution], None]
    ) -> None:
        """Add a callback for all executions."""
        self._execution_callbacks.append(callback)
    
    def add_order_book_callback(
        self,
        callback: Callable[[OrderBookUpdate], None]
    ) -> None:
        """Add a callback for order book updates."""
        self._order_book_callbacks.append(callback)
    
    async def _notify_order_status(self, order: Order) -> None:
        """Notify all listeners and callbacks of an order status change."""
        # Update internal state
        self._orders[order.client_order_id] = order
        
        # Notify listeners
        tasks = []
        for listener in self._listeners:
            tasks.append(asyncio.create_task(listener.on_order_status(order)))
        
        # Notify order-specific callbacks
        if order.client_order_id in self._order_callbacks:
            for callback in self._order_callbacks[order.client_order_id]:
                tasks.append(asyncio.create_task(callback(order)))
        
        # Wait for all notifications to complete
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _notify_execution(self, execution: OrderExecution) -> None:
        """Notify all listeners and callbacks of an execution."""
        # Update internal state
        if execution.order_id not in self._executions:
            self._executions[execution.order_id] = []
        self._executions[execution.order_id].append(execution)
        
        # Notify listeners
        tasks = [
            asyncio.create_task(listener.on_execution(execution))
            for listener in self._listeners
        ]
        
        # Notify execution callbacks
        tasks.extend([
            asyncio.create_task(callback(execution))
            for callback in self._execution_callbacks
        ])
        
        # Wait for all notifications to complete
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _notify_order_book_update(self, update: OrderBookUpdate) -> None:
        """Notify all listeners and callbacks of an order book update."""
        # Notify listeners
        tasks = [
            asyncio.create_task(listener.on_order_book_update(update))
            for listener in self._listeners
        ]
        
        # Notify order book callbacks
        tasks.extend([
            asyncio.create_task(callback(update))
            for callback in self._order_book_callbacks
        ])
        
        # Wait for all notifications to complete
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    @abstractmethod
    async def submit_order(self, order: Order) -> str:
        """Submit a new order.
        
        Args:
            order: The order to submit
            
        Returns:
            The order ID assigned by the exchange
        """
        pass
    
    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order.
        
        Args:
            order_id: The ID of the order to cancel
            
        Returns:
            True if the cancel request was successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def replace_order(
        self, 
        order_id: str, 
        **changes
    ) -> Optional[Order]:
        """Modify an existing order.
        
        Args:
            order_id: The ID of the order to modify
            **changes: Fields to update (e.g., quantity, limit_price)
            
        Returns:
            The updated order, or None if the order couldn't be modified
        """
        pass
    
    @abstractmethod
    async def get_order(self, order_id: str) -> Optional[Order]:
        """Get order details.
        
        Args:
            order_id: The ID of the order to retrieve
            
        Returns:
            The order, or None if not found
        """
        pass
    
    @abstractmethod
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Get all open orders.
        
        Args:
            symbol: Optional symbol to filter by
            
        Returns:
            List of open orders
        """
        pass
    
    @abstractmethod
    async def get_executions(
        self, 
        order_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[OrderExecution]:
        """Get order executions.
        
        Args:
            order_id: Optional order ID to filter by
            start_time: Optional start time filter
            end_time: Optional end time filter
            
        Returns:
            List of order executions matching the criteria
        """
        pass
