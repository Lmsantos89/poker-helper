#!/usr/bin/env python3
"""
Poker Tournament Helper - GUI Version
A tool to help make poker decisions based on probabilities with a graphical interface.
"""
import random
import itertools
import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import threading

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
    
    def calculate_hand_strength(self, hole_cards, num_players, known_community_cards=None):
        """Calculate the strength of the current hand.
        
        Args:
            hole_cards: List of 2 Card objects representing player's hole cards
            num_players: Number of players at the table
            known_community_cards: List of Card objects for known community cards (flop, turn, river)
        """
        # Remove hole cards and known community cards from deck
        used_cards = hole_cards.copy()
        if known_community_cards:
            used_cards.extend(known_community_cards)
            
        available_deck = [card for card in self.deck if card not in used_cards]
        
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
            offset = 5 if not known_community_cards else len(known_community_cards)
            
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

class PokerHelperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Tournament Helper")
        self.root.geometry("700x700")
        self.root.resizable(False, False)
        
        self.helper = PokerHelper()
        self.create_widgets()
        
    def create_widgets(self):
        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TRadiobutton", font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 16, "bold"))
        style.configure("Subheader.TLabel", font=("Arial", 14, "bold"))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Poker Tournament Helper", style="Header.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Number of players
        players_label = ttk.Label(main_frame, text="Number of players:")
        players_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.players_var = tk.StringVar(value="6")
        players_combo = ttk.Combobox(main_frame, textvariable=self.players_var, width=5)
        players_combo['values'] = tuple(range(2, 10))
        players_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Hole cards
        cards_label = ttk.Label(main_frame, text="Your hole cards:", style="Subheader.TLabel")
        cards_label.grid(row=2, column=0, sticky=tk.W, pady=(15, 5))
        
        cards_frame = ttk.Frame(main_frame)
        cards_frame.grid(row=2, column=1, sticky=tk.W, pady=(15, 5))
        
        # First card
        self.card1_rank = tk.StringVar()
        self.card1_suit = tk.StringVar()
        
        card1_rank_combo = ttk.Combobox(cards_frame, textvariable=self.card1_rank, width=3)
        card1_rank_combo['values'] = RANKS
        card1_rank_combo.pack(side=tk.LEFT, padx=2)
        
        card1_suit_combo = ttk.Combobox(cards_frame, textvariable=self.card1_suit, width=3)
        card1_suit_combo['values'] = SUITS
        card1_suit_combo.pack(side=tk.LEFT, padx=2)
        
        # Second card
        self.card2_rank = tk.StringVar()
        self.card2_suit = tk.StringVar()
        
        card2_rank_combo = ttk.Combobox(cards_frame, textvariable=self.card2_rank, width=3)
        card2_rank_combo['values'] = RANKS
        card2_rank_combo.pack(side=tk.LEFT, padx=(10, 2))
        
        card2_suit_combo = ttk.Combobox(cards_frame, textvariable=self.card2_suit, width=3)
        card2_suit_combo['values'] = SUITS
        card2_suit_combo.pack(side=tk.LEFT, padx=2)
        
        # Community cards section
        community_label = ttk.Label(main_frame, text="Community cards:", style="Subheader.TLabel")
        community_label.grid(row=3, column=0, sticky=tk.W, pady=(15, 5))
        
        # Flop frame
        flop_frame = ttk.LabelFrame(main_frame, text="Flop (optional)")
        flop_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Flop cards
        self.flop_cards = []
        for i in range(3):
            card_frame = ttk.Frame(flop_frame)
            card_frame.pack(side=tk.LEFT, padx=10, pady=5)
            
            rank_var = tk.StringVar()
            suit_var = tk.StringVar()
            
            ttk.Label(card_frame, text=f"Card {i+1}:").pack(side=tk.LEFT)
            
            rank_combo = ttk.Combobox(card_frame, textvariable=rank_var, width=3)
            rank_combo['values'] = [''] + RANKS
            rank_combo.pack(side=tk.LEFT, padx=2)
            
            suit_combo = ttk.Combobox(card_frame, textvariable=suit_var, width=3)
            suit_combo['values'] = [''] + SUITS
            suit_combo.pack(side=tk.LEFT, padx=2)
            
            self.flop_cards.append((rank_var, suit_var))
        
        # Turn frame
        turn_frame = ttk.LabelFrame(main_frame, text="Turn (optional)")
        turn_frame.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Turn card
        card_frame = ttk.Frame(turn_frame)
        card_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.turn_rank = tk.StringVar()
        self.turn_suit = tk.StringVar()
        
        ttk.Label(card_frame, text="Card:").pack(side=tk.LEFT)
        
        turn_rank_combo = ttk.Combobox(card_frame, textvariable=self.turn_rank, width=3)
        turn_rank_combo['values'] = [''] + RANKS
        turn_rank_combo.pack(side=tk.LEFT, padx=2)
        
        turn_suit_combo = ttk.Combobox(card_frame, textvariable=self.turn_suit, width=3)
        turn_suit_combo['values'] = [''] + SUITS
        turn_suit_combo.pack(side=tk.LEFT, padx=2)
        
        # River frame
        river_frame = ttk.LabelFrame(main_frame, text="River (optional)")
        river_frame.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # River card
        card_frame = ttk.Frame(river_frame)
        card_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.river_rank = tk.StringVar()
        self.river_suit = tk.StringVar()
        
        ttk.Label(card_frame, text="Card:").pack(side=tk.LEFT)
        
        river_rank_combo = ttk.Combobox(card_frame, textvariable=self.river_rank, width=3)
        river_rank_combo['values'] = [''] + RANKS
        river_rank_combo.pack(side=tk.LEFT, padx=2)
        
        river_suit_combo = ttk.Combobox(card_frame, textvariable=self.river_suit, width=3)
        river_suit_combo['values'] = [''] + SUITS
        river_suit_combo.pack(side=tk.LEFT, padx=2)
        
        # Position
        position_label = ttk.Label(main_frame, text="Your position:")
        position_label.grid(row=7, column=0, sticky=tk.W, pady=(15, 5))
        
        position_frame = ttk.Frame(main_frame)
        position_frame.grid(row=7, column=1, sticky=tk.W, pady=(15, 5))
        
        self.position_var = tk.StringVar(value="middle")
        
        early_radio = ttk.Radiobutton(position_frame, text="Early", variable=self.position_var, value="early")
        early_radio.pack(side=tk.LEFT, padx=5)
        
        middle_radio = ttk.Radiobutton(position_frame, text="Middle", variable=self.position_var, value="middle")
        middle_radio.pack(side=tk.LEFT, padx=5)
        
        late_radio = ttk.Radiobutton(position_frame, text="Late", variable=self.position_var, value="late")
        late_radio.pack(side=tk.LEFT, padx=5)
        
        # Calculate button
        calculate_button = ttk.Button(main_frame, text="Calculate", command=self.calculate)
        calculate_button.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding=10)
        results_frame.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Hand strength
        strength_label = ttk.Label(results_frame, text="Hand strength:")
        strength_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.strength_var = tk.StringVar(value="--")
        strength_result = ttk.Label(results_frame, textvariable=self.strength_var)
        strength_result.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Recommendation
        recommendation_label = ttk.Label(results_frame, text="Recommended action:")
        recommendation_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.recommendation_var = tk.StringVar(value="--")
        recommendation_result = ttk.Label(results_frame, textvariable=self.recommendation_var, font=("Arial", 12, "bold"))
        recommendation_result.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Additional info
        info_label = ttk.Label(results_frame, text="Additional info:")
        info_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.info_var = tk.StringVar(value="--")
        info_result = ttk.Label(results_frame, textvariable=self.info_var)
        info_result.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, 
                                        length=650, mode='determinate', 
                                        variable=self.progress_var)
        self.progress.grid(row=10, column=0, columnspan=2, pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 10))
        status_label.grid(row=11, column=0, columnspan=2)
        
    def calculate(self):
        # Validate inputs
        try:
            num_players = int(self.players_var.get())
            if num_players < 2 or num_players > 9:
                messagebox.showerror("Input Error", "Number of players must be between 2 and 9.")
                return
                
            card1_rank = self.card1_rank.get().upper()
            card1_suit = self.card1_suit.get().lower()
            card2_rank = self.card2_rank.get().upper()
            card2_suit = self.card2_suit.get().lower()
            
            if not card1_rank or not card1_suit or not card2_rank or not card2_suit:
                messagebox.showerror("Input Error", "Please select both hole cards completely.")
                return
                
            card1 = self.helper.parse_card(f"{card1_rank}{card1_suit}")
            card2 = self.helper.parse_card(f"{card2_rank}{card2_suit}")
            
            if str(card1) == str(card2):
                messagebox.showerror("Input Error", "You cannot select the same card twice.")
                return
            
            # Parse community cards
            community_cards = []
            
            # Parse flop
            for i, (rank_var, suit_var) in enumerate(self.flop_cards):
                rank = rank_var.get().upper()
                suit = suit_var.get().lower()
                
                if rank and suit:
                    try:
                        card = self.helper.parse_card(f"{rank}{suit}")
                        if card in [card1, card2] or card in community_cards:
                            messagebox.showerror("Input Error", f"Flop card {i+1} is a duplicate.")
                            return
                        community_cards.append(card)
                    except ValueError as e:
                        messagebox.showerror("Input Error", f"Invalid flop card {i+1}: {e}")
                        return
                elif rank or suit:
                    messagebox.showerror("Input Error", f"Flop card {i+1} is incomplete.")
                    return
            
            # Parse turn
            turn_rank = self.turn_rank.get().upper()
            turn_suit = self.turn_suit.get().lower()
            
            if turn_rank and turn_suit:
                try:
                    turn_card = self.helper.parse_card(f"{turn_rank}{turn_suit}")
                    if turn_card in [card1, card2] or turn_card in community_cards:
                        messagebox.showerror("Input Error", "Turn card is a duplicate.")
                        return
                    community_cards.append(turn_card)
                except ValueError as e:
                    messagebox.showerror("Input Error", f"Invalid turn card: {e}")
                    return
            elif turn_rank or turn_suit:
                messagebox.showerror("Input Error", "Turn card is incomplete.")
                return
            
            # Parse river
            river_rank = self.river_rank.get().upper()
            river_suit = self.river_suit.get().lower()
            
            if river_rank and river_suit:
                try:
                    river_card = self.helper.parse_card(f"{river_rank}{river_suit}")
                    if river_card in [card1, card2] or river_card in community_cards:
                        messagebox.showerror("Input Error", "River card is a duplicate.")
                        return
                    community_cards.append(river_card)
                except ValueError as e:
                    messagebox.showerror("Input Error", f"Invalid river card: {e}")
                    return
            elif river_rank or river_suit:
                messagebox.showerror("Input Error", "River card is incomplete.")
                return
            
            # Validate community cards sequence
            if len(community_cards) > 0:
                # If we have turn, we must have flop
                if len(community_cards) >= 4 and len(community_cards) < 3:
                    messagebox.showerror("Input Error", "If turn is specified, all flop cards must be specified.")
                    return
                # If we have river, we must have turn and flop
                if len(community_cards) == 5 and len(community_cards) < 4:
                    messagebox.showerror("Input Error", "If river is specified, turn and all flop cards must be specified.")
                    return
            
            position = self.position_var.get()
            
            # Start calculation in a separate thread
            self.status_var.set("Calculating...")
            self.progress_var.set(0)
            self.root.update_idletasks()
            
            calculation_thread = threading.Thread(
                target=self.run_calculation,
                args=(card1, card2, num_players, position, community_cards)
            )
            calculation_thread.daemon = True
            calculation_thread.start()
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    def run_calculation(self, card1, card2, num_players, position, community_cards=None):
        try:
            # Update progress periodically
            for i in range(1, 11):
                self.progress_var.set(i * 10)
                self.root.update_idletasks()
                if i < 10:  # Don't sleep on the last iteration
                    self.root.after(100)
            
            # Calculate hand strength
            hole_cards = [card1, card2]
            
            # Use community cards if provided
            if community_cards and len(community_cards) > 0:
                hand_strength = self.helper.calculate_hand_strength(hole_cards, num_players, community_cards)
            else:
                hand_strength = self.helper.calculate_hand_strength(hole_cards, num_players)
            
            # Get recommendation
            recommendation = self.helper.get_action_recommendation(hand_strength, position)
            
            # Additional info
            if hand_strength > 0.8:
                info = "This is a very strong hand!"
            elif hand_strength > 0.6:
                info = "This is a good hand."
            elif hand_strength > 0.4:
                info = "This is a marginal hand. Consider the pot odds."
            else:
                info = "This is a weak hand. Be cautious."
            
            # Update UI with results
            self.root.after(0, self.update_results, hand_strength, recommendation, info)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Calculation Error", str(e)))
        finally:
            self.root.after(0, lambda: self.status_var.set("Ready"))
    
    def update_results(self, hand_strength, recommendation, info):
        self.strength_var.set(f"{hand_strength:.2%}")
        self.recommendation_var.set(recommendation)
        self.info_var.set(info)

def main():
    root = tk.Tk()
    app = PokerHelperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
