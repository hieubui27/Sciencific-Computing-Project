import random
import math
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 3  # Size of each particle (pixels)
INITIAL_PARTICLE_COUNT = 200  # Initial number of free particles
TARGET_FREE_PARTICLES = 200  # Target number of free particles to maintain
CITY_RADIUS = 20  # Radius of cities
CHECKPOINT_SIZE = (30, 5)  # Size of checkpoint (width, height)
GRADIENT_DISTANCE_THRESHOLD = 50  # Distance threshold for gradient-based movement (pixels)
SNAPSHOT_INTERVAL = 500  # Save image every 500 steps
MAX_STEPS = 100000  # Maximum simulation steps

# Four possible directions (up, right, down, left)
DIRECTIONS = [
    math.pi / 2,  # Up
    0,           # Right
    3 * math.pi / 2,  # Down
    math.pi      # Left
]

# City class
class City:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.infected = False

# Checkpoint class
class Checkpoint:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.width, self.height = CHECKPOINT_SIZE

# Particle class
class Particle:
    def __init__(self, x, y, infected=False, stuck=False):
        self.x = x
        self.y = y
        self.infected = infected
        self.stuck = stuck
        self.fixed_direction = random.choice(DIRECTIONS)

    def move(self, particles, cities, checkpoints):
        if not self.infected and not self.stuck:
            # Find the closest infected particle
            closest_infected = None
            min_dist = float('inf')
            for p in particles:
                if p.infected:
                    dist = math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)
                    if dist < min_dist:
                        min_dist = dist
                        closest_infected = p

            # If close to an infected particle, use Gradient Method
            if closest_infected and min_dist <= GRADIENT_DISTANCE_THRESHOLD:
                dx = closest_infected.x - self.x
                dy = closest_infected.y - self.y
                angle = math.atan2(dy, dx)
            else:
                angle = self.fixed_direction

            # Move in the determined direction
            self.x += math.cos(angle) * GRID_SIZE
            self.y += math.sin(angle) * GRID_SIZE
            # Keep particle within bounds
            self.x = max(0, min(self.x, WIDTH - GRID_SIZE))
            self.y = max(0, min(self.y, HEIGHT - GRID_SIZE))

    def check_collision(self, particles, cities, checkpoints):
        if not self.infected and not self.stuck:
            for p in particles:
                if p.infected:
                    # Check if there is a checkpoint blocking the infection spread
                    blocked = False
                    for checkpoint in checkpoints:
                        dist_to_checkpoint_self = math.sqrt((self.x - checkpoint.x) ** 2 + (self.y - checkpoint.y) ** 2)
                        dist_to_checkpoint_infected = math.sqrt((p.x - checkpoint.x) ** 2 + (p.y - checkpoint.y) ** 2)
                        if dist_to_checkpoint_self <= max(CHECKPOINT_SIZE) or dist_to_checkpoint_infected <= max(CHECKPOINT_SIZE):
                            dist_between_particles = math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)
                            if dist_to_checkpoint_self + dist_to_checkpoint_infected <= dist_between_particles + 10:
                                blocked = True
                                break
                    if blocked:
                        continue

                    # If not blocked, check for infection
                    if abs(self.x - p.x) <= GRID_SIZE and abs(self.y - p.y) <= GRID_SIZE:
                        self.infected = True
                        self.stuck = True
                        for city in cities:
                            dist = math.sqrt((self.x - city.x) ** 2 + (self.y - city.y) ** 2)
                            if dist <= city.radius + GRID_SIZE:
                                city.infected = True
                        return True
        return False

    def is_at_edge(self):
        return (self.x <= 0 or self.x >= WIDTH - GRID_SIZE or 
                self.y <= 0 or self.y >= HEIGHT - GRID_SIZE)

# Create cities
cities = [
    City(WIDTH // 4, HEIGHT // 4, CITY_RADIUS),
    City(3 * WIDTH // 4, 3 * HEIGHT // 4, CITY_RADIUS),
    City(WIDTH // 2, HEIGHT // 3, CITY_RADIUS),
    City(WIDTH // 5, 3 * HEIGHT // 5, CITY_RADIUS),
    City(4 * WIDTH // 5, HEIGHT // 5, CITY_RADIUS),
    City(WIDTH // 2, HEIGHT // 2, CITY_RADIUS)
]

# Sort cities by x-coordinate to determine adjacent pairs
cities.sort(key=lambda city: city.x)

# Create checkpoints between adjacent cities
checkpoints = []
for i in range(len(cities) - 1):
    city1 = cities[i]
    city2 = cities[i + 1]
    if random.random() < 0.5:
        mid_x = (city1.x + city2.x) // 2
        mid_y = (city1.y + city2.y) // 2
        angle = random.uniform(0, 360)
        checkpoints.append(Checkpoint(mid_x, mid_y, angle))

# Initialize particles
particles = []
for _ in range(INITIAL_PARTICLE_COUNT):
    while True:
        x = random.randint(0, WIDTH - GRID_SIZE)
        y = random.randint(0, HEIGHT - GRID_SIZE)
        in_city_or_checkpoint = False
        for city in cities:
            if math.sqrt((x - city.x) ** 2 + (y - city.y) ** 2) <= city.radius:
                in_city_or_checkpoint = True
                break
        for checkpoint in checkpoints:
            if math.sqrt((x - checkpoint.x) ** 2 + (y - checkpoint.y) ** 2) <= max(CHECKPOINT_SIZE):
                in_city_or_checkpoint = True
                break
        if not in_city_or_checkpoint:
            break
    particles.append(Particle(x, y))

# Start infection in the first city
first_city = cities[0]
first_city.infected = True
for _ in range(5):
    particles.append(Particle(first_city.x, first_city.y, infected=True, stuck=True))

# Create directory to save images
if not os.path.exists("simulation_images"):
    os.makedirs("simulation_images")

# Simulation loop
step = 0
infection_active = True
while step < MAX_STEPS and infection_active:
    # Check if infection has reached the edge
    edge_reached = False
    for particle in particles:
        if particle.infected and particle.is_at_edge():
            edge_reached = True
            break

    if edge_reached:
        infection_active = False

    # Move particles and check for infection
    if infection_active:
        particles_to_remove = []
        for particle in particles:
            particle.move(particles, cities, checkpoints)
            if particle.is_at_edge():
                particles_to_remove.append(particle)

        for particle in particles_to_remove:
            if particle in particles:
                particles.remove(particle)

        for particle in particles:
            particle.check_collision(particles, cities, checkpoints)

        # Maintain the number of free particles at 200
        free_particles = sum(1 for p in particles if not p.infected and not p.stuck)
        while free_particles < TARGET_FREE_PARTICLES:
            while True:
                x = random.randint(0, WIDTH - GRID_SIZE)
                y = random.randint(0, HEIGHT - GRID_SIZE)
                in_city_or_checkpoint = False
                for city in cities:
                    if math.sqrt((x - city.x) ** 2 + (y - city.y) ** 2) <= city.radius:
                        in_city_or_checkpoint = True
                        break
                for checkpoint in checkpoints:
                    if math.sqrt((x - checkpoint.x) ** 2 + (y - checkpoint.y) ** 2) <= max(CHECKPOINT_SIZE):
                        in_city_or_checkpoint = True
                        break
                if not in_city_or_checkpoint:
                    break
            particles.append(Particle(x, y))
            free_particles += 1

    # Save image every SNAPSHOT_INTERVAL steps
    if step % SNAPSHOT_INTERVAL == 0:
        # Create a new figure
        plt.figure(figsize=(8, 6))
        plt.xlim(0, WIDTH)
        plt.ylim(0, HEIGHT)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.gca().invert_yaxis()  # Invert y-axis to match typical graphics coordinates

        # Plot particles
        for particle in particles:
            color = 'red' if particle.infected else 'blue'
            plt.plot(particle.x, particle.y, marker='s', color=color, markersize=3)

        # Plot cities
        for city in cities:
            color = 'red' if city.infected else 'yellow'
            circle = plt.Circle((city.x, city.y), city.radius, color=color, alpha=0.5)
            plt.gca().add_patch(circle)

        # Plot checkpoints
        for checkpoint in checkpoints:
            rect = Rectangle(
                (checkpoint.x - checkpoint.width / 2, checkpoint.y - checkpoint.height / 2),
                checkpoint.width, checkpoint.height,
                angle=checkpoint.angle, color='green', alpha=0.5
            )
            plt.gca().add_patch(rect)

        plt.title(f"Step {step}")
        plt.savefig(f"simulation_images/snapshot_step_{step}.png")
        plt.close()

    step += 1

print(f"Simulation completed after {step} steps. Images saved in 'simulation_images' directory.")