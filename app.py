#!/usr/bin/env python3
"""
Poker Tournament Helper - Web Application
A Flask-based web application to help make poker decisions based on probabilities.
Optimized version with performance improvements and ICM calculations.
"""
from flask import Flask, request, jsonify, render_template
from poker_engine import PokerEngine, HandRange
from icm import ICMCalculator
from utils import benchmark_performance, get_hand_description, get_stack_description

app = Flask(__name__)

# Create global instances
poker_engine = PokerEngine()
icm_calculator = ICMCalculator()

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
        
        card1 = poker_engine.parse_card(card1_str)
        card2 = poker_engine.parse_card(card2_str)
        
        if not card1 or not card2:
            return jsonify({'error': 'Invalid hole cards format'}), 400
            
        if str(card1) == str(card2):
            return jsonify({'error': 'Duplicate hole cards'}), 400
        
        # Parse community cards
        community_cards = []
        for card_str in data.get('communityCards', []):
            if card_str:
                card = poker_engine.parse_card(card_str)
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
        
        # Parse tournament stage
        tournament_stage = data.get('tournamentStage', 'middle')
        if tournament_stage not in ['early', 'middle', 'bubble', 'final']:
            tournament_stage = 'middle'
        
        # Parse opponent range if provided
        opponent_range = None
        if 'opponentRange' in data and data['opponentRange']:
            try:
                opponent_range = HandRange(data['opponentRange'])
            except Exception as e:
                return jsonify({'error': f'Invalid opponent range: {str(e)}'}), 400
        
        # Parse ICM data if provided
        icm_pressure = None
        if 'icmData' in data and data['icmData']:
            try:
                icm_data = data['icmData']
                stack_sizes = icm_data.get('stackSizes', [])
                payouts = icm_data.get('payouts', [])
                player_index = icm_data.get('playerIndex', 0)
                
                if stack_sizes and payouts:
                    icm_pressure = icm_calculator.calculate_icm_pressure(stack_sizes, payouts, player_index)
            except Exception as e:
                return jsonify({'warning': f'ICM calculation error: {str(e)}'}), 200
        
        # Calculate hand strength
        hole_cards = [card1, card2]
        
        if community_cards:
            hand_strength = poker_engine.calculate_hand_strength(hole_cards, num_players, community_cards, opponent_range)
        else:
            hand_strength = poker_engine.calculate_hand_strength(hole_cards, num_players, None, opponent_range)
        
        # Get recommendation
        recommendation = poker_engine.get_action_recommendation(
            hand_strength, position, big_blinds, tournament_stage, icm_pressure
        )
        
        # Get additional info
        info = get_hand_description(hand_strength)
        
        # Add stack size context if provided
        if big_blinds is not None:
            info += get_stack_description(big_blinds)
        
        # Add ICM context if available
        if icm_pressure is not None:
            icm_pressure_pct = round(icm_pressure * 100)
            if icm_pressure_pct > 70:
                info += f" ICM pressure is very high ({icm_pressure_pct}%), be cautious."
            elif icm_pressure_pct > 40:
                info += f" Consider ICM pressure ({icm_pressure_pct}%) in your decision."
            else:
                info += f" ICM pressure is low ({icm_pressure_pct}%)."
        
        return jsonify({
            'handStrength': round(hand_strength * 100, 2),
            'recommendation': recommendation,
            'info': info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculate_icm', methods=['POST'])
def calculate_icm():
    """Calculate ICM values for tournament players."""
    try:
        data = request.json
        
        stack_sizes = data.get('stackSizes', [])
        payouts = data.get('payouts', [])
        
        if not stack_sizes or not payouts:
            return jsonify({'error': 'Stack sizes and payouts are required'}), 400
        
        # Calculate ICM values
        icm_values = icm_calculator.calculate_icm(stack_sizes, payouts)
        
        # Calculate ICM pressure for each player
        icm_pressures = []
        for i in range(len(stack_sizes)):
            pressure = icm_calculator.calculate_icm_pressure(stack_sizes, payouts, i)
            icm_pressures.append(round(pressure * 100, 2))
        
        return jsonify({
            'icmValues': [round(val, 2) for val in icm_values],
            'icmPressures': icm_pressures
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/nash_ranges', methods=['POST'])
def nash_ranges():
    """Calculate Nash equilibrium push/fold ranges."""
    try:
        data = request.json
        
        stack_sizes = data.get('stackSizes', [])
        positions = data.get('positions', [])
        blinds = data.get('blinds', [1, 2])
        payouts = data.get('payouts', None)
        
        if not stack_sizes or not positions or len(stack_sizes) != len(positions):
            return jsonify({'error': 'Valid stack sizes and positions are required'}), 400
        
        # Calculate Nash equilibrium ranges
        nash_ranges = icm_calculator.nash_equilibrium_push_fold(stack_sizes, positions, blinds, payouts)
        
        return jsonify({
            'nashRanges': nash_ranges
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
