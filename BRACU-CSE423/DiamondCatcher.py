#assignment2 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import os

width=800
height=600
catcher_width =120
catcher_height =22
catcher_x = width// 2 - catcher_width // 2 #340
catcher_y = 30
catcher_color = [1.0, 1.0, 1.0, 1.0]

diamond_x = random.randint(50, 750)
diamond_y =600
diamond_speed =50
diamond_asc =20
d_size =20
diamond_color = [1, 1, 1]

score = 0
game_running = True
game_over = False  
game_paused = False
winner=False
cheat = False

catcher_speed =30 
max_speed=150 
keys = {'left': False, 'right': False}
lives=1
last_time = time.time()

def Find_Zone(x1, y1, x2, y2):     
    dx = x2 - x1
    dy = y2 - y1
    zone=0
    if abs(dx) >= abs(dy):
        if dx > 0 and dy > 0:
            zone=0
        elif dx < 0 and dy > 0:
            zone=3
        elif dx < 0 and dy < 0:
            zone=4
        elif dx > 0 and dy < 0:
            zone= 7
    else:
        if dx > 0 and dy > 0:
            zone=1
        elif dx < 0 and dy > 0:
            zone= 2
        elif dx < 0 and dy < 0:
            zone= 5
        elif dx > 0 and dy < 0:
            zone= 6
    return zone

def convertToZone0(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y

def convertFromZone0(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, x
    if zone == 3:
        return -x,y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y
    
def DrawLine(x1, y1, x2, y2, color):# 8way
    
    if x1 == x2:
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_POINTS)

        if y1 > y2:
            y1, y2 = y2, y1

        for y in range(int(y1), int(y2)+1):
            glVertex2f(x1, y)

        glEnd()
        return
    zone = Find_Zone(x1, y1, x2, y2)
    x1_prime, y1_prime = convertToZone0(x1, y1, zone)
    x2_prime, y2_prime = convertToZone0(x2, y2, zone)

    x1_prime, y1_prime, x2_prime, y2_prime = int(x1_prime), int(y1_prime), int(x2_prime), int(y2_prime)
    if x1_prime > x2_prime:
        x1_prime, x2_prime = x2_prime, x1_prime
        y1_prime, y2_prime = y2_prime, y1_prime
    
    dx = x2_prime - x1_prime
    dy = y2_prime - y1_prime
    d = 2*dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1_prime
    
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    for x in range(x1_prime, x2_prime + 1):
        x_orig, y_orig = convertFromZone0(x, y, zone)
        glVertex2f(x_orig, y_orig)
          
        if d > 0:
            d = d + incNE
            y = y + 1
        else:
            d = d + incE
    glEnd()
    


def drawUI():

   
    DrawLine(50,560,90,560,(0,0.8,0.8))
    DrawLine(50,560,70,580,(0,0.8,0.8))
    DrawLine(50,560,70,540,(0,0.8,0.8))

    
    DrawLine(710,540,750,580,(1,0,0)) #/
    DrawLine(710,580,750,540,(1,0,0)) #\

    
    if not game_paused:
        DrawLine(385,540,385,580,(1,0.7,0))
        DrawLine(405,540,405,580,(1,0.7,0))
    else:
        DrawLine(385,540,385,580,(1,0.7,0))
        DrawLine(385,540,415,560,(1,0.7,0))
        DrawLine(385,580,415,560,(1,0.7,0))

def drawDiamond():
    d = {
        "1": ((diamond_x, diamond_y+d_size), (diamond_x+d_size, diamond_y)),
        "2": ((diamond_x+d_size, diamond_y), (diamond_x, diamond_y-d_size)),
        "3": ((diamond_x, diamond_y-d_size), (diamond_x-d_size, diamond_y)),
        "4": ((diamond_x-d_size, diamond_y), (diamond_x, diamond_y+d_size))
    }
    for k in d: DrawLine(d[k][0][0],
                          d[k][0][1],
                            d[k][1][0],
                              d[k][1][1], diamond_color)

def drawCatcher():
    c_clr = (1, 0, 0) if game_over else (1, 1, 1)
    c = {
        "top": ((catcher_x, 50), (catcher_x+120, 50)),
        "bot": ((catcher_x+20,20), (catcher_x+100, 20)),
        "l": ((catcher_x, 50), (catcher_x+20, 20)),
        "r": ((catcher_x+120,50), (catcher_x+100, 20))
    }
    for k in c: DrawLine(c[k][0][0], c[k][0][1], c[k][1][0], c[k][1][1], c_clr)


def draw_score():
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(10,10)
    for char in f"Score: {score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def draw_cheat_indicator():
    if cheat:
        glColor3f(0.0, 1.0, 0.0)
        glRasterPos2f(170, 560)
        for char in "CHEAT MODE":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def draw_game_over():
    if game_over and not winner:
         glColor3f(1.0, 0.0, 0.0)
         glRasterPos2f(330, 320)
         for char in "GAME OVER":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
         glRasterPos2f(330, 270)
         for char in f"Final Score: {score}":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
def draw_winner():
    if winner:
         glColor3f(1.0,1.0, 0.0)
         glRasterPos2f(330, 320)
         for char in "You Win!!!":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
         glRasterPos2f(330, 270)
         for char in f"Winner! MaxScore: {score}":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def draw_paused():
    if game_paused and not game_over:
        glColor3f(1.0, 1.0, 0.0)
        glRasterPos2f(350, 300)
        for char in "PAUSED":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def AABB_Collision(box1, box2):
    return (box1['x'] < box2['x'] + box2['width'] and
            box1['x'] + box1['width'] > box2['x'] and
            box1['y'] < box2['y'] + box2['height'] and
            box1['y'] + box1['height'] > box2['y'])

def CheckCollision():
    diamond_box = {
        'x': diamond_x - d_size,
        'y': diamond_y - d_size,
        'width': d_size * 2,
        'height': d_size * 2
    }
    
    catcher_box = {
        'x': catcher_x,
        'y': catcher_y,
        'width': catcher_width,
        'height': catcher_height
    }   
    return AABB_Collision(diamond_box, catcher_box)


def SpawnDiamond():
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(d_size,width - d_size)
    diamond_y =600
    diamond_color = [random.uniform(0.5, 1.0),
                      random.uniform(0.5, 1.0),
                        random.uniform(0.5, 1.0), 1.0]

def ResetGame():
    global score,game_over,game_paused,catcher_color,diamond_speed, diamond_x,diamond_y,catcher_x
    global winner,cheat
    score = 0
    cheat=False
    game_over = False
    game_paused = False
    winner=False
    catcher_color = [1.0, 1.0, 1.0, 1.0]
    diamond_speed = 50
    catcher_x = width// 2 - catcher_width // 2 #340
    SpawnDiamond()
    print("Starting Over")

def get_catcher_speed():
    base_catcher_speed = 20 
    speed = base_catcher_speed + (score//2) 
    max_speed =80
    return min(speed, max_speed)

def UpdateGame(dt):
    global diamond_y, diamond_speed, score, game_over, catcher_x, diamond_x, catcher_color
    global catcher_speed, winner 

   
    if game_paused or game_over or winner:
        return

    base_catcher_speed =20
    base_diamond_speed =50

    
    diamond_speed = base_diamond_speed +(score * 15)
    normal_catcher_speed =base_catcher_speed +(score * 10)

  
    diamond_speed = min(diamond_speed, 300)
    normal_catcher_speed = min(normal_catcher_speed, 120)

    
    diamond_y -= diamond_speed* dt 

   
    if CheckCollision():
        score += 1
        print(f"Score: {score}")
        SpawnDiamond()
        if score == 30:
            winner = True
            catcher_color = [0, 0.5, 0.5,]
            print(f"Winner!! MaxScore: {score}")

    if not winner:
      if diamond_y < -d_size :
        game_over = True
        catcher_color = [1.0, 0.0, 0.0]
        print(f"Game Over - Final Score: {score}")

  
    if cheat and not game_over and not winner:
       
      cheat_speed = min(5 + score // 5, 15) 
    
      target_center = diamond_x
      current_center = catcher_x +(catcher_width // 2) #+60
      distance = target_center - current_center

   
      if abs(distance) > 1: 
         move_amount = min(abs(distance), cheat_speed)
         if distance > 0 :
            catcher_x += move_amount 
         else :
             catcher_x-=move_amount

    
    catcher_x = max(0, min(width - catcher_width, catcher_x))

def CheckMiss():
    global lives, game_over
    if diamond_y < -d_size:
        lives -= 1
        if lives <= 0:
            game_over = True
        else:
            SpawnDiamond()

     
def keyboard(key, x, y):
    global cheat, game_running
    
    if key == b'\x1b': 
        game_running = False
        glutLeaveMainLoop()
    
    if key == b'c' or key == b'C':
        cheat = not cheat
        print("Cheat Mode:", "Activated" if cheat else "Deactivated")

# 
button_restart = {'x': 50, 'y': 550, 'width': 60, 'height': 40, 'color': [0.0, 0.8, 0.8, 1.0]}
button_pause = {'x': 370, 'y': 550, 'width': 60, 'height': 40, 'color': [1.0, 0.65, 0.0, 1.0]}
button_exit = {'x': 690, 'y': 550, 'width': 60, 'height': 40, 'color': [1.0, 0.0, 0.0, 1.0]}

def mouse(button, state, x, y):
    global game_paused, game_over, score, diamond_speed, diamond_y, diamond_x, catcher_x
    if state != GLUT_DOWN:
        return
    
    if button == GLUT_LEFT_BUTTON:
        mx = x
        my = height - y

        if 40 <= mx <= 100 and 530 <= my <= 590:
            print("Restarting...")
            ResetGame()
                  
        elif 370 <= mx <= 430 and 530 <= my <= 590:
            if not game_over:
                game_paused = not game_paused
                
        
        elif 700 <= mx <= 760 and 530 <= my <= 590:
            game_over=True
            print(f"Goodbye! Final Score: {score}")
            print("Closing Game...Exiting!!")
            #glutLeaveMainLoop()
            os._exit(0)
            #glutDestroyWindow(glutGetWindow()) 
            
def special_key(key, x, y):
    global catcher_x
    if not game_paused and not game_over and not winner:
        speed = get_catcher_speed()
        
        if key == GLUT_KEY_LEFT:
            catcher_x -=speed
        elif key == GLUT_KEY_RIGHT:
            catcher_x +=speed

        
        catcher_x = max(0, min(width - catcher_width, catcher_x))
def display():
    glClearColor(0.1,0.1,0.1,1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glPointSize(3)
    drawUI() 
    drawDiamond()
    drawCatcher()
    
    draw_score()
    draw_cheat_indicator()
    draw_game_over()
    draw_winner()
    draw_paused()
    
    glutSwapBuffers()

def setup_projection():
    glViewport(0, 0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0,height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def animate():
    global last_time
    current_time = time.time()
    dt = current_time -last_time 
    last_time = current_time
    
    UpdateGame(dt)  
    glutPostRedisplay()

def main():
    glutInit()
   
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(width,height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Assignment 2 DiamondCatcher")
    
    
    setup_projection()
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_key)
    glutMouseFunc(mouse)
    
   
    SpawnDiamond()   
    glutMainLoop()

if __name__ == "__main__":
    main()
