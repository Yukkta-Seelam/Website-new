#!/usr/bin/env python3
"""
Main training script for benchmarking GRPO, PPO, and TRPO algorithms.

This script trains all three algorithms under identical experimental conditions
and logs key metrics for comparison.
"""
import os
import sys
import time
import argparse
from pathlib import Path
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO, TRPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from stable_baselines3.common.monitor import Monitor

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.algorithms.grpo import GRPO
from src.utils.logger import MetricsLogger
from src.utils.config_loader import load_config


class CustomMetricsCallback:
    """Callback to extract and log custom metrics during training."""
    
    def __init__(self, metrics_logger: MetricsLogger):
        self.metrics_logger = metrics_logger
        self.iteration = 0
        self.start_time = None
        self.last_iter_time = None
        
    def on_training_start(self):
        """Called at the start of training."""
        self.start_time = time.time()
        self.last_iter_time = time.time()
    
    def on_step(self, algorithm, iteration: int = None):
        """Called after each training step."""
        if iteration is None:
            iteration = self.iteration
        
        # Get metrics from algorithm's logger
        logger = algorithm.logger
        
        # Extract metrics
        policy_loss = logger.name_to_value.get('train/policy_loss', None)
        value_loss = logger.name_to_value.get('train/value_loss', None)
        kl_div = logger.name_to_value.get('train/approx_kl', None)
        entropy = logger.name_to_value.get('train/entropy', None)
        
        # Compute training time
        current_time = time.time()
        training_time = current_time - self.last_iter_time if self.last_iter_time else 0
        self.last_iter_time = current_time
        
        # Evaluate episodic return
        if hasattr(algorithm, 'env') and algorithm.env is not None:
            episodic_returns = []
            eval_env = algorithm.env
            for _ in range(10):  # Run 10 episodes for average
                obs = eval_env.reset()
                done = False
                episode_return = 0
                while not done:
                    action, _ = algorithm.predict(obs, deterministic=False)
                    obs, reward, done, info = eval_env.step(action)
                    episode_return += reward
                    if done:
                        break
                episodic_returns.append(episode_return)
            avg_episodic_return = np.mean(episodic_returns)
        else:
            avg_episodic_return = 0
        
        # Log metrics
        self.metrics_logger.log(
            iteration=iteration,
            episodic_return=avg_episodic_return,
            policy_loss=policy_loss,
            value_loss=value_loss,
            kl_divergence=kl_div,
            entropy=entropy,
            training_time=training_time,
            total_timesteps=algorithm.num_timesteps,
            episode=iteration
        )
        
        self.iteration += 1


def train_algorithm(
    algorithm_name: str,
    algorithm_class,
    env_name: str,
    config: dict,
    log_dir: str,
    results_dir: str,
    seed: int = 42
):
    """
    Train a single algorithm.
    
    Args:
        algorithm_name: Name of the algorithm ('ppo', 'trpo', 'grpo')
        algorithm_class: Algorithm class to instantiate
        env_name: Gym environment name
        config: Configuration dictionary
        log_dir: Directory for logs
        results_dir: Directory for results
        seed: Random seed
    """
    print(f"\n{'='*60}")
    print(f"Training {algorithm_name.upper()}")
    print(f"{'='*60}\n")
    
    # Create environment
    env = make_vec_env(
        env_name,
        n_envs=config['training']['n_envs'],
        seed=seed,
        monitor_dir=str(Path(log_dir) / algorithm_name / "monitor")
    )
    
    # Get algorithm-specific config
    algo_config = config['algorithms'][algorithm_name]
    network_config = config['network']
    
    # Create metrics logger
    metrics_logger = MetricsLogger(log_dir, algorithm_name)
    
    # Create algorithm instance
    policy_kwargs = {
        'net_arch': network_config['net_arch'],
        'activation_fn': {'tanh': 'tanh', 'relu': 'relu'}.get(
            network_config['activation_fn'], 'tanh'
        )
    }
    
    # Initialize algorithm with appropriate parameters
    if algorithm_name == 'grpo':
        model = algorithm_class(
            policy=network_config['policy'],
            env=env,
            learning_rate=algo_config['learning_rate'],
            n_steps=algo_config['n_steps'],
            batch_size=algo_config['batch_size'],
            n_epochs=algo_config['n_epochs'],
            gamma=algo_config['gamma'],
            gae_lambda=algo_config['gae_lambda'],
            clip_range=algo_config['clip_range'],
            ent_coef=algo_config['ent_coef'],
            vf_coef=algo_config['vf_coef'],
            max_grad_norm=algo_config['max_grad_norm'],
            group_size=algo_config['group_size'],
            tensorboard_log=str(Path(log_dir) / "tensorboard" / algorithm_name),
            policy_kwargs=policy_kwargs,
            verbose=config['logging']['verbose'],
            seed=seed,
        )
    elif algorithm_name == 'ppo':
        model = algorithm_class(
            policy=network_config['policy'],
            env=env,
            learning_rate=algo_config['learning_rate'],
            n_steps=algo_config['n_steps'],
            batch_size=algo_config['batch_size'],
            n_epochs=algo_config['n_epochs'],
            gamma=algo_config['gamma'],
            gae_lambda=algo_config['gae_lambda'],
            clip_range=algo_config['clip_range'],
            ent_coef=algo_config['ent_coef'],
            vf_coef=algo_config['vf_coef'],
            max_grad_norm=algo_config['max_grad_norm'],
            tensorboard_log=str(Path(log_dir) / "tensorboard" / algorithm_name),
            policy_kwargs=policy_kwargs,
            verbose=config['logging']['verbose'],
            seed=seed,
        )
    elif algorithm_name == 'trpo':
        model = algorithm_class(
            policy=network_config['policy'],
            env=env,
            learning_rate=algo_config['learning_rate'],
            n_steps=algo_config['n_steps'],
            batch_size=algo_config['batch_size'],
            gamma=algo_config['gamma'],
            gae_lambda=algo_config['gae_lambda'],
            cg_max_steps=algo_config['cg_max_steps'],
            cg_damping=algo_config['cg_damping'],
            line_search_shrinking_factor=algo_config['line_search_shrinking_factor'],
            line_search_max_iter=algo_config['line_search_max_iter'],
            n_critic_updates=algo_config['n_critic_updates'],
            target_kl=algo_config['target_kl'],
            tensorboard_log=str(Path(log_dir) / "tensorboard" / algorithm_name),
            policy_kwargs=policy_kwargs,
            verbose=config['logging']['verbose'],
            seed=seed,
        )
    
    # Create evaluation callback
    eval_env = make_vec_env(env_name, n_envs=1, seed=seed)
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=str(Path(results_dir) / algorithm_name / "best_model"),
        log_path=str(Path(log_dir) / algorithm_name / "eval"),
        eval_freq=config['logging']['eval_freq'],
        n_eval_episodes=config['logging']['n_eval_episodes'],
        deterministic=True,
        render=False,
    )
    
    # Create checkpoint callback
    checkpoint_callback = CheckpointCallback(
        save_freq=config['logging']['save_freq'],
        save_path=str(Path(results_dir) / algorithm_name / "checkpoints"),
        name_prefix=algorithm_name,
    )
    
    # Custom metrics callback
    metrics_callback = CustomMetricsCallback(metrics_logger)
    metrics_callback.on_training_start()
    
    # Train model
    print(f"Starting training for {algorithm_name.upper()}...")
    start_time = time.time()
    
    try:
        model.learn(
            total_timesteps=config['training']['total_timesteps'],
            callback=[eval_callback, checkpoint_callback],
            progress_bar=True,
        )
        
        # Manually log final metrics
        final_iter = model.num_timesteps // config['algorithms'][algorithm_name]['n_steps']
        metrics_callback.on_step(model, iteration=final_iter)
        
    except Exception as e:
        print(f"Error during training: {e}")
        raise
    
    training_time = time.time() - start_time
    
    # Save final model
    model_path = Path(results_dir) / algorithm_name / "final_model"
    model_path.mkdir(parents=True, exist_ok=True)
    model.save(str(model_path / f"{algorithm_name}_final"))
    
    # Save metrics summary
    summary = metrics_logger.save_summary()
    summary['total_training_time'] = training_time
    print(f"\nTraining completed in {training_time:.2f} seconds")
    print(f"Summary: {summary}")
    
    return model, metrics_logger


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description="Train GRPO, PPO, and TRPO algorithms")
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration YAML file (default: uses default_config.yaml)"
    )
    parser.add_argument(
        "--algorithms",
        type=str,
        nargs="+",
        choices=['grpo', 'ppo', 'trpo', 'all'],
        default=['all'],
        help="Algorithms to train (default: all)"
    )
    parser.add_argument(
        "--env",
        type=str,
        default=None,
        help="Environment name (overrides config)"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override environment if specified
    if args.env:
        config['env']['name'] = args.env
    
    # Determine which algorithms to train
    if 'all' in args.algorithms:
        algorithms_to_train = ['grpo', 'ppo', 'trpo']
    else:
        algorithms_to_train = args.algorithms
    
    # Algorithm mapping
    algorithm_classes = {
        'grpo': GRPO,
        'ppo': PPO,
        'trpo': TRPO,
    }
    
    # Create directories
    log_dir = config['logging']['log_dir']
    results_dir = config['results_dir']
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    Path(results_dir).mkdir(parents=True, exist_ok=True)
    
    # Set seed
    seed = config['training']['seed']
    np.random.seed(seed)
    
    # Train each algorithm
    results = {}
    for algo_name in algorithms_to_train:
        if algo_name not in algorithm_classes:
            print(f"Warning: Unknown algorithm {algo_name}, skipping...")
            continue
        
        try:
            model, logger = train_algorithm(
                algorithm_name=algo_name,
                algorithm_class=algorithm_classes[algo_name],
                env_name=config['env']['name'],
                config=config,
                log_dir=log_dir,
                results_dir=results_dir,
                seed=seed,
            )
            results[algo_name] = logger.get_summary()
        except Exception as e:
            print(f"Failed to train {algo_name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Print final comparison
    print(f"\n{'='*60}")
    print("TRAINING COMPLETE - SUMMARY")
    print(f"{'='*60}\n")
    
    for algo_name, summary in results.items():
        print(f"{algo_name.upper()}:")
        print(f"  Mean Episodic Return: {summary['mean_episodic_return']:.2f} ± {summary['std_episodic_return']:.2f}")
        print(f"  Max Episodic Return: {summary['max_episodic_return']:.2f}")
        print(f"  Total Training Time: {summary['total_training_time']:.2f}s")
        print()


if __name__ == "__main__":
    main()

