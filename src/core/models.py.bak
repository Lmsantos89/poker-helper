#!/usr/bin/env python3
"""
Poker Tournament Helper - Improved Models
Core classes and data structures for the poker helper application.
Includes improvements for starting hand evaluation using precomputed values.
"""
import random
import itertools
import json
import os
from collections import Counter
import multiprocessing
from functools import lru_cache

# Define card constants
SUITS = ['h', 'd', 'c', 's']  # hearts, diamonds, clubs, spades
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
# Precompute rank values for faster lookup
RANK_VALUES = {rank: idx for idx, rank in enumerate(RANKS)}

class Card:
    """
    Represents a playing card with optimized memory usage and comparison operations.
    """
    __slots__ = ('rank', 'suit', 'value')
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUES[rank]  # Precompute the value for faster comparisons
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not other:
            return False
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        # Implement hash for faster set operations and caching
        return hash((self.rank, self.suit))

class PokerHelper:
    """
    Core class that handles poker hand evaluation and decision making.
    """
    def __init__(self):
        # Precompute the deck once
        self.deck = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        # Create a lookup dictionary for faster card retrieval
        self.card_lookup = {f"{rank}{suit}": Card(rank, suit) for rank in RANKS for suit in SUITS}
        # Number of CPU cores for parallel processing
        self.num_cores = max(1, multiprocessing.cpu_count() - 1)  # Leave one core free
        
        # Load precomputed starting hand values
        self.starting_hands = self._load_starting_hands()
        
    def _load_starting_hands(self):
        """Load precomputed starting hand values from JSON file."""
        try:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    'texas_holdem_starting_hands.json')
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Warning: Could not load starting hands file. Using default calculations.")
            return {}
        
    def get_starting_hand_key(self, hole_cards):
        """Get the key for the starting hand in the format used in the JSON file."""
        # Sort cards by rank value (higher first)
        sorted_cards = sorted(hole_cards, key=lambda card: card.value, reverse=True)
        
        # Check if suited
        suited = sorted_cards[0].suit == sorted_cards[1].suit
        
        # Create key in format "A-K" (for unsuited) or "A-Ks" (for suited)
        key = f"{sorted_cards[0].rank}-{sorted_cards[1].rank}"
        if suited and sorted_cards[0].rank != sorted_cards[1].rank:
            key += "s"
            
        return key
        
    def get_starting_hand_strength(self, hole_cards):
        """
        Get the strength category of a starting hand based on precomputed values.
        Returns: 'any', 'mid_late', 'late', or 'unplayable'
        """
        key = self.get_starting_hand_key(hole_cards)
        
        # Handle suited hands by removing the 's' and checking if it exists
        if key.endswith('s'):
            base_key = key[:-1]
            # Suited hands are generally stronger than unsuited
            if base_key in self.starting_hands:
                category = self.starting_hands[base_key]
                # Upgrade the category for suited hands
                if category == 'mid_late':
                    return 'any'
                elif category == 'late':
                    return 'mid_late'
                elif category == 'unplayable':
                    return 'late'
                return category
        
        # For pairs and unsuited hands, check directly
        if key in self.starting_hands:
            return self.starting_hands[key]
            
        # Default to unplayable if not found
        return 'unplayable'
        
    def parse_card(self, card_str):
        """Parse a card string like 'Ah' into a Card object using the lookup table."""
        if not card_str or len(card_str) != 2:
            return None
        
        # Normalize the card string
        card_key = f"{card_str[0].upper()}{card_str[1].lower()}"
        return self.card_lookup.get(card_key)
    
    def calculate_hand_strength(self, hole_cards, num_players, known_community_cards=None):
        """Calculate the strength of the current hand using parallel processing."""
        # For premium starting hands, use higher base values
        # Check for premium pairs (AA, KK, QQ)
        if hole_cards[0].rank == hole_cards[1].rank and hole_cards[0].value >= RANK_VALUES['Q']:
            # AA: 0.85, KK: 0.82, QQ: 0.80
            if hole_cards[0].rank == 'A':
                return 0.85
            elif hole_cards[0].rank == 'K':
                return 0.82
            elif hole_cards[0].rank == 'Q':
                return 0.80
        # Premium non-pairs (AK, AQ)
        elif hole_cards[0].value == RANK_VALUES['A'] or hole_cards[1].value == RANK_VALUES['A']:
            if 'K' in [hole_cards[0].rank, hole_cards[1].rank]:
                return 0.75
            elif 'Q' in [hole_cards[0].rank, hole_cards[1].rank]:
                return 0.72
        
        # For all other hands, use Monte Carlo simulation with optimizations
            
        # Remove hole cards and known community cards from deck
        used_cards = set(hole_cards)
        if known_community_cards:
            used_cards.update(known_community_cards)
            
        # Use set operations for faster filtering
        available_deck = [card for card in self.deck if card not in used_cards]
        
        # Determine number of simulations based on community cards
        # If we have community cards, we need fewer simulations as there's less uncertainty
        base_simulations = 5000
        if known_community_cards:
            # Reduce simulations based on how many community cards we know
            reduction_factor = 0.7 ** len(known_community_cards)  # Exponential reduction
            num_simulations = max(1000, int(base_simulations * reduction_factor))
        else:
            num_simulations = base_simulations
            
        # For small number of players, parallel processing overhead might not be worth it
        if num_players <= 3:
            # For heads-up or 3-player games, we can use fewer simulations
            return self._run_simulation_batch(hole_cards, available_deck, num_players, known_community_cards, 
                                             max(1000, num_simulations // 2))
        
        # Determine number of simulations per process
        simulations_per_process = num_simulations // self.num_cores
        
        # Create a pool of worker processes
        with multiprocessing.Pool(processes=self.num_cores) as pool:
            # Prepare arguments for each worker process
            args = []
            for i in range(self.num_cores):
                # Create a deep copy of the cards to avoid shared references
                hole_cards_copy = [Card(card.rank, card.suit) for card in hole_cards]
                community_cards_copy = None
                if known_community_cards:
                    community_cards_copy = [Card(card.rank, card.suit) for card in known_community_cards]
                
                args.append((hole_cards_copy, available_deck.copy(), num_players, 
                           community_cards_copy, simulations_per_process))
            
            # Run simulations in parallel
            results = pool.starmap(self._run_simulation_batch, args)
            
        # Combine results from all processes
        total_wins = sum(results)
        return total_wins / num_simulations
    
    def _run_simulation_batch(self, hole_cards, available_deck, num_players, known_community_cards, num_simulations):
        """Run a batch of simulations in a separate process."""
        # LRU cache can't be used with unhashable types like lists
        # We'll optimize in other ways
        wins = 0
        
        for _ in range(num_simulations):
            # Shuffle the deck
            random.shuffle(available_deck)
            
            # Deal remaining community cards if needed
            if known_community_cards:
                num_needed = 5 - len(known_community_cards)
                community_cards = known_community_cards + available_deck[:num_needed]
                offset = num_needed
            else:
                community_cards = available_deck[:5]
                offset = 5
            
            # Calculate our best hand
            my_hand_cards = hole_cards + community_cards
            my_best_hand = self._best_hand_value(my_hand_cards)
            
            # Check against other players
            is_winner = True
            
            # Early exit optimization: check if we have a very strong hand
            # If we have a straight flush or four of a kind, we're likely to win
            if my_best_hand >= 7000:  # Four of a kind or better
                wins += 1
                continue
                
            for player in range(num_players - 1):
                # Deal hole cards to opponent
                opponent_hole_cards = [available_deck[offset + player*2], available_deck[offset + player*2 + 1]]
                opponent_hand_cards = opponent_hole_cards + community_cards
                opponent_best_hand = self._best_hand_value(opponent_hand_cards)
                
                if opponent_best_hand > my_best_hand:
                    is_winner = False
                    break
            
            if is_winner:
                wins += 1
        
        return wins
    
    def _best_hand_value(self, cards):
        """Calculate the best 5-card hand value from 7 cards."""
        best_value = 0
        # Only generate combinations if we have more than 5 cards
        if len(cards) > 5:
            for hand in itertools.combinations(cards, 5):
                value = self._evaluate_hand(hand)
                if value > best_value:
                    best_value = value
        else:
            best_value = self._evaluate_hand(cards)
            
        return best_value
    
    def _evaluate_hand(self, hand):
        """Evaluate a 5-card poker hand with optimized calculations."""
        # Extract suits using list comprehension for speed
        suits = [card.suit for card in hand]
        
        # Use precomputed values for faster comparison
        rank_values = [card.value for card in hand]
        
        # Check for flush (all suits the same)
        is_flush = len(set(suits)) == 1
        
        # Check for straight - optimized check
        sorted_values = sorted(rank_values)
        min_val = sorted_values[0]
        max_val = sorted_values[-1]
        is_straight = (max_val - min_val == 4 and len(set(sorted_values)) == 5)
        
        # Special case for A-5 straight (wheel)
        if not is_straight and sorted_values == [0, 1, 2, 3, 12]:  # 2,3,4,5,A
            is_straight = True
            sorted_values = [-1, 0, 1, 2, 3]  # Treat A as 1 for this straight
        
        # Count occurrences of each rank using Counter
        rank_counts = Counter(rank_values)
        counts = sorted(rank_counts.values(), reverse=True)
        
        # Determine hand type and return a score - optimized evaluation order
        if is_straight and is_flush:
            return 8000 + max(sorted_values)  # Straight flush
        elif counts[0] == 4:  # Four of a kind (faster than checking full list)
            return 7000 + [r for r, c in rank_counts.items() if c == 4][0]
        elif counts[0] == 3 and counts[1] == 2:  # Full house (faster check)
            return 6000 + [r for r, c in rank_counts.items() if c == 3][0]
        elif is_flush:
            return 5000 + sum(sorted_values)  # Flush
        elif is_straight:
            return 4000 + max(sorted_values)  # Straight
        elif counts[0] == 3:  # Three of a kind
            return 3000 + [r for r, c in rank_counts.items() if c == 3][0]
        elif counts[0] == 2 and counts[1] == 2:  # Two pair
            pairs = [r for r, c in rank_counts.items() if c == 2]
            return 2000 + max(pairs) * 20 + min(pairs)
        elif counts[0] == 2:  # One pair
            return 1000 + [r for r, c in rank_counts.items() if c == 2][0]
        else:
            return max(rank_values)  # High card
    
    def get_action_recommendation(self, hand_strength, position='middle', big_blinds=None):
        """Recommend an action based on hand strength, position, and stack size."""
        # Special case for premium hands (hand strength > 0.75)
        if hand_strength > 0.75:
            if big_blinds is not None and big_blinds <= 15:
                return "All-In"
            return "Raise"
            
        # Adjust thresholds based on whether this is a Monte Carlo result or fixed value
        # Monte Carlo simulations typically produce lower values (around 0.25-0.35 for decent hands)
        is_monte_carlo = hand_strength < 0.7  # Likely a Monte Carlo result if below 0.7
        
        # If big blinds not provided, use only hand strength and position
        if big_blinds is None:
            if position == 'early':
                if hand_strength > 0.7 or (is_monte_carlo and hand_strength > 0.35):
                    return "Raise"
                elif hand_strength > 0.5 or (is_monte_carlo and hand_strength > 0.28):
                    return "Call"
                else:
                    return "Fold"
            elif position == 'middle':
                if hand_strength > 0.65 or (is_monte_carlo and hand_strength > 0.32):
                    return "Raise"
                elif hand_strength > 0.45 or (is_monte_carlo and hand_strength > 0.25):
                    return "Call"
                else:
                    return "Fold"
            else:  # late position
                if hand_strength > 0.6 or (is_monte_carlo and hand_strength > 0.30):
                    return "Raise"
                elif hand_strength > 0.4 or (is_monte_carlo and hand_strength > 0.22):
                    return "Call"
                else:
                    return "Fold"
        
        # Consider stack size (big blinds) in the decision
        if big_blinds <= 10:  # Short stack strategy
            if hand_strength > 0.5 or (is_monte_carlo and hand_strength > 0.30):
                return "All-In"
            elif (hand_strength > 0.45 or (is_monte_carlo and hand_strength > 0.25)) and position == 'late':
                return "All-In"
            else:
                return "Fold"
        elif big_blinds <= 20:  # Medium stack strategy
            if hand_strength > 0.65 or (is_monte_carlo and hand_strength > 0.32):
                return "Raise"
            elif (hand_strength > 0.5 or (is_monte_carlo and hand_strength > 0.28)) and position != 'early':
                return "Call"
            elif (hand_strength > 0.4 or (is_monte_carlo and hand_strength > 0.24)) and position == 'late':
                return "Call"
            else:
                return "Fold"
        else:  # Large stack strategy
            if position == 'early':
                if hand_strength > 0.7 or (is_monte_carlo and hand_strength > 0.35):
                    return "Raise"
                elif hand_strength > 0.55 or (is_monte_carlo and hand_strength > 0.30):
                    return "Call"
                else:
                    return "Fold"
            elif position == 'middle':
                if hand_strength > 0.65 or (is_monte_carlo and hand_strength > 0.32):
                    return "Raise"
                elif hand_strength > 0.5 or (is_monte_carlo and hand_strength > 0.27):
                    return "Call"
                else:
                    return "Fold"
            else:  # late position
                if hand_strength > 0.6 or (is_monte_carlo and hand_strength > 0.30):
                    return "Raise"
                elif hand_strength > 0.45 or (is_monte_carlo and hand_strength > 0.23):
                    return "Call"
                else:
                    return "Fold"
