"""Core Risk-Management interfaces and a very small VaR implementation.

This module is intentionally lightweight: enough structure to plug in more
sophisticated models later while already giving the rest of the terminal a risk
API to depend on.
"""
from __future__ import annotations

import abc
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Protocol

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Interfaces
# ---------------------------------------------------------------------------


class PositionProvider(Protocol):
    """Anything that can return current positions as {symbol: quantity}."""

    def get_positions(self) -> Dict[str, Decimal]:
        ...


class PriceProvider(Protocol):
    """Anything that can return the latest *price* for a symbol."""

    def get_price(self, symbol: str) -> Decimal:  # noqa: D401
        """Return latest mid-price for *symbol*."""
        ...


# ---------------------------------------------------------------------------
# Simple Historical VaR
# ---------------------------------------------------------------------------


@dataclass
class VaRResult:
    value_at_risk: Decimal
    confidence: float
    window: int
    timestamp: datetime


class HistoricalVaRCalculator(abc.ABC):
    """Base-class for historical Value-at-Risk calculation."""

    def __init__(self, confidence: float = 0.99, window: int = 252):
        self.confidence = confidence
        self.window = window

    @abc.abstractmethod
    def compute_var(self) -> VaRResult:  # pragma: no cover – abstract
        """Return latest VaR figure."""
        raise NotImplementedError


class PortfolioHistoricalVaR(HistoricalVaRCalculator):
    """Very small portfolio VaR implementation (non-parametric)."""

    def __init__(
        self,
        positions: PositionProvider,
        prices: PriceProvider,
        historical_prices: pd.DataFrame,
        confidence: float = 0.99,
        window: int = 252,
    ) -> None:
        super().__init__(confidence, window)
        self._positions_provider = positions
        self._price_provider = prices
        self._hist_prices = historical_prices  # wide DF: index-date, columns-symbols

    def compute_var(self) -> VaRResult:  # noqa: D401
        # Slice last *window* days of returns
        px = self._hist_prices.iloc[-self.window :]
        rets = px.pct_change().dropna()
        if rets.empty:
            return VaRResult(Decimal("0"), self.confidence, self.window, datetime.utcnow())

        # Portfolio daily PnL vector
        pos = self._positions_provider.get_positions()
        w = np.array([float(pos.get(sym, 0)) for sym in px.columns])
        price_last = px.iloc[-1].values.astype(float)
        pnl_series = (rets.values * (w * price_last)).sum(axis=1)

        # Historical VaR at given percentile
        var_value = np.percentile(-pnl_series, self.confidence * 100)
        return VaRResult(
            value_at_risk=Decimal(str(var_value)),
            confidence=self.confidence,
            window=self.window,
            timestamp=datetime.utcnow(),
        )
