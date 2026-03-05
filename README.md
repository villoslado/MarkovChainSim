# Markov Chain User Journey

A Python simulation that models how users move through a product over time using a Markov chain.

## What it does

Each user starts at Home and moves between states — Explore, Feature A, Feature B, Feature C, Subscribe, or Churn — based on a transition probability matrix. At each step, the next state is drawn at random according to those probabilities. The simulation runs 1,000 users over 52 weeks and tracks where everyone ends up at each step.

The output is two charts:

- **State flow over time** — a stacked area chart showing the share of users in each state week by week. You can see early dropout happening fast in weeks 1–4, the mid-funnel states slowly draining, and Subscribe and Churn absorbing the population by year end.
- **Outcome trajectories** — three lines showing how the Subscribe, Churn, and active free user populations evolve across 52 weeks.

## Assumptions

- Users start at Home (week 0)
- Subscribe probability: 1% per step from any active state
- Free user churn is highest early (roughly 10–12% per week in shallow states) and lower for users deeper in the funnel, mimicking a cohort retention curve that goes from ~67% at week 4 to ~33% by week 52
- Once subscribed, monthly retention is 95% (≈1.27% weekly churn)
- Churn is an absorbing state — users do not return

## Dependencies

pip install numpy matplotlib

## Usage

python markov_journey.py

## Files

- `markov_journey.py` — simulation and visualization
- `journey_52w.png` — output chart (generated on run)
