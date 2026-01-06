# Car-interface-simulator
 Supercar Vehicle Dynamics Simulator (Python + Pygame)

A real-time vehicle dynamics simulator written in Python, using Pygame for visualization.

This project models the longitudinal behavior of a high-performance supercar, focusing on how engine torque, gearing, traction, aerodynamics, and control systems interact over time.

It is not a racing game but rather a physics-first driving sandbox.

# Features

# 1. Core Vehicle Dynamics

Engine RPM evolution with idle and redline

Multi-gear transmission with realistic gear ratios

Clutch engagement and drivetrain coupling

RPM-dependent torque curve

Force-based longitudinal motion (Newtonian mechanics)


# 2. Real-World Constraints

Traction-limited acceleration (no infinite grip)

Wheelspin detection and visualization

Quadratic aerodynamic drag

Speed-dependent loss of acceleration

Realistic high-speed behavior (acceleration tapers naturally)


# 3. Control Systems

Launch Control

RPM hold at optimal launch RPM

Prevents excessive wheelspin

Automatically disengages as speed increases

Effective throttle modulation layered on top of raw input


# 4. Instrumentation & HUD

Analog RPM gauge with redline arc

Analog speedometer (km/h)

Digital gear indicator

Wheelspin meter

Longitudinal G-force readout

Smooth, inertia-weighted gauges (no jitter)

# Controls
Key	Action:

↑ Arrow	= THROTTLE

↓ Arrow =	BRAKE

Z =	CLUTCH

A	= DOWNSHIFT

S =	UPSHIFT

ESC =	QUIT


# Launch Control
Launch Control engages automatically when:

Gear = 1

Speed < 5 km/h

Throttle fully pressed

Clutch released


# Expected Behaviour

With the default supercar parameters:

Violent low-speed acceleration

Strong mid-range pull

Noticeably slower acceleration past ~100 km/h

Wheelspin during aggressive launches

G-force spikes that correlate with what you feel, not just what you see


# Requirements

Python 3.9+

pygame

Install dependencies:

pip install pygame


Run the simulator:

python race.py

# Project Status

This is an active learning and exploration project, built to understand:

vehicle dynamics

drivetrain behavior

traction limits

control systems (launch control)

real-time simulation structure

instrumentation and feedback

# Possible Extensions

Ideas for future work:

Traction Control (TC)

ABS-style braking limits

Variable tire grip

Engine inertia modeling

Telemetry graphs (speed, RPM, G-force)

Sound tied to RPM and load
