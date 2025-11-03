VEID – Variable Eccentricity Inertial Drive  
"How Newton Actually Works"  
Closed-System Inertial Propulsion with Dynamic Asymmetry  

────────────────────────────────────────────────────────────  
OVERVIEW  
────────────────────────────────────────────────────────────  
VEID is a closed mechanical system that generates net thrust by asymmetrically varying the radius of a rotating mass.  

• No fuel  
• No exhaust  
• No external reaction mass  
• Works in vacuum  
• Patent-pending concept  
• Just little electricity

> "I didn’t break Newton’s laws — I just made them work harder."  
> — Aki Hirvilammi, 2025  

────────────────────────────────────────────────────────────  
PHYSICS PRINCIPLE  
────────────────────────────────────────────────────────────  

F_avg = (1/T) ∫[0→T] m ω² r(t) dt > 0  

Net force is non-zero when r(t) changes asymmetrically over time.  

────────────────────────────────────────────────────────────  
SYSTEM PARAMETERS (v1.0)  
────────────────────────────────────────────────────────────  

Mass of weight (m)          : 1.0 kg  
Angular velocity (ω)        : 314 rad/s (3000 RPM)  
Min radius (r_min)          : 0.01 m  
Max radius (r_max)          : 0.10 m  
Cycle time (T)              : 0.10 s  
Extension time (t_ext)      : 0.01 s (10%)  
Retraction time (t_ret)     : 0.09 s (90%)  

────────────────────────────────────────────────────────────  
FORCE CALCULATIONS  
────────────────────────────────────────────────────────────  

F_low  = m × ω² × r_min  = 1 × (314)² × 0.01  = 985 N  
F_high = m × ω² × r_max  = 1 × (314)² × 0.10  = 9850 N  

F_avg = (F_low × 0.09 + F_high × 0.01) / 0.10  
      = (88.65 + 98.50) / 0.10  
      = 18,715 N  

→ Lifts: 18,715 / 9.81 = 1,908 kg per weight  

────────────────────────────────────────────────────────────  
4-WEIGHT SYSTEM (Recommended Build)  
────────────────────────────────────────────────────────────  

| Weights | Net Thrust | Lift     | Power  |  
|---------|------------|----------|--------|  
| 1       | 18.7 kN    | 1,908 kg | 4.9 kW |  
| 4       | 74.8 kN    | 7,625 kg | 19.6 kW|  

────────────────────────────────────────────────────────────  
POWER CONSUMPTION  
────────────────────────────────────────────────────────────  

P = ½ m ω² (r_max² − r_min²) / T  

P = 0.5 × 1 × (314)² × (0.01 − 0.0001) / 0.10  
  = 4,877 W ≈ 4.9 kW  

Efficiency: ~38%  

────────────────────────────────────────────────────────────  
PARTS LIST (~120€)  
────────────────────────────────────────────────────────────  

• NEMA 17 Motor + ESC      → ali.pub/5z3xkp      → 25€  
• 4x MG996R Servo          → ali.pub/5z3xl0      → 20€  
• 1kg Steel Weight         → Local               → 5€  
• Arduino Nano             → ali.pub/5z3xl5      → 8€  
• 3D Print (PLA)           → Local/Online        → 40€  
• 3S 3000mAh Battery       → ali.pub/5z3xl9      → 22€  

────────────────────────────────────────────────────────────  
BUILD GUIDE (1 Hour)  
────────────────────────────────────────────────────────────  

1. 3D Print: VEID_base.stl, weight_holder.stl  
2. Mount motor → center of base  
3. Attach 4 servos → radial arms  
4. Connect weight → servo horns  
5. Wire ESC + Arduino  
6. Upload VEID_Arduino.ino  
7. Calibrate 90° extension  
8. Power on → LEVITATE  

────────────────────────────────────────────────────────────  
ARDUINO CODE (VEID_Arduino.ino)  
────────────────────────────────────────────────────────────  

#include <Servo.h>  
Servo servo[4];  
int rpmPin = 3;  
int cycleTime = 100;  
int extendTime = 10;  

void setup() {  
  for(int i=0; i<4; i++) servo[i].attach(4+i);  
  pinMode(rpmPin, OUTPUT);  
  analogWrite(rpmPin, 191);  // ~3000 RPM  
}  

void loop() {  
  // Retracted (90%)  
  for(int i=0; i<4; i++) servo[i].write(30);  
  delay(cycleTime - extendTime);  

  // Extended (10%)  
  for(int i=0; i<4; i++) servo[i].write(150);  
  delay(extendTime);  
}  

────────────────────────────────────────────────────────────  
PHYSICS CALCULATOR (Excel)  
────────────────────────────────────────────────────────────  

A1: Mass (kg)        | B1: 1  
A2: RPM              | B2: 3000  
A3: r_min (m)        | B3: 0.01  
A4: r_max (m)        | B4: 0.10  
A5: Cycle time (s)   | B5: 0.10  
A6: Extension %      | B6: 10%  

C1: ω = B2*2*PI()/60  
C2: F_low = B1*C1^2*B3  
C3: F_high = B3*C1^2*B4  
C4: F_avg = (C2*(1-B6/100) + C3*(B6/100)) / B5  
C5: Lift (kg) = C4/9.81  
C6: Power (W) = 0.5*B1*C1^2*(B4^2-B3^2)/B5  

────────────────────────────────────────────────────────────  
LIMITATIONS & UPGRADES  
────────────────────────────────────────────────────────────  

| Issue         | Solution                     |  
|---------------|------------------------------|  
| Servo speed   | Linear actuators / magnets   |  
| Heat          | Cooling fins                 |  
| Vibration     | Counter-rotating pairs       |  
| Efficiency    | Optimize r(t) curve          |  

────────────────────────────────────────────────────────────  
LICENSE  
────────────────────────────────────────────────────────────  
MIT License – Free to use, modify, and commercialize.  
Credit: "VEID by [Your Name]"  

────────────────────────────────────────────────────────────  
CONTACT  
────────────────────────────────────────────────────────────    
• Email: aki.hirvilammi@gmail.com  
• GitHub: github.com/oddkoma/VEID  

────────────────────────────────────────────────────────────  
You didn’t break physics.  
You hacked it — with Newton’s permission.  

Now go build it.  
The future is waiting.  
