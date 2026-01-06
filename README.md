# Car-interface-simulator
 Supercar Vehicle Dynamics Simulator (Python + Pygame)

A real-time vehicle dynamics simulator written in Python, using Pygame for visualization.

This project models the longitudinal behavior of a high-performance supercar, focusing on how engine torque, gearing, traction, aerodynamics, and control systems interact over time.

It is not a racing game but rather a physics-first driving sandbox.

# Features

# Core Vehicle Dynamics

Engine RPM evolution with idle and redline

Multi-gear transmission with realistic gear ratios

Clutch engagement and drivetrain coupling

RPM-dependent torque curve

Force-based longitudinal motion (Newtonian mechanics)


# Real-World Constraints

Traction-limited acceleration (no infinite grip)

Wheelspin detection and visualization

Quadratic aerodynamic drag

Speed-dependent loss of acceleration

Realistic high-speed behavior (acceleration tapers naturally)


# Control Systems

Launch Control

RPM hold at optimal launch RPM

Prevents excessive wheelspin

Automatically disengages as speed increases

Effective throttle modulation layered on top of raw input


# Instrumentation & HUD

Analog RPM gauge with redline arc

Analog speedometer (km/h)

Digital gear indicator

Wheelspin meter

Longitudinal G-force readout

Smooth, inertia-weighted gauges (no jitter)
