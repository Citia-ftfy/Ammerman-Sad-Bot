#runner for drawing elements
import pygame
import math
import random as rand
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from tdobj import TDObject as nrobj
import threading
import time


# Define your cube vertices and indices (for a unit cube)
running = False 
clear, increase, decrease, reset, prand, randomizer = False, False, False, False, False, False
tdobjs = []
camera_yaw = 0.0
jumprecent = False
jumps = 2
camera_pitch = 0.0
camera_pos = [0.0, 0.0, 5.0]  # Start slightly back
camera_vel = [0.0, 0.0, 0.0]  # Initial velocity
move_speed = 0.2
mousepaused = False
ground = None
fullscreen = True
ToAddCounter = 0

def draw_obj_vbo(obj):
    glPushMatrix()
    glTranslatef(*obj.get_position())
    glScalef(obj.get_size(), obj.get_size(), obj.get_size())
    glColor3fv(obj.get_color_fill())
    obj.get_vbo().draw()
    glPopMatrix()

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
    glBegin(GL_QUADS)
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
    global camera_yaw, camera_pitch, camera_pos, display, info, running, tdobjs
    pygame.init()
    #display = (1800,1200)
    glBegin(pygame.OPENGL)
    info = pygame.display.Info()
    display = (info.current_w, info.current_h)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    gluPerspective(45, (display[0]/display[1]), 0.1, 5000.0)
    glEnable(GL_DEPTH_TEST)
    ground = nrobj(vertices=[(-100, -1, -100), (100, -1, -100), (100, -1, 100), (-100, -1, 100)],
                edges=[(0, 1), (1, 2), (2, 3), (3, 0)],
                faces=[(0, 1, 2, 3)],
                position=(0, -1, 0),
                cf=(0.5, 0.5, 0.5),
                cl=(0.2, 0.2, 0.2),
                size=200)
    tdobjs = [obj1 := nrobj()] # Create an instance of TDObject
    running = True
    gravity_thread = threading.Thread(target=gravity_worker, daemon=True)
    gravity_thread.start()

    event_thread = threading.Thread(target=event_worker, daemon=True)
    event_thread.start()

    cam_thread = threading.Thread(target=camera_worker, daemon=True)
    cam_thread.start()

    jump_thread = threading.Thread(target=jump_worker, daemon=True)
    jump_thread.start()

    glClearColor(1.0, 1.0, 1.0, 1.0) 
   
    while eventhandler():
        # Mouse look
        global move_speed, mousepaused, ToAddCounter, clear, increase, decrease, reset, prand, randomizer
        mx, my = pygame.mouse.get_rel()
        if mousepaused:
            mx, my = 0, 0
        camera_yaw += mx * 0.2
        camera_pitch += my * 0.2
        camera_pitch = max(-89, min(89, camera_pitch))

        
        glLoadIdentity()
        gluPerspective(70, (display[0]/display[1]), 0.1, 5000.0)
        glRotatef(camera_pitch, 1, 0, 0)
        glRotatef(camera_yaw, 0, 1, 0)
        glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])   

        while ToAddCounter > 0:
            tdobjs.append(nrobj(position=(rand.uniform(camera_pos[0]-200, camera_pos[0]+200), rand.uniform(0, 200), rand.uniform(camera_pos[2]-200, camera_pos[2]+200)),cf=(rand.random(), rand.random(), rand.random()), cl=(rand.random(), rand.random(), rand.random())))
            ToAddCounter -= 1
        ToAddCounter = 0  # Reset counter after adding objects
        if clear:
            clear = False
            tdobjs.clear()
            tdobjs.append(nrobj(position=(0, 0, 0), cf=(1, 0, 0), cl=(0, 1, 0)))
        if randomizer:
            randomizer = False
            for obj in tdobjs:
                #obj.set_position((rand.uniform(-20, 20), rand.uniform(-20, 20), rand.uniform(-20, 20)))
                obj.set_vertices([(rand.uniform(-1, 1), rand.uniform(-1, 1), rand.uniform(-1, 1)) for _ in obj.get_vertices()])
                obj.set_edges([(rand.randint(0, len(obj.get_vertices()) - 1), rand.randint(0, len(obj.get_vertices()) - 1)) for _ in obj.get_edges()])
        if increase:
            #increase = False
            for obj in tdobjs:
                new_size = obj.get_size() + 0.1
                obj.set_size(new_size)
        if decrease:
            decrease = False
            for obj in tdobjs:
                new_size = max(0.1, obj.get_size() - 0.1)
        if reset:
            reset = False
            for obj in tdobjs:
                obj.reset()
        if prand:
            prand = False
            for obj in tdobjs:
                obj.set_position((rand.uniform(-200, 200), rand.uniform(0, 200), rand.uniform(-200, 200)))


        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #do_gravity()  # Apply gravity to objects
        draw_obj(ground)
        for obj in tdobjs:
            draw_obj_vbo(obj)
           


        pygame.display.flip()
        

        pygame.time.wait(10)


    running = False
    pygame.quit()
    return "Drawing completed"

def event_worker():
    global running, tdobjs, camera_pos, camera_yaw, camera_pitch, move_speed, mousepaused, randomizer, increase, decrease, reset, prand, clear, ToAddCounter, camera_vel, jumps, jumprecent
    time.sleep(2)  # Allow time for the main thread to set up
    while running:
        # WASD movement
        keys = pygame.key.get_pressed()
        yaw_rad = math.radians(camera_yaw)
        pitch_rad = math.radians(camera_pitch)
        forward = [math.sin(yaw_rad), 0, -math.cos(yaw_rad)]
        right = [math.cos(yaw_rad), 0, math.sin(yaw_rad)]
        up = [0, 1, 0]
        

        

        if keys[pygame.K_w]:
            camera_vel[0] += forward[0] * move_speed
            camera_vel[2] += forward[2] * move_speed
        if keys[pygame.K_s]:
            camera_vel[0] -= forward[0] * move_speed
            camera_vel[2] -= forward[2] * move_speed
        if keys[pygame.K_a]:
            camera_vel[0] -= right[0] * move_speed
            camera_vel[2] -= right[2] * move_speed
        if keys[pygame.K_d]:
            camera_vel[0] += right[0] * move_speed
            camera_vel[2] += right[2] * move_speed
        if keys[pygame.K_SPACE]:
            if camera_pos[1] > 3:  # Prevent jumping if already at max height
                if jumps > 0 and not jumprecent:
                    jumprecent = True
                    camera_vel[1] = move_speed * 8
                    jumps -= 1
                camera_vel[1] += 0 
            else:
                camera_vel[1] += move_speed * 8
        if keys[pygame.K_LCTRL] or keys[pygame.K_RSHIFT]:
            camera_pos[1] -= move_speed
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RCTRL]:
            move_speed = 0.8 if move_speed == 0.2 else 0.2  # Toggle speed between 0.2 and 0.5
        if keys[pygame.K_k]:
            ToAddCounter += 1
            #print("New object added")
        if keys[pygame.K_r]:
            randomizer = True
            #print("Vertices and edges randomized")
        if keys[pygame.K_KP_PLUS]:
            increase = True
            #print("Size increased")
        if keys[pygame.K_KP_MINUS]:
            decrease = True
            #print("Size decreased")
        if keys[pygame.K_p]:
            reset = True
            #print("Objects reset")
        if keys[pygame.K_i]:
            prand = True
            #print("Positions randomized")
        if keys[pygame.K_DELETE]:
            clear = True
            
       
        time.sleep(0.01)  # Adjust for event handling rate

def jump_worker():
    global jumprecent, running
    while running:
        if jumprecent:
            time.sleep(0.1)
            jumprecent = False
        time.sleep(0.01)  # Adjust for jump handling rate
            


def camera_worker():
    time.sleep(2)
    global camera_pos, camera_yaw, camera_pitch, move_speed, running
    while running:
        #INNERTIAL CAMERA MOVEMENT
        camera_pos[0] += camera_vel[0]
        camera_pos[1] += camera_vel[1]
        camera_pos[2] += camera_vel[2]
        camera_vel[0] *= 0.9  # Dampen horizontal velocity
        camera_vel[2] *= 0.9  # Dampen horizontal velocity
        if camera_pos[1] > 3:
            camera_vel[1] -= 0.1
        else:
            jumps = 2  # Reset jumps when on ground
            camera_pos[1] = 3  # Prevent camera from falling below ground level
            camera_vel[1] = 0  # Reset vertical velocity when on ground
        time.sleep(0.01)

def gravity_worker():
    global tdobjs, running, ToAddCounter, camera_pos
    ToAddCounter = 0
    while running:
        for obj in tdobjs:
            if obj.get_position()[1] > -1:
                velocity = obj.get_velocity()
                new_pos = list(obj.get_position())
                new_pos[0] += velocity[0]
                new_pos[1] += velocity[1]
                new_pos[2] += velocity[2]
                obj.set_velocity((velocity[0], velocity[1] - 0.05, velocity[2]))  # Apply gravity
                obj.set_position(tuple(new_pos))
            else:
                tdobjs.remove(obj)  # Remove object if it falls below ground level
                ToAddCounter += 1
                #tdobjs.append(nrobj(position=(rand.uniform(-200, 20), rand.uniform(0, 200), rand.uniform(-20, 200)),cf=(rand.random(), rand.random(), rand.random()), cl=(rand.random(), rand.random(), rand.random())))
                #obj.set_position((obj.get_position()[0], -1, obj.get_position()[2]))

        time.sleep(0.01)  # Adjust for gravity update rate

'''
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
'''
def isRunning():
    return running  # Returns True if pygame is initialized


def eventhandler():
    global tdobjs, mousepaused, fullscreen, display
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if(pygame.event.get_grab()):
                    pygame.event.set_grab(False)
                    pygame.mouse.set_visible(True)
                    mousepaused = True
                else:
                    pygame.event.set_grab(True)
                    pygame.mouse.set_visible(False)
                    mousepaused = False
                #return False
            if event.key == K_F11:
                if fullscreen:
                    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
                    display = (1800,1200)
                    fullscreen = False
                else:
                    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)
                    display = (info.current_w, info.current_h)
                    fullscreen = True
    return True
