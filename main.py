import pymunk
import pygame
from pygame.locals import *
import pymunk.pygame_util
import matplotlib.pyplot as plt
from collections import deque

# Initialize pygame and pymunk
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Spring Simulation with Energy Graph")
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, -10)  # 중력 제거
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Create a static anchor point for the spring
anchor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
anchor_body.position = (400, 100)

# Create a dynamic body for the object attached to the spring
mass = 1
radius = 20
moment = pymunk.moment_for_circle(mass, 0, radius)
ball_body = pymunk.Body(mass, moment)
ball_body.position = (400, 300)
ball_shape = pymunk.Circle(ball_body, radius)
ball_shape.elasticity = 0  # 충돌 탄성 계수 제거
space.add(ball_body, ball_shape)

# Create a spring (DampedSpring)
spring = pymunk.DampedSpring(
    anchor_body,#코드 누가 짯냐  진자 개못하네 
    ball_body, 
    (0, 0), 
    (0, 0), 
    rest_length=200, 
    stiffness=10,  # 용수철 강성
    damping=0 # 감쇠를 제거하여 역학적 에너지 보존
)
space.add(spring)

# Function to calculate kinetic energy
def calculate_kinetic_energy(body):
    velocity = body.velocity
    speed_squared =  velocity.y**2
    return 0.5 * body.mass * speed_squared

# Function to calculate potential energy (spring)
def calculate_potential_energy(spring, body):
    displacement = spring.rest_length - (body.position - spring.a.position).length
    spring_energy = 0.5 * spring.stiffness * displacement**2
    return spring_energy 

# Function to calculate potnetial energy (gravitational)
def calculate_gravitational_potential_energy(body):
    # height = body.position.y - anchor_body.position.y  # 기준점을 앵커 위치로
    # height = body.position.y - 100  # 기준점을 앵커 위치로
    height = body.position.y - 300  # 기준점을 앵커 위치로
    gravitational_energy = body.mass * space.gravity[1] * height
    return gravitational_energy

# Energy data for graph
kinetic_energy_data = deque(maxlen=500)
potential_energy_data = deque(maxlen=500)
gravitational_energy_data = deque(maxlen=500)  # 중력 에너지 데이터 추가
total_energy_data = deque(maxlen=500)

# Define the initial position of the ball to match the spring's rest length
initial_position = (400, 100 + 200)  # Anchor point y + rest_length

# Scaling factor for energy display
energy_scale = 0.05  # 에너지 값을 20분의 1로 축소

# Main loop
running = True
dragging = False
paused = False  # 상황 고정을 위한 상태 변수

# Set the ball's initial position and velocity to ensure zero energy at the start
ball_body.position = initial_position
ball_body.velocity = (0, 0)

# 시간 간격 줄이기
time_step = 1 / 480.0  # 더 작은 시간 간격

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if ball_shape.point_query(event.pos).distance <= 0:
                dragging = True
        elif event.type == MOUSEBUTTONUP:
            dragging = False
        elif event.type == KEYDOWN:
            if event.key == K_r:  # Press 'R' to reset
                ball_body.position = initial_position
                ball_body.velocity = (0, 0)
            elif event.key == K_p:  # Press 'P' to pause/resume
                paused = not paused

    if dragging:
        mouse_pos = pygame.mouse.get_pos()
        # Update only the vertical (y) position of the ball
        ball_body.position = (ball_body.position.x, mouse_pos[1])
        ball_body.velocity = (0, 0)  # Reset velocity to prevent unintended motion

    if not paused:  # 시뮬레이션이 멈추지 않았을 때만 업데이트
        # Clear screen
        screen.fill((255, 255, 255))

        # Step the simulation
        space.step(time_step)

        # Draw objects
        space.debug_draw(draw_options)

        # Calculate energies
        kinetic_energy = calculate_kinetic_energy(ball_body)
        potential_energy = calculate_potential_energy(spring, ball_body)
        gravitational_energy = calculate_gravitational_potential_energy(ball_body)
        total_energy = - kinetic_energy - potential_energy + gravitational_energy

        # Append energy data for graph
        kinetic_energy_data.append(kinetic_energy)
        potential_energy_data.append(potential_energy)
        gravitational_energy_data.append(gravitational_energy)
        total_energy_data.append(total_energy)

        # Display kinetic energy
        font = pygame.font.Font(None, 36)
        text = font.render(f"Kinetic Energy: {kinetic_energy * energy_scale:.2f} J", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # Display potential energy (spring)
        text = font.render(f"Spring PE: {potential_energy * energy_scale:.2f} J", True, (0, 0, 0))
        screen.blit(text, (10, 50))

        # Display gravitational potential energy
        text = font.render(f"Gravity PE: {gravitational_energy * energy_scale:.2f} J", True, (0, 0, 0))
        screen.blit(text, (10, 90))

        # Display total energy
        text = font.render(f"Total Energy: {total_energy * energy_scale:.2f} J", True, (0, 0, 0))
        screen.blit(text, (10, 130))

        # Update display
        pygame.display.flip()
        clock.tick(240)

# Plot energy graph
plt.figure(figsize=(10, 6))
plt.plot([e * energy_scale for e in kinetic_energy_data], label="Kinetic Energy")
plt.plot([e * energy_scale for e in potential_energy_data], label="Spring PE")
plt.plot([e * energy_scale for e in gravitational_energy_data], label="Gravity PE")
plt.plot([e * energy_scale for e in total_energy_data], label="Total Energy")
plt.xlabel("Time Steps")
plt.ylabel("Energy (Scaled, J)")
plt.title("Energy Transformation (Scaled)")
plt.legend()
plt.show()

# Ensure pygame quits properly
pygame.quit()