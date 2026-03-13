# Video Transcripts for Code Explanation

## 1. windy_cliff_env.py

**Transcript:**

"Let's start with the environment file. This implements the Windy Cliff Walking gridworld.

The environment is a 7 by 10 grid. The agent starts at the bottom-left and needs to reach the bottom-right goal. The bottom row is a cliff - if you step on it, you get a -100 penalty and reset to the start.

The key feature is the wind. Columns 3 through 8 have upward wind that pushes the agent up by 1 or 2 cells depending on the column. This makes navigation challenging because you need to account for wind drift.

Looking at the step function - it first applies the action to move the agent, then applies the wind effect which pushes the agent up. Then it calculates rewards: -1 for each step, -100 for hitting the cliff, and 0 when reaching the goal.

The environment tracks the current state, number of steps, and handles episode termination when the goal is reached or max steps is exceeded."

---

## 2. n_step_sarsa.py

**Transcript:**

"Now let's look at n-step SARSA. This is an on-policy control algorithm that learns Q-values.

The key difference from standard SARSA is that instead of updating Q-values using just the immediate reward and next state, n-step SARSA looks ahead n steps into the future.

In the learn method, we store states, actions, and rewards in lists. When we've collected n steps of experience, we compute the n-step return - that's the sum of rewards over n steps plus the discounted Q-value of the state-action pair n steps ahead.

Then we update the Q-value using this n-step return. This gives us a better estimate because we're using more information, but it also means we have to wait n steps before we can update.

The parameter n controls the trade-off: n=1 is standard SARSA, while larger n values use more information but update less frequently."

---

## 3. td_lambda.py

**Transcript:**

"TD Lambda is a prediction algorithm that learns state values V of s, not action values.

The key innovation here is eligibility traces. Instead of updating just the current state, we maintain a trace vector that tracks which states were recently visited. When we get a TD error, we update all states in proportion to their trace values.

The lambda parameter controls trace decay. When lambda is 0, we get TD zero - only the current state is updated. When lambda is 1, we get Monte Carlo - all states in the episode get updated. Intermediate lambda values give us a weighted combination.

In the code, we initialize traces to zero, then increment the trace for the current state. We compute the TD error using the reward and next state value. Then we update all state values weighted by their traces, and decay the traces by gamma times lambda.

Note that this algorithm also maintains Q-values for action selection using epsilon-greedy policy, even though its main purpose is learning state values."

---

## 4. sarsa_lambda.py

**Transcript:**

"SARSA Lambda is similar to TD Lambda, but it's a control algorithm that learns Q-values for state-action pairs.

The structure is very similar - we use eligibility traces to efficiently assign credit to past state-action pairs. The key difference is we're learning Q s comma a instead of V of s.

In the learn method, we maintain eligibility traces for state-action pairs. When we take an action and observe a reward, we compute the TD error using the current Q-value and the Q-value of the next state-action pair.

Then we update all Q-values in proportion to their trace values. The traces decay by gamma times lambda each step.

This is an on-policy algorithm - it follows the epsilon-greedy policy, so it learns the value of the policy it's actually following, not necessarily the optimal policy."

---

## 5. watkins_q_lambda.py

**Transcript:**

"Watkins Q Lambda is an off-policy algorithm that combines Q-learning with eligibility traces.

The key difference from SARSA Lambda is that it uses the maximum Q-value of the next state, not the Q-value of the action actually taken. This makes it off-policy - it learns about the optimal policy while following an exploratory policy.

The most important feature is trace cutting. When we take a non-greedy action - meaning we explore instead of exploiting - we cut the traces by setting them all to zero. This prevents incorrect credit assignment.

In the code, after updating Q-values, we check if the next action is greedy. If it is, we decay traces normally. If it's not greedy, we cut the traces completely.

This trace cutting mechanism is what makes Watkins Q Lambda stable with high lambda values, whereas SARSA Lambda can have numerical issues when lambda equals 1."

---

## 6. experiments.py

**Transcript:**

"This file orchestrates all the experiments and generates visualizations.

The main function is run_all_experiments, which runs experiments for all four algorithms with different parameter values. For n-step SARSA, we test n values of 1, 2, 4, and 8. For the lambda-based algorithms, we test lambda values of 0, 0.3, 0.7, and 1.0.

Each experiment runs multiple independent runs - by default 10 runs - and averages the results to get stable performance metrics.

The plot_learning_curves function creates visualizations showing episodes versus cumulative reward. It smooths the curves using a moving average to make trends clearer.

The compute_convergence_metrics function calculates when each algorithm converges - defined as the first episode where reward exceeds negative 50 - and the final average reward in the last 10 percent of episodes.

Finally, we generate comparison plots showing all algorithms together, and print convergence metrics to the console."

---

## 7. main.py

**Transcript:**

"This is the main entry point for running all experiments.

It's a simple script that imports the run_all_experiments function and calls it with default parameters: 10 runs and 500 episodes per run.

After the experiments complete, it prints a summary of all the generated plot files.

You can adjust the number of runs and episodes here - more runs give more stable results but take longer to compute."

---

## 8. test_env.py

**Transcript:**

"This is a simple test script to verify the environment works correctly.

It creates an environment instance, prints out the configuration like grid size and wind strength, then runs a few test steps cycling through different actions.

This is useful for debugging - you can quickly check that the environment is behaving as expected before running the full experiments. It's a good practice to test components individually before combining them."

---

## General Introduction Script

**Transcript:**

"Hi, today I'm going to walk you through my implementation of four reinforcement learning algorithms on the Windy Cliff Walking environment.

This is Assignment 4, where we compare n-step SARSA, TD Lambda, SARSA Lambda, and Watkins Q Lambda. All algorithms learn to navigate a 7 by 10 gridworld with wind effects and a dangerous cliff.

The codebase consists of eight Python files: one environment file, four algorithm implementations, an experiment runner, a main script, and a test file.

Let me show you each file and explain how they work together to solve this reinforcement learning problem."

---

## Closing Script

**Transcript:**

"To summarize what we've covered:

The environment file defines the gridworld with wind and cliff mechanics. The four algorithm files implement different temporal difference learning methods with various techniques for credit assignment.

The experiments file runs all algorithms with different hyperparameters, generates learning curves, and computes convergence metrics. The main script ties everything together.

The key differences between algorithms are: n-step SARSA uses fixed lookahead, TD Lambda learns state values, SARSA Lambda is on-policy with traces, and Watkins Q Lambda is off-policy with trace cutting.

All algorithms successfully learn to navigate the environment, with Watkins Q Lambda showing the best performance when lambda equals 1.0.

Thank you for watching!"

