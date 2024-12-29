import pygame
import math
import random

bounces = 0

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Physics Simulation")

# Colors of the rainbow
RAINBOW_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 255, 0),
                  (0, 255, 255), (0, 0, 255), (75, 0, 130), (148, 0, 211)]  # Add more colors as needed

# Ball settings
initial_ball_radius = 1
ball_radius = initial_ball_radius
ball_center = [WIDTH // 2, HEIGHT // 3.5]
ball_velocity = [9.5, 10.5]  # Initial velocity
ball_mass = 3
elasticity = 1.0  # Elasticity factor (no energy lost in collision)
velocity_increase_factor = 1.0082  # Increase factor for velocity after each bounce

# Circle settings
circle_center = [WIDTH // 2, HEIGHT // 2]
circle_radius = min(WIDTH, HEIGHT) // 2 - 80  # Adjusted to be 50px from the edge

# Gravity
gravity = 1.4

# Trace settings
traces = []
max_traces = 20  # Maximum number of traces allowed
traces_per_frame = 7  # Number of traces added per frame
trace_opacity_decay = 6  # Opacity decay factor for the traces

# Color transition settings
transition_speed = 0.003  # Adjust the speed of color transition

# List to keep track of additional bouncing balls
bouncing_balls = []

# List to store collision points
collision_points = []

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font settings
font = pygame.font.Font(None, 36)

# Function to smoothly transition between colors
def transition_color(phase, speed):
    color_index = phase * (len(RAINBOW_COLORS) - 1)
    color1 = RAINBOW_COLORS[int(color_index) % len(RAINBOW_COLORS)]
    color2 = RAINBOW_COLORS[(int(color_index) + 1) % len(RAINBOW_COLORS)]
    factor = color_index % 1
    new_color = [int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3)]
    return new_color

# Main game loop
running = True
color_phase = 0
bounce_counter = 0
last_bounce_time = pygame.time.get_ticks()  # Initialize last bounce time

ball_positions = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply gravity
    ball_velocity[1] += gravity

    # Update ball position
    ball_center[0] += ball_velocity[0]
    ball_center[1] += ball_velocity[1]

    # Check for collision with walls
    if ball_center[0] <= ball_radius:
        ball_center[0] = ball_radius
        ball_velocity[0] *= -elasticity  # Reverse direction
        ball_velocity[0] *= velocity_increase_factor  # Increase velocity upon collision
        bounce_counter += 1
    elif ball_center[0] >= WIDTH - ball_radius:
        ball_center[0] = WIDTH - ball_radius
        ball_velocity[0] *= -elasticity  # Reverse direction
        ball_velocity[0] *= velocity_increase_factor  # Increase velocity upon collision
        bounce_counter += 1

    if ball_center[1] <= ball_radius:
        ball_center[1] = ball_radius
        ball_velocity[1] *= -elasticity  # Reverse direction
        ball_velocity[1] *= velocity_increase_factor  # Increase velocity upon collision
        bounce_counter += 1
    elif ball_center[1] >= HEIGHT - ball_radius:
        ball_center[1] = HEIGHT - ball_radius
        ball_velocity[1] *= -elasticity  # Reverse direction
        ball_velocity[1] *= velocity_increase_factor  # Increase velocity upon collision
        bounce_counter += 1

    # Check for collision with circle
    distance_from_center = (ball_center[0] - circle_center[0]) ** 2 + (ball_center[1] - circle_center[1]) ** 2
    if distance_from_center >= (circle_radius - ball_radius) ** 2:
        # Calculate normal vector
        bounces += 1
        normal = [ball_center[0] - circle_center[0], ball_center[1] - circle_center[1]]
        length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
        normal = [n / length for n in normal]

        # Calculate dot product
        dot_product = ball_velocity[0] * normal[0] + ball_velocity[1] * normal[1]

        # Calculate reflection
        reflection = [ball_velocity[i] - 2 * dot_product * normal[i] for i in range(2)]

        # Update velocity with reflection
        ball_velocity[0] = reflection[0]
        ball_velocity[1] = reflection[1]

        # Increase ball size by 3% each bounce, up to a maximum of 250px radius
        ball_radius += 1.30

        # Ensure ball doesn't get stuck on the edge of the circle
        angle = math.atan2(ball_center[1] - circle_center[1], ball_center[0] - circle_center[0])
        offset = 2  # Offset to move ball away from the edge
        ball_center[0] = circle_center[0] + (circle_radius - ball_radius - offset) * math.cos(angle)
        ball_center[1] = circle_center[1] + (circle_radius - ball_radius - offset) * math.sin(angle)

        # Store collision point
        collision_points.append((circle_center[0] + (circle_radius * math.cos(angle)),
                                 circle_center[1] + (circle_radius * math.sin(angle))))

        # Increase velocity upon collision with circle, unless radius exceeds 250px
        ball_velocity[0] *= velocity_increase_factor
        ball_velocity[1] *= velocity_increase_factor

        # Increment bounce counter
        bounce_counter += 1

    # Transition ball color smoothly
    ball_color = transition_color(color_phase, transition_speed)

    # Add multiple traces if inside the circle perimeter
    for _ in range(traces_per_frame):
        trace_color_with_alpha = tuple(list(ball_color) + [random.randint(50, 200)])  # Trace color matches ball with varying alpha
        max_trace_radius = min(ball_radius, circle_radius)  # Maximum allowed trace radius
        trace_radius = random.uniform(0.5, 1.5) * max_trace_radius  # Vary trace size within limits
        traces.append({'position': ball_center.copy(), 'color': trace_color_with_alpha, 'radius': min(trace_radius, max_trace_radius)})

        # Limit the number of traces
        if len(traces) > max_traces:
            traces.pop(0)  # Remove the oldest trace

    # Transition circle outline color smoothly
    circle_outline_color = transition_color(color_phase, transition_speed)

    # Draw the small circle within the main circle
    screen.fill((0, 0, 0))  # Fill the screen with black background
    pygame.draw.circle(screen, (0, 0, 0), circle_center, circle_radius)  # Black inner color
    pygame.draw.circle(screen, circle_outline_color, circle_center, circle_radius + 20, 20)  # Circle outline with smooth color transition

    # Draw traces
    for trace in traces:
        trace_alpha = max(0, trace['color'][3] - trace_opacity_decay)  # Decrease alpha
        trace_alpha *= 0.2  # Reduce opacity to 70%
        trace_color_with_alpha = tuple(list(trace['color'][:3]) + [int(trace_alpha)])  # Update color with new alpha
        trace_position = (int(trace['position'][0]), int(trace['position'][1]))
        trace_radius = int(trace['radius'])
        
        # Draw white outline
        pygame.draw.circle(screen, (255, 255, 255), trace_position, trace_radius + 0.5)
        
        # Draw trace
        pygame.draw.circle(screen, trace_color_with_alpha, trace_position, trace_radius)

    # Draw lines from collision points to the current ball position
    for point in collision_points:
        pygame.draw.line(screen, (ball_color), point, ball_center, 2)

    ball_positions.insert(0, (int(ball_center[0]), int(ball_center[1])))  # Add current position at the start
    if len(ball_positions) > 8:
        ball_positions.pop()  # Remove the oldest position if more than 8

    # Step 3: Draw the afterimages
    for i, position in enumerate(ball_positions):
        # Calculate alpha for fading effect: start with 255 and decrease
        alpha = max(255 - (i * 30), 0)  # Decrease alpha for older positions
        # Assuming 'color' is a pygame.Color object and 'alpha' is an integer
        rgba_color = tuple(ball_color + [alpha])      
        temp_surface = pygame.Surface((2 * ball_radius, 2 * ball_radius), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, rgba_color, (ball_radius, ball_radius), ball_radius)
        screen.blit(temp_surface, (position[0] - ball_radius, position[1] - ball_radius))

    pygame.draw.circle(screen, ball_color, ball_center, int(ball_radius))
    pygame.draw.circle(screen, (255, 255, 255), ball_center, int(ball_radius), 2)

    font = pygame.font.Font(None, 36)
    text = font.render(f"Bounces: {bounces}", True, (255, 255, 255))
    screen.blit(text, (WIDTH/2-65, HEIGHT-36))

    pygame.display.flip()

    clock.tick(60)

    # Update color phase
    color_phase += transition_speed

pygame.quit()
