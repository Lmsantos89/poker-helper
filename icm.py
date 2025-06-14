#!/usr/bin/env python3
"""
Poker Tournament Helper - ICM Calculator
Independent Chip Model (ICM) calculations for poker tournaments.
"""
import numpy as np
from functools import lru_cache

class ICMCalculator:
    """
    Independent Chip Model (ICM) calculator for poker tournaments.
    Calculates equity distribution based on chip stacks and payouts.
    """
    
    def __init__(self):
        """Initialize the ICM calculator."""
        pass
    
    @lru_cache(maxsize=128)
    def calculate_simple_icm(self, stacks_tuple, payouts_tuple):
        """
        Calculate ICM values using a simple proportional model.
        
        Args:
            stacks_tuple: Tuple of integers representing each player's stack
            payouts_tuple: Tuple of integers representing the prize pool distribution
            
        Returns:
            List of floats representing each player's equity in the prize pool
        """
        # Convert tuples to lists for easier manipulation
        stack_sizes = list(stacks_tuple)
        payouts = list(payouts_tuple)
        
        total_chips = sum(stack_sizes)
        
        # Calculate probability of finishing in each position
        n_players = len(stack_sizes)
        
        # Ensure payouts list is at least as long as the number of players
        if len(payouts) < n_players:
            payouts = payouts + [0] * (n_players - len(payouts))
        
        # Simple ICM calculation (probability of finishing in each position)
        equities = []
        for i, stack in enumerate(stack_sizes):
            equity = 0
            # Probability of finishing first is proportional to stack size
            equity += (stack / total_chips) * payouts[0]
            
            # For remaining positions, use a simplified model
            remaining = 1.0 - (stack / total_chips)
            for j in range(1, min(len(payouts), n_players)):
                # Distribute remaining equity proportionally for lower positions
                position_prob = remaining * (stack / total_chips) * (n_players - j) / n_players
                equity += position_prob * payouts[j]
            
            equities.append(equity)
        
        return equities
    
    def calculate_icm(self, stack_sizes, payouts):
        """
        Calculate ICM values using a more accurate recursive model.
        
        Args:
            stack_sizes: List of integers representing each player's stack
            payouts: List of integers representing the prize pool distribution
            
        Returns:
            List of floats representing each player's equity in the prize pool
        """
        # Convert inputs to tuples for caching
        stacks_tuple = tuple(stack_sizes)
        payouts_tuple = tuple(payouts)
        
        # Use the simple model for now, but could be extended with a more accurate model
        return self.calculate_simple_icm(stacks_tuple, payouts_tuple)
    
    def calculate_icm_pressure(self, stack_sizes, payouts, player_index):
        """
        Calculate ICM pressure for a specific player.
        
        Args:
            stack_sizes: List of integers representing each player's stack
            payouts: List of integers representing the prize pool distribution
            player_index: Index of the player to calculate pressure for
            
        Returns:
            Float between 0 and 1 representing ICM pressure (higher = more pressure)
        """
        # Calculate current ICM equity
        current_equity = self.calculate_icm(stack_sizes, payouts)[player_index]
        
        # Calculate equity if player loses half their stack
        half_stack = stack_sizes.copy()
        half_stack[player_index] = max(1, half_stack[player_index] // 2)
        half_equity = self.calculate_icm(half_stack, payouts)[player_index]
        
        # Calculate equity if player doubles up
        double_stack = stack_sizes.copy()
        double_stack[player_index] = double_stack[player_index] * 2
        double_equity = self.calculate_icm(double_stack, payouts)[player_index]
        
        # Calculate risk/reward ratio
        risk = current_equity - half_equity
        reward = double_equity - current_equity
        
        if reward == 0:
            return 1.0  # Maximum pressure if no reward
        
        # Normalize to 0-1 range
        pressure = min(1.0, risk / reward)
        return pressure
    
    def nash_equilibrium_push_fold(self, stack_sizes, positions, blinds, payouts=None):
        """
        Calculate Nash equilibrium push/fold ranges for a given tournament situation.
        
        Args:
            stack_sizes: List of integers representing each player's stack
            positions: List of strings representing each player's position
            blinds: Tuple of (small_blind, big_blind)
            payouts: Optional list of integers representing the prize pool distribution
            
        Returns:
            Dictionary mapping positions to (push_threshold, call_threshold) tuples
        """
        # This is a simplified model - a full Nash calculator would be much more complex
        # and would require extensive precomputation or simulation
        
        # Default thresholds based on position
        position_thresholds = {
            'btn': (0.5, 0.65),  # (push_threshold, call_threshold)
            'sb': (0.55, 0.7),
            'bb': (0.6, 0.6),
            'utg': (0.7, 0.75),
            'utg+1': (0.65, 0.75),
            'mp': (0.6, 0.7),
            'mp+1': (0.58, 0.68),
            'hj': (0.55, 0.65),
            'co': (0.52, 0.65)
        }
        
        # Adjust thresholds based on stack sizes
        adjusted_thresholds = {}
        for i, (stack, position) in enumerate(zip(stack_sizes, positions)):
            if position in position_thresholds:
                base_push, base_call = position_thresholds[position]
                
                # Adjust for stack size (shorter stacks can push wider)
                bb_stack = stack / blinds[1]
                if bb_stack < 5:
                    push_adj = base_push * 0.7  # Push much wider with very short stack
                    call_adj = base_call * 1.1  # Call tighter with very short stack
                elif bb_stack < 10:
                    push_adj = base_push * 0.8  # Push wider with short stack
                    call_adj = base_call * 1.05  # Call slightly tighter with short stack
                elif bb_stack < 15:
                    push_adj = base_push * 0.9  # Push slightly wider with medium stack
                    call_adj = base_call * 1.0  # Normal calling range with medium stack
                else:
                    push_adj = base_push  # Normal pushing range with big stack
                    call_adj = base_call * 0.95  # Call slightly wider with big stack
                
                # Adjust for ICM if payouts are provided
                if payouts:
                    icm_pressure = self.calculate_icm_pressure(stack_sizes, payouts, i)
                    push_adj *= (1 + icm_pressure * 0.3)  # Push tighter under ICM pressure
                    call_adj *= (1 + icm_pressure * 0.3)  # Call tighter under ICM pressure
                
                adjusted_thresholds[position] = (min(0.9, push_adj), min(0.9, call_adj))
            else:
                # Default values for unknown positions
                adjusted_thresholds[position] = (0.6, 0.7)
        
        return adjusted_thresholds
