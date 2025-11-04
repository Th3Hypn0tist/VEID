import numpy as np
import matplotlib.pyplot as plt

# --- VEID: Aki Hirvilammi 2025 – "Snap + Slow Retract" ---
f1 = 10.0           # Kierrosta / s (10 Hz = 600 RPM)
r_max = 0.10        # Ulkona [m]
r_min = 0.01        # Sisällä [m]
m = 1.0             # Massa [kg]
T = 10.0            # Simulaatioaika [s]
fs = 1000           # Näytteistys [Hz]
dt = 1/fs
N = int(T * fs)
t = np.linspace(0, T, N)

# Vaihekulmat
theta = 2 * np.pi * f1 * t  # Ulkopyörintä
theta_mod = theta % (2 * np.pi)

# --- 1. 90°: Uloshyppy (nopea, 100 Hz vastaava) ---
# --- 2. Snap nollaan ---
# --- 3. 270°: Hidas kelaus (vauhti hidastuu 100 → 5 Hz ennen nollaa) ---
r = np.full(N, r_min)
F_cent = np.zeros(N)
p = np.zeros(N)

for i in range(N):
    phi = theta_mod[i]
    
    # --- ULOSHYPY: 0° → 90° (ensin 90° ikkuna) ---
    if 0 <= phi < np.pi/2:
        r[i] = r_max
        omega_eff = 2 * np.pi * (f1 + 90)  # Nopea pulssi (~100 Hz)
    
    # --- SNAP NOLLAAN: 90° tarkalleen ---
    elif np.pi/2 <= phi < np.pi/2 + 0.01:
        r[i] = r_min
        omega_eff = 0  # Snap = äkillinen pysäytys
    
    # --- HIDAS KELAUS: 90° → 360° (270°), vauhti hidastuu ---
    else:
        # Hidas kelaus: slip laskee lineaarisesti 100 → 5 Hz
        progress = (phi - np.pi/2) / (3 * np.pi / 2)  # 0 → 1
        slip = 100 * (1 - progress) + 5 * progress
        omega_eff = 2 * np.pi * (f1 + slip)
        r[i] = r_min
    
    # Keskipakovoima
    F_cent[i] = m * omega_eff**2 * r[i]
    
    # Netto momentum (unidirectional)
    if i > 0:
        p[i] = p[i-1] + F_cent[i] * dt

# --- Tulokset ---
print(f"Netto momentum (10 s): {p[-1]:.3f} N·s")
print(f"Keskim. F_net: {np.mean(F_cent):.3f} N")
print(f"Maksimi F: {np.max(F_cent):.1f} N")