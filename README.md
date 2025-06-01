Particle Infection Simulation
Overview
This Python script simulates the spread of an infection through a population of moving particles within a defined area. The simulation includes cities that can become infected, checkpoints that block infection spread, and particles that move either randomly or towards infected particles based on a gradient method. The simulation visualizes the process using Matplotlib, saving snapshots at regular intervals.
Features

Particles: Move in fixed directions (up, right, down, left) or towards infected particles within a threshold distance.
Cities: Circular areas that can become infected if an infected particle is nearby.
Checkpoints: Rectangular barriers that prevent infection spread between particles.
Infection Spread: Particles become infected and stuck when they collide with infected particles, unless blocked by a checkpoint.
Visualization: Snapshots of the simulation are saved as PNG images every 500 steps.
Dynamic Particle Management: Maintains a constant number of free (non-infected, non-stuck) particles by adding new ones as needed.
Simulation Termination: Stops when the infection reaches the simulation boundaries or after a maximum number of steps (100,000).

Requirements

Python 3.x
Libraries:
matplotlib
numpy (used implicitly via matplotlib)



Install dependencies using:
pip install matplotlib

Usage

Save the script as simulation.py.
Run the script:python simulation.py


The simulation will create a directory named simulation_images and save snapshot images (snapshot_step_<step>.png) every 500 steps.
The simulation runs until the infection reaches the edge of the simulation area or the maximum step count is reached.
Upon completion, the script prints the number of steps taken and the location of saved images.

Configuration
The simulation parameters are defined as constants at the top of the script:

WIDTH, HEIGHT: Simulation area dimensions (800x600 pixels).
GRID_SIZE: Particle size and movement step (3 pixels).
INITIAL_PARTICLE_COUNT: Starting number of free particles (200).
TARGET_FREE_PARTICLES: Number of free particles to maintain (200).
CITY_RADIUS: Radius of cities (20 pixels).
CHECKPOINT_SIZE: Dimensions of checkpoints (30x5 pixels).
GRADIENT_DISTANCE_THRESHOLD: Distance for gradient-based movement (50 pixels).
SNAPSHOT_INTERVAL: Steps between snapshots (500).
MAX_STEPS: Maximum simulation steps (100,000).

Modify these constants to adjust the simulation behavior.
Output

Images: Saved in the simulation_images directory with filenames like snapshot_step_0.png, snapshot_step_500.png, etc.
Console Output: Displays the total number of steps and the location of saved images upon completion.

Simulation Details

Particles: Start with 200 free particles and 5 infected particles in the first city. Free particles move in one of four directions unless near an infected particle, then move towards it.
Cities: Six cities are placed at fixed positions. The first city is initially infected. Cities become infected if an infected particle is within their radius.
Checkpoints: Randomly placed between adjacent cities (sorted by x-coordinate) with a 50% chance. They block infection if both particles are near the checkpoint.
Movement: Particles bounce off simulation boundaries and maintain a grid-based movement (multiples of GRID_SIZE).
Infection: A free particle becomes infected and stuck upon colliding with an infected particle, unless a checkpoint blocks the spread.
Termination: The simulation stops if an infected particle reaches the edge or after 100,000 steps.

Notes

The simulation uses a simple random walk for particle movement when not influenced by infected particles.
Checkpoints are oriented randomly, affecting their blocking effectiveness.
The script ensures particles do not spawn inside cities or checkpoints.
Matplotlib plots are closed after saving to prevent memory issues.


Check the simulation_images directory for PNG files showing the simulation state at various steps.



