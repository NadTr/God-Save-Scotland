# game data

from random import randint, choice
import pgzrun


WIDTH = 800
HEIGHT = 600

# GROUND = 458 #--- original
GROUND = 466
GRAVITY = 350

NUMBER_OF_BACKGROUND = 2
GAME_SPEED = 160
game_speed = GAME_SPEED
JUMP_SPEED = 280

LIFES_NUMBER = 3

game_status = "Titre"

# hero initialisation

hero = Actor("hero", anchor=('middle', 'bottom'))
hero.pos = (64, GROUND +100)
# hero_speed = 0
jump_hero = 0
hero_vx = 0 
hero_vy = 0
hero_lifes = []
for x in range(10, LIFES_NUMBER * 19, 18):
    # life = Actor("life", anchor=["left", "top"])
    # life.pos = [x, HEIGHT - 22]
    life = Actor("whiskey", anchor=["left", "bottom"])
    life.pos = [x, 40]
    hero_lifes.append(life)

# enemies initialisations
OBS_IMG = {"rosebush_biggest" : 25, 
            "rosebush_bigger" : 20,
            "rosebush_big": 18, 
            "rosebush_middle" : 15, 
            "rosebush_little" : 10
        }

OBSTACLES_APPARTION = (2, 5)
next_obstacle_time = randint(OBSTACLES_APPARTION[0], OBSTACLES_APPARTION[1])
obstacles = []
obstacles_timeout = 0
obstacles_timeout_max = 2


ennemy = Actor("ennemy", anchor=('middle', 'top'))
ennemy.pos = WIDTH + 100, randint(GROUND - hero.height, GROUND- 50)
ennemy_speed_x = 160
ennemy_speed_y = 60

ennemy_alive = True


# background inititalisation

lochness_corps= Actor("bosse", anchor=["left", "bottom"])
lochness_corps_x = 0
lochness_corps_y = HEIGHT
lochness_corps.pos = (lochness_corps_x,lochness_corps_y)
lochness_corps_speed = -50
lochness_tete= Actor("tete", anchor=["left", "center"])
lochness_tete_x = 0
lochness_tete_y = 999
lochness_tete.pos = (lochness_tete_x,lochness_tete_y)
lochness_tete_speed = -100

backgrounds_bottom = []
backgrounds_top = []

for n in range(NUMBER_OF_BACKGROUND):
    bg_b = Actor("bg_1", anchor=('left', 'top'))
    bg_b.pos = n * WIDTH, 0
    backgrounds_bottom.append(bg_b)

    bg_t = Actor("bg_2", anchor=('left', 'top'))
    bg_t.pos = n * WIDTH, 0
    backgrounds_top.append(bg_t)

    # backgrounds_top.append(lochness_corps)
    # backgrounds_top.append(lochness_tete)



def draw():
    if game_status =="Game":
        screen.clear()

        for bg in backgrounds_top:
            bg.draw()

        lochness_tete.draw()
        lochness_corps.draw()

        for bg in backgrounds_bottom:
            bg.draw()

        for obstacle in obstacles:
            obstacle.draw()

        for life in hero_lifes:
            life.draw()
        if ennemy_alive :
            ennemy.draw()

        hero.draw()
        screen.draw.text("Appuyer sur ENTER pour mettre en PAUSE", (WIDTH/2 + 42, HEIGHT - 22), fontsize=25) # à rajouter
    
    #affichage ecran pause et game over    
    elif game_status == "Pause":
        screen.clear()
        ecran_pause =Actor("pause",anchor=('center','center'))
        ecran_pause.pos=(WIDTH/2,HEIGHT/2)
        ecran_pause.draw()

    elif game_status =="GameOver":
        screen.clear() #à rajouter
        ecran_game_over =Actor("game_over",anchor=('center','center'))
        ecran_game_over.pos=(WIDTH/2,HEIGHT/2)
        ecran_game_over.draw()

    elif game_status =="Titre":
        screen.clear() #à rajouter
        ecran_titre =Actor("titre",anchor=('center','center'))
        ecran_titre.pos=(WIDTH/2,HEIGHT/2)
        ecran_titre.draw()

def update(dt):
    global game_status
    global game_speed
    global obstacles_timeout
    global obstacles_timeout_max
    global next_obstacle_time
    global ennemy_alive
    global ennemy_speed_x
    global ennemy_speed_y
    global hero_vx
    global hero_vy
    global jump_hero
    global lochness_corps_y
    global lochness_corps_x
    global lochness_corps_speed
    global lochness_tete_y
    global lochness_tete_x
    global lochness_tete_speed

    screen.clear()
    draw()

    if game_status == "Game":

        # game_speed *= 1.05 * dt
        game_speed *= 1.0000005 
        #mouvement objet background
        if (lochness_corps_y < GROUND+105 or lochness_corps_y > 1000) :
            lochness_corps_speed *= -1
        lochness_corps_y += lochness_corps_speed*dt
        lochness_corps.pos = (lochness_corps_x,lochness_corps_y)
        if (lochness_tete_y < GROUND -70 or lochness_tete_y > 1000) :
            lochness_tete_speed *= -1
        lochness_tete_y += lochness_tete_speed*dt
        lochness_tete.pos = (lochness_tete_x,lochness_tete_y)

        # enemies update
        # obstacle

        next_obstacle_time -= dt
        obstacles_timeout += dt

        if next_obstacle_time <= 0:
            # obstacle = Actor("rosebush_big", anchor=('left', 'bottom'))
            rose_size = choice(list(OBS_IMG.items()))
            obstacle = Actor(rose_size[0], anchor=('left', 'bottom'))
            obstacle.pos = WIDTH, GROUND + rose_size[1]
            obstacles.append(obstacle)
            next_obstacle_time = randint(OBSTACLES_APPARTION[0], OBSTACLES_APPARTION[1])

        for obstacle in obstacles:
            x, y = obstacle.pos
            x -= game_speed * dt
            obstacle.pos = x, y
            # if obstacle.colliderect(hero) :
            if obstacle.colliderect(hero) and (hero.x  + 1/2 * hero.width >= obstacle.x + 1/5 *obstacle.width or hero.x - 1/2 * hero.width <= obstacle.x + 4/5 * obstacle.width ):
                if len(hero_lifes) >= 1 and obstacles_timeout >= obstacles_timeout_max:
                    hero_lifes.pop()
                    sounds.hurt.play()

                    obstacles_timeout = 0
                    screen.clear()
                    game_play = False
                elif obstacles_timeout < obstacles_timeout_max:
                    pass
                else:
                    game_status = "GameOver"

        if obstacles:
            if obstacles[0].pos[0] <= - 32:
                obstacles.pop(0)

        # ennemy update + collision 
 
        en_x, en_y = ennemy.pos
        en_x -= ennemy_speed_x * dt
        if en_y > GROUND - 50 or en_y < GROUND - hero.height:
            ennemy_speed_y *= -1     
        en_y += ennemy_speed_y * dt
        ennemy.pos = en_x, en_y
        

        if ennemy.x < -50:
           ennemy.pos = WIDTH + randint(50, 150), randint(GROUND - hero.height, GROUND -50 )
        
        if hero.colliderect(ennemy) and ennemy_alive:
            if hero_vy > 0 and hero.y + hero.height >= ennemy.y + 1:
                ennemy_alive = False
                # hero.y -= 20
                hero_vy *= -1
                sounds.boing.play()

            
            elif obstacles_timeout >= obstacles_timeout_max:
                if len(hero_lifes) > 0:
                    hero_lifes.pop()
                    obstacles_timeout = 0
                else:
                    game_play = False
        
        if not ennemy_alive :
            new_y = randint(GROUND - hero.height, GROUND - 50)
            ennemy.pos = WIDTH + randint(50, 150), new_y
            ennemy_alive = True

        # hero update

        # global hero_speed

        # hero_speed -= GRAVITY * dt
        # x, y = hero.pos
        # y -= hero_speed * dt

        # if y > GROUND:
        #     y = GROUND
        #     hero_speed = 0

        # hero.pos = x, y
        hero_vy += GRAVITY * dt

        x, y = hero.pos
        x += hero_vx * dt
        y += hero_vy * dt

        if y > GROUND:
            y = GROUND
            hero_vy = 0
            jump_hero = 0


        hero.pos = x, y
        

        # bg update

        for bg in backgrounds_bottom:
            x, y = bg.pos
            x -= game_speed * dt
            bg.pos = x, y

        # + 10 pour retirer la ligne noire de transition
        if backgrounds_bottom[0].pos[0] <= - WIDTH + 10:
            bg = backgrounds_bottom.pop(0)
            bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
            backgrounds_bottom.append(bg)

        for bg in backgrounds_top:
            x, y = bg.pos
            x -= game_speed/3 * dt
            bg.pos = x, y

        if backgrounds_top[0].pos[0] <= - WIDTH:
            bg = backgrounds_top.pop(0)
            bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
            backgrounds_top.append(bg)
        
    #elif game_status == "Pause":
        #screen.clear()
        #screen.draw.text("PAUSE", (225, 300), fontsize=100)

    #elif game_status == "GameOver":
        #screen.clear() #à rajouter
        #screen.draw.text("GAME OVER", (225, 300), fontsize=100)        


def on_key_down(key):
    global hero_vy
    global game_status
    global obstacles
    global jump_hero
    global game_speed


    # jump
    # if key == key.SPACE:

    #     if hero_speed == 0:
    #         hero_speed = JUMP_SPEED
    # if key == keys.SPACE and hero_vy == 0 :
    #     hero_vy = -JUMP_SPEED
    if key == keys.SPACE:
        # if hero_vy >= 0 and jump_hero <= 1:
        if jump_hero < 1:
            hero_vy = -JUMP_SPEED
            jump_hero += 1
        elif jump_hero == 1:
            hero_vy = -0.8*JUMP_SPEED
            jump_hero += 1
        
        # if hero_vy > 0 and hero.y + hero.height >= HEIGHT/2 - 10:
        #     jump_hero -= 1
        

    #changement de status pause - jeu - relancer
    elif key == 13:
        if game_status =="Game": #a rajouter
            game_status = "Pause"
        elif game_status == "Pause":
            game_status = "Game"

        elif game_status == "Titre":
            game_status = "Game"

        elif game_status =="GameOver":
            for x in range(10, LIFES_NUMBER * 19, 18):
                life = Actor("life", anchor=["left", "top"])
                life.pos = [x, HEIGHT - 22]
                hero_lifes.append(life)
                game_speed = GAME_SPEED
            obstacles = []
            game_status = "Game"


pgzrun.go()