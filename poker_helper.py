#!/usr/bin/env python3
"""
Poker Tournament Helper
A tool to help make poker decisions based on probabilities.
"""
import random
import itertools
from collections import Counter

# Define card constants
SUITS = ['h', 'd', 'c', 's']  # hearts, diamonds, clubs, spades
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

class PokerHelper:
    def __init__(self):
        self.deck = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        
    def parse_card(self, card_str):
        """Parse a card string like 'Ah' into a Card object."""
        if len(card_str) != 2:
            raise ValueError(f"Invalid card format: {card_str}. Use format like 'Ah' for Ace of hearts.")
        rank, suit = card_str[0].upper(), card_str[1].lower()
        if rank not in RANKS:
            raise ValueError(f"Invalid rank: {rank}. Valid ranks are: {', '.join(RANKS)}")
        if suit not in SUITS:
            raise ValueError(f"Invalid suit: {suit}. Valid suits are: {', '.join(SUITS)}")
        return Card(rank, suit)
    
    def calculate_hand_strength(self, hole_cards, num_players):
        """Calculate the strength of the current hand."""
        # Remove hole cards from deck
        available_deck = [card for card in self.deck if card not in hole_cards]
        
        # Monte Carlo simulation
        num_simulations = 1000
        wins = 0
        
        for _ in range(num_simulations):
            # Shuffle the deck
            random.shuffle(available_deck)
            
            # Deal community cards
            community_cards = available_deck[:5]
            
            # Calculate our best hand
            my_best_hand = self._best_hand_value(hole_cards + community_cards)
            
            # Check against other players
            is_winner = True
            for player in range(num_players - 1):
                # Deal hole cards to opponent
                opponent_hole_cards = [available_deck[5 + player*2], available_deck[6 + player*2]]
                opponent_best_hand = self._best_hand_value(opponent_hole_cards + community_cards)
                
                if opponent_best_hand > my_best_hand:
                    is_winner = False
                    break
            
            if is_winner:
                wins += 1
        
        return wins / num_simulations
    
    def _best_hand_value(self, cards):
        """Calculate the best 5-card hand value from 7 cards."""
        best_value = 0
        for hand in itertools.combinations(cards, 5):
            value = self._evaluate_hand(hand)
            if value > best_value:
                best_value = value
        return best_value
    
    def _evaluate_hand(self, hand):
        """Evaluate a 5-card poker hand."""
        ranks = [card.rank for card in hand]
        suits = [card.suit for card in hand]
        
        # Convert ranks to values for comparison
        rank_values = [RANKS.index(rank) for rank in ranks]
        
        # Check for flush
        is_flush = len(set(suits)) == 1
        
        # Check for straight
        sorted_values = sorted(rank_values)
        is_straight = (sorted_values == list(range(min(sorted_values), max(sorted_values) + 1)))
        
        # Special case for A-5 straight
        if sorted_values == [0, 1, 2, 3, 12]:  # 2,3,4,5,A
            is_straight = True
            sorted_values = [-1, 0, 1, 2, 3]  # Treat A as 1 for this straight
        
        # Count occurrences of each rank
        rank_counts = Counter(rank_values)
        counts = sorted(rank_counts.values(), reverse=True)
        
        # Determine hand type and return a score
        if is_straight and is_flush:
            return 8000 + max(sorted_values)  # Straight flush
        elif counts == [4, 1]:
            return 7000 + [r for r, c in rank_counts.items() if c == 4][0]  # Four of a kind
        elif counts == [3, 2]:
            return 6000 + [r for r, c in rank_counts.items() if c == 3][0]  # Full house
        elif is_flush:
            return 5000 + sum(sorted_values)  # Flush
        elif is_straight:
            return 4000 + max(sorted_values)  # Straight
        elif counts == [3, 1, 1]:
            return 3000 + [r for r, c in rank_counts.items() if c == 3][0]  # Three of a kind
        elif counts == [2, 2, 1]:
            pairs = [r for r, c in rank_counts.items() if c == 2]
            return 2000 + max(pairs) * 20 + min(pairs)  # Two pair
        elif counts == [2, 1, 1, 1]:
            return 1000 + [r for r, c in rank_counts.items() if c == 2][0]  # One pair
        else:
            return max(rank_values)  # High card
    
    def get_action_recommendation(self, hand_strength, position='middle'):
        """Recommend an action based on hand strength and position."""
        if position == 'early':
            if hand_strength > 0.7:
                return "Raise"
            elif hand_strength > 0.5:
                return "Call"
            else:
                return "Fold"
        elif position == 'middle':
            if hand_strength > 0.65:
                return "Raise"
            elif hand_strength > 0.45:
                return "Call"
            else:
                return "Fold"
        else:  # late position
            if hand_strength > 0.6:
                return "Raise"
            elif hand_strength > 0.4:
                return "Call"
            else:
                return "Fold"

def main():
    print("=" * 50)
    print("Poker Tournament Helper")
    print("=" * 50)
    
    helper = PokerHelper()
    
    try:
        # Get number of players
        num_players = int(input("Enter number of players at the table (2-9): "))
        if num_players < 2 or num_players > 9:
            print("Number of players must be between 2 and 9.")
            return
        
        # Get hole cards
        print("\nEnter your hole cards (e.g., 'Ah Kd' for Ace of hearts and King of diamonds)")
        print("Valid ranks: 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A")
        print("Valid suits: h (hearts), d (diamonds), c (clubs), s (spades)")
        
        hole_cards_input = input("Your cards: ")
        card_strings = hole_cards_input.split()
        
        if len(card_strings) != 2:
            print("You must enter exactly 2 cards.")
            return
        
        hole_cards = [helper.parse_card(card) for card in card_strings]
        
        # Get position
        print("\nWhat is your position?")
        print("1. Early (first few to act)")
        print("2. Middle")
        print("3. Late (button or close to it)")
        position_choice = input("Choose position (1-3): ")
        
        position_map = {
            '1': 'early',
            '2': 'middle',
            '3': 'late'
        }
        
        position = position_map.get(position_choice, 'middle')
        
        print("\nCalculating probabilities...")
        hand_strength = helper.calculate_hand_strength(hole_cards, num_players)
        
        print(f"\nHand strength: {hand_strength:.2%}")
        recommendation = helper.get_action_recommendation(hand_strength, position)
        
        print(f"Recommended action: {recommendation}")
        
        # Additional information
        if hand_strength > 0.8:
            print("This is a very strong hand!")
        elif hand_strength > 0.6:
            print("This is a good hand.")
        elif hand_strength > 0.4:
            print("This is a marginal hand. Consider the pot odds.")
        else:
            print("This is a weak hand. Be cautious.")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
