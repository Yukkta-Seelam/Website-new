"""
Group Relative Policy Optimization (GRPO) implementation.

GRPO is a policy gradient method that uses group-based relative comparisons
for policy updates, similar to PPO but with group-relative advantages.
"""
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Any, Optional, Tuple
from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.type_aliases import GymEnv, MaybeCallback
from stable_baselines3.common.utils import explained_variance, get_schedule_fn
from stable_baselines3.common.vec_env import VecEnv
from stable_baselines3 import PPO


class GRPO(PPO):
    """
    Group Relative Policy Optimization (GRPO) algorithm.
    
    Extends PPO with group-relative advantage computation.
    """
    
    def __init__(
        self,
        policy: str,
        env: GymEnv,
        learning_rate: float = 3e-4,
        n_steps: int = 2048,
        batch_size: int = 64,
        n_epochs: int = 10,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        clip_range: float = 0.2,
        ent_coef: float = 0.0,
        vf_coef: float = 0.5,
        max_grad_norm: float = 0.5,
        group_size: int = 4,
        tensorboard_log: Optional[str] = None,
        policy_kwargs: Optional[Dict[str, Any]] = None,
        verbose: int = 0,
        seed: Optional[int] = None,
        device: str = "auto",
        _init_setup_model: bool = True,
    ):
        """
        Initialize GRPO.
        
        Args:
            group_size: Size of groups for relative advantage computation
            Other args: Same as PPO
        """
        self.group_size = group_size
        super().__init__(
            policy=policy,
            env=env,
            learning_rate=learning_rate,
            n_steps=n_steps,
            batch_size=batch_size,
            n_epochs=n_epochs,
            gamma=gamma,
            gae_lambda=gae_lambda,
            clip_range=clip_range,
            ent_coef=ent_coef,
            vf_coef=vf_coef,
            max_grad_norm=max_grad_norm,
            tensorboard_log=tensorboard_log,
            policy_kwargs=policy_kwargs,
            verbose=verbose,
            seed=seed,
            device=device,
            _init_setup_model=_init_setup_model,
        )
    
    def _compute_group_relative_advantages(
        self, 
        advantages: np.ndarray, 
        group_size: int
    ) -> np.ndarray:
        """
        Compute group-relative advantages.
        
        Groups advantages and computes relative advantages within each group.
        
        Args:
            advantages: Raw advantages
            group_size: Size of each group
            
        Returns:
            Group-relative advantages
        """
        n_samples = len(advantages)
        n_groups = n_samples // group_size
        remaining = n_samples % group_size
        
        # Reshape advantages into groups
        if remaining > 0:
            # Pad with zeros if needed
            padded_advantages = np.pad(
                advantages, 
                (0, group_size - remaining), 
                mode='constant', 
                constant_values=0
            )
        else:
            padded_advantages = advantages
        
        # Reshape into groups
        grouped_advantages = padded_advantages.reshape(n_groups + (1 if remaining > 0 else 0), group_size)
        
        # Compute group-relative advantages (subtract group mean)
        group_means = np.mean(grouped_advantages, axis=1, keepdims=True)
        relative_advantages = grouped_advantages - group_means
        
        # Flatten back
        if remaining > 0:
            relative_advantages = relative_advantages[:-1].flatten()[:n_samples]
        else:
            relative_advantages = relative_advantages.flatten()
        
        return relative_advantages
    
    def train(self) -> None:
        """
        Update policy using GRPO algorithm.
        Overrides PPO's train method to use group-relative advantages.
        """
        # Switch to train mode
        self.policy.set_training_mode(True)
        
        # Update learning rate
        self._update_learning_rate(self.policy.optimizer)
        
        # Get rollout buffer
        rollout_data = self.rollout_buffer.get(batch_size=None)
        
        # Compute group-relative advantages
        advantages = rollout_data.advantages
        group_relative_advantages = self._compute_group_relative_advantages(
            advantages, 
            self.group_size
        )
        
        # Normalize advantages
        group_relative_advantages = (group_relative_advantages - group_relative_advantages.mean()) / (
            group_relative_advantages.std() + 1e-8
        )
        
        # Replace advantages in rollout data
        rollout_data.advantages = group_relative_advantages
        
        # Continue with standard PPO training using group-relative advantages
        # This reuses PPO's training loop but with modified advantages
        clip_range = self.clip_range(self._current_progress_remaining)
        ent_coef = self.ent_coef_schedule(self._current_progress_remaining)
        
        # Prepare data for training
        values = rollout_data.old_values
        returns = rollout_data.returns
        old_log_probs = rollout_data.old_log_prob
        
        # Get current policy outputs
        obs = rollout_data.observations
        actions = rollout_data.actions
        
        # Convert to tensors
        if isinstance(obs, np.ndarray):
            obs = torch.tensor(obs, device=self.device)
        if isinstance(actions, np.ndarray):
            actions = torch.tensor(actions, device=self.device)
        if isinstance(values, np.ndarray):
            values = torch.tensor(values, device=self.device)
        if isinstance(returns, np.ndarray):
            returns = torch.tensor(returns, device=self.device)
        if isinstance(old_log_probs, np.ndarray):
            old_log_probs = torch.tensor(old_log_probs, device=self.device)
        if isinstance(group_relative_advantages, np.ndarray):
            group_relative_advantages = torch.tensor(group_relative_advantages, device=self.device)
        
        # Training loop
        for epoch in range(self.n_epochs):
            # Shuffle data
            indices = torch.randperm(len(obs), device=self.device)
            
            for start in range(0, len(obs), self.batch_size):
                end = start + self.batch_size
                batch_indices = indices[start:end]
                
                batch_obs = obs[batch_indices]
                batch_actions = actions[batch_indices]
                batch_old_log_probs = old_log_probs[batch_indices]
                batch_advantages = group_relative_advantages[batch_indices]
                batch_returns = returns[batch_indices]
                batch_old_values = values[batch_indices]
                
                # Get current policy outputs
                _, new_log_probs, entropy = self.policy.evaluate_actions(
                    batch_obs, batch_actions
                )
                values_pred = self.policy.predict_values(batch_obs)
                
                # Compute policy loss (PPO clip)
                ratio = torch.exp(new_log_probs - batch_old_log_probs)
                policy_loss_1 = -batch_advantages * ratio
                policy_loss_2 = -batch_advantages * torch.clamp(
                    ratio, 1 - clip_range, 1 + clip_range
                )
                policy_loss = torch.max(policy_loss_1, policy_loss_2).mean()
                
                # Compute value loss
                value_loss = 0.5 * ((values_pred.flatten() - batch_returns) ** 2).mean()
                
                # Compute entropy loss
                entropy_loss = -entropy.mean()
                
                # Total loss
                loss = (
                    policy_loss
                    + self.vf_coef * value_loss
                    + ent_coef * entropy_loss
                )
                
                # Optimize
                self.policy.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.policy.parameters(), self.max_grad_norm)
                self.policy.optimizer.step()
        
        # Log metrics
        explained_var = explained_variance(
            self.rollout_buffer.values.flatten(),
            self.rollout_buffer.returns.flatten()
        )
        
        self._n_updates += self.n_epochs
        self.logger.record("train/learning_rate", self.lr_schedule(self._current_progress_remaining))
        self.logger.record("train/policy_loss", policy_loss.item())
        self.logger.record("train/value_loss", value_loss.item())
        self.logger.record("train/entropy", entropy.mean().item())
        self.logger.record("train/explained_variance", explained_var)
        self.logger.record("train/n_updates", self._n_updates)
        
        # Compute KL divergence (approximate)
        with torch.no_grad():
            kl_div = (new_log_probs - batch_old_log_probs).mean().item()
            self.logger.record("train/approx_kl", kl_div)

