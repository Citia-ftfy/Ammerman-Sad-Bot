#runner for drawing elements
import pygame
import random as rand
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from tdobj import TDObject as nrobj


running = False
tdobjs = [obj1 := nrobj()] 



def draw_obj(obj):
    vertices = obj.get_vertices()
    edges = obj.get_edges()
    faces = obj.get_faces()
    position = obj.get_position()  # Get the object's position
    cf = obj.get_color_fill()  # Get the color fill
    cl = obj.get_color_line()  # Get the color line

    glPushMatrix()
    glTranslatef(*position)  # Move to the object's position

    # Draw faces (shaded)
    glBegin(GL_POLYGON)
    glColor3fv(cf)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    # Draw edges (wireframe)
    glColor3fv(cl)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glPopMatrix()

def draw(obj):
    pygame.init()
    display = (1800,1200)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)
    running = True
    while eventhandler():
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for obj in tdobjs:
            draw_obj(obj)
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()
    return "Drawing completed"

def isRunning():
    return running  # Returns True if pygame is initialized

def eventhandler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
            if event.key == K_SPACE:
                global tdobjs
                tdobjs.append(nrobj(position=(rand.uniform(-2, 2), rand.uniform(-2, 2), rand.uniform(-2, 2)),cf=(rand.random(), rand.random(), rand.random()), cl=(rand.random(), rand.random(), rand.random())))
                print("New object added")
                print("Space key pressed")

    return True
