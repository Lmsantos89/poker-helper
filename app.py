#!/usr/bin/env python3
"""
Poker Tournament Helper - Web Application
A Flask-based web application to help make poker decisions based on probabilities.
Optimized version with performance improvements.
"""
from flask import Flask, request, jsonify, render_template
from models import PokerHelper
from utils import benchmark_performance, get_hand_description, get_stack_description

app = Flask(__name__)

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
        
        # Get additional info
        info = get_hand_description(hand_strength)
        
        # Add stack size context if provided
        if big_blinds is not None:
            info += get_stack_description(big_blinds)
        
        return jsonify({
            'handStrength': round(hand_strength * 100, 2),
            'recommendation': recommendation,
            'info': info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/benchmark')
def run_benchmark():
    """API endpoint to run the benchmark."""
    elapsed_time = benchmark_performance()
    return jsonify({
        'status': 'success',
        'elapsed_time': elapsed_time
    })

if __name__ == '__main__':
    app.run(debug=True)
