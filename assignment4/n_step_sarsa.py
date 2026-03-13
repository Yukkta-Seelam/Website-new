"""
n-step SARSA Algorithm
"""
import numpy as np
from collections import deque


class NStepSARSA:
    """
    n-step SARSA for control in tabular setting.
    """
    
    def __init__(self, env, n=1, alpha=0.5, gamma=1.0, epsilon=0.1):
        """
        Initialize n-step SARSA.
        
        Args:
            env: WindyCliffEnv instance
            n: Number of steps (n=1 is standard SARSA)
            alpha: Learning rate
            gamma: Discount factor
            epsilon: Epsilon for epsilon-greedy policy
        """
        self.env = env
        self.n = n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
        # Q-table: state-action values
        self.Q = np.zeros((env.n_states, env.n_actions))
        
        # Store for n-step returns
        self.states = deque(maxlen=n + 1)
        self.actions = deque(maxlen=n + 1)
        self.rewards = deque(maxlen=n + 1)
    
    def get_state_index(self, state):
        """Convert state tuple to index."""
        row, col = state
        return row * self.env.width + col
    
    def epsilon_greedy(self, state, Q):
        """Epsilon-greedy action selection."""
        state_idx = self.get_state_index(state)
        if np.random.random() < self.epsilon:
            return np.random.choice(self.env.n_actions)
        else:
            return np.argmax(Q[state_idx])
    
    def learn(self, num_episodes=500):
        """
        Learn using n-step SARSA.
        
        Returns:
            List of cumulative rewards per episode
        """
        episode_rewards = []
        
        for episode in range(num_episodes):
            state = self.env.reset()
            action = self.epsilon_greedy(state, self.Q)
            
            # Use lists instead of deque for easier indexing
            states = [state]
            actions = [action]
            rewards = [0]  # R_0 = 0
            
            total_reward = 0
            t = 0
            T = float('inf')
            
            while True:
                if t < T:
                    # Take action A_t, observe R_{t+1}, S_{t+1}
                    next_state, reward, done, _ = self.env.step(action)
                    total_reward += reward
                    
                    states.append(next_state)
                    rewards.append(reward)
                    
                    if done:
                        T = t + 1
                    else:
                        # Select and store A_{t+1}
                        next_action = self.epsilon_greedy(next_state, self.Q)
                        actions.append(next_action)
                        action = next_action
                
                # Update time of update
                tau = t - self.n + 1
                
                if tau >= 0:
                    # Compute n-step return
                    G = 0
                    for i in range(tau + 1, min(tau + self.n + 1, T + 1)):
                        G += (self.gamma ** (i - tau - 1)) * rewards[i]
                    
                    if tau + self.n < T:
                        state_tau_n = states[tau + self.n]
                        action_tau_n = actions[tau + self.n]
                        state_tau_n_idx = self.get_state_index(state_tau_n)
                        G += (self.gamma ** self.n) * self.Q[state_tau_n_idx, action_tau_n]
                    
                    # Update Q
                    state_tau = states[tau]
                    action_tau = actions[tau]
                    state_tau_idx = self.get_state_index(state_tau)
                    self.Q[state_tau_idx, action_tau] += self.alpha * (
                        G - self.Q[state_tau_idx, action_tau]
                    )
                
                t += 1
                
                if tau == T - 1:
                    break
            
            episode_rewards.append(total_reward)
        
        return episode_rewards

