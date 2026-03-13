"""
Logging utilities for tracking training metrics.
"""
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any
import numpy as np
import pandas as pd
from stable_baselines3.common.logger import configure


class MetricsLogger:
    """Logger for tracking training metrics across algorithms."""
    
    def __init__(self, log_dir: str, algorithm_name: str):
        """
        Initialize logger.
        
        Args:
            log_dir: Directory to save logs
            algorithm_name: Name of the algorithm being logged
        """
        self.log_dir = Path(log_dir) / algorithm_name
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.algorithm_name = algorithm_name
        
        # Metrics storage
        self.metrics = {
            'episode': [],
            'episodic_return': [],
            'policy_loss': [],
            'value_loss': [],
            'kl_divergence': [],
            'entropy': [],
            'training_time_per_iter': [],
            'total_timesteps': [],
            'iteration': []
        }
        
        # CSV file for metrics
        self.csv_path = self.log_dir / "metrics.csv"
        
    def log(self, 
            iteration: int,
            episodic_return: float,
            policy_loss: float = None,
            value_loss: float = None,
            kl_divergence: float = None,
            entropy: float = None,
            training_time: float = None,
            total_timesteps: int = None,
            episode: int = None):
        """
        Log metrics for a training iteration.
        
        Args:
            iteration: Training iteration number
            episodic_return: Average episodic return
            policy_loss: Policy loss value
            value_loss: Value function loss
            kl_divergence: KL divergence between old and new policy
            entropy: Policy entropy
            training_time: Time taken for this iteration (seconds)
            total_timesteps: Total timesteps collected so far
            episode: Episode number
        """
        if episode is None:
            episode = len(self.metrics['episode'])
            
        self.metrics['iteration'].append(iteration)
        self.metrics['episode'].append(episode)
        self.metrics['episodic_return'].append(episodic_return)
        self.metrics['policy_loss'].append(policy_loss if policy_loss is not None else np.nan)
        self.metrics['value_loss'].append(value_loss if value_loss is not None else np.nan)
        self.metrics['kl_divergence'].append(kl_divergence if kl_divergence is not None else np.nan)
        self.metrics['entropy'].append(entropy if entropy is not None else np.nan)
        self.metrics['training_time_per_iter'].append(training_time if training_time is not None else np.nan)
        self.metrics['total_timesteps'].append(total_timesteps if total_timesteps is not None else np.nan)
        
        # Save to CSV periodically
        if len(self.metrics['iteration']) % 10 == 0:
            self.save_to_csv()
    
    def save_to_csv(self):
        """Save metrics to CSV file."""
        df = pd.DataFrame(self.metrics)
        df.to_csv(self.csv_path, index=False)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of logged metrics."""
        df = pd.DataFrame(self.metrics)
        summary = {
            'algorithm': self.algorithm_name,
            'total_iterations': len(self.metrics['iteration']),
            'mean_episodic_return': df['episodic_return'].mean() if len(df) > 0 else 0,
            'std_episodic_return': df['episodic_return'].std() if len(df) > 0 else 0,
            'max_episodic_return': df['episodic_return'].max() if len(df) > 0 else 0,
            'mean_policy_loss': df['policy_loss'].mean() if len(df) > 0 else 0,
            'mean_kl_divergence': df['kl_divergence'].mean() if len(df) > 0 else 0,
            'total_training_time': df['training_time_per_iter'].sum() if len(df) > 0 else 0,
        }
        return summary
    
    def save_summary(self):
        """Save summary to JSON file."""
        summary = self.get_summary()
        summary_path = self.log_dir / "summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        return summary

