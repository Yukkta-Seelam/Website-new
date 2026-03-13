# GRPO, PPO, and TRPO Benchmarking

A comprehensive benchmarking framework for comparing Group Relative Policy Optimization (GRPO), Proximal Policy Optimization (PPO), and Trust Region Policy Optimization (TRPO) algorithms under identical experimental conditions.

## Overview

This project implements a fair comparison framework for three policy gradient algorithms:
- **GRPO** (Group Relative Policy Optimization): A variant of PPO with group-relative advantage computation
- **PPO** (Proximal Policy Optimization): Implemented via stable-baselines3
- **TRPO** (Trust Region Policy Optimization): Implemented via stable-baselines3

All algorithms are trained under the same conditions:
- Same environment
- Same number of timesteps
- Identical network architecture
- Consistent hyperparameter tuning strategy

## Features

- **Fair Comparison**: All algorithms use identical experimental conditions
- **Comprehensive Logging**: Tracks average episodic return, policy loss, KL divergence, and training time per iteration
- **Flexible Configuration**: YAML-based configuration system
- **Multiple Environments**: Supports MuJoCo environments (HalfCheetah-v4, Walker2d-v4, etc.)
- **TensorBoard Integration**: Real-time visualization of training metrics
- **Reproducibility**: Seed-based reproducibility for consistent results

## Installation

### Prerequisites

- Python 3.8+
- MuJoCo (for MuJoCo environments)

### Setup

1. Clone the repository:
```bash
cd ~/Desktop/Github/grpo-ppo-trpo-benchmark
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install MuJoCo (if using MuJoCo environments):
```bash
# Follow instructions at https://github.com/google-deepmind/mujoco
# Or use pip install mujoco (for newer versions)
```

## Usage

### Basic Training

Train all three algorithms with default settings:
```bash
python train.py
```

### Train Specific Algorithms

Train only selected algorithms:
```bash
python train.py --algorithms grpo ppo
```

### Custom Configuration

Use a custom configuration file:
```bash
python train.py --config path/to/config.yaml
```

### Specify Environment

Override the environment from config:
```bash
python train.py --env Walker2d-v4
```

### Command Line Options

```
--config PATH          Path to configuration YAML file
--algorithms ALG ...   Algorithms to train (grpo, ppo, trpo, all)
--env ENV_NAME         Environment name (overrides config)
```

## Configuration

The default configuration is in `src/config/default_config.yaml`. Key settings:

- **Environment**: Environment name and seed
- **Training**: Total timesteps, number of parallel environments, seed
- **Network**: Policy network architecture (shared across all algorithms)
- **Algorithms**: Algorithm-specific hyperparameters
- **Logging**: Logging frequency and directories

### Example Configuration

```yaml
env:
  name: "HalfCheetah-v4"
  seed: 42

training:
  total_timesteps: 1000000
  n_envs: 1
  seed: 42

network:
  policy: "MlpPolicy"
  net_arch:
    pi: [64, 64]
    vf: [64, 64]
  activation_fn: "tanh"
```

## Project Structure

```
grpo-ppo-trpo-benchmark/
├── src/
│   ├── algorithms/
│   │   ├── __init__.py
│   │   └── grpo.py          # GRPO implementation
│   ├── config/
│   │   └── default_config.yaml
│   └── utils/
│       ├── __init__.py
│       ├── logger.py        # Metrics logging
│       └── config_loader.py # Configuration loading
├── logs/                    # Training logs
├── results/                 # Saved models and results
├── train.py                 # Main training script
├── requirements.txt
└── README.md
```

## Logged Metrics

The framework logs the following metrics for each algorithm:

- **Average Episodic Return**: Mean return per episode
- **Policy Loss**: Policy gradient loss
- **Value Loss**: Value function loss
- **KL Divergence**: KL divergence between old and new policies
- **Entropy**: Policy entropy
- **Training Time per Iteration**: Time taken for each training iteration
- **Total Timesteps**: Cumulative timesteps collected

Metrics are saved to:
- CSV files: `logs/{algorithm}/metrics.csv`
- TensorBoard: `logs/tensorboard/{algorithm}/`
- Summary JSON: `logs/{algorithm}/summary.json`

## Results

After training, results are saved in:
- **Models**: `results/{algorithm}/best_model/` and `results/{algorithm}/final_model/`
- **Checkpoints**: `results/{algorithm}/checkpoints/`
- **Metrics**: `logs/{algorithm}/metrics.csv`
- **Summaries**: `logs/{algorithm}/summary.json`

## Visualization

View training progress with TensorBoard:
```bash
tensorboard --logdir logs/tensorboard
```

## Algorithm Details

### GRPO (Group Relative Policy Optimization)

GRPO extends PPO by computing group-relative advantages. Advantages are grouped and normalized within each group, which can help with variance reduction in policy gradient estimation.

Key parameter: `group_size` - Size of groups for relative advantage computation

### PPO (Proximal Policy Optimization)

Standard PPO implementation from stable-baselines3 with clipped surrogate objective.

### TRPO (Trust Region Policy Optimization)

TRPO implementation from stable-baselines3 using natural policy gradients with trust region constraints.

## Reproducibility

All experiments use fixed seeds for reproducibility. Set the seed in the configuration file:

```yaml
training:
  seed: 42
env:
  seed: 42
```

## Troubleshooting

### MuJoCo Installation Issues

If you encounter MuJoCo-related errors:
1. Ensure MuJoCo is properly installed
2. Check that the environment name is correct (e.g., `HalfCheetah-v4` not `HalfCheetah-v3`)
3. Try using PyBullet environments instead (modify config to use PyBullet envs)

### CUDA/GPU Issues

If you want to use CPU only, the code will automatically detect and use CPU. For GPU usage, ensure PyTorch is installed with CUDA support.

### Memory Issues

If you run out of memory:
- Reduce `n_steps` in the algorithm configuration
- Reduce `batch_size`
- Use fewer parallel environments (`n_envs: 1`)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## References

- PPO: [Schulman et al., 2017](https://arxiv.org/abs/1707.06347)
- TRPO: [Schulman et al., 2015](https://arxiv.org/abs/1502.05477)
- GRPO: Group Relative Policy Optimization (implementation based on PPO with group-relative advantages)

## Citation

If you use this code in your research, please cite:

```bibtex
@software{grpo_ppo_trpo_benchmark,
  title = {GRPO, PPO, and TRPO Benchmarking Framework},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/yourusername/grpo-ppo-trpo-benchmark}
}
```

