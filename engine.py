import pygame
import random
import math

pygame.display.set_caption("Simple Engine Prototype")
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
background_colour = (255,255,255)

#environment variables
gravity = [math.pi, 0.002]
drag = 1
elasticity = 0.75


def add_vectors(angle1,length1,angle2,length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return angle, length

def find_particle(particles,x,y):
    for p in particles:
        if math.hypot(p.x-x,p.y-y) <= p.size:
            return p
    return None

def collide(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dx,dy)
    if distance < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        p1.angle = 2 * tangent - p1.angle
        p2.angle = 2 * tangent - p2.angle
        (p1.speed, p2.speed) = (p2.speed, p1.speed)
        p1.speed *= elasticity
        p2.speed *= elasticity

        angle = 0.5 * math.pi + tangent
        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


class Particle:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0,0,255,255)
        self.thickness = 1
        #self.speed = 0.01
        #self.angle = math.pi/2

    def display(self):
        pygame.draw.circle(screen,self.colour,(int(self.x),int(self.y)),self.size,self.thickness)

    def move(self):
        self.x += math.sin(self.angle)*self.speed
        self.y -= math.cos(self.angle)*self.speed

        #gravity
        (self.angle, self.speed) = add_vectors(self.angle, self.speed, gravity[0], gravity[1])
        #drag
        self.speed *= drag


    def bounce(self):
        #right wall
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = -self.angle
            # elasticity
            self.speed *= elasticity
        #left wall
        if self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            # elasticity
            self.speed *= elasticity
        #floor
        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            # elasticity
            self.speed *= elasticity
        #ceiling
        if self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            # elasticity
            self.speed *= elasticity


num_of_particles = 30
my_particles = []

#creating particles
for n in range(num_of_particles):
    size = random.randint(10,20)
    x = random.randint(size, width-size)
    #y = random.randint(size, height-size)
    y = 20

    particle = Particle(x,y,size)
    particle.speed = random.random()
    particle.angle = random.uniform(0,2*math.pi)

    my_particles.append(particle)

selected_particle = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX,mouseY) = pygame.mouse.get_pos()
            selected_particle = find_particle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    # dragging particles with varying speed
    if selected_particle:
        selected_particle.colour = (255, 0, 0)
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = math.atan2(dy, dx) + 0.5 * math.pi
        selected_particle.speed = math.hypot(dx, dy) * 0.1
    # change color if not used
    else:
        for particle in my_particles:
            particle.colour = (0, 0, 255, 255)

    # displaying particles
    screen.fill(background_colour)

    for i,particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
            collide(particle,particle2)
        particle.display()


    pygame.display.flip()