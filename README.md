# Poker Tournament Helper

A high-performance web application to help make poker decisions based on probabilities during tournaments.

## Features

- Calculate hand strength based on your hole cards
- Consider the number of players at the table
- Take position into account for decision making
- Provide action recommendations (fold, call, raise, all-in)
- User-friendly web interface
- Support for known community cards (flop, turn, river)
- Optimized performance with parallel processing

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

## Card Format

- Ranks: 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A
- Suits: h (hearts), d (diamonds), c (clubs), s (spades)

Example: "Ah" is the Ace of hearts, "Td" is the Ten of diamonds

## Project Structure

The application is organized into modular components:

- `app.py` - Main Flask web application
- `models.py` - Core poker logic and data structures
- `utils.py` - Helper functions and benchmarking tools
- `templates/` - HTML templates for the web interface
- `static/` - CSS and JavaScript files
- `tests/` - Unit tests for all components
- `run_tests.py` - Script to run all unit tests

## How It Works

The application uses optimized Monte Carlo simulation to estimate the probability of winning with your hole cards against the specified number of opponents. It simulates thousands of random community cards and opponent hole cards to calculate your hand strength.

Based on this strength and your position, it provides an action recommendation that can help guide your decision-making process during a poker tournament.

### Performance Optimizations

This application includes several performance optimizations:

1. **Parallel Processing**: Utilizes multiple CPU cores to run simulations in parallel
2. **Optimized Card Representation**: Uses memory-efficient card objects with precomputed values
3. **Fast Hand Evaluation**: Implements optimized algorithms for evaluating poker hands
4. **Efficient Deck Management**: Uses set operations and lookup tables for faster card operations

## API Endpoints

- `/` - Main web interface
- `/calculate` - POST endpoint for calculating hand strength and recommendations
- `/benchmark` - GET endpoint to run a performance benchmark
## Testing

The application includes comprehensive unit tests for all components:

1. Run all tests with coverage reporting:
   ```bash
   python run_tests.py
   ```
   
   This will:
   - Run all unit tests
   - Display test results
   - Show coverage statistics
   - Generate an HTML coverage report in the `htmlcov` directory

2. Current test coverage:
   - app.py: 86%
   - models.py: 70%
   - utils.py: 97%
   - Overall: 77%
