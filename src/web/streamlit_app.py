#!/usr/bin/env python3
"""
Poker Tournament Helper - Streamlit Web Interface
A Streamlit-based web application for the poker tournament helper.

This module provides an alternative web interface using Streamlit, which offers:
- Interactive widgets for input
- Real-time calculation updates
- Data visualization components
- Mobile-friendly responsive design
"""
from typing import Dict, List, Any, Optional, Union, Tuple
import streamlit as st
import pandas as pd
import numpy as np
import time
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.poker_engine import PokerEngine, HandRange, Card
from src.core.icm import ICMCalculator
from src.utils.helpers import get_hand_description, get_stack_description, hand_range_to_percentage

# Initialize the poker engine and ICM calculator
poker_engine = PokerEngine()
icm_calculator = ICMCalculator()

# Define constants
SUITS = ['h', 'd', 'c', 's']
RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
POSITIONS = ['early', 'middle', 'late']
TOURNAMENT_STAGES = ['early', 'middle', 'bubble', 'final']

# Set page config
st.set_page_config(
    page_title="Poker Tournament Helper",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🃏 Poker Tournament Helper")
st.markdown("""
This tool helps you make better decisions in poker tournaments by calculating hand strength, 
providing action recommendations, and analyzing ICM implications.
""")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Hand Analyzer", "ICM Calculator", "Nash Ranges"])

# Tab 1: Hand Analyzer
with tab1:
    st.header("Hand Strength & Action Recommendation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Hand")
        
        # Card selection
        card_col1, card_col2 = st.columns(2)
        
        with card_col1:
            rank1 = st.selectbox("Card 1 Rank", RANKS, key="rank1")
            suit1 = st.selectbox("Card 1 Suit", ["h (♥)", "d (♦)", "c (♣)", "s (♠)"], key="suit1")
            suit1 = suit1[0]  # Extract first character
        
        with card_col2:
            rank2 = st.selectbox("Card 2 Rank", RANKS, key="rank2")
            suit2 = st.selectbox("Card 2 Suit", ["h (♥)", "d (♦)", "c (♣)", "s (♠)"], key="suit2")
            suit2 = suit2[0]  # Extract first character
        
        # Table information
        num_players = st.slider("Number of Players", 2, 9, 6)
        position = st.selectbox("Your Position", POSITIONS)
        big_blinds = st.number_input("Your Stack (in BB)", min_value=1, max_value=500, value=20)
        tournament_stage = st.selectbox("Tournament Stage", TOURNAMENT_STAGES)
        
        # Community cards
        st.subheader("Community Cards (optional)")
        use_community = st.checkbox("Enter community cards")
        
        community_cards = []
        if use_community:
            comm_cols = st.columns(5)
            for i, col in enumerate(comm_cols):
                with col:
                    use_card = st.checkbox(f"Card {i+1}", key=f"use_comm_{i}")
                    if use_card:
                        comm_rank = st.selectbox(f"Rank {i+1}", RANKS, key=f"comm_rank_{i}")
                        comm_suit = st.selectbox(f"Suit {i+1}", ["h (♥)", "d (♦)", "c (♣)", "s (♠)"], key=f"comm_suit_{i}")
                        comm_suit = comm_suit[0]  # Extract first character
                        community_cards.append(f"{comm_rank}{comm_suit}")
        
        # Opponent range
        st.subheader("Opponent Range (optional)")
        use_range = st.checkbox("Specify opponent range")
        opponent_range = None
        if use_range:
            range_str = st.text_input("Range (e.g., 'AA,KK,QQ,AKs')", "")
            if range_str:
                try:
                    opponent_range = HandRange(range_str)
                    st.info(f"Range contains approximately {hand_range_to_percentage(range_str):.1f}% of starting hands")
                except Exception as e:
                    st.error(f"Invalid range format: {str(e)}")
        
        # ICM considerations
        st.subheader("ICM Considerations (optional)")
        use_icm = st.checkbox("Include ICM calculations")
        icm_pressure = None
        if use_icm:
            num_players_icm = st.slider("Number of Players Remaining", 2, 9, min(num_players, 6), key="icm_players")
            
            # Stack sizes
            st.write("Stack Sizes (in BB)")
            stack_cols = st.columns(num_players_icm)
            stack_sizes = []
            for i, col in enumerate(stack_cols):
                with col:
                    if i == 0:
                        # First player is the user
                        st.write(f"You: {big_blinds}")
                        stack_sizes.append(big_blinds)
                    else:
                        stack = st.number_input(f"P{i+1}", min_value=1, max_value=500, value=20, key=f"stack_{i}")
                        stack_sizes.append(stack)
            
            # Payouts
            st.write("Payouts")
            num_payouts = st.slider("Number of Payouts", 1, num_players_icm, min(3, num_players_icm))
            payout_cols = st.columns(num_payouts)
            payouts = []
            for i, col in enumerate(payout_cols):
                with col:
                    if i == 0:
                        payout = st.number_input(f"1st", min_value=1, value=100, key=f"payout_{i}")
                    else:
                        payout = st.number_input(f"{i+1}{'st' if i==0 else 'nd' if i==1 else 'rd' if i==2 else 'th'}", 
                                               min_value=1, value=max(1, 100 // (i+1)), key=f"payout_{i}")
                    payouts.append(payout)
            
            # Calculate ICM pressure
            if st.button("Calculate ICM Pressure"):
                try:
                    icm_pressure = icm_calculator.calculate_icm_pressure(stack_sizes, payouts, 0)
                    st.info(f"ICM Pressure: {icm_pressure:.2f} (0 = none, 1 = maximum)")
                    
                    # Show ICM values
                    icm_values = icm_calculator.calculate_icm(stack_sizes, payouts)
                    icm_df = pd.DataFrame({
                        'Player': [f"You" if i == 0 else f"P{i+1}" for i in range(len(stack_sizes))],
                        'Stack (BB)': stack_sizes,
                        'ICM Value': [f"{val:.2f}" for val in icm_values],
                        'ICM %': [f"{val/sum(icm_values)*100:.1f}%" for val in icm_values]
                    })
                    st.dataframe(icm_df)
                except Exception as e:
                    st.error(f"ICM calculation error: {str(e)}")
    
    with col2:
        st.subheader("Results")
        
        # Calculate button
        if st.button("Calculate", type="primary"):
            # Show spinner during calculation
            with st.spinner("Calculating hand strength..."):
                try:
                    # Parse cards
                    card1 = poker_engine.parse_card(f"{rank1}{suit1}")
                    card2 = poker_engine.parse_card(f"{rank2}{suit2}")
                    
                    if not card1 or not card2:
                        st.error("Invalid card format")
                    elif str(card1) == str(card2):
                        st.error("Duplicate cards are not allowed")
                    else:
                        # Parse community cards
                        comm_cards = []
                        for card_str in community_cards:
                            card = poker_engine.parse_card(card_str)
                            if card:
                                if card in [card1, card2] or any(str(card) == str(c) for c in comm_cards):
                                    st.error(f"Duplicate card detected: {card_str}")
                                    break
                                comm_cards.append(card)
                        
                        # Calculate hand strength
                        start_time = time.time()
                        hole_cards = [card1, card2]
                        
                        if comm_cards:
                            hand_strength = poker_engine.calculate_hand_strength(
                                hole_cards, num_players, comm_cards, opponent_range
                            )
                        else:
                            hand_strength = poker_engine.calculate_hand_strength(
                                hole_cards, num_players, None, opponent_range
                            )
                        
                        # Ensure hand_strength is between 0 and 1
                        hand_strength = max(0.0, min(1.0, hand_strength))
                        
                        calc_time = time.time() - start_time
                        
                        # Get recommendation
                        recommendation = poker_engine.get_action_recommendation(
                            hand_strength, position, big_blinds, tournament_stage, icm_pressure
                        )
                        
                        # Display results
                        st.metric("Hand Strength", f"{hand_strength*100:.1f}%")
                        
                        # Color-code recommendation
                        if recommendation == "Fold":
                            st.error(f"Recommendation: {recommendation}")
                        elif recommendation == "Call":
                            st.warning(f"Recommendation: {recommendation}")
                        elif recommendation == "Raise":
                            st.success(f"Recommendation: {recommendation}")
                        elif recommendation == "All-In":
                            st.success(f"Recommendation: {recommendation} 🚀")
                        
                        # Additional info
                        info = get_hand_description(hand_strength)
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
                        
                        st.info(info)
                        
                        # Show calculation time
                        st.caption(f"Calculation completed in {calc_time:.2f} seconds")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Tab 2: ICM Calculator
with tab2:
    st.header("ICM Calculator")
    st.markdown("""
    The Independent Chip Model (ICM) calculates the dollar value of your tournament chips based on the payout structure.
    This helps you make better decisions in tournaments, especially near the bubble or final table.
    """)
    
    # Tournament setup
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tournament Setup")
        num_players_icm = st.slider("Number of Players", 2, 9, 6, key="icm_tab_players")
        
        # Stack sizes
        st.write("Stack Sizes")
        stack_sizes = []
        for i in range(num_players_icm):
            stack = st.number_input(f"Player {i+1}", min_value=1, max_value=10000, value=1000 // (i+1), key=f"icm_stack_{i}")
            stack_sizes.append(stack)
        
        # Payouts
        st.write("Payouts")
        num_payouts = st.slider("Number of Payouts", 1, num_players_icm, min(3, num_players_icm), key="icm_num_payouts")
        payouts = []
        for i in range(num_payouts):
            if i == 0:
                payout = st.number_input(f"1st Place", min_value=1, value=100, key=f"icm_payout_{i}")
            else:
                payout = st.number_input(f"{i+1}{'st' if i==0 else 'nd' if i==1 else 'rd' if i==2 else 'th'} Place", 
                                       min_value=1, value=max(1, 100 // (i+1)), key=f"icm_payout_{i}")
            payouts.append(payout)
    
    with col2:
        st.subheader("ICM Results")
        
        if st.button("Calculate ICM Values", type="primary", key="calc_icm"):
            try:
                # Calculate ICM values
                icm_values = icm_calculator.calculate_icm(stack_sizes, payouts)
                
                # Calculate ICM pressures
                icm_pressures = []
                for i in range(len(stack_sizes)):
                    pressure = icm_calculator.calculate_icm_pressure(stack_sizes, payouts, i)
                    icm_pressures.append(pressure)
                
                # Create dataframe for display
                icm_df = pd.DataFrame({
                    'Player': [f"Player {i+1}" for i in range(len(stack_sizes))],
                    'Stack': stack_sizes,
                    'Stack %': [f"{s/sum(stack_sizes)*100:.1f}%" for s in stack_sizes],
                    'ICM Value': [f"{val:.2f}" for val in icm_values],
                    'ICM %': [f"{val/sum(icm_values)*100:.1f}%" for val in icm_values],
                    'ICM Pressure': [f"{p:.2f}" for p in icm_pressures]
                })
                
                st.dataframe(icm_df)
                
                # Visualization
                st.subheader("Stack vs ICM Value")
                chart_data = pd.DataFrame({
                    'Player': [f"P{i+1}" for i in range(len(stack_sizes))],
                    'Stack %': [s/sum(stack_sizes)*100 for s in stack_sizes],
                    'ICM %': [val/sum(icm_values)*100 for val in icm_values]
                })
                
                st.bar_chart(chart_data.set_index('Player'))
                
                # ICM implications
                st.subheader("ICM Implications")
                implications = []
                for i, pressure in enumerate(icm_pressures):
                    if pressure > 0.7:
                        implications.append(f"Player {i+1} is under very high ICM pressure and should play very tight")
                    elif pressure > 0.4:
                        implications.append(f"Player {i+1} is under moderate ICM pressure")
                    else:
                        implications.append(f"Player {i+1} can play relatively aggressively")
                
                for imp in implications:
                    st.write(f"• {imp}")
                
            except Exception as e:
                st.error(f"ICM calculation error: {str(e)}")

# Tab 3: Nash Ranges
with tab3:
    st.header("Nash Equilibrium Push/Fold Ranges")
    st.markdown("""
    Nash equilibrium ranges tell you which hands to push all-in with (or call an all-in with) 
    in short-stacked situations, based on game theory optimal play.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tournament Situation")
        
        # Number of players
        num_players_nash = st.slider("Number of Players", 2, 9, 6, key="nash_players")
        
        # Positions
        st.write("Player Positions")
        positions = []
        position_options = ['btn', 'sb', 'bb', 'utg', 'utg+1', 'mp', 'mp+1', 'hj', 'co']
        
        # Default positions based on number of players
        default_positions = {
            2: ['btn', 'bb'],
            3: ['btn', 'sb', 'bb'],
            4: ['btn', 'sb', 'bb', 'utg'],
            5: ['btn', 'sb', 'bb', 'utg', 'co'],
            6: ['btn', 'sb', 'bb', 'utg', 'utg+1', 'co'],
            7: ['btn', 'sb', 'bb', 'utg', 'utg+1', 'mp', 'co'],
            8: ['btn', 'sb', 'bb', 'utg', 'utg+1', 'mp', 'hj', 'co'],
            9: ['btn', 'sb', 'bb', 'utg', 'utg+1', 'mp', 'mp+1', 'hj', 'co']
        }
        
        for i in range(num_players_nash):
            default_pos = default_positions.get(num_players_nash, ['btn'])[i] if i < len(default_positions.get(num_players_nash, [])) else 'btn'
            pos = st.selectbox(f"Player {i+1}", position_options, index=position_options.index(default_pos), key=f"nash_pos_{i}")
            positions.append(pos)
        
        # Stack sizes
        st.write("Stack Sizes (in BB)")
        stack_sizes = []
        for i in range(num_players_nash):
            stack = st.number_input(f"Player {i+1}", min_value=1, max_value=100, value=10, key=f"nash_stack_{i}")
            stack_sizes.append(stack)
        
        # Blinds
        st.write("Blinds")
        sb = st.number_input("Small Blind", min_value=0.5, max_value=10.0, value=1.0, step=0.5, key="nash_sb")
        bb = st.number_input("Big Blind", min_value=1.0, max_value=20.0, value=2.0, step=1.0, key="nash_bb")
        blinds = [sb, bb]
        
        # ICM considerations
        use_icm_nash = st.checkbox("Include ICM considerations", key="use_icm_nash")
        payouts_nash = None
        if use_icm_nash:
            st.write("Payouts")
            num_payouts_nash = st.slider("Number of Payouts", 1, num_players_nash, min(3, num_players_nash), key="nash_num_payouts")
            payouts_nash = []
            for i in range(num_payouts_nash):
                payout = st.number_input(f"{i+1}{'st' if i==0 else 'nd' if i==1 else 'rd' if i==2 else 'th'} Place", 
                                       min_value=1, value=max(1, 100 // (i+1)), key=f"nash_payout_{i}")
                payouts_nash.append(payout)
    
    with col2:
        st.subheader("Nash Ranges")
        
        if st.button("Calculate Nash Ranges", type="primary", key="calc_nash"):
            try:
                # Calculate Nash ranges
                nash_ranges = icm_calculator.nash_equilibrium_push_fold(stack_sizes, positions, blinds, payouts_nash)
                
                # Display results
                for i, pos in enumerate(positions):
                    st.write(f"**Player {i+1} ({pos}, {stack_sizes[i]} BB)**")
                    
                    if pos in nash_ranges:
                        push_threshold, call_threshold = nash_ranges[pos]
                        
                        # Convert thresholds to hand ranges
                        push_pct = min(100, (1 - push_threshold) * 100)
                        call_pct = min(100, (1 - call_threshold) * 100)
                        
                        # Display thresholds
                        st.write(f"Push with top {push_pct:.1f}% of hands")
                        st.write(f"Call all-in with top {call_pct:.1f}% of hands")
                        
                        # Example hands
                        if push_pct > 20:
                            st.write("Push examples: AA-22, AK-A2s, KQ-K9s, QJ-Q9s, JT-J9s, T9s...")
                        elif push_pct > 10:
                            st.write("Push examples: AA-77, AK-AT, KQ-KT, QJ-QT...")
                        elif push_pct > 5:
                            st.write("Push examples: AA-TT, AK-AQ, KQ...")
                        else:
                            st.write("Push examples: AA-QQ, AK...")
                        
                        if call_pct > 20:
                            st.write("Call examples: AA-22, AK-A2s, KQ-K9s, QJ-Q9s, JT-J9s, T9s...")
                        elif call_pct > 10:
                            st.write("Call examples: AA-77, AK-AT, KQ-KT, QJ-QT...")
                        elif call_pct > 5:
                            st.write("Call examples: AA-TT, AK-AQ, KQ...")
                        else:
                            st.write("Call examples: AA-QQ, AK...")
                    else:
                        st.write("Position not found in Nash ranges")
                    
                    st.write("---")
                
            except Exception as e:
                st.error(f"Nash calculation error: {str(e)}")

# Footer
st.markdown("---")
st.caption("Poker Tournament Helper - Developed with ❤️ for poker players")
st.caption("Disclaimer: This tool is for educational purposes only. Use at your own risk in real games.")
