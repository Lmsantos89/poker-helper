
# Poker Tournament Tool – Developer Plan

## 🎯 Project Goal

Build a poker tournament helper tool to improve strategic decisions using equity calculation, Monte Carlo simulations, and ICM modeling.

---

## ✅ MVP Use Case

> “Should I shove, call, or fold in this spot, considering stack sizes, positions, and ICM?”

---

## 🧰 Components

| Component         | Purpose                              | Suggested Tools              |
|------------------|--------------------------------------|------------------------------|
| Hand Evaluator   | Calculate equity vs. hand/range      | `treys`, `deuces`, `eval7`   |
| Monte Carlo Sim  | Estimate win/tie/loss % over samples | Custom logic using deck/range|
| ICM Calculator    | Value chip stacks for payouts        | Custom model or ICM libs     |
| Range Parser     | Interpret % or combos (e.g. 22+, A5s+) | Manual, regex, chart parsing |
| GUI              | Display decisions/sim results         | CLI, Streamlit, Flask        |

---

## 🧪 Sample Monte Carlo Simulation Code (Python + treys)

```python
from treys import Evaluator, Card, Deck

evaluator = Evaluator()

hand1 = [Card.new('As'), Card.new('Kd')]
hand2 = [Card.new('Qs'), Card.new('Qh')]

wins = { "P1": 0, "P2": 0, "tie": 0 }

for _ in range(10000):
    deck = Deck()
    for card in hand1 + hand2:
        deck.cards.remove(card)
    board = deck.draw(5)

    score1 = evaluator.evaluate(board, hand1)
    score2 = evaluator.evaluate(board, hand2)

    if score1 < score2:
        wins["P1"] += 1
    elif score2 < score1:
        wins["P2"] += 1
    else:
        wins["tie"] += 1

print(wins)
```

---

## 🧮 ICM Calculation Example (Simplified)

```python
def compute_icm(stack_sizes, payouts):
    total = sum(stack_sizes)
    return [s / total * payouts[0] for s in stack_sizes]  # naive model
```

More accurate models consider elimination orders → use Monte Carlo or a library.

---

## 📚 Useful Libraries & Tools

- `treys`, `deuces`, `eval7` – Fast poker hand evaluators
- [`poker-icm`](https://github.com/robz/poker-icm) – ICM calculator
- [`streamlit`](https://streamlit.io) – Fast UI for Python
- [`argparse`] – For command-line interfaces

---

## 🔧 Suggested Tech Stack

| Layer     | Choice           |
|-----------|------------------|
| Backend   | Python            |
| Frontend  | CLI / Streamlit   |
| Storage   | JSON or SQLite    |
| Performance | Optional: C++ module for large sims |

---

## 🛣️ Roadmap

1. ✅ MVP: CLI-based equity & ICM calculator
2. ✅ Add Streamlit web interface
3. ✅ Opponent hand ranges support
4. 🔜 ICM-aware multiway decisions
5. 🔜 Import/analyze hand histories
6. 🔜 Training or quiz mode

---

## 🚀 Advanced Ideas

- Nash Push/Fold charts
- Real-time HUD (online or live)
- GTO strategy trees with Monte Carlo rollouts
- Database of reviewable hands
