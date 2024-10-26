import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Bullet Class
class Bullet:
    def __init__(self, x, y, speed, angle):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)

# BulletHell Class
class BulletHell:
    def __init__(self):
        self.bullets = []
        self.pattern_index = 0
        self.patterns = ['circular', 'spiral', 'wave', 'random', 'converging']

    def create_circular(self, num_bullets):
        radius = 100  # Radius of the circle
        for i in range(num_bullets):
            angle = i * math.pi * 2 / num_bullets  # Evenly distribute around a circle
            speed = 2  # Constant speed
            bullet = Bullet(400 + radius * math.cos(angle), 300 + radius * math.sin(angle), speed, angle)
            self.bullets.append(bullet)

    def create_spiral(self, num_bullets):
        for i in range(num_bullets):
            angle = i * math.pi / 180 * 10 * (i / num_bullets)  # Increase angle gradually
            speed = 3  # Constant speed
            bullet = Bullet(400, 300, speed, angle)  # Start from the center
            self.bullets.append(bullet)

    def create_wave(self, num_bullets):
        for i in range(num_bullets):
            angle = math.sin(i * 0.3) * (math.pi / 4)  # Sine wave effect
            speed = 2 + i * 0.1  # Increasing speed for each bullet
            bullet = Bullet(400, 300, speed, angle)  # Start from the center
            self.bullets.append(bullet)

    def create_random(self, num_bullets):
        for _ in range(num_bullets):
            angle = random.uniform(0, 2 * math.pi)  # Random angle
            speed = random.uniform(2, 5)  # Random speed
            bullet = Bullet(400, 300, speed, angle)  # Start from the center
            self.bullets.append(bullet)

    def create_converging(self, num_bullets):
        for i in range(num_bullets):
            angle = i * math.pi * 2 / num_bullets  # Evenly distribute around a circle
            speed = 3  # Constant speed
            bullet = Bullet(400 + 200 * math.cos(angle), 300 + 200 * math.sin(angle), speed, angle + math.pi)  # Move towards the center
            self.bullets.append(bullet)

    def create_pattern(self, num_bullets):
        if self.pattern_index == 0:
            self.create_circular(num_bullets)
        elif self.pattern_index == 1:
            self.create_spiral(num_bullets)
        elif self.pattern_index == 2:
            self.create_wave(num_bullets)
        elif self.pattern_index == 3:
            self.create_random(num_bullets)
        elif self.pattern_index == 4:
            self.create_converging(num_bullets)

    def update(self):
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

# Main Function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Bullet Hell Patterns')
    clock = pygame.time.Clock()
    
    bullet_hell = BulletHell()
    bullet_hell.create_pattern(36)  # Create the first pattern
    pattern_switch_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        if current_time - pattern_switch_time > 5000:  # Switch patterns every 5 seconds
            bullet_hell.bullets = []  # Clear the bullets
            bullet_hell.pattern_index = (bullet_hell.pattern_index + 1) % 5  # Move to the next pattern
            bullet_hell.create_pattern(36)  # Create the new pattern
            pattern_switch_time = current_time

        screen.fill((0, 0, 0))
        bullet_hell.update()
        bullet_hell.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()