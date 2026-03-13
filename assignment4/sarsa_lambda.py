"""
SARSA(λ) Algorithm
"""
import numpy as np


class SARSALambda:
    """
    SARSA(λ) for control in tabular setting.
    """
    
    def __init__(self, env, lam=0.0, alpha=0.5, gamma=1.0, epsilon=0.1):
        """
        Initialize SARSA(λ).
        
        Args:
            env: WindyCliffEnv instance
            lam: Lambda parameter (0=1-step SARSA, 1=MC)
            alpha: Learning rate
            gamma: Discount factor
            epsilon: Epsilon for epsilon-greedy policy
        """
        self.env = env
        self.lam = lam
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
        # Q-table: state-action values
        self.Q = np.zeros((env.n_states, env.n_actions))
    
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
        Learn using SARSA(λ).
        
        Returns:
            List of cumulative rewards per episode
        """
        episode_rewards = []
        
        for episode in range(num_episodes):
            state = self.env.reset()
            action = self.epsilon_greedy(state, self.Q)
            
            # Eligibility traces for state-action pairs
            z = np.zeros((self.env.n_states, self.env.n_actions))
            
            total_reward = 0
            
            while True:
                # Take action, observe reward and next state
                next_state, reward, done, _ = self.env.step(action)
                total_reward += reward
                
                state_idx = self.get_state_index(state)
                next_state_idx = self.get_state_index(next_state)
                
                # Select next action
                if done:
                    next_action = None
                    Q_next = 0
                else:
                    next_action = self.epsilon_greedy(next_state, self.Q)
                    Q_next = self.Q[next_state_idx, next_action]
                
                # TD error
                delta = reward + self.gamma * Q_next - self.Q[state_idx, action]
                
                # Update eligibility trace
                z[state_idx, action] += 1
                
                # Update Q for all state-action pairs
                self.Q += self.alpha * delta * z
                
                # Decay eligibility traces
                z = self.gamma * self.lam * z
                
                if done:
                    break
                
                state = next_state
                action = next_action
            
            episode_rewards.append(total_reward)
        
        return episode_rewards

