# Assignment 4: Windy Cliff Environment - Reinforcement Learning Algorithms

This assignment implements and compares several reinforcement learning algorithms on the windy cliff environment:
- n-step SARSA
- TD(λ)
- SARSA(λ)
- Watkins Q(λ)

## Environment

The windy cliff environment is a gridworld with:
- **Grid size**: 7×10 (height × width)
- **Wind**: Upward wind in specified columns (pushes agent up)
- **Cliff**: Bottom row (except start and goal positions)
- **Start**: Bottom-left corner
- **Goal**: Bottom-right corner
- **Rewards**:
  - -1 per step
  - -100 for stepping into the cliff (resets to start)
  - 0 on reaching the goal
- **Termination**: Episode ends at goal or after max steps (1000)

## Algorithms

### 1. n-step SARSA
- **Purpose**: Control (learns Q-values)
- **Parameters**: n ∈ {1, 2, 4, 8}
- **Description**: Generalizes 1-step SARSA to n-step returns

### 2. TD(λ)
- **Purpose**: Prediction (learns state values V)
- **Parameters**: λ ∈ {0, 0.3, 0.7, 1.0}
- **Description**: Uses eligibility traces for efficient learning

### 3. SARSA(λ)
- **Purpose**: Control (learns Q-values)
- **Parameters**: λ ∈ {0, 0.3, 0.7, 1.0}
- **Description**: SARSA with eligibility traces

### 4. Watkins Q(λ)
- **Purpose**: Control (learns Q-values)
- **Parameters**: λ ∈ {0, 0.3, 0.7, 1.0}
- **Description**: Off-policy Q-learning with eligibility traces (cuts traces on non-greedy actions)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the main experiment script:

```bash
python main.py
```

Or run experiments directly:

```bash
python experiments.py
```

## Output

The script generates:
1. **Learning curves** for each algorithm with different parameter values
2. **Comparison plots** showing all algorithms together
3. **Convergence metrics** printed to console

## Analysis

### Impact of λ (Lambda)

- **λ = 0**: Pure TD(0) or 1-step methods. Low variance, high bias. Fast updates but may be less accurate.
- **λ = 0.3**: Moderate trace decay. Balances bias and variance.
- **λ = 0.7**: Stronger trace decay. More variance but potentially better long-term estimates.
- **λ = 1.0**: Monte Carlo methods. High variance, low bias. Uses full episode returns.

### Impact of n (n-step SARSA)

- **n = 1**: Standard SARSA. Fast but may be less accurate.
- **n = 2-4**: Moderate lookahead. Good balance.
- **n = 8**: Long lookahead. More accurate but slower updates.

### Bias-Variance Trade-off

- **Lower λ/n**: Lower variance, higher bias. Faster convergence but may converge to suboptimal values.
- **Higher λ/n**: Higher variance, lower bias. Slower convergence but more accurate estimates.

## Files

- `windy_cliff_env.py`: Environment implementation
- `n_step_sarsa.py`: n-step SARSA algorithm
- `td_lambda.py`: TD(λ) algorithm
- `sarsa_lambda.py`: SARSA(λ) algorithm
- `watkins_q_lambda.py`: Watkins Q(λ) algorithm
- `experiments.py`: Experiment runner and visualization
- `main.py`: Main script
- `requirements.txt`: Python dependencies

## Results

The experiments analyze:
1. **Learning curves**: Episodes vs. cumulative reward
2. **Convergence speed**: How quickly algorithms reach good performance
3. **Final performance**: Average reward in final episodes
4. **Bias-variance trade-off**: How different parameters affect learning

