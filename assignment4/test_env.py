"""
Quick test script to verify the environment works correctly.
"""
from windy_cliff_env import WindyCliffEnv

def test_environment():
    """Test the windy cliff environment."""
    print("Testing Windy Cliff Environment")
    print("=" * 40)
    
    env = WindyCliffEnv()
    
    print(f"Grid size: {env.height}×{env.width}")
    print(f"Start: {env.start_pos}")
    print(f"Goal: {env.goal_pos}")
    print(f"Wind strength: {env.wind_strength}")
    print()
    
    # Test a few steps
    print("Testing a few steps:")
    state = env.reset()
    print(f"Initial state: {state}")
    
    for i in range(5):
        action = env.actions[i % len(env.actions)]  # Cycle through actions
        next_state, reward, done, _ = env.step(action)
        print(f"Step {i+1}: Action={action}, Reward={reward}, Next state={next_state}, Done={done}")
        if done:
            break
        state = next_state
    
    print("\nEnvironment test completed!")

if __name__ == "__main__":
    test_environment()

