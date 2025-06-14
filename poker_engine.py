#!/usr/bin/env python3
"""
Poker Tournament Helper - Enhanced Poker Engine
Uses treys library for hand evaluation and implements ICM calculations.
"""
import random
import itertools
from collections import Counter
import multiprocessing
from functools import lru_cache
import json
import os

try:
    from treys import Card as TreysCard
    from treys import Evaluator as TreysEvaluator
    TREYS_AVAILABLE = True
except ImportError:
    TREYS_AVAILABLE = False
    print("Warning: treys library not available. Using built-in evaluator.")

# Define card constants
SUITS = ['h', 'd', 'c', 's']  # hearts, diamonds, clubs, spades
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
# Precompute rank values for faster lookup
RANK_VALUES = {rank: idx for idx, rank in enumerate(RANKS)}

# Mapping for converting between our card format and treys format
SUIT_MAPPING = {'h': 'h', 'd': 'd', 'c': 'c', 's': 's'}
RANK_MAPPING = {
    '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    'T': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
}

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
    
    def to_treys_card(self):
        """Convert to treys card format if available."""
        if TREYS_AVAILABLE:
            return TreysCard.new(f"{self.rank}{self.suit}")
        return None

class HandRange:
    """
    Represents a range of starting hands in poker.
    Can parse common range notations like "22+", "ATs+", etc.
    """
    def __init__(self, range_str=None):
        self.hands = set()
        if range_str:
            self.parse_range(range_str)
    
    def parse_range(self, range_str):
        """Parse a range string into a set of hands."""
        # Split by commas if multiple ranges are provided
        parts = [p.strip() for p in range_str.split(',')]
        
        for part in parts:
            # Handle pair ranges like "22+"
            if len(part) >= 3 and part[0] == part[1] and part[2] == '+':
                start_rank = part[0]
                start_idx = RANKS.index(start_rank)
                for rank in RANKS[start_idx:]:
                    self.add_pair(rank)
            
            # Handle suited ranges like "ATs+"
            elif len(part) >= 4 and part[2] == 's' and part[3] == '+':
                high_rank, low_rank = part[0], part[1]
                high_idx = RANKS.index(high_rank)
                low_idx = RANKS.index(low_rank)
                
                for i in range(low_idx, high_idx):
                    self.add_suited(high_rank, RANKS[i])
            
            # Handle offsuit ranges like "ATo+"
            elif len(part) >= 4 and part[2] == 'o' and part[3] == '+':
                high_rank, low_rank = part[0], part[1]
                high_idx = RANKS.index(high_rank)
                low_idx = RANKS.index(low_rank)
                
                for i in range(low_idx, high_idx):
                    self.add_offsuit(high_rank, RANKS[i])
            
            # Handle specific pairs like "AA"
            elif len(part) == 2 and part[0] == part[1]:
                self.add_pair(part[0])
            
            # Handle specific suited hands like "AKs"
            elif len(part) == 3 and part[2] == 's':
                self.add_suited(part[0], part[1])
            
            # Handle specific offsuit hands like "AKo"
            elif len(part) == 3 and part[2] == 'o':
                self.add_offsuit(part[0], part[1])
            
            # Handle any version of a hand like "AK"
            elif len(part) == 2:
                self.add_suited(part[0], part[1])
                self.add_offsuit(part[0], part[1])
    
    def add_pair(self, rank):
        """Add all combinations of a pair to the range."""
        for s1, s2 in itertools.combinations(SUITS, 2):
            self.hands.add((f"{rank}{s1}", f"{rank}{s2}"))
    
    def add_suited(self, high_rank, low_rank):
        """Add all suited combinations of two ranks to the range."""
        for suit in SUITS:
            self.hands.add((f"{high_rank}{suit}", f"{low_rank}{suit}"))
    
    def add_offsuit(self, high_rank, low_rank):
        """Add all offsuit combinations of two ranks to the range."""
        for s1, s2 in itertools.product(SUITS, SUITS):
            if s1 != s2:
                self.hands.add((f"{high_rank}{s1}", f"{low_rank}{s2}"))
    
    def get_random_hand(self):
        """Get a random hand from the range."""
        if not self.hands:
            return None
        return random.choice(list(self.hands))
    
    def __len__(self):
        return len(self.hands)

class PokerEngine:
    """
    Enhanced poker engine that uses treys for hand evaluation when available
    and implements ICM calculations.
    """
    def __init__(self):
        # Precompute the deck once
        self.deck = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        # Create a lookup dictionary for faster card retrieval
        self.card_lookup = {f"{rank}{suit}": Card(rank, suit) for rank in RANKS for suit in SUITS}
        # Number of CPU cores for parallel processing
        self.num_cores = max(1, multiprocessing.cpu_count() - 1)  # Leave one core free
        
        # Initialize treys evaluator if available
        self.treys_evaluator = TreysEvaluator() if TREYS_AVAILABLE else None
        
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
    
    def calculate_hand_strength(self, hole_cards, num_players, known_community_cards=None, opponent_range=None):
        """
        Calculate the strength of the current hand using parallel processing.
        
        Args:
            hole_cards: List of Card objects representing the player's hole cards
            num_players: Number of players at the table
            known_community_cards: Optional list of Card objects for known community cards
            opponent_range: Optional HandRange object representing opponent's range
            
        Returns:
            float: Hand strength as a value between 0 and 1
        """
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
                                             max(1000, num_simulations // 2), opponent_range)
        
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
                           community_cards_copy, simulations_per_process, opponent_range))
            
            # Run simulations in parallel
            results = pool.starmap(self._run_simulation_batch, args)
            
        # Combine results from all processes
        total_wins = sum(results)
        return total_wins / num_simulations
    
    def _run_simulation_batch(self, hole_cards, available_deck, num_players, known_community_cards, num_simulations, opponent_range=None):
        """Run a batch of simulations in a separate process."""
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
            
            # Use treys evaluator if available, otherwise use our built-in evaluator
            if TREYS_AVAILABLE and self.treys_evaluator:
                my_treys_hand = [card.to_treys_card() for card in hole_cards]
                board_cards = [card.to_treys_card() for card in community_cards]
                my_score = self.treys_evaluator.evaluate(board_cards, my_treys_hand)
                # Note: In treys, lower scores are better
            else:
                my_best_hand = self._best_hand_value(my_hand_cards)
            
            # Check against other players
            is_winner = True
            
            # Early exit optimization: check if we have a very strong hand with our evaluator
            if not TREYS_AVAILABLE and my_best_hand >= 7000:  # Four of a kind or better
                wins += 1
                continue
                
            for player in range(num_players - 1):
                # Deal hole cards to opponent based on range if provided
                if opponent_range and len(opponent_range) > 0:
                    # Get a random hand from the opponent's range
                    opponent_cards = opponent_range.get_random_hand()
                    if opponent_cards:
                        opponent_hole_cards = [self.parse_card(opponent_cards[0]), self.parse_card(opponent_cards[1])]
                    else:
                        # Fallback to random cards if range is empty
                        opponent_hole_cards = [available_deck[offset + player*2], available_deck[offset + player*2 + 1]]
                else:
                    # Use random cards from the deck
                    opponent_hole_cards = [available_deck[offset + player*2], available_deck[offset + player*2 + 1]]
                
                opponent_hand_cards = opponent_hole_cards + community_cards
                
                # Use treys evaluator if available
                if TREYS_AVAILABLE and self.treys_evaluator:
                    opponent_treys_hand = [card.to_treys_card() for card in opponent_hole_cards]
                    opponent_score = self.treys_evaluator.evaluate(board_cards, opponent_treys_hand)
                    # In treys, lower scores are better
                    if opponent_score < my_score:
                        is_winner = False
                        break
                else:
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
    
    def get_action_recommendation(self, hand_strength, position='middle', big_blinds=None, tournament_stage='middle', icm_pressure=None):
        """
        Recommend an action based on hand strength, position, stack size, and tournament factors.
        
        Args:
            hand_strength: Float between 0 and 1 representing hand strength
            position: String 'early', 'middle', or 'late'
            big_blinds: Integer representing stack size in big blinds
            tournament_stage: String 'early', 'middle', 'bubble', or 'final'
            icm_pressure: Float between 0 and 1 representing ICM pressure (higher = more pressure)
            
        Returns:
            String: Recommended action ('Fold', 'Call', 'Raise', 'All-In')
        """
        # Special case for premium hands (hand strength > 0.75)
        if hand_strength > 0.75:
            if big_blinds is not None and big_blinds <= 15:
                return "All-In"
            return "Raise"
            
        # Adjust thresholds based on whether this is a Monte Carlo result or fixed value
        # Monte Carlo simulations typically produce lower values (around 0.25-0.35 for decent hands)
        is_monte_carlo = hand_strength < 0.7  # Likely a Monte Carlo result if below 0.7
        
        # Adjust for tournament stage and ICM pressure
        icm_factor = 1.0
        if tournament_stage == 'bubble' or icm_pressure is not None:
            # On the bubble or with high ICM pressure, we need stronger hands to commit chips
            if icm_pressure is not None:
                icm_factor = 1.0 + icm_pressure * 0.5  # Increase threshold by up to 50%
            else:
                icm_factor = 1.2  # Default 20% increase on the bubble
        elif tournament_stage == 'early':
            # Early in tournaments, we can be more conservative
            icm_factor = 1.1
        elif tournament_stage == 'final':
            # At final table, we need to be more aggressive
            icm_factor = 0.9
        
        # If big blinds not provided, use only hand strength and position
        if big_blinds is None:
            if position == 'early':
                if hand_strength > 0.7 / icm_factor or (is_monte_carlo and hand_strength > 0.35 / icm_factor):
                    return "Raise"
                elif hand_strength > 0.5 / icm_factor or (is_monte_carlo and hand_strength > 0.28 / icm_factor):
                    return "Call"
                else:
                    return "Fold"
            elif position == 'middle':
                if hand_strength > 0.65 / icm_factor or (is_monte_carlo and hand_strength > 0.32 / icm_factor):
                    return "Raise"
                elif hand_strength > 0.45 / icm_factor or (is_monte_carlo and hand_strength > 0.25 / icm_factor):
                    return "Call"
                else:
                    return "Fold"
            else:  # late position
                if hand_strength > 0.6 / icm_factor or (is_monte_carlo and hand_strength > 0.30 / icm_factor):
                    return "Raise"
                elif hand_strength > 0.4 / icm_factor or (is_monte_carlo and hand_strength > 0.22 / icm_factor):
                    return "Call"
                else:
                    return "Fold"
        
        # Consider stack size (big blinds) in the decision
        if big_blinds <= 10:  # Short stack strategy
            if hand_strength > 0.5 / icm_factor or (is_monte_carlo and hand_strength > 0.30 / icm_factor):
                return "All-In"
            elif (hand_strength > 0.45 / icm_factor or (is_monte_carlo and hand_strength > 0.25 / icm_factor)) and position == 'late':
                return "All-In"
            else:
                return "Fold"
        elif big_blinds <= 20:  # Medium stack strategy
            if hand_strength > 0.65 / icm_factor or (is_monte_carlo and hand_strength > 0.32 / icm_factor):
                return "Raise"
            elif (hand_strength > 0.5 / icm_factor or (is_monte_carlo and hand_strength > 0.28 / icm_factor)) and position != 'early':
                return "Call"
            elif (hand_strength > 0.4 / icm_factor or (is_monte_carlo and hand_strength > 0.24 / icm_factor)) and position == 'late':
                return "Call"
            else:
                return "Fold"
        else:  # Large stack strategy
            if position == 'early':
                if hand_strength > 0.7 / icm_factor or (is_monte_carlo and hand_strength > 0.35 / icm_factor):
                    return "Raise"
                elif hand_strength > 0.55 / icm_factor or (is_monte_carlo and hand_strength > 0.30 / icm_factor):
                    return "Call"
                else:
                    return "Fold"
            elif position == 'middle':
                if hand_strength > 0.65 / icm_factor or (is_monte_carlo and hand_strength > 0.32 / icm_factor):
                    return "Raise"
                elif hand_strength > 0.5 / icm_factor or (is_monte_carlo and hand_strength > 0.27 / icm_factor):
                    return "Call"
                else:
                    return "Fold"
            else:  # late position
                if hand_strength > 0.6 / icm_factor or (is_monte_carlo and hand_strength > 0.30 / icm_factor):
                    return "Raise"
                elif hand_strength > 0.45 / icm_factor or (is_monte_carlo and hand_strength > 0.23 / icm_factor):
                    return "Call"
                else:
                    return "Fold"
    
    def calculate_icm(self, stack_sizes, payouts):
        """
        Calculate Independent Chip Model (ICM) values for tournament players.
        
        Args:
            stack_sizes: List of integers representing each player's stack
            payouts: List of integers representing the prize pool distribution
            
        Returns:
            List of floats representing each player's equity in the prize pool
        """
        # Simple ICM implementation
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
