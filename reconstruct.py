import sys
import pycxsom as cx
import numpy as np
import matplotlib.pyplot as plt

def quantize_thrust(continuous_value):
    """
    Snap continuous thrust prediction to discrete action space.
    
    The normalized thrust values are mapped as follows:
    - Original discrete values: -1, 0, 15
    - After normalization to [0,1]: approximately 0.0, 0.0625, 1.0
    
    Mapping strategy:
    - [0.0, 0.33) -> -1 (strong negative thrust)
    - [0.33, 0.67) -> 0 (no thrust)
    - [0.67, 1.0] -> 15 (strong positive thrust)
    
    For denormalization: thrust_real = thrust_min + value * (thrust_max - thrust_min)
    With typical values: -1 + value * 16 = -1 + value * 16
    """
    if continuous_value < 0.33:
        return -1
    elif continuous_value < 0.67:
        return 0
    else:
        return 15

if len(sys.argv) < 2:
    print(f'Usage : {sys.argv[0]} <root-dir>')
    sys.exit(0)

root_dir = sys.argv[1]

# Note: This script was originally for RGB image reconstruction.
# It's been adapted for rocket thrust prediction.
# The variable names 'rgb' refer to the old image context but now represent thrust.

try:
    # Try to load predicted thrust from the new location
    PRED = np.fromiter(
        (value for _, value in cx.variable.data_range_full(
            cx.variable.path_from(root_dir, 'predict-out', 'predicted-thrust')
        )), 
        dtype=float
    )
    print(f"Loaded {len(PRED)} thrust predictions from 'predicted-thrust'")
    
    # Quantize continuous predictions to discrete values
    PRED_QUANTIZED = np.array([quantize_thrust(val) for val in PRED])
    
    # Display statistics
    print(f"\nContinuous thrust predictions:")
    print(f"  Min: {PRED.min():.4f}, Max: {PRED.max():.4f}, Mean: {PRED.mean():.4f}")
    print(f"\nQuantized thrust distribution:")
    unique, counts = np.unique(PRED_QUANTIZED, return_counts=True)
    for val, count in zip(unique, counts):
        print(f"  Thrust = {val:2.0f}: {count:4d} samples ({100*count/len(PRED_QUANTIZED):.1f}%)")
    
    # If normalization parameters exist, show denormalized values
    try:
        norm_params = np.load('data/normalization_params.npy', allow_pickle=True).item()
        thrust_min = norm_params['thrust_min']
        thrust_max = norm_params['thrust_max']
        
        # Denormalize
        PRED_DENORM = thrust_min + PRED * (thrust_max - thrust_min)
        print(f"\nDenormalized continuous predictions:")
        print(f"  Min: {PRED_DENORM.min():.2f}, Max: {PRED_DENORM.max():.2f}, Mean: {PRED_DENORM.mean():.2f}")
        
    except FileNotFoundError:
        print("\nNormalization parameters not found - cannot denormalize.")
    
    print(f"\n✓ Thrust predictions analyzed successfully.")
    print(f"  Use these quantized values for rocket control: {np.unique(PRED_QUANTIZED)}")
    
except Exception as e:
    print(f"Error: {e}")
    print(f"Make sure you have run 'make predict' first.")
    sys.exit(1)
