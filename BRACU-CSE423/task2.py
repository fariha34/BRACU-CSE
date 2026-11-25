##Task 2####
from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLUT import *    # GLUT library for window and input handling
from OpenGL.GLU import *     # OpenGL Utility library
import random


# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
balls=[]
b_count=0
blink=False
#blink_period=1.0
frozen=False
b_speed=0.5
visible=True
size=3
# ===== Coordinate Conversion =====
def convert_coordinate(x, y):
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT/2) - y
    return a, b


# ===== Draw Functions =====
def draw_point(x, y, size): ##single point/ball
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_axes():  ##bounding box
    glLineWidth(5)
    glBegin(GL_LINES)
                         # X-axis (red) bottom
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-250,-250)
    glVertex2f(250,-250)
                         # Y-axis (blue) 
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(250,-250)
    glVertex2f(250,250)

    glColor3f(1.0, 0.0, 0.0) #up
    glVertex2f(250,250)
    glVertex2f(-250,250)
                         # Y-axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-250,250)
    glVertex2f(-250,-250)
    glEnd()

    glLineWidth(4)
    glBegin(GL_LINES)
                         # X-axis (red) bottom
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-180,-180)
    glVertex2f(180,-180)
                         # Y-axis (blue) 
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(180,-180)
    glVertex2f(180,180)

    glColor3f(1.0, 0.0, 0.0) #up
    glVertex2f(180,180)
    glVertex2f(-180,180)
                         # Y-axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-180,180)
    glVertex2f(-180,-180)
    glEnd()

def draw_balls():
    global visible
    for p in balls:
        if blink or not visible:
            glColor3f(0,0,0) #black
            #glColor3f(1,1,1) # white
        else:
            glColor3f(p[4], p[5], p[6])
        draw_point(p[0],p[1],6)
    
# ===== Keyboard & Mouse Interaction =====
def keyboard(key, x, y):    
    global frozen
    if key == b' ':  # space
        frozen= not frozen

def special_key(key, x, y):  
    global b_speed
    if frozen:
        return  
    if key == GLUT_KEY_UP:
        b_speed *=1.5
        if b_speed >10:
            b_speed=10
        #print("Speed increased")
    elif key == GLUT_KEY_DOWN:
        b_speed /=1.5
        if b_speed< 0.05:
            b_speed=0.05
        #print("Speed decreased")   
    #glutPostRedisplay()


def mouse(b_click, state, x, y):
    global balls, blink,visible, b_count
    if frozen:
        return
    if b_click == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink= not blink
        if blink:   ###
            visible=True
            b_count=0
        else:
            visible=True
    elif b_click == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        new_x,new_y= convert_coordinate(x, y)
        di_x= random.choice([-1,1])
        di_y= random.choice([-1,1])
        r,g,b= random.random(), random.random(),random.random()
        balls.append([new_x,new_y,di_x,di_y,r,g,b])

# ===== Projection Setup =====
def setup_projection():
   
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)

# ===== Display & Animation =====
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_axes() #box
    
    draw_balls()

    glutSwapBuffers()


def animate():
    
    global balls ,b_count, visible,frozen,blink
    #glutPostRedisplay()

    if not frozen:
        for p in balls:
            p[0]+=p[2]*b_speed
            p[1]+=p[3]*b_speed
            if  p[0]<= -180 or p[0]>=180:
                p[2]*=-1
            if p[1]>= 180 or p[1]<=-180:
                p[3]*=-1
        if blink:
            b_count+=1
        if b_count >=50:
            visible=not visible
            b_count=0
    glutPostRedisplay()


# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Task 2")
    # Register callback functions
    #glClearColor(1,1,1,1)
    setup_projection()
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_key)
    glutMouseFunc(mouse)

    glutMainLoop()

# ===== Entry Point =====
if __name__ == "__main__":
    main()
