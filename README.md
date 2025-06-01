Infection Spread Simulation
Overview
This project simulates the spread of an infection across a 2D plane with particles and cities, using a combination of random movement and gradient-based attraction towards infected particles. The simulation visualizes the spread of infection over time, with particles moving in a grid and cities becoming infected when infected particles reach them. Snapshots of the simulation are saved as images at regular intervals.
Features

Particles: Free particles move randomly or towards infected particles within a threshold distance. Infected particles are static and can infect nearby free particles.
Cities: Represented as circular regions, cities become infected when an infected particle is within their radius.
Simulation Mechanics:
Particles move in four directions (up, right, down, left) with a fixed direction unless influenced by an infected particle.
The simulation maintains a constant number of free particles (200) by spawning new ones as needed.
The simulation stops if an infected particle reaches the edge of the simulation area or after 100,000 steps.


Visualization: Snapshots are saved every 200 steps as PNG images in the simulation_images directory, showing particles (blue for free, red for infected) and cities (yellow for uninfected, red for infected).

Prerequisites

Python 3.x
Required Python libraries:
matplotlib
random
math
os



Installation

Clone or download this repository.
Install the required Python libraries:pip install matplotlib


Ensure you have Python 3.x installed.

Usage

Place the simulation script (e.g., simulation.py) in a directory.
Run the script:python simulation.py


The simulation will:
Create a simulation_images directory if it doesn't exist.
Run for up to 100,000 steps or until an infected particle reaches the edge.
Save snapshot images every 200 steps in the simulation_images directory.


Check the simulation_images directory for output PNG files named snapshot_step_X.png.

Configuration
The simulation parameters can be modified in the script by adjusting the following constants:

WIDTH, HEIGHT: Simulation area dimensions (default: 800x600 pixels).
GRID_SIZE: Size of each particle (default: 3 pixels).
INITIAL_PARTICLE_COUNT: Initial number of free particles (default: 200).
TARGET_FREE_PARTICLES: Target number of free particles to maintain (default: 200).
CITY_RADIUS: Radius of cities (default: 20 pixels).
GRADIENT_DISTANCE_THRESHOLD: Distance for gradient-based movement (default: 50 pixels).
SNAPSHOT_INTERVAL: Steps between saving images (default: 200).
MAX_STEPS: Maximum simulation steps (default: 100,000).

Output

Console Output: Displays the number of steps taken when the simulation completes.
Image Output: PNG files in the simulation_images directory, showing the state of particles and cities at each snapshot interval.

Notes

The simulation assumes a 2D grid where particles move in discrete steps.
Cities are initialized with one city infected, and five infected particles are placed in it to start the spread.
The simulation is deterministic for a given random seed but appears stochastic due to random particle placement and movement.

