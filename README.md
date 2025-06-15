# Poker Tournament Helper

A high-performance web application to help make poker decisions based on probabilities during tournaments, with ICM considerations.

## Features

- Calculate hand strength based on your hole cards
- Consider the number of players at the table
- Take position into account for decision making
- Provide action recommendations (fold, call, raise, all-in)
- ICM calculations for tournament play
- Nash equilibrium push/fold ranges
- Support for opponent hand ranges
- User-friendly web interface with Streamlit option
- Support for known community cards (flop, turn, river)
- Optimized performance with parallel processing

## Project Structure

```
poker-helper/
├── src/                           # Source code directory
│   ├── core/                      # Core functionality
│   │   ├── poker_engine.py        # Core poker logic
│   │   ├── icm.py                 # ICM calculations
│   │   └── models.py              # Data models (compatibility wrapper)
│   ├── web/                       # Web interfaces
│   │   ├── app.py                 # Flask application
│   │   ├── streamlit_app.py       # Streamlit interface
│   │   ├── templates/             # Flask templates
│   │   └── static/                # Static assets
│   └── utils/                     # Utility functions
│       └── helpers.py             # Helper functions
├── tests/                         # Test directory
├── data/                          # Data files
├── scripts/                       # Scripts directory
├── docs/                          # Documentation
└── README.md
```

## Installation

### Using pip

```bash
# Install from the current directory
pip install -e .
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/poker-helper.git
   cd poker-helper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Web Application Usage

1. Run the Flask web application:
   ```bash
   python -m src.web.app
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. Alternatively, run the Streamlit interface:
   ```bash
   streamlit run src/web/streamlit_app.py
   ```

4. In the web interface:
   - Select the number of players at the table (2-9)
   - Enter your stack size in big blinds
   - Choose your hole cards from the dropdown menus
   - Optionally enter known community cards (flop, turn, river)
   - Select your position at the table (early, middle, late)
   - Choose the tournament stage (early, middle, bubble, final)
   - Optionally specify opponent ranges and ICM considerations
   - Click "Calculate" to get your recommendation

## Quick Start

For convenience, you can use the included script to set up and run the application:

```bash
./scripts/run_poker_helper.py
```

This script will:
- Create a virtual environment if needed
- Install all required dependencies
- Run the Flask application

## Development

### Running Tests

Run all tests with coverage reporting:

```bash
./scripts/run_tests.py
```

This will:
- Run all unit tests
- Display test results
- Show coverage statistics
- Generate an HTML coverage report in the `htmlcov` directory

### Type Checking

The codebase includes type hints. You can check types with mypy:

```bash
mypy src
```

## Card Format

- Ranks: 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A
- Suits: h (hearts), d (diamonds), c (clubs), s (spades)

Example: "Ah" is the Ace of hearts, "Td" is the Ten of diamonds

## How It Works

The application uses optimized Monte Carlo simulation to estimate the probability of winning with your hole cards against the specified number of opponents. It simulates thousands of random community cards and opponent hole cards to calculate your hand strength.

For premium hands (AA, KK, QQ, AK, AQ), it uses precomputed values for more accurate results.

Based on this strength, your position, stack size, and tournament stage, it provides an action recommendation that can help guide your decision-making process during a poker tournament.

### ICM Calculations

The Independent Chip Model (ICM) calculates the dollar value of your tournament chips based on the payout structure. This helps you make better decisions in tournaments, especially near the bubble or final table.

The application can:
- Calculate ICM equity for each player
- Determine ICM pressure for each player
- Adjust recommendations based on ICM considerations
- Generate Nash equilibrium push/fold ranges
