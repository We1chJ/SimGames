import pygame
import numpy as np
import math

pygame.init()
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
BLACK = (0,0,0)
ORANGE = (255,165,0)
RED = (255,0,0)

CIRCLE_CENTER = np.array([WIDTH/2, HEIGHT/2], dtype=np.float64)
CIRCLE_RADIUS = 150
BALL_RADIUS = 5
ball_pos = np.array([WIDTH/2, HEIGHT/2], dtype=np.float64)

GRAVITY = 0.2
# ball_v = np.array([1,0], dtype=np.float64)
ball_v = np.random.rand(2) * 2 - 1

# arc 
arc_degree = 60
start_angle = math.radians(-arc_degree/2)
end_angle = math.radians(arc_degree/2)
spinning_speed = 0.01
def draw_arc(window, center, radius, start_angle, end_angle):
    p1 = center + (radius+1000) * np.array([math.cos(start_angle), math.sin(start_angle)])
    p2 = center + (radius+1000) * np.array([math.cos(end_angle), math.sin(end_angle)])
    pygame.draw.polygon(window, BLACK, [center, p1, p2])

def is_ball_in_arc(ball_pos, CIRCLE_CENTER, start_angle, end_angle):
    dx = ball_pos[0] - CIRCLE_CENTER[0]
    dy = ball_pos[1] - CIRCLE_CENTER[1]
    ball_angle = math.atan2(dy, dx)
    if start_angle <= ball_angle <= end_angle:
        return True

running = True
is_ball_in = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill(BLACK)

    start_angle += spinning_speed
    end_angle += spinning_speed
    start_angle = start_angle % (2*math.pi)
    end_angle = end_angle % (2*math.pi)
    if end_angle < start_angle:
        end_angle += 2*math.pi

    ball_v[1] += GRAVITY
    ball_pos += ball_v

    dist = np.linalg.norm(ball_pos-CIRCLE_CENTER)
    if dist + BALL_RADIUS > CIRCLE_RADIUS:
        if is_ball_in_arc(ball_pos, CIRCLE_CENTER, start_angle, end_angle):
            is_ball_in = False
        if is_ball_in:
            ball_pos = CIRCLE_CENTER + (ball_pos - CIRCLE_CENTER) / dist * (CIRCLE_RADIUS-BALL_RADIUS)
            v_dist = ball_pos-CIRCLE_CENTER
            tangent = np.array([-v_dist[1], v_dist[0]])
            proj = np.dot(tangent, ball_v)/(np.linalg.norm(tangent)**2)*tangent
            ball_v = 2 * proj - ball_v
            ball_v += tangent*spinning_speed

    pygame.draw.circle(window, ORANGE, CIRCLE_CENTER, CIRCLE_RADIUS, 3)
    draw_arc(window, CIRCLE_CENTER, CIRCLE_RADIUS, start_angle, end_angle)
    pygame.draw.circle(window, RED, ball_pos, BALL_RADIUS)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()