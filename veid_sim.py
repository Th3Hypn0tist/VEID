import numpy as np
import matplotlib.pyplot as plt

# VEID – Variable Eccentricity Inertial Drive Sim (Updated v1.0)
# Aki Hirvilammi, 2025 – Asymmetry: 90° extension + snap to zero + 270° low retract

# Parameters
f1 = 50.0        # Outer rotation [Hz]
slip_slow = 10.0 # Retract slip [Hz]
slip_fast = 100.0 # Extension slip [Hz]
r_min = 0.01     # Retract radius [m]
r_max = 0.10     # Extension radius [m]
m = 1.0          # Mass [kg]
friction_coeff = 0.05 # Friction loss [fraction per cycle]
Tsim = 2.0       # Sim time [s]
fs = 1000        # Sampling [Hz]

# Derived
dt = 1.0 / fs
N = int(round(Tsim * fs))
t = np.arange(N) * dt
twopi = 2 * np.pi

# Signals
r = np.zeros(N)
F_cent = np.zeros(N)
F_net = np.zeros(N)
p_cum = np.zeros(N)

th1_c = 0.0  # Outer phase [cycles]

for n in range(N):
    th1_c += f1 * dt
    th1_c -= np.floor(th1_c)
    phir = th1_c * twopi  # Current phase [rad]

    # Extension sector: 90° (pi/2 rad) – high r
    if np.sin(phir) > 0:  # Simplified 90° window (sin >0 for "upper half")
        r[n] = r_max
        f2n = f1 + slip_fast
    else:
        r[n] = r_min
        f2n = f1 + slip_slow

    # Centrifugal force
    F_cent[n] = m * (twopi * f1)**2 * r[n]

    # Friction (proportional to F_cent in retract)
    friction = friction_coeff * F_cent[n] if r[n] == r_min else 0
    F_net[n] = F_cent[n] - friction

    # Cumulative momentum (unidirectional bias – no negative)
    p_cum[n] = p_cum[n-1] if n > 0 else 0 + F_net[n] * dt

print("Net Thrust Proxy: Mean F_net =", np.mean(F_net), "N")
print("Cumulative Momentum: p_cum =", p_cum[-1], "N·s")

# Plots (Comment out for no display)
plt.figure(figsize=(10, 8))
plt.subplot(2,2,1); plt.plot(t, r); plt.title('r(t) – Radius'); plt.ylabel('r [m]')
plt.subplot(2,2,2); plt.plot(t, F_cent); plt.title('F_cent(t)'); plt.ylabel('F [N]')
plt.subplot(2,2,3); plt.plot(t, F_net); plt.title('F_net(t) – with Friction'); plt.ylabel('F [N]')
plt.subplot(2,2,4); plt.plot(t, p_cum); plt.title('Cumulative p(t)'); plt.ylabel('p [N·s]')
plt.tight_layout()
plt.show()