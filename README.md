# Poker Tournament Helper

A web application to help make poker decisions based on probabilities during tournaments.

## Features

- Calculate hand strength based on your hole cards
- Consider the number of players at the table
- Take position into account for decision making
- Provide action recommendations (fold, call, raise)
- User-friendly web interface
- Support for known community cards (flop, turn, river)

## Web Application Usage

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask web application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

4. In the web interface:
   - Select the number of players at the table (2-9)
   - Enter your stack size in big blinds (optional)
   - Choose your hole cards from the dropdown menus
   - Optionally enter known community cards (flop, turn, river)
   - Select your position at the table (early, middle, late)
   - Click "Calculate" to get your recommendation

## Desktop Application

You can also use the desktop GUI version:

```bash
python poker_helper_gui.py
```

Or the command-line version:

```bash
python poker_helper.py
```

## Card Format

- Ranks: 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A
- Suits: h (hearts), d (diamonds), c (clubs), s (spades)

Example: "Ah" is the Ace of hearts, "Td" is the Ten of diamonds

## How It Works

The application uses Monte Carlo simulation to estimate the probability of winning with your hole cards against the specified number of opponents. It simulates thousands of random community cards and opponent hole cards to calculate your hand strength.

Based on this strength and your position, it provides an action recommendation that can help guide your decision-making process during a poker tournament.
## Card Format

- Ranks: 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A
- Suits: h (hearts), d (diamonds), c (clubs), s (spades)

Example: "Ah" is the Ace of hearts, "Td" is the Ten of diamonds

## How It Works

The application uses Monte Carlo simulation to estimate the probability of winning with your hole cards against the specified number of opponents. It simulates thousands of random community cards and opponent hole cards to calculate your hand strength.

Based on this strength and your position, it provides an action recommendation that can help guide your decision-making process during a poker tournament.
