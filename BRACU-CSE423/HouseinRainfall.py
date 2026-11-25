#Assignment 1 ##TASK! 1
from OpenGL.GL import *    # Core OpenGL functions (drawing, colors, etc.)
from OpenGL.GLU import *   # OpenGL Utility Library (projection utilities)
from OpenGL.GLUT import *  # GLUT library (window creation, display, loop)
import random

# Global Coordinates
x, y = 500, 500 #width,height
brightness=0.0    # Night
day_bright=0.0
f_red,f_green,f_blue=0.05,0.25,0.05
                 #Rain variables
no_of_rain=50
rain_drops= []  #
rain_speed=5.0
wind_speed=2.0 #controls bending of rain

def draw_screen():
   glColor(0.0,0.0,0.2) #sky
   glBegin(GL_LINES)
   glVertex2f(0,250)
   glVertex2f(500,250)

   glVertex2f(500,250)
   glVertex2f(500,500)

   glVertex2f(500,500)
   glVertex2f(0,500)
   glVertex2f(0,500)
   glVertex2f(0,250)
   glEnd()

   glColor(f_red,f_green,f_blue)
   glBegin(GL_LINES)  #field
   glVertex2f(0,0)
   glVertex2f(500,0)
   glVertex2f(500,0)
   glVertex2f(500,249)
   glVertex2f(500,249)
   glVertex2f(0,249)
   glVertex2f(0,249)
   glVertex2f(0,0)
   glEnd()
   glColor3f(0.20, 0.30, 0.05) #coloring
   glBegin(GL_TRIANGLES)
   glVertex2f(0,0) 
   glVertex2f(500,0)  
   glVertex2f(500,247) 
   glVertex2f(0,0)  
   glVertex2f(500,247) 
   glVertex2f(0,247)  
   glEnd()


   glColor3f(0.40, 0.20, 0.05)   #Tree bottom
   glBegin(GL_TRIANGLES)
   glVertex2f(350,150) 
   glVertex2f(390,150)  
   glVertex2f(390,220)    
   glVertex2f(350,150)  
   glVertex2f(390, 220) 
   glVertex2f(350, 220)  
   glEnd()
   glColor3f(0.0, 0.5, 0.1)  #Tree up
   glBegin(GL_TRIANGLES)
   glVertex2f(320, 220)
   glVertex2f(420, 220)
   glVertex2f(375, 340)
   glEnd()


   glColor3f(0.0,0.7,0.3)  #more smallTree
   glBegin(GL_TRIANGLES)
   glVertex2f(0,150)
   glVertex2f(40,150)
   glVertex2f(20,198)
   glEnd()
   glColor3f(0.0,0.8,0.4)  # smallTree
   glBegin(GL_TRIANGLES)
   glVertex2f(41,150)
   glVertex2f(90,150)
   glVertex2f(70,198)
   glEnd()
   glColor3f(0.0,0.7,0.3)  # smallTree
   glBegin(GL_TRIANGLES)
   glVertex2f(91,150)
   glVertex2f(130,150)
   glVertex2f(110,198)
   glEnd()
   glColor3f(0.0,0.2,0.098)  # smallTree rightside
   glBegin(GL_TRIANGLES)
   glVertex2f(460,150)
   glVertex2f(500,150)
   glVertex2f(480,198)
   glEnd()
   glColor3f(0.0,0.2,0.098)  # smallTree rightside
   glBegin(GL_TRIANGLES)
   glVertex2f(420,150)
   glVertex2f(460,150)
   glVertex2f(460,198)
   glEnd()
   glColor3f(0.0,0.4,0.098)  # smallTree houseside
   glBegin(GL_TRIANGLES)
   glVertex2f(301,150)
   glVertex2f(350,150)
   glVertex2f(326,198)
   glEnd()
   #sun? Moon
   glColor3f(0.9, 0.9, 0.2)  #yellow
   glPointSize(11)            
   glBegin(GL_POINTS)
   glVertex2f(402,438)      
   glEnd()

   glColor3f(0.9, 0.5, 0.5) #Tree bottom2
   glBegin(GL_TRIANGLES)
   glVertex2f(50, 200)
   glVertex2f(90, 200)
   glVertex2f(90, 260)
   glVertex2f(50,200)
   glVertex2f(90,260)
   glVertex2f(50,260)
   glEnd()
   glColor3f(0.1, 0.5, 0.25)  #Tree up
   glBegin(GL_TRIANGLES)
   glVertex2f(30, 260)
   glVertex2f(110,260)
   glVertex2f(70, 370)
   glEnd()
   glColor3f(0.4, 0.2, 0.05) #Tree bottom3
   glBegin(GL_TRIANGLES)
   glVertex2f(450, 210)
   glVertex2f(480, 210)
   glVertex2f(480, 260)
   glVertex2f(450,210)
   glVertex2f(480,260)
   glVertex2f(450,260)
   glEnd()
   glColor3f(0.1, 0.5, 0.25)  #Tree up
   glBegin(GL_TRIANGLES)
   glVertex2f(430, 260)
   glVertex2f(500,260)
   glVertex2f(465, 340)
   glEnd()
   #path
   glColor3f(0.6,0.4,0.35)  #coloring
   glBegin(GL_TRIANGLES)
   glVertex2f(150,0) 
   glVertex2f(300,0)  
   glVertex2f(230,149)    

   glVertex2f(150,0)  
   glVertex2f(230,149) 
   glVertex2f(190,149)  
   glEnd()

def draw_house():
   #"""Draw a simple house using GL_LINES"""
   glLineWidth(4)
   glColor3f(0.7, 0.4, 0.0)  # Brown
  
   # House base
   glBegin(GL_LINES)
   glVertex2f(130,150) # bottom left
   glVertex2f(300,150) # b right
   glVertex2f(300,150) #b right
   glVertex2f(300,220)  #u right
   glVertex2f(300,220)   #u right
   glVertex2f(180,220)  #u left
   glVertex2f(180,220) # u left
   glVertex2f(130,150) #bottom left
   glEnd()

   glColor3f(1, 1, 1)  #coloring
   glBegin(GL_TRIANGLES)
   glVertex2f(132, 150)
   glVertex2f(299,150)
   glVertex2f(300, 220)

   glVertex2f(132, 150)
   glVertex2f(300,220)
   glVertex2f(132,220)
   glEnd()
   # Roof with.line
   glColor3f(0.7, 0.0, 0.0)  # Red
   glBegin(GL_LINES)
   glVertex2f(120,220)
   glVertex2f(320,220)
   glVertex2f(320,220) 
   glVertex2f(220, 310) #peek
   glVertex2f(220, 310)
   glVertex2f(120,220)
   glEnd()
   glColor3f(0.7, 0.3, 0.1)  #coloring
   glBegin(GL_TRIANGLES)
   glVertex2f(120,220)
   glVertex2f(320,220)
   glVertex2f(220,310)
   glEnd()
   # Door
   glColor3f(0.2, 0.2, 0.2) #dark gray
   glBegin(GL_LINES)
   glVertex2f(200,150)
   glVertex2f(220,150)
   glVertex2f(220, 150)
   glVertex2f(220, 190)
   glVertex2f(220, 190)
   glVertex2f(200, 190)
   glVertex2f(200, 190)
   glVertex2f(200, 150)
   glEnd()
   glColor3f(0.7,0.4,0.2)  #coloring
   glBegin(GL_TRIANGLES)
   glVertex2f(203,147) 
   glVertex2f(217,147)  
   glVertex2f(217,187)    

   glVertex2f(203,147)  
   glVertex2f(217,187) 
   glVertex2f(203,187)  
   glEnd()
   
# Window right
   glColor3f(0.2, 0.2, 0.4) #dark gray
   glBegin(GL_LINES)
   glVertex2f(250,165)
   glVertex2f(280,165)
   glVertex2f(280, 165)
   glVertex2f(280, 180)
   glVertex2f(280, 180)
   glVertex2f(250, 180)
   glVertex2f(250, 180)
   glVertex2f(250, 165)
   glEnd()
   glColor3f(0.2, 0.2, 0.4) #dark gray window gril
   glBegin(GL_LINES)
   glVertex2f(265,165)
   glVertex2f(265,180)   
   glEnd()
#Window left
   glColor3f(0.2, 0.2, 0.4) #dark gray
   glBegin(GL_LINES)
   glVertex2f(140,165)
   glVertex2f(170,165)
   glVertex2f(170, 165)
   glVertex2f(170, 180)
   glVertex2f(170, 180)
   glVertex2f(140, 180)
   glVertex2f(140, 180)
   glVertex2f(140, 165)
   glEnd()
   glColor3f(0.2, 0.2, 0.4) #dark gray window gril
   glBegin(GL_LINES)
   glVertex2f(155,165)
   glVertex2f(155,180)   
   glEnd()
def draw_rain():
   global rain_drops 
   #glPointSize(2)
   glColor3f(0.7+0.3*brightness, 0.8+0.2*brightness, 1.0) # Light Blue rain
   glBegin(GL_LINES)                                      #changes
   for drop in rain_drops:
       x,y=drop
       glVertex2f(x,y)
       glVertex(x+wind_speed*5,y-25)
   glEnd()   
   for drop in rain_drops:  
       drop[1] -= rain_speed # Fall down
       drop[0] += wind_speed # Applying wind
      
       #if off screen
       if drop[1] < 0:
           drop[1] =random.uniform(400,500)
           drop[0] = random.uniform(0,500)
       if  drop[0]> 500:
           drop[0]=0
       if drop[0]< 0:
          drop[0]=500


# ===== Set up 2D coordinate system =====
def setup_projection():
   glViewport(0, 0, 500, 500)     # Define the portion of the window to render to
   glMatrixMode(GL_PROJECTION)    # Switch to the projection matrix
   glLoadIdentity()               # Reset the projection matrix
   glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)  # Define a 2D orthographic projection
   glMatrixMode(GL_MODELVIEW)     # Switch back to the modelview matrix




# ===== Display callback =====
def display():
   global brightness
  
   # background change
   if abs(brightness - day_bright) > 0.01:
       brightness += (day_bright - brightness) * 0.05
  
   # Night (0.0, 0.0, 0.1) to Day (0.5, 0.7, 1.0)
   r = 0.0+(0.5* brightness)
   g = 0.0+(0.7*brightness)
   b = 0.1+(0.9*brightness)
  
   glClearColor(r, g, b, 1.0)
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen and depth buffer
   glLoadIdentity()                                    # Reset transformations
   setup_projection()                                  # Set up coordinate system
   #glColor3f(1.0, 1.0, 0.0)  
                            # Set color (R, G, B) → Yellow
   #draw_points(x, y) 
   draw_screen()
   draw_house()
   draw_rain()                                 # Draw the point
   glutSwapBuffers()                      # Swap buffers (double buffering)


def animate():
   glutPostRedisplay()


# --- Input Handlers ---
def special_key(key, x, y):
   global wind_speed
   if key == GLUT_KEY_LEFT:
       wind_speed -=0.5 # Bend left
   elif key == GLUT_KEY_RIGHT:
       wind_speed+=0.5  # Bend right
   if wind_speed< -10:
       wind_speed=-10
   if wind_speed >10:
       wind_speed=10
   
   glutPostRedisplay()


def keyboard_con(key, x, y):  #Gradually shift kora lagbe
   global day_bright
   if key == b'd': # Day
       day_bright = 1.0
   elif key == b'n': # Night
       day_bright= 0.0
   glutPostRedisplay()

#Initialize Raindrops
for _ in range(no_of_rain):
   rain_drops.append([random.uniform(0,500), random.uniform(250, 500)])

# ===== Main entry point =====
def main():
   glutInit()                               # Initialize GLUT
   glutInitDisplayMode(GLUT_RGBA)           # Set display mode: RGBA color
   glutInitWindowSize(500, 500)             # Set window size (width, height)
   glutInitWindowPosition(50, 50)             # Set window position (top-left corner)
   glutCreateWindow(b"Task 1: House in Rainfall")     # Create window with a title
   glutDisplayFunc(display)                 # Register display callback
   glutIdleFunc(animate)
   glutSpecialFunc(special_key)
   glutKeyboardFunc(keyboard_con)
   glutMainLoop()                           # Start the main event-processing loop

if __name__ == "__main__":
   main()



##Task 2
from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLUT import *    # GLUT library for window and input handling
from OpenGL.GLU import *     # OpenGL Utility library
import random


# ===== Global Variables =====
WINDOW_WIDTH=500
WINDOW_HEIGHT= 500
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
def draw_point(x, y,size): ##single point/ball
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

def spawn_balls():
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

#when we click left the ball should start blinking till we click left again
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
    spawn_balls() 
    glutSwapBuffers()


def animate():   
    global balls ,b_count, visible,frozen,blink
    #glutPostRedisplay()

    if not frozen:  #bouncing wall
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



