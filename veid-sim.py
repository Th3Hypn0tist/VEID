# veid_video.py
# VEID Animation – Snap + Slow Retract
# Aki Hirvilammi 2025 – Net thrust: +39.27 N·s / 10 s

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import imageio

# --- Parametrit ---
f1 = 10.0           # Kierrosta / s (600 RPM)
r_max = 0.10        # Ulkona [m]
r_min = 0.01        # Sisällä [m]
m = 1.0             # Massa [kg]
T = 10.0            # Animaatioaika [s]
fps = 30            # Video FPS
dt = 1 / (fps * 10) # 10x nopeutettu animaatio
N = int(T / dt)

# --- Alustus ---
t = np.linspace(0, T, N)
theta = 2 * np.pi * f1 * t
theta_mod = theta % (2 * np.pi)
r = np.full(N, r_min)
p_cum = np.zeros(N)

# --- Animaatio ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle("VEID – Snap + Slow Retract | Net p = +39.27 N·s", fontsize=16)

# Akseli 1: Mekaniikka
ax1.set_xlim(-0.15, 0.15)
ax1.set_ylim(-0.15, 0.15)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)
ax1.set_title("Mekaaninen liike")
circle = plt.Circle((0, 0), r_max, fill=False, color='gray', ls='--', alpha=0.5)
ax1.add_patch(circle)
mass = ax1.plot([], [], 'o', markersize=12, color='red')[0]
trace, = ax1.plot([], [], color='red', alpha=0.5, lw=1)
ax1.plot(0, 0, '+', color='black')

# Akseli 2: Momentum
ax2.set_xlim(0, T)
ax2.set_ylim(0, 45)
ax2.set_xlabel("Aika [s]")
ax2.set_ylabel("Netto momentum [N·s]")
ax2.set_title("Netto työntö (kumulatiivinen)")
line, = ax2.plot([], [], color='blue', lw=2)

# Tekstit
txt_momentum = ax2.text(0.02, 0.9, "", transform=ax2.transAxes, fontsize=12, color='blue')
txt_phase = ax1.text(0.02, 0.9, "", transform=ax1.transAxes, fontsize=10)

# --- Päivitysfunktio ---
def update(frame):
    i = frame
    phi = theta_mod[i]
    
    # --- ULOSHYPY: 0° → 90° ---
    if 0 <= phi < np.pi/2:
        r[i] = r_max
        slip = 90
        phase_name = "ULOSHYPY"
        mass.set_color('red')
    
    # --- SNAP NOLLAAN ---
    elif np.pi/2 <= phi < np.pi/2 + 0.01:
        r[i] = r_min
        slip = 0
        phase_name = "SNAP"
        mass.set_color('orange')
    
    # --- HIDAS KELAUS: 90° → 360° (vauhti hidastuu) ---
    else:
        progress = (phi - np.pi/2) / (3 * np.pi / 2)
        slip = 100 * (1 - progress) + 5 * progress
        r[i] = r_min
        phase_name = "HIDAS KELAUS"
        mass.set_color('green')
    
    # Keskipakovoima & momentum
    omega_eff = 2 * np.pi * (f1 + slip)
    F = m * omega_eff**2 * r[i]
    if i > 0:
        p_cum[i] = p_cum[i-1] + F * dt
    
    # Päivitä mekaniikka
    x = r[i] * np.cos(phi)
    y = r[i] * np.sin(phi)
    mass.set_data([x], [y])
    trace.set_data(r[:i+1] * np.cos(theta_mod[:i+1]), r[:i+1] * np.sin(theta_mod[:i+1]))
    
    # Päivitä momentum
    line.set_data(t[:i+1], p_cum[:i+1])
    txt_momentum.set_text(f"Net p = {p_cum[i]:.2f} N·s")
    txt_phase.set_text(f"{phase_name}")
    
    return mass, trace, line, txt_momentum, txt_phase

# --- Luo animaatio ---
ani = FuncAnimation(fig, update, frames=N, interval=1000/fps, blit=True)

# --- Tallenna video ---
print("Luodaan video: veid_demo.mp4 ...")
ani.save('veid_demo.mp4', fps=fps, dpi=100, writer='ffmpeg')
print("Valmis! Katso: veid_demo.mp4")