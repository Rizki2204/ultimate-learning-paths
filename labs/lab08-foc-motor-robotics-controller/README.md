# Laboratory 08: Field-Oriented Control (FOC) & Robotics Kinematics

## 1. Architectural Overview
This laboratory implements an embedded motion controller featuring Field-Oriented Control (FOC) for Permanent Magnet Synchronous Motors (PMSM) and analytical kinematics for a 2-Degree-of-Freedom (2-DoF) planar robotic manipulator in C and Python. The controller achieves decoupled torque and flux control via Clarke and Park coordinate transformations, regulates stator currents using dual discrete proportional-integral (PI) regulators with anti-windup clamping, synthesizes inverter gate signals via Space Vector Pulse-Width Modulation (SVPWM), and solves forward and inverse kinematics.

```
+-----------------------------------------------------------------------+
|                    FOC Motion & Kinematics Control                    |
|                                                                       |
|   Target Position (x, y)                                              |
|          |                                                            |
|          v                                                            |
|   +---------------------------------------------------------------+   |
|   | 2-DoF Inverse Kinematics (IK)                                 |   |
|   | Analytical Solution: Joint Angles (theta1, theta2)            |   |
|   +---------------------------------------------------------------+   |
|          |                                                            |
|          v Target Current Setpoint (i_d* = 0, i_q* = Torque)          |
|   +---------------------------------------------------------------+   |
|   | Dual Discrete PI Current Controllers (Anti-Windup Clamping)   |   |
|   +---------------------------------------------------------------+   |
|          | v_d, v_q                                                   |
|          v                                                            |
|   +---------------------------------------------------------------+   |
|   | Inverse Park Transform (dq -> alpha, beta)                    |   |
|   +---------------------------------------------------------------+   |
|          | v_alpha, v_beta                                            |
|          v                                                            |
|   +---------------------------------------------------------------+   |
|   | Space Vector PWM (SVPWM)                                      |   |
|   | Hexagon Sectors 1..6 -> Active Dwell Times T1, T2, T0         |   |
|   | Center-Aligned Symmetric Duty Cycles (PWM_a, PWM_b, PWM_c)    |   |
|   +---------------------------------------------------------------+   |
|          |                                                            |
|          v Inverter Power Stage                                       |
|   +---------------------------------------------------------------+   |
|   | 3-Phase PMSM Motor & Stator Current Sensing (i_a, i_b, i_c)   |   |
|   |   Clarke Transform -> i_alpha, i_beta                         |   |
|   |   Park Transform   -> i_d, i_q (Rotor Angle Feedback)         |   |
|   +---------------------------------------------------------------+   |
+-----------------------------------------------------------------------+
```

## 2. Mathematical Formulations

### 1. Clarke Transform ($abc \to \alpha\beta$)
Maps balanced 3-phase currents ($i_a + i_b + i_c = 0$) onto orthogonal stationary axes:
$$i_\alpha = i_a$$
$$i_\beta = \frac{1}{\sqrt{3}}(i_a + 2 i_b)$$

### 2. Park Transform ($\alpha\beta \to dq$)
Rotates stationary $\alpha\beta$ quantities into a synchronous frame rotating with rotor electrical angle $\theta_e$:
$$i_d = i_\alpha \cos\theta_e + i_\beta \sin\theta_e$$
$$i_q = -i_\alpha \sin\theta_e + i_\beta \cos\theta_e$$
- $i_d$: Direct-axis current representing rotor flux. Set to $0$ for surface PMSM (Maximum Torque Per Ampere / MTPA).
- $i_q$: Quadrature-axis current directly proportional to electromagnetic torque: $\tau = \frac{3}{2} p \lambda_m i_q$.

### 3. Space Vector PWM (SVPWM)
Given reference voltage $\vec{V}_{ref} = V_\alpha + j V_\beta$:
1. Compute angle $\theta = \text{atan2}(V_\beta, V_\alpha) \in [0, 2\pi)$.
2. Identify hexagon sector $S = \lfloor \theta / (\pi/3) \rfloor + 1 \in \{1, 2, 3, 4, 5, 6\}$.
3. Compute dwell times within sector angle $\alpha_{rel} = \theta - (S - 1)\frac{\pi}{3}$:
   $$T_1 = \sqrt{3} \frac{|\vec{V}_{ref}|}{V_{dc}} T_{pwm} \sin\left(\frac{\pi}{3} - \alpha_{rel}\right)$$
   $$T_2 = \sqrt{3} \frac{|\vec{V}_{ref}|}{V_{dc}} T_{pwm} \sin(\alpha_{rel})$$
   $$T_0 = T_{pwm} - (T_1 + T_2)$$

### 4. 2-DoF Robot Arm Kinematics
Given link lengths $L_1, L_2$:
- **Forward Kinematics (FK)**:
  $$x = L_1 \cos\theta_1 + L_2 \cos(\theta_1 + \theta_2)$$
  $$y = L_1 \sin\theta_1 + L_2 \sin(\theta_1 + \theta_2)$$
- **Inverse Kinematics (IK)**:
  $$D = \frac{x^2 + y^2 - L_1^2 - L_2^2}{2 L_1 L_2}$$
  $$\theta_2 = \text{atan2}(\pm \sqrt{1 - D^2}, D)$$
  $$\theta_1 = \text{atan2}(y, x) - \text{atan2}(L_2 \sin\theta_2, L_1 + L_2 \cos\theta_2)$$

## 3. Scaffolding & Directory Structure
```
labs/lab08-foc-motor-robotics-controller/
├── README.md               # Architecture documentation
├── Makefile                # Build and test automation
├── run_tests.py            # Standalone test runner
├── include/                # Header definitions
│   ├── foc_math.h          # Clarke, Park, and inverse transforms
│   ├── pi_controller.h     # Discrete PI with anti-windup clamping
│   ├── svpwm.h             # Space Vector PWM sector & duty logic
│   └── kinematics.h        # 2-DoF FK and analytical IK solvers
├── starter/                # Student starter scaffolding
│   ├── Makefile            # Starter compilation rules
│   └── foc_starter.c       # Clean Clarke/Park starter skeleton
├── src/                    # Complete production reference implementation
│   ├── foc_math.c          # Coordinate frame transform math
│   ├── pi_controller.c     # Current regulator implementation
│   ├── svpwm.c             # Space vector duty cycle synthesis
│   ├── kinematics.c        # 2-DoF robot arm FK/IK implementation
│   ├── simulation.c        # Closed-loop motor integration simulation
│   └── main.c              # Test harness and simulation CLI
└── tests/                  # Automated test suite
    ├── test_clarke_park.py # Norm invariance & transform roundtrips
    ├── test_pi_controller.py # Step response and anti-windup clamping
    ├── test_svpwm.py       # Dwell time conservation and duty bounds
    ├── test_kinematics.py  # FK/IK round-trip workspace reachability
    └── test_integration.py # Closed-loop PMSM torque tracking
```

## 4. Milestone Progression Guide
1. **Milestone 1 (Clarke & Park Transforms)**:
   Verify power/norm invariance ($i_\alpha^2 + i_\beta^2 == i_d^2 + i_q^2$) and exact inverse reconstruction.
2. **Milestone 2 (Current Regulators)**:
   Implement discrete-time PI controllers with integrator saturation limits to eliminate steady-state error.
3. **Milestone 3 (Space Vector PWM)**:
   Calculate voltage vector sector dwelling times $T_1, T_2, T_0$ and synthesize 3-phase duty cycles within $[0.0, 1.0]$.
4. **Milestone 4 (2-DoF Manipulator Kinematics)**:
   Implement planar arm forward kinematics and analytical inverse kinematics with elbow-up and elbow-down configurations.
5. **Milestone 5 (Closed-Loop System Simulation)**:
   Simulate electrical dynamics $L \frac{di}{dt} = V - R i$ demonstrating stable current convergence to target torque setpoints.

## 5. Verification and Execution
Run the automated test runner:
```bash
python run_tests.py
```
Or use the Makefile:
```bash
mingw32-make test
```
All 5 motor and kinematics test suites execute in under 50 milliseconds and pass with exit code 0.
