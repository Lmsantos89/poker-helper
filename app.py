#!/usr/bin/env python3
"""
Poker Tournament Helper - Web Application
A Flask-based web application to help make poker decisions based on probabilities.
"""
from flask import Flask, request, jsonify, render_template
import random
import itertools
from collections import Counter

app = Flask(__name__)

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
        if not other:
            return False
        return self.rank == other.rank and self.suit == other.suit

class PokerHelper:
    def __init__(self):
        self.deck = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        
    def parse_card(self, card_str):
        """Parse a card string like 'Ah' into a Card object."""
        if not card_str or len(card_str) != 2:
            return None
        
        rank, suit = card_str[0].upper(), card_str[1].lower()
        if rank not in RANKS or suit not in SUITS:
            return None
            
        return Card(rank, suit)
    
    def calculate_hand_strength(self, hole_cards, num_players, known_community_cards=None):
        """Calculate the strength of the current hand."""
        # Remove hole cards and known community cards from deck
        used_cards = hole_cards.copy()
        if known_community_cards:
            used_cards.extend(known_community_cards)
            
        available_deck = [card for card in self.deck if not any(str(card) == str(used_card) for used_card in used_cards)]
        
        # Monte Carlo simulation
        num_simulations = 1000
        wins = 0
        
        for _ in range(num_simulations):
            # Shuffle the deck
            random.shuffle(available_deck)
            
            # Deal remaining community cards if needed
            if known_community_cards:
                num_needed = 5 - len(known_community_cards)
                community_cards = known_community_cards + available_deck[:num_needed]
            else:
                community_cards = available_deck[:5]
            
            # Calculate our best hand
            my_best_hand = self._best_hand_value(hole_cards + community_cards)
            
            # Check against other players
            is_winner = True
            offset = 5 if not known_community_cards else num_needed
            
            for player in range(num_players - 1):
                # Deal hole cards to opponent
                opponent_hole_cards = [available_deck[offset + player*2], available_deck[offset + player*2 + 1]]
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
    
    def get_action_recommendation(self, hand_strength, position='middle', big_blinds=None):
        """Recommend an action based on hand strength, position, and stack size.
        
        Args:
            hand_strength: Float between 0 and 1 representing hand strength
            position: String 'early', 'middle', or 'late'
            big_blinds: Integer representing stack size in big blinds
        """
        # If big blinds not provided, use only hand strength and position
        if big_blinds is None:
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
        
        # Consider stack size (big blinds) in the decision
        if big_blinds <= 10:  # Short stack strategy
            if hand_strength > 0.6:
                return "All-In"
            elif hand_strength > 0.45 and position == 'late':
                return "All-In"
            else:
                return "Fold"
        elif big_blinds <= 20:  # Medium stack strategy
            if hand_strength > 0.65:
                return "Raise"
            elif hand_strength > 0.5 and position != 'early':
                return "Call"
            elif hand_strength > 0.4 and position == 'late':
                return "Call"
            else:
                return "Fold"
        else:  # Large stack strategy
            if position == 'early':
                if hand_strength > 0.7:
                    return "Raise"
                elif hand_strength > 0.55:
                    return "Call"
                else:
                    return "Fold"
            elif position == 'middle':
                if hand_strength > 0.65:
                    return "Raise"
                elif hand_strength > 0.5:
                    return "Call"
                else:
                    return "Fold"
            else:  # late position
                if hand_strength > 0.6:
                    return "Raise"
                elif hand_strength > 0.45:
                    return "Call"
                else:
                    return "Fold"

# Create a global instance of the poker helper
poker_helper = PokerHelper()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate hand strength and recommendation."""
    try:
        data = request.json
        
        # Parse number of players
        num_players = int(data.get('numPlayers', 6))
        if num_players < 2 or num_players > 9:
            return jsonify({'error': 'Number of players must be between 2 and 9'}), 400
        
        # Parse hole cards
        card1_str = data.get('card1', '')
        card2_str = data.get('card2', '')
        
        card1 = poker_helper.parse_card(card1_str)
        card2 = poker_helper.parse_card(card2_str)
        
        if not card1 or not card2:
            return jsonify({'error': 'Invalid hole cards format'}), 400
            
        if str(card1) == str(card2):
            return jsonify({'error': 'Duplicate hole cards'}), 400
        
        # Parse community cards
        community_cards = []
        for card_str in data.get('communityCards', []):
            if card_str:
                card = poker_helper.parse_card(card_str)
                if card:
                    if card in [card1, card2] or any(str(card) == str(c) for c in community_cards):
                        return jsonify({'error': 'Duplicate card detected'}), 400
                    community_cards.append(card)
        
        # Parse position
        position = data.get('position', 'middle')
        if position not in ['early', 'middle', 'late']:
            position = 'middle'
        
        # Parse big blinds (stack size)
        big_blinds = None
        if 'bigBlinds' in data and data['bigBlinds']:
            try:
                big_blinds = int(data['bigBlinds'])
                if big_blinds <= 0:
                    return jsonify({'error': 'Big blinds must be a positive number'}), 400
            except ValueError:
                return jsonify({'error': 'Big blinds must be a valid number'}), 400
        
        # Calculate hand strength
        hole_cards = [card1, card2]
        
        if community_cards:
            hand_strength = poker_helper.calculate_hand_strength(hole_cards, num_players, community_cards)
        else:
            hand_strength = poker_helper.calculate_hand_strength(hole_cards, num_players)
        
        # Get recommendation
        recommendation = poker_helper.get_action_recommendation(hand_strength, position, big_blinds)
        
        # Additional info
        if hand_strength > 0.8:
            info = "This is a very strong hand!"
        elif hand_strength > 0.6:
            info = "This is a good hand."
        elif hand_strength > 0.4:
            info = "This is a marginal hand. Consider the pot odds."
        else:
            info = "This is a weak hand. Be cautious."
        
        # Add stack size context if provided
        if big_blinds is not None:
            if big_blinds <= 10:
                info += f" With {big_blinds} BB, you're in push/fold territory."
            elif big_blinds <= 20:
                info += f" With {big_blinds} BB, be selective with your hands."
            else:
                info += f" With {big_blinds} BB, you have room to play strategically."
        
        return jsonify({
            'handStrength': round(hand_strength * 100, 2),
            'recommendation': recommendation,
            'info': info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
