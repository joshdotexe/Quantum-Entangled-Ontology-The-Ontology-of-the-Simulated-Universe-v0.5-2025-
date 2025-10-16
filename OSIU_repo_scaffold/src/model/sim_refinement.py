import numpy as np
import matplotlib.pyplot as plt

# Parameters from PDF
t_steps = 200  # Time steps per generation
epsilon = 0.01  # Stability constant
rho_initial = 0.7  # Responsiveness
phi_initial = 0.6  # Pluralism

# Parent universe: Near-optimal (high M(t), low sigma, high kappa)
parent_kappa = 0.9  # High care
parent_sigma = 0.05  # Low suffering (near-utopian)

# Calculate initial M(t) for parent
parent_M = (parent_kappa / (parent_sigma + epsilon)) * rho_initial * phi_initial

# Child universes (spawned from parent)
# Utopian child: Very low sigma (utopia, no suffering gradient)
utopia_kappa = 0.95  # Even higher care
utopia_sigma = 0.01  # Minimal suffering

# Balanced child: Introduced minimal sigma for balance
balanced_kappa = 0.9  # High care
balanced_sigma = 0.2  # Slight suffering to preserve gradient

# Arrays for simulation (parent is baseline, so no array)
utopia_M = np.zeros(t_steps)
balanced_M = np.zeros(t_steps)
utopia_rho = np.zeros(t_steps)
utopia_phi = np.zeros(t_steps)
balanced_rho = np.zeros(t_steps)
balanced_phi = np.zeros(t_steps)

# Initial values for children
utopia_M[0] = (utopia_kappa / (utopia_sigma + epsilon)) * rho_initial * phi_initial
balanced_M[0] = (balanced_kappa / (balanced_sigma + epsilon)) * rho_initial * phi_initial
utopia_rho[0] = rho_initial
utopia_phi[0] = phi_initial
balanced_rho[0] = rho_initial
balanced_phi[0] = phi_initial

# Simulation dynamics for children
decay_rate = 0.001  # Stagnation decay in utopia
growth_rate = 0.0005  # Adaptation growth in balanced
noise = 0.01  # Small random noise for realism

for t in range(1, t_steps):
    # Utopian child: Stagnation (decay due to no suffering gradient)
    utopia_rho[t] = max(0.1, utopia_rho[t-1] - decay_rate + np.random.normal(0, noise))
    utopia_phi[t] = max(0.1, utopia_phi[t-1] - decay_rate + np.random.normal(0, noise))
    utopia_M[t] = (utopia_kappa / (utopia_sigma + epsilon)) * utopia_rho[t] * utopia_phi[t]
    
    # Balanced child: Preservation of balance (slight growth/adaptation)
    balanced_rho[t] = min(0.9, balanced_rho[t-1] + growth_rate + np.random.normal(0, noise))
    balanced_phi[t] = min(0.9, balanced_phi[t-1] + growth_rate + np.random.normal(0, noise))
    balanced_M[t] = (balanced_kappa / (balanced_sigma + epsilon)) * balanced_rho[t] * balanced_phi[t]

# Normalize M(t) to [0,1] per PDF section 5 (min-max across all values)
all_M = np.concatenate((utopia_M, balanced_M))
M_min, M_max = np.min(all_M), np.max(all_M)
utopia_M = (utopia_M - M_min) / (M_max - M_min)
balanced_M = (balanced_M - M_min) / (M_max - M_min)

# Grandchild from balanced child (spawned at end of balanced sim, t=199 final state)
# Grandchild: Inherits from balanced, with minimal sigma introduced for balance (to avoid utopia)
grandchild_kappa = balanced_kappa  # Inherited high care
grandchild_sigma = 0.15  # Slightly higher sigma than parent/child for preserved gradient
grandchild_rho = np.zeros(t_steps)
grandchild_phi = np.zeros(t_steps)
grandchild_M = np.zeros(t_steps)

# Initial for grandchild (from balanced final)
grandchild_rho[0] = balanced_rho[-1]
grandchild_phi[0] = balanced_phi[-1]
grandchild_M[0] = (grandchild_kappa / (grandchild_sigma + epsilon)) * grandchild_rho[0] * grandchild_phi[0]

# Simulate grandchild dynamics (similar to balanced: growth with noise)
for t in range(1, t_steps):
    grandchild_rho[t] = min(0.95, grandchild_rho[t-1] + growth_rate * 1.1 + np.random.normal(0, noise))  # Slight boost for refinement
    grandchild_phi[t] = min(0.95, grandchild_phi[t-1] + growth_rate * 1.1 + np.random.normal(0, noise))
    grandchild_M[t] = (grandchild_kappa / (grandchild_sigma + epsilon)) * grandchild_rho[t] * grandchild_phi[t]

# Normalize grandchild M(t) to same scale
grandchild_M = (grandchild_M - M_min) / (M_max - M_min)

# Plot results: Parent baseline, children, and grandchild
plt.figure(figsize=(12, 8))
plt.plot(range(t_steps), utopia_M, label='Utopian Child M(t) (Stagnation)', color='r')
plt.plot(range(t_steps), balanced_M, label='Balanced Child M(t) (Preserved Gradient)', color='g')
plt.plot(range(t_steps), grandchild_M, label='Grandchild from Balanced M(t) (Further Refinement)', color='b')
plt.axhline(y=(parent_M - M_min) / (M_max - M_min), color='k', linestyle='--', label='Parent Universe M(t)')
plt.axvline(x=t_steps-1, color='gray', linestyle=':', label='Spawn Point for Grandchild')
plt.xlabel('Time Steps (Evolution in Universe)')
plt.ylabel('Normalized Morality Gradient M(t) [0,1]')
plt.title('Simulation: Utopia vs. Balanced Child and Grandchild Universes')
plt.legend()
plt.grid(True)
plt.show()