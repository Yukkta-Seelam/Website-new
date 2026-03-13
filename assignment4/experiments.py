"""
Experiment runner for comparing different algorithms and parameters.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from windy_cliff_env import WindyCliffEnv
from n_step_sarsa import NStepSARSA
from td_lambda import TDLambda
from sarsa_lambda import SARSALambda
from watkins_q_lambda import WatkinsQLambda

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_n_step_sarsa_experiments(num_runs=10, num_episodes=500):
    """Run n-step SARSA with different n values."""
    print("Running n-step SARSA experiments...")
    
    n_values = [1, 2, 4, 8]
    results = {}
    
    for n in n_values:
        print(f"  Testing n={n}...")
        all_rewards = []
        
        for run in range(num_runs):
            env = WindyCliffEnv()
            agent = NStepSARSA(env, n=n, alpha=0.5, gamma=1.0, epsilon=0.1)
            rewards = agent.learn(num_episodes=num_episodes)
            all_rewards.append(rewards)
        
        # Average across runs
        results[n] = np.mean(all_rewards, axis=0)
    
    return results


def run_lambda_experiments(algorithm_name, num_runs=10, num_episodes=500):
    """Run experiments with different lambda values."""
    print(f"Running {algorithm_name} experiments...")
    
    lambda_values = [0.0, 0.3, 0.7, 1.0]
    results = {}
    
    for lam in lambda_values:
        print(f"  Testing λ={lam}...")
        all_rewards = []
        
        for run in range(num_runs):
            env = WindyCliffEnv()
            
            if algorithm_name == "TD(λ)":
                agent = TDLambda(env, lam=lam, alpha=0.5, gamma=1.0, epsilon=0.1)
            elif algorithm_name == "SARSA(λ)":
                agent = SARSALambda(env, lam=lam, alpha=0.5, gamma=1.0, epsilon=0.1)
            elif algorithm_name == "Watkins Q(λ)":
                agent = WatkinsQLambda(env, lam=lam, alpha=0.5, gamma=1.0, epsilon=0.1)
            else:
                raise ValueError(f"Unknown algorithm: {algorithm_name}")
            
            rewards = agent.learn(num_episodes=num_episodes)
            all_rewards.append(rewards)
        
        # Average across runs
        results[lam] = np.mean(all_rewards, axis=0)
    
    return results


def plot_learning_curves(results, title, xlabel="Episode", ylabel="Cumulative Reward", save_path=None):
    """Plot learning curves."""
    plt.figure(figsize=(10, 6))
    
    for key, rewards in results.items():
        # Smooth the curve using moving average
        window = 10
        if len(rewards) > window:
            smoothed = np.convolve(rewards, np.ones(window)/window, mode='valid')
            episodes = np.arange(window-1, len(rewards))
        else:
            smoothed = rewards
            episodes = np.arange(len(rewards))
        
        plt.plot(episodes, smoothed, label=f"{key}", linewidth=2)
    
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {save_path}")
    
    plt.show()


def compute_convergence_metrics(rewards, threshold=-50):
    """
    Compute convergence metrics.
    
    Args:
        rewards: Array of cumulative rewards per episode
        threshold: Reward threshold to consider "converged"
    
    Returns:
        Dictionary with convergence metrics
    """
    # Find first episode where reward exceeds threshold
    converged_episode = None
    for i, reward in enumerate(rewards):
        if reward >= threshold:
            converged_episode = i
            break
    
    # Average reward in last 10% of episodes
    last_10_percent = int(0.1 * len(rewards))
    avg_final_reward = np.mean(rewards[-last_10_percent:]) if last_10_percent > 0 else rewards[-1]
    
    return {
        'converged_episode': converged_episode,
        'avg_final_reward': avg_final_reward,
        'final_reward': rewards[-1]
    }


def run_all_experiments(num_runs=10, num_episodes=500):
    """Run all experiments and generate plots."""
    print("=" * 60)
    print("Starting Assignment 4 Experiments")
    print("=" * 60)
    
    # 1. n-step SARSA experiments
    print("\n1. n-step SARSA Experiments")
    print("-" * 60)
    n_step_results = run_n_step_sarsa_experiments(num_runs=num_runs, num_episodes=num_episodes)
    plot_learning_curves(
        {f"n={n}": rewards for n, rewards in n_step_results.items()},
        "n-step SARSA: Learning Curves",
        save_path=os.path.join(SCRIPT_DIR, "n_step_sarsa_curves.png")
    )
    
    # 2. TD(λ) experiments
    print("\n2. TD(λ) Experiments")
    print("-" * 60)
    td_results = run_lambda_experiments("TD(λ)", num_runs=num_runs, num_episodes=num_episodes)
    plot_learning_curves(
        {f"λ={lam}": rewards for lam, rewards in td_results.items()},
        "TD(λ): Learning Curves",
        save_path=os.path.join(SCRIPT_DIR, "td_lambda_curves.png")
    )
    
    # 3. SARSA(λ) experiments
    print("\n3. SARSA(λ) Experiments")
    print("-" * 60)
    sarsa_results = run_lambda_experiments("SARSA(λ)", num_runs=num_runs, num_episodes=num_episodes)
    plot_learning_curves(
        {f"λ={lam}": rewards for lam, rewards in sarsa_results.items()},
        "SARSA(λ): Learning Curves",
        save_path=os.path.join(SCRIPT_DIR, "sarsa_lambda_curves.png")
    )
    
    # 4. Watkins Q(λ) experiments
    print("\n4. Watkins Q(λ) Experiments")
    print("-" * 60)
    watkins_results = run_lambda_experiments("Watkins Q(λ)", num_runs=num_runs, num_episodes=num_episodes)
    plot_learning_curves(
        {f"λ={lam}": rewards for lam, rewards in watkins_results.items()},
        "Watkins Q(λ): Learning Curves",
        save_path=os.path.join(SCRIPT_DIR, "watkins_q_lambda_curves.png")
    )
    
    # 5. Comparison plot: All algorithms with λ=0.7
    print("\n5. Algorithm Comparison (λ=0.7 for λ-based algorithms)")
    print("-" * 60)
    comparison_results = {}
    
    # n-step SARSA with n=4
    comparison_results["n-step SARSA (n=4)"] = n_step_results[4]
    
    # λ-based algorithms with λ=0.7
    comparison_results["TD(λ) (λ=0.7)"] = td_results[0.7]
    comparison_results["SARSA(λ) (λ=0.7)"] = sarsa_results[0.7]
    comparison_results["Watkins Q(λ) (λ=0.7)"] = watkins_results[0.7]
    
    plot_learning_curves(
        comparison_results,
        "Algorithm Comparison",
        save_path=os.path.join(SCRIPT_DIR, "algorithm_comparison.png")
    )
    
    # Print convergence metrics
    print("\n" + "=" * 60)
    print("Convergence Metrics")
    print("=" * 60)
    
    print("\nn-step SARSA:")
    for n, rewards in n_step_results.items():
        metrics = compute_convergence_metrics(rewards)
        print(f"  n={n}: Converged at episode {metrics['converged_episode']}, "
              f"Final avg reward: {metrics['avg_final_reward']:.2f}")
    
    print("\nTD(λ):")
    for lam, rewards in td_results.items():
        metrics = compute_convergence_metrics(rewards)
        print(f"  λ={lam}: Converged at episode {metrics['converged_episode']}, "
              f"Final avg reward: {metrics['avg_final_reward']:.2f}")
    
    print("\nSARSA(λ):")
    for lam, rewards in sarsa_results.items():
        metrics = compute_convergence_metrics(rewards)
        print(f"  λ={lam}: Converged at episode {metrics['converged_episode']}, "
              f"Final avg reward: {metrics['avg_final_reward']:.2f}")
    
    print("\nWatkins Q(λ):")
    for lam, rewards in watkins_results.items():
        metrics = compute_convergence_metrics(rewards)
        print(f"  λ={lam}: Converged at episode {metrics['converged_episode']}, "
              f"Final avg reward: {metrics['avg_final_reward']:.2f}")
    
    return {
        'n_step_sarsa': n_step_results,
        'td_lambda': td_results,
        'sarsa_lambda': sarsa_results,
        'watkins_q_lambda': watkins_results
    }


if __name__ == "__main__":
    # Run experiments with fewer runs for faster execution
    # Increase num_runs for more stable results
    results = run_all_experiments(num_runs=5, num_episodes=500)

