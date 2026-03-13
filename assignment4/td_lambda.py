"""
TD(λ) Algorithm for Prediction
"""
import numpy as np


class TDLambda:
    """
    TD(λ) for prediction with state values and epsilon-greedy exploration.
    """
    
    def __init__(self, env, lam=0.0, alpha=0.5, gamma=1.0, epsilon=0.1):
        """
        Initialize TD(λ).
        
        Args:
            env: WindyCliffEnv instance
            lam: Lambda parameter (0=TD(0), 1=MC)
            alpha: Learning rate
            gamma: Discount factor
            epsilon: Epsilon for epsilon-greedy policy
        """
        self.env = env
        self.lam = lam
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
        # V-table: state values
        self.V = np.zeros(env.n_states)
        
        # Epsilon-greedy policy (for action selection)
        # We'll use a simple policy: prefer actions that lead to higher value states
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
        Learn using TD(λ) with epsilon-greedy exploration.
        
        Returns:
            List of cumulative rewards per episode
        """
        episode_rewards = []
        
        for episode in range(num_episodes):
            state = self.env.reset()
            action = self.epsilon_greedy(state, self.Q)
            
            # Eligibility traces
            z = np.zeros(self.env.n_states)
            
            total_reward = 0
            
            while True:
                # Take action, observe reward and next state
                next_state, reward, done, _ = self.env.step(action)
                total_reward += reward
                
                state_idx = self.get_state_index(state)
                next_state_idx = self.get_state_index(next_state)
                
                # TD error
                delta = reward + self.gamma * self.V[next_state_idx] - self.V[state_idx]
                
                # Update eligibility trace
                z[state_idx] += 1
                
                # Update value function
                self.V += self.alpha * delta * z
                
                # Update eligibility traces
                z = self.gamma * self.lam * z
                
                # Update Q for policy improvement (using TD update)
                if not done:
                    next_action = self.epsilon_greedy(next_state, self.Q)
                    # Simple Q update for policy
                    self.Q[state_idx, action] += self.alpha * (
                        reward + self.gamma * self.Q[next_state_idx, next_action] - self.Q[state_idx, action]
                    )
                    action = next_action
                
                state = next_state
                
                if done:
                    break
            
            episode_rewards.append(total_reward)
        
        return episode_rewards

