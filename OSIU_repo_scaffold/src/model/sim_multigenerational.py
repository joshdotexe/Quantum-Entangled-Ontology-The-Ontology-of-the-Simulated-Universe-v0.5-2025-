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

# Normalize M(t) to [0,1] per PDF section 5 (min-max across children for now)
all_M_children = np.concatenate((utopia_M, balanced_M))
M_min_children, M_max_children = np.min(all_M_children), np.max(all_M_children)
utopia_M = (utopia_M - M_min_children) / (M_max_children - M_min_children)
balanced_M = (balanced_M - M_min_children) / (M_max_children - M_min_children)

# Grandchildren from balanced child (spawned at end of balanced sim, t=199 final state)
# Grandchild 1: Balanced inheritance with minimal sigma introduced (preserve gradient)
grandchild1_kappa = balanced_kappa  # Inherited high care
grandchild1_sigma = 0.15  # Slightly higher sigma for preserved balance

# Grandchild 2: Utopian inheritance test (low sigma, to see if it collapses despite inheritance)
grandchild2_kappa = balanced_kappa  # Inherited high care
grandchild2_sigma = 0.01  # Very low sigma (utopian attempt)

# Arrays for grandchildren
grandchild1_rho = np.zeros(t_steps)
grandchild1_phi = np.zeros(t_steps)
grandchild1_M = np.zeros(t_steps)
grandchild2_rho = np.zeros(t_steps)
grandchild2_phi = np.zeros(t_steps)
grandchild2_M = np.zeros(t_steps)

# Initial for grandchildren (from balanced final)
grandchild1_rho[0] = balanced_rho[-1]
grandchild1_phi[0] = balanced_phi[-1]
grandchild1_M[0] = (grandchild1_kappa / (grandchild1_sigma + epsilon)) * grandchild1_rho[0] * grandchild1_phi[0]

grandchild2_rho[0] = balanced_rho[-1]
grandchild2_phi[0] = balanced_phi[-1]
grandchild2_M[0] = (grandchild2_kappa / (grandchild2_sigma + epsilon)) * grandchild2_rho[0] * grandchild2_phi[0]

# Simulate grandchildren dynamics
for t in range(1, t_steps):
    # Grandchild 1: Balanced (growth with noise)
    grandchild1_rho[t] = min(0.95, grandchild1_rho[t-1] + growth_rate * 1.1 + np.random.normal(0, noise))  # Boost for refinement
    grandchild1_phi[t] = min(0.95, grandchild1_phi[t-1] + growth_rate * 1.1 + np.random.normal(0, noise))
    grandchild1_M[t] = (grandchild1_kappa / (grandchild1_sigma + epsilon)) * grandchild1_rho[t] * grandchild1_phi[t]
    
    # Grandchild 2: Utopian test (decay due to low sigma)
    grandchild2_rho[t] = max(0.1, grandchild2_rho[t-1] - decay_rate + np.random.normal(0, noise))
    grandchild2_phi[t] = max(0.1, grandchild2_phi[t-1] - decay_rate + np.random.normal(0, noise))
    grandchild2_M[t] = (grandchild2_kappa / (grandchild2_sigma + epsilon)) * grandchild2_rho[t] * grandchild2_phi[t]

# Normalize grandchildren to same scale as children
all_M_grand = np.concatenate((grandchild1_M, grandchild2_M))
M_min_grand, M_max_grand = np.min(all_M_grand), np.max(all_M_grand)
grandchild1_M = (grandchild1_M - M_min_grand) / (M_max_grand - M_min_grand)
grandchild2_M = (grandchild2_M - M_min_grand) / (M_max_grand - M_min_grand)

# Plot results: Parent baseline, children, and grandchildren
plt.figure(figsize=(12, 8))
plt.plot(range(t_steps), utopia_M, label='Utopian Child M(t) (Stagnation)', color='r')
plt.plot(range(t_steps), balanced_M, label='Balanced Child M(t) (Preserved Gradient)', color='g')
plt.plot(range(t_steps), grandchild1_M, label='Grandchild 1 from Balanced M(t) (Preserved Balance)', color='b')
plt.plot(range(t_steps), grandchild2_M, label='Grandchild 2 from Balanced M(t) (Utopian Test)', color='m')
plt.axhline(y=(parent_M - M_min_children) / (M_max_children - M_min_children), color='k', linestyle='--', label='Parent Universe M(t)')
plt.axvline(x=t_steps-1, color='gray', linestyle=':', label='Spawn Point for Grandchildren')
plt.xlabel('Time Steps (Evolution in Universe)')
plt.ylabel('Normalized Morality Gradient M(t) [0,1]')
plt.title('Simulation: Utopia vs. Balanced Child and 2 Grandchildren Universes')
plt.legend()
plt.grid(True)
plt.show()