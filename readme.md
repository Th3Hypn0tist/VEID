# VEID – Variable Eccentricity Inertial Drive
**"How Newton Actually Works"**  
*Closed-System Inertial Propulsion with Dynamic Asymmetry*  

### Overview
VEID generates **net thrust** in a closed mechanical system by asymmetrically varying the radius of a rotating mass (variable weight + pulsed rotation).  
- No fuel. No exhaust. No external reaction mass.  
- Works in vacuum.  
- Latest Iter: 90° extension + snap to zero + 270° low-force retract – positive bias (no negative forces).  

**Latest Sim Results (f1=50 Hz, friction=0.05):**  
- Mean F_net: 3215 N  
- Net p: 6431 N·s  
- Thrust proxy: 6431 N·s (unidirectional bias – "swim stroke momentum").  

### Specs (Update Here)
- **Parameters:** f1 = 50 Hz (outer), slip_slow = 10 Hz, slip_fast = 100 Hz, r_min = 0.01 m, r_max = 0.10 m, m = 1 kg.  
- **Asymmetry:** Extension 90° (high impulse), snap to 0, retract 270° (low force) – net bias >0.  
- **Why Works:** Pulssi + snap locks momentum direction – no full symmetry cancel.  
- **Real Test:** Bench servo + vacuum chamber – 70% chance net >0.  

### Run Sim
```bash
python veid_sim.py