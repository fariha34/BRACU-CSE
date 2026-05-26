from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
from OpenGL.GLUT import fonts

WINDOW_W, WINDOW_H = 1000, 800
GRID_LENGTH   = 600      
GRID_LINES    = 10       
WALL_HEIGHT   = 150     
 
PLAYER_SPEED  = 10
TURN_SPEED    = 5       
BULLET_SPEED  = 10
BULLET_SIZE   = 12
MAX_ENEMIES   = 5
MISS_LIMIT    = 10
MAX_LIVES     = 5
ENEMY_SPEED   = 0.6

WIN_SCORE=100
CHEAT_FIRE_DELAY =25  
CHEAT_AIM_SPEED = 3.0  
CHEAT_AIM_TOL      = 5.0 
CHEAT_ROTATE_SPEED = 4.0 

player_x =0.0
player_y = 0.0     
gun_angle  = 0.0     # player direction
game_over  = False
player_won=False
lives      = MAX_LIVES
score      = 0
bullets_missed = 0
angle_diff=0.0

# 3rd person camara position
cam_angle  = 0.0   
cam_elev   = 500.0  
cam_radius = 700.0  
first_person   = False   
cheat_vision   = False  
cheat_mode = False
hit_timer = 0  
cheat_fire_timer=0

bullets = []
enemies = []
fovY = 80
 

def clamp(v, lo, hi):
    return max(lo, min(hi, v))
 
def dist2d(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by)
 
def random_enemy_pos():
    """Spawn far from the player."""
    while True:
        x = random.uniform(-GRID_LENGTH +80, GRID_LENGTH -80)
        y = random.uniform(-GRID_LENGTH +80, GRID_LENGTH -80)
        if dist2d(x, y, player_x, player_y) > 250:
            return x, y
 
def spawn_enemy():
    x, y = random_enemy_pos()
    enemies.append({"x": x, "y": y, "r": 30.0, "grow": 1})
 
def init_game():
    global player_x, player_y, gun_angle, game_over, lives, score,player_won
    global bullets_missed, hit_timer,cheat_fire_timer
    global bullets, enemies, cheat_mode, cheat_vision, first_person,angle_diff
    player_x, player_y = 0.0, 0.0
    gun_angle  = 0.0
    game_over  = False
    player_won=False
    lives      = MAX_LIVES
    score      = 0
    bullets_missed = 0
    hit_timer  = 0
    cheat_fire_timer = 0
    angle_diff=0.0
    bullets    = []
    enemies    = []
    cheat_mode = False
    cheat_vision = False
    first_person = False
    for _ in range(MAX_ENEMIES):
        spawn_enemy()
   


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text_color(x, y, text, r, g, b, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(r, g, b)  

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)


def draw_grid():
    cell = (2 * GRID_LENGTH) / GRID_LINES   #120
 
    glBegin(GL_LINES)
    for i in range(GRID_LINES + 1):
        coord = -GRID_LENGTH + i * cell
 
      #even darker
        col = 0.3 if i % 2 == 0 else 0.5
        glColor3f(col, col, col)
        glVertex3f(coord, -GRID_LENGTH, 0)#vertical
        glVertex3f(coord,  GRID_LENGTH, 0)
 
       
        glVertex3f(-GRID_LENGTH, coord, 0)
        glVertex3f( GRID_LENGTH, coord, 0)
    glEnd()
 
    
    glBegin(GL_QUADS)
    for row in range(GRID_LINES):
        for col in range(GRID_LINES):
            x0 = -GRID_LENGTH + col * cell
            y0 = -GRID_LENGTH + row * cell
            x1 = x0 + cell
            y1 = y0 + cell
            if (row + col) % 2 == 0:
                glColor3f(0.7, 0.5, 0.9)
            else:
                glColor3f(1, 1,1)
            glVertex3f(x0, y0, 0)
            glVertex3f(x1, y0, 0)
            glVertex3f(x1, y1, 0)
            glVertex3f(x0, y1, 0)
    glEnd()



def draw_walls():
    glColor3f(0.3, 0.5, 0.8)
    thick = 10
    GL = GRID_LENGTH
    WH = WALL_HEIGHT
 
    
    walls = [
       [( -GL, -GL, 0), ( GL, -GL, 0), ( GL, -GL, WH), (-GL, -GL, WH)],
        
        [( GL, -GL, 0), ( GL,  GL, 0), ( GL,  GL, WH), ( GL, -GL, WH)],
      
        [( -GL,  GL, 0), ( GL,  GL, 0), ( GL,  GL, WH), (-GL,  GL, WH)],
        
        [( -GL, -GL, 0), (-GL,  GL, 0), (-GL,  GL, WH), (-GL, -GL, WH)],
    ]
    colors = [
        (0.5, 0.8, 1.0),  
        (0.0, 0.0, 1.0), 
        (1.0, 1.0, 1.0), 
        (0.0, 1.0, 0.0),  
    ]
    
    glBegin(GL_QUADS)
    for i, w in enumerate(walls):
        glColor3f(*colors[i]) 
        for v in w:
            glVertex3f(*v)
    glEnd()

def draw_cube(tx, ty, tz, sx, sy, sz, r, g, b):
    """Draw a scaled, translated solid cube."""
    glColor3f(r, g, b)
    glPushMatrix()
    glTranslatef(tx, ty, tz)
    glScalef(sx, sy, sz)
    glutSolidCube(1.0)
    glPopMatrix()

def draw_player():
    global game_over
    if first_person:
        return
    
        
    glPushMatrix()
    glTranslatef(player_x, player_y, 0)
    glRotatef(-gun_angle, 0, 0, 1)
    if game_over:
        
        glRotatef(90, 1, 0, 0)
    q = gluNewQuadric()

   
           
    glColor3f(0.165, 0.322, 0.176)  
    draw_cube(0, 0, 60, 38, 20, 18, 0.165, 0.322, 0.176)  
    draw_cube(0, 0, 78, 40, 20, 18, 0.13, 0.27, 0.14) 
    draw_cube(0, 0, 85, 42, 22, 18, 0.165, 0.322, 0.176)   
    draw_cube(0, 0, 108, 14, 12, 10, 0.9, 0.75, 0.60)

       
    glColor3f(0.1, 0.3, 0.7)
    for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 12, 0, 0)
            gluCylinder(q, 8, 6, 50, 8, 4)
            glPopMatrix()
            
        
    glColor3f(0.165, 0.322, 0.176) 
    glPushMatrix()
    glTranslatef(0, 0, 70)
    glScalef(1.2, 0.6, 1.0)
    glutSolidCube(40)
    glPopMatrix()

        
    glColor3f(1.0, 0.93, 0.80)
    glPushMatrix()
    glTranslatef(-25,7,80) 
    glRotatef(-90, 1, 0, 0)   
    gluCylinder(q, 6,5,40, 8, 4)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(25,7,80)
    glRotatef(-90,1, 0,0)
    gluCylinder(q, 6, 5,40, 8, 4)
    glPopMatrix()

       
    glColor3f(0.55, 0.55, 0.55)
    glPushMatrix()
    glTranslatef(0,60,80)
    glRotatef(90,1,0, 0)    
    gluCylinder(q, 5,4,70, 8, 4)
    glPopMatrix()

       
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 110)
    gluSphere(q, 18, 12, 12)
    glPopMatrix()
    
    glPopMatrix()


def draw_player_fps():
    if not first_person:
        return
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(fovY, WINDOW_W / WINDOW_H, 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()   
    glDisable(GL_DEPTH_TEST)

    
    glColor3f(1.0, 0.93, 0.80)
    glPushMatrix()
    glTranslatef(-0.18, -0.35, -1.0)
    #glRotatef(-30, 0, 0, 1)   
    glRotatef(90, 1, 0, 0)   
    gluCylinder(gluNewQuadric(), 0.08, 0.08, 0.5, 9, 5)
    glPopMatrix()

    
    glPushMatrix()
    glTranslatef(0.18, -0.35, -1.0)
    #glRotatef(30, 0, 0, 1)  
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 0.08, 0.08, 0.5,9, 4)
    glPopMatrix()

     
    glColor3f(0.55, 0.55, 0.55)
    glPushMatrix()
    glTranslatef(0.0, -0.25, -1.0)
    glRotatef(90, 1, 0, 0)   
    gluCylinder(gluNewQuadric(), 0.06, 0.080, 0.8, 8, 4)
    glPopMatrix()

    glEnable(GL_DEPTH_TEST)

    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_enemy(e):
    glPushMatrix()
    glTranslatef(e["x"], e["y"], 0) 
    r = e["r"]
 
    
    glColor3f(0.60, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(0, 0, r)
    gluSphere(gluNewQuadric(), r, 12, 12)
    glPopMatrix()
 
   
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, r * 2 + r * 0.5)
    gluSphere(gluNewQuadric(), r * 0.5, 10, 10)
    glPopMatrix()
 
    glPopMatrix()



def draw_bullet(b):
    glPushMatrix()
    glTranslatef(b[0], b[1],88)
    glColor3f(1.0, 1.0, 0.0)
    glutSolidCube(BULLET_SIZE)
    glPopMatrix()
 



def fire_bullet(angle_deg=None):
    if game_over:
        return
    a = angle_deg if angle_deg is not None else gun_angle
    rad = math.radians(a)

    dx = math.sin(rad) * BULLET_SPEED
    dy = math.cos(rad) * BULLET_SPEED

    forward_x = math.sin(rad)
    forward_y = math.cos(rad)

    gun_tip_x = player_x + forward_x * 60
    gun_tip_y = player_y + forward_y * 60

    bullets.append([gun_tip_x, gun_tip_y, dx, dy, True])

    #print(f"[FIRE] angle={a:.2f} | pos=({gun_tip_x:.1f},{gun_tip_y:.1f})")



def setupCamera():
    global cam_angle
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    fov = 120 if (cheat_mode and first_person and cheat_vision) else fovY
    gluPerspective(fov, WINDOW_W / WINDOW_H, 1.0, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
 
    if first_person:
        rad = math.radians(gun_angle)        
        ex = player_x 
        ey = player_y
        ez =100        
        fx = ex + math.sin(rad) * 300
        fy = ey + math.cos(rad) * 300
        fz = ez
        gluLookAt(
                ex, ey, ez,
                fx, fy, fz,
                0, 0, 1
        )
        

    else:
        
        rad = math.radians(cam_angle)
        cx = player_x + math.sin(rad) * cam_radius
        cy = player_y - math.cos(rad) * cam_radius
        cz = cam_elev
        gluLookAt(cx,       cy,       cz,
                  player_x, player_y, 0,
                  0,        0,        1)
 



def update():
    global bullets_missed, lives, game_over, score,hit_timer, cheat_fire_timer
    global cheat_mode, gun_angle,angle_diff, WIN_SCORE,player_won,cam_angle
 
    if game_over:
        return
    if hit_timer>0:
        hit_timer -= 1
    if cheat_fire_timer > 0:  
        cheat_fire_timer -= 1

    
    for e in enemies:
        e["r"] += 0.3 * e["grow"]
        if e["r"] > 38 or e["r"] < 22:
            e["grow"] *= -1
 
    
    for e in enemies:
        dx = player_x - e["x"]
        dy = player_y - e["y"]
        d  = math.hypot(dx, dy)
        if d > 0:
            e["x"] += (dx / d) * ENEMY_SPEED
            e["y"] += (dy / d) * ENEMY_SPEED
 
   
    for e in enemies:
        if dist2d(e["x"], e["y"], player_x, player_y) < e["r"] + 30 and hit_timer == 0:
            lives -= 1
            print(f"[PLAYER HIT] Lives left={lives}")
            hit_timer = 60  # 1 second invincibility
            e["x"], e["y"] = random_enemy_pos()
            if lives <= 0:
                game_over = True
                enemies.clear()
                bullets.clear()
                print("[GAME OVER]")
                return
 
    
    for b in bullets:
        if b[4]:
            b[0] += b[2]
            b[1] += b[3]
 
    
    for b in bullets:
        if b[4] and (abs(b[0]) > GRID_LENGTH or abs(b[1]) > GRID_LENGTH):
            b[4] = False
            bullets_missed += 1
            print(f"[MISS] Missed={bullets_missed}")
            if bullets_missed >= MISS_LIMIT:
                game_over = True
                enemies.clear()
                bullets.clear()
                print("[GAME OVER]")
                return
 
    
    for b in bullets:
        if not b[4]:
            continue
        for e in enemies:
            if dist2d(b[0], b[1], e["x"], e["y"]) < e["r"] + BULLET_SIZE:
                b[4] = False
                score += 1
                
                if score >= WIN_SCORE:
                    game_over = True
                    player_won = True
                    enemies.clear()
                    bullets.clear()
                    return
                e["x"], e["y"] = random_enemy_pos()
                break
 
 
    if cheat_mode:
        gun_angle = (gun_angle + CHEAT_ROTATE_SPEED) % 360
        if first_person and cheat_vision:
            cam_angle = gun_angle 
        
         
        enemy_in_sight = False
        for e in enemies:
            dx = e["x"] - player_x
            dy = e["y"] - player_y
            
            enemy_angle = math.degrees(math.atan2(dx, dy)) % 360
            
            diff = (enemy_angle - gun_angle + 180) % 360 - 180
            if abs(diff) < CHEAT_AIM_TOL:
                enemy_in_sight = True
                break

        
        if enemy_in_sight and cheat_fire_timer <= 0:
            fire_bullet()
            cheat_fire_timer = CHEAT_FIRE_DELAY



def keyboardListener(key, x, y):
    global player_x, player_y, gun_angle, game_over
    global cheat_mode, cheat_vision, first_person, lives, score, bullets_missed
    global bullets, enemies,cheat_fire_timer
    
    if key == b'r':
        init_game()
        return
    if game_over:
        return
    
    rad = math.radians(gun_angle)
    
    if key == b'w':
        nx = player_x + math.sin(rad) * PLAYER_SPEED
        ny = player_y + math.cos(rad) * PLAYER_SPEED
        player_x = clamp(nx, -GRID_LENGTH + 30, GRID_LENGTH - 30)
        player_y = clamp(ny, -GRID_LENGTH + 30, GRID_LENGTH - 30)
    if key == b's':
        nx = player_x - math.sin(rad) * PLAYER_SPEED
        ny = player_y - math.cos(rad) * PLAYER_SPEED
        player_x = clamp(nx, -GRID_LENGTH + 30, GRID_LENGTH - 30)
        player_y = clamp(ny, -GRID_LENGTH + 30, GRID_LENGTH - 30)
    
    if not cheat_mode:
      if key == b'a':
           gun_angle = (gun_angle - TURN_SPEED) % 360
   
      if key == b'd':
           gun_angle = (gun_angle + TURN_SPEED) % 360

    
    if key == b'c':
        cheat_mode = not cheat_mode
        if not cheat_mode:
            first_person=False
            cheat_vision=False
            cheat_fire_timer=0

    if key == b'v':
      if cheat_mode and first_person:
         cheat_vision = not cheat_vision
 
    glutPostRedisplay()
 



def specialKeyListener(key, x, y):
    global cam_angle, cam_elev
 
    if key == GLUT_KEY_UP:
        cam_elev = clamp(cam_elev + 20, 100, 1200)
 
    if key == GLUT_KEY_DOWN:
        cam_elev = clamp(cam_elev - 20, 100, 1200)
 
    if key == GLUT_KEY_LEFT:
        cam_angle = (cam_angle - 3) % 360
 
    if key == GLUT_KEY_RIGHT:
        cam_angle = (cam_angle + 3) % 360
 
    glutPostRedisplay()
 

def mouseListener(button, state, x, y):
    global first_person
   
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
       if not cheat_mode:
           fire_bullet()   
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person
 
    glutPostRedisplay()


def idle():
    update()
    glutPostRedisplay()
 



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_W, WINDOW_H) 
    setupCamera()
 
    draw_grid()
    draw_walls()
    draw_player() 
    draw_player_fps()

    for e in enemies:
        draw_enemy(e)
 
   
    for b in bullets:
        if b[4]:
            draw_bullet(b)
 
   
    if game_over:
        
        if player_won:            
            draw_text_color(400, 440, "WINNER!!!", 0.0, 1.0, 0.0, GLUT_BITMAP_TIMES_ROMAN_24)
        else:           
            draw_text_color(400, 440, "GAME OVER", 1.0, 0.0, 0.0, GLUT_BITMAP_TIMES_ROMAN_24)
 
        draw_text_color(10,770, f"Game is Over. Your score is {score}", 1.0, 1.0, 1.0, GLUT_BITMAP_HELVETICA_18)
        draw_text_color(10,740, "Press R to RESTART the Game", 1.0, 1.0, 0.0, GLUT_BITMAP_HELVETICA_18)
    else:
       
        draw_text(10, 770, f"Player Life Remaining: {lives}   Score: {score}   Bullet Missed: {bullets_missed}/{MISS_LIMIT}")
        if cheat_mode:
            draw_text(10, 740, "CHEAT ON")
        cam_str = "FIRST PERSON" if first_person else "THIRD PERSON"
        draw_text(10, 710, f"Camera: {cam_str}")
        if cheat_mode and first_person and cheat_vision:
            draw_text(10, 680, "CHEAT VISION ON")
            
 
    glutSwapBuffers()
 



def main():
    init_game()
 
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy")
 
    glEnable(GL_DEPTH_TEST)
 
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
 
    glutMainLoop()
 
if __name__ == "__main__":
    main()
 