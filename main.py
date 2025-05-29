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
space.gravity = (0, 900)  # 중력 추가 (예: 900 픽셀/s^2)
draw_options = pymunk.pygame_util.DrawOptions(screen)
pygame.font.init()
font = pygame.font.SysFont("서울알림체ttfmedium", 20)

# Create rectangular walls (left, right, top, bottom)
static_lines = [
    pymunk.Segment(space.static_body, (0, 0), (0, 600), 5),      # Left wall
    pymunk.Segment(space.static_body, (0, 600), (800, 600), 5),  # Bottom wall
    pymunk.Segment(space.static_body, (800, 600), (800, 0), 5),  # Right wall
    pymunk.Segment(space.static_body, (800, 0), (0, 0), 5),      # Top wall
]
for line in static_lines:
    line.elasticity = 1.0
    line.friction = 0.5
space.add(*static_lines)

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
ball_shape.elasticity = 1     # 충돌 탄성 계수 제거
ball_shape.friction = 0.0

space.add(ball_body, ball_shape)
spring = pymunk.DampedSpring(
    anchor_body, ball_body,
    (0, 0), (0, 0),  # anchor point is at the top of the screen
    rest_length=200,  # 용수철의 자연 길이
    stiffness=50,  # 용수철 강성
    damping=0  # 감쇠 계수
)
space.add(spring)

# 총 에너지
# Energy data for graph
kinetic_energy_data = deque(maxlen=500)
potential_energy_data = deque(maxlen=500)
gravitational_energy_data = deque(maxlen=500)  # 중력 에너지 데이터 추가
total_energy_data = deque(maxlen=500)

# Define the initial position of the ball to match the spring's rest length
initial_position = (400, 100 + 200)  # Anchor point y + rest_length

# Scaling factor for energy display
energy_scale = 1/1000  # 에너지 값을 20분의 1로 축소

# 슬로우 모션 배율 변수 추가
slow_motion = 1.0  # 1.0 = 정상속도, 0.1 = 10배 느리게

# Main loop
running = True
dragging = False
paused = False  # 상황 고정을 위한 상태 변수

# Set the ball's initial position and velocity to ensure zero energy at the start
ball_body.position = initial_position
ball_body.velocity = (0, 0)
# 시간 간격 줄이기

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if ball_shape.point_query(event.pos).distance <= 0:
                dragging = True
                ball_body.velocity = (0, 0)  # 드래그 시작 시 속도 초기화
        elif event.type == MOUSEBUTTONUP:
            dragging = False
        elif event.type == KEYDOWN:
            if event.key == K_r:  # Press 'R' to reset
                ball_body.position = initial_position
                ball_body.velocity = (0, 0)
            elif event.key == K_p:  # Press 'P' to pause/resume
                paused = not paused
            elif event.key == K_1:  # 1번키: 정상속도
                slow_motion = 1.0
            elif event.key == K_2:  # 2번키: 2배 느리게
                slow_motion = 0.5
            elif event.key == K_3:  # 3번키: 5배 느리게
                slow_motion = 0.2
            elif event.key == K_4:  # 4번키: 10배 느리게
                slow_motion = 0.1

    if dragging:
        mouse_pos = pygame.mouse.get_pos()
        # Update only the vertical (y) position of the ball
        ball_body.position = (ball_body.position.x, mouse_pos[1])
        ball_body.velocity = (0, 0)  # Reset velocity to prevent unintended motion
    
    if not paused:  # 시뮬레이션이 멈추지 않았을 때만 업데이트
        # Clear screen
        screen.fill((255, 255, 255))
        time_step = (1/480) * slow_motion  # 슬로우 모션 적용
        # Step the simulation
        space.step(time_step)

        # Draw objects
        space.debug_draw(draw_options)

        if velocity := ball_body.velocity:
            # Draw the velocity vector
            start_pos = ball_body.position
            end_pos = (start_pos.x + velocity.x * 20, start_pos.y + velocity.y * 20)
            pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 2)
            # Find the highest and lowest y positions reached so far
            if not hasattr(ball_body, "max_y"):
                ball_body.max_y = ball_body.position.y
                ball_body.min_y = ball_body.position.y
            else:
                ball_body.max_y = max(ball_body.max_y, ball_body.position.y)
                ball_body.min_y = min(ball_body.min_y, ball_body.position.y)

            # Draw a horizontal line at the highest position (min_y)
            pygame.draw.line(
                screen, (0, 128, 255),
                (0, ball_body.min_y),
                (800, ball_body.min_y),
                2
            )
            # Draw a horizontal line at the lowest position (max_y)
            pygame.draw.line(
                screen, (255, 128, 0),
                (0, ball_body.max_y),
                (800, ball_body.max_y),
                2
            )
            # Draw a horizontal line at the equilibrium position (rest length from anchor)
            equilibrium_y = anchor_body.position.y + spring.rest_length
            pygame.draw.line(
                screen, (0, 200, 0),
                (0, equilibrium_y),
                (800, equilibrium_y),
                2
            )
            # Draw a moving vertical line at the current x position of the ball
            pygame.draw.line(
                screen, (128, 0, 128),
                (0, ball_body.position.y),
                (800, ball_body.position.y),
                2
            )
        # Calculate equilibrium point (where spring force balances gravity)
        equilibrium_y = anchor_body.position.y + spring.rest_length + (ball_body.mass * abs(space.gravity[1])) / spring.stiffness

        # Set the ball's initial position to the equilibrium point if not already set
        if not hasattr(ball_body, "equilibrium_initialized"):
            ball_body.position = (anchor_body.position.x, equilibrium_y)
            ball_body.velocity = (0, 0)
            ball_body.equilibrium_initialized = True

        # Calculate energie
        # Calculate equilibrium point (where spring force balances gravity)
        equilibrium_y = anchor_body.position.y + spring.rest_length + (ball_body.mass * abs(space.gravity[1])) / spring.stiffness

        # Draw a horizontal line at the new equilibrium position (force balance)
        pygame.draw.line(
            screen, (255, 0, 255),
            (0, equilibrium_y),
            (800, equilibrium_y),
            2
        )

        # Calculate displacement from equilibrium for potential energy
        displacement_from_equilibrium = ball_body.position.y - equilibrium_y

        # Spring potential energy (relative to equilibrium)
        potential_energy = 0.5 * spring.stiffness * (ball_body.position.y - 300) ** 2

        # Gravitational potential energy (relative to equilibrium)
        gravitational_energy = ball_body.mass * space.gravity[1] * (ball_body.position.y - equilibrium_y)
        calculate_kinetic_energy = lambda body: 0.5 * body.mass * (velocity.y ** 2)
        kinetic_energy = calculate_kinetic_energy(ball_body)
        # Total energy
        
        total_energy = kinetic_energy + potential_energy - gravitational_energy
        # Append energy data for graph
        kinetic_energy_data.append(kinetic_energy)
        potential_energy_data.append(potential_energy)
        gravitational_energy_data.append(-gravitational_energy)
        total_energy_data.append(total_energy)

        # Display kinetic energy
        # font = pygame.font.Font(None, 36)
        text = font.render(f"Kinetic Energy: {kinetic_energy * energy_scale:.2f} J", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # Display potential energy (spring)
        text = font.render(f"Spring PE: {potential_energy * energy_scale:.2f} J", True, (0, 0, 0))
        screen.blit(text, (10, 50))

        # Display gravitational potential energy
        text = font.render(f"Gravity PE: {-gravitational_energy * energy_scale:.2f} J", True, (0, 0, 0))
        screen.blit(text, (10, 90))

        # Display total energy
        text = font.render(f"Total Energy: {total_energy * energy_scale:.2f} J", True, (0, 0, 0))
        screen.blit(text, (10, 130))

        # font = pygame.font.Font(None, 28)   
        # 1. 평형점과 최고점(최소 y) 사이 거리
        eq_min_dist = abs(equilibrium_y - ball_body.min_y)
        text = font.render(f"평형점-최고점: {eq_min_dist:.1f}", True, (0, 128, 255))
        screen.blit(text, (550, 10))

        # 2. 평형점과 최저점(최대 y) 사이 거리
        max_eq_dist = abs(ball_body.max_y - equilibrium_y)
        text = font.render(f"최저점-평형점: {max_eq_dist:.1f}", True, (255, 128, 0))
        screen.blit(text, (550, 40))

        # 3. 현재 위치와 평형점 사이 거리
        cur_eq_dist = abs(ball_body.position.y - equilibrium_y)
        text = font.render(f"현재-평형점: {cur_eq_dist:.1f}", True, (0, 200, 0))
        screen.blit(text, (550, 70))

        # 4. 현재 위치와 최고점(최소 y) 사이 거리
        cur_min_dist = abs(ball_body.position.y - ball_body.min_y)
        text = font.render(f"현재-최고점: {cur_min_dist:.1f}", True, (0, 128, 255))
        screen.blit(text, (550, 100))

        # 5. 현재 위치와 최저점(최대 y) 사이 거리
        cur_max_dist = abs(ball_body.position.y - ball_body.max_y)
        text = font.render(f"현재-최저점: {cur_max_dist:.1f}", True, (255, 128, 0))
        screen.blit(text, (550, 130))
        # Update display
        pygame.display.flip()
        clock.tick(480)

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