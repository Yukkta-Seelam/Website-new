"""
Main script to run Assignment 4 experiments.
"""
from experiments import run_all_experiments

if __name__ == "__main__":
    print("Assignment 4: Windy Cliff Environment - RL Algorithms")
    print("=" * 60)
    
    # Run all experiments
    # Adjust num_runs and num_episodes as needed
    # More runs = more stable results but slower
    results = run_all_experiments(num_runs=10, num_episodes=500)
    
    print("\n" + "=" * 60)
    print("Experiments completed!")
    print("=" * 60)
    print("\nGenerated plots:")
    print("  - n_step_sarsa_curves.png")
    print("  - td_lambda_curves.png")
    print("  - sarsa_lambda_curves.png")
    print("  - watkins_q_lambda_curves.png")
    print("  - algorithm_comparison.png")

