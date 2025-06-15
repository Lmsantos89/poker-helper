#!/usr/bin/env python3
"""
Poker Tournament Helper - Models
This module is now a wrapper around poker_engine.py to maintain backward compatibility.
All new code should use poker_engine.py directly.
"""

# Import from poker_engine to maintain backward compatibility
from src.core.poker_engine import (
    Card,
    PokerEngine as PokerHelper,  # Alias for backward compatibility
    SUITS,
    RANKS,
    RANK_VALUES,
    HandRange
)

# Warning about deprecation
import warnings
warnings.warn(
    "The models module is deprecated and will be removed in a future version. "
    "Please use src.core.poker_engine instead.",
    DeprecationWarning,
    stacklevel=2
)
