import pygame, random, sys, math, time
score1=score2=0

def init_variables():
    #Initiliase stuff
    global leftpos, rightpos, blist, Buildexplosion, tankexplosion, result
    global orange, yellow, black, purple, white, green, red, aqua, brightred
    global redd, brightgreen, greenn, brightblue, blue, brightyellow, darkgray
    global EXPLOSION_COLOR, colour, usertext

    global screen_width, screen_height, no_buildings, building_width
    global player_width, player_height, input_width, input_height
    global input_offset, g, exp, bg, win

    leftpos=[]
    rightpos=[]
    blist=[]
    Buildexplosion=int(700/ 50)
    tankexplosion = 30
    result=0
    #sounds
    '''
    pygame.mixer.init()
    exp=pygame.mixer.Sound('Cannon+1.wav')
    bg=pygame.mixer.Sound('bgsd.wav')
    win=pygame.mixer.Sound('win.wav')
    '''
    # Initialing Color
    orange=(255,69,0)
    yellow=(155,155,0)
    black = (0,0,0)
    purple=(138,43,226)
    white = (255,255,255)
    green = (0,255,0)
    red = (255,0,0)
    aqua=(0,255,255)
    brightred = (255,0,0)
    redd =(155,0,0)
    brightgreen = (0,255,0)
    greenn = (0,155,0)
    brightblue=(0,0,255)
    blue=(0,0,155)
    brightyellow = (255,255,0)
    darkgray=(40,40,40)
    EXPLOSION_COLOR = (255, 0, 0)
    slate=(106,90,205)
    chocolate=(210,105,30)
    grey=(169,169,169)
    orred=(255,80,0)
    ight=(176,196,222)
    drab=	(107,142,35)
    firebrick=(178,34,34)
    colour=[grey,slate,blue,brightgreen,drab,brightblue,orred,brightyellow,firebrick,purple,aqua]
    usertext=''

    screen_width=1200
    screen_height=700
    no_buildings=10
    building_width=screen_width/no_buildings
    player_width = 35
    player_height = 50
    input_width = 60
    input_height = 32
    input_offset = 40
    # Acceleration due to gravity (assume we are on earth)
    g = 9.8

# Drawing Rectangle
def drect( x ,y ,b  ,l, c=(255,255,255), width=0):
    global screen

    rect = pygame.draw.rect(screen, c, pygame.Rect(x,y,b,l), width)
    pygame.display.flip()
    return rect

#Cannonball
CANNON_ASCII = """
           
            XXXXX
           XXXXXXX
          XXXXXXXXX
         XXXXXXXXXXX
          XXXXXXXXX
           XXXXXXX
            XXXXX
             
        """

def makeSurfaceFromASCII(ascii, fgColor=(255,255,255), bgColor=(0,0,0)):
    ascii = ascii.split('\n')[1:-1]
    width = max([len(x) for x in ascii])
    height = len(ascii)
    surf = pygame.Surface((width, height))
    surf.fill(bgColor)

    pArr = pygame.PixelArray(surf)
    for y in range(height):
        for x in range(len(ascii[y])):
            if ascii[y][x] == 'X':
                pArr[x][y] = fgColor
    return surf

def getcannonRect(x, y):
    global cannon_ball

    return pygame.Rect((x, y), cannon_ball.get_size())

def doExplosion(screen, x, y, explosionSize=int(700/50), speed=0.006):
    for r in range(1, explosionSize):
        pygame.draw.circle(screen, brightred, (x, y), r)
        pygame.draw.circle(screen, orange, (x, y), r)
        pygame.display.update()
        time.sleep(speed)
        #exp.play()
    for r in range(explosionSize, 1, -1):
        pygame.draw.circle(screen, black, (x, y), explosionSize)
        pygame.draw.circle(screen, black, (x, y), explosionSize)
        pygame.draw.circle(screen, brightred, (x, y), r)
        pygame.draw.circle(screen, brightred, (x, y), r)
        pygame.display.update()
        time.sleep(speed)
    pygame.draw.circle(screen, black, (x, y), 2)
    pygame.draw.circle(screen, black, (x, y), 2)
    pygame.display.update()
#font and stuff

def game_init():
    global screen, cannon_ball, black, basefont,clock

    init_variables()
    pygame.init()
    screen=pygame.display.set_mode((1200,700))
    clock = pygame.time.Clock()
    screen.fill(black)
    pygame.font.init()
    basefont=pygame.font.Font(None,32)
    clock.tick(30)

    #cannon ball
    cannon_ball = makeSurfaceFromASCII(CANNON_ASCII)

def draw_scores():
    global screen, basefont, yellow, score1, score2

    # TODO: Blank the rectangle first
    p1display=basefont.render("Player 1 Score: "+str(score1),True, yellow)
    p2display=basefont.render("Player 2 Score: "+str(score2),True, yellow)
    screen.blit(p1display,(0,0))
    screen.blit(p2display,(1000,0))
    pygame.display.flip()

def draw_buildings():
    global no_buildings, leftpos, rightpos, screen_height, screen_width

    for i in range(0,no_buildings):
        # generate building height
        r=random.randint(100,350)
        #the_new_rect=pygame.draw.rect(screen,colors[i],(120*i,700-r,120,r))
        the_new_rect=drect(building_width*i,screen_height-r,building_width,r,colour[i])
        blist.append(the_new_rect)
        if i==0 or i==1 or i ==2:
            leftpos=leftpos+[screen_height-r]
        if i==7 or i==8 or i==9:
            rightpos=rightpos+[screen_height-r]

def draw_players():
    global player1, player2, xa, ya, xb, yb, leftpos, rightpos, aqua, white

    # Player 2 will be on top of building 7 to 10 at random
    rt=random.randrange(7,10)
    # Player 1 will be on top of building 0 to 3 at random
    l=random.randrange(0,3)

    #calculate dimensions for bounding boxes of players
    xa=l*building_width+player_width
    ya=int(leftpos[l])-player_height
    xb=rt*building_width+player_width
    yb=int(rightpos[rt-7])-player_height

    # draw the players
    player1=drect(xa,ya,50,50,aqua)
    player2=drect(xb,yb,50,50,white)
    blist.append(player1)
    blist.append(player2)
#    pygame.display.flip()

# Read the angle and velocity from the user
def get_input(player_num):
    global screen_width, input_offset, input_height, basefont, screen, aqua, black

    #Hack offset for player 2
    magic_offset = screen_width - 100

    #print("Before event loop")

    for i in range(2):
        inputrect=drect(player_num * magic_offset,input_offset * (i+1),input_width,input_height,aqua,3)
        screen.fill(black,inputrect)
    for i in range(2):
        user_input = ''
        inputrect=drect(player_num * magic_offset,input_offset * (i+1),input_width,input_height,aqua,3)
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    done = True
                    if i==0:
                        a=int(user_input)
                    if i==1:
                        u=int(user_input)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        screen.fill(black,inputrect)
                        pygame.draw.rect(screen,aqua,inputrect,3)
                        user_input = ''
                    else:
                        user_input += chr(event.key)
            # Create text surface.
            txtInput=basefont.render(user_input, True, aqua)
            # And blit it onto the screen.
            screen.blit(txtInput, (inputrect.x+5 , inputrect.y+5))
            #pygame.display.flip()
            pygame.display.update()

    #Return angle in radians and the initial velocity
    print("Angle =",a, "Velocity =",u)
    return (a*math.pi/180,u)

def detect_collision(x,y):
    global player1, player2, screen, score1, score2

    crect=getcannonRect(x,y)
    if crect.colliderect(player1):
        doExplosion(screen,x+20,y+10,tankexplosion)
        print("Collision1")
        score2+=1
        return True
    elif crect.colliderect(player2):
        doExplosion(screen,x+20,y+10,tankexplosion)
        print("Collision2")
        score1+=1
        return True
    else:
        for eachbuilding in blist:
            if crect.colliderect(eachbuilding):
                doExplosion(screen,x+20,y+10)
                print("Collision")
                return True
    return False

def projectile_motion(player_no,a,u):
    global screen, cannon_ball

    projectile_moving=True
    offset = 20

    if (player_no == 0):
        x = x1 = xa + offset
        y = y1 = ya - offset
        sign = 1
    else:
        x = x1 = xb + offset
        y = y1 = yb - offset
        sign = -1

    # Time
    t = 0
    while (projectile_moving == True):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                quit()

        # draw the projectile
        screen.blit(cannon_ball,(x,y))
        pygame.display.update()
        #sleep
        time.sleep(0.05)
        #erase by putting back the original background. Hack to be black for now
        crect=getcannonRect(x,y)
        screen.fill(black,crect)
        #update time
        t+=0.1

        # Move it
        x=x1+sign*(u*math.cos(a)*t)*1.50
        y=y1-u*math.sin(a)*t + 0.5 * g * t * t

        projectile_moving = not(detect_collision(x,y))

        # This is just a boundary check; should never hit this
        if(x>screen_width or x<0):
            projectile_moving=False

def play_a_round():
    global score1, score2

    current_score1 = score1
    current_score2 = score2
    player = 0

    while (current_score1 == score1 and current_score2 == score2):
        (a,u) = get_input(player)
        projectile_motion(player, a, u)
        player = (player + 1) % 2#flip player number

def play_many_rounds(no_rounds):
    global screen, black, score1, score2

    score1=score2=0
    for i in range(no_rounds):
        play_a_round()
        screen.fill(black)
        pygame.display.update()
        init_variables()
        draw_scores()
        draw_buildings()
        draw_players()


def start_screen():
    global redd, aqua, yellow, purple, white, green, screen, colour
    screen.fill(black)

    no_rounds=1
    #bg.play(-1)


    usertext=''
    he="The Bomber Blocks"
    s1='Prathyusha:  Hello there ! This game is based on a popular 90s game "gorilla.bas"'
    s2="             but we made it interesting, with no banana bombs and no gorillas :)"
    s3="Dyuthi:      There are two blocks== two players, and they throw bombs (put on your physics caps!) "
    s4="             at one another, the aim is to destroy your opponent, you can "
    s5="             choose the number of rounds,you must first enter the angle of projection "
    s6="             of the bomb and then its velocity, keep note of gravity and the city skyline!"

    r="Enter number of rounds:"

    textsurfaceh=basefont.render(he,True, yellow)
    textsurface1=basefont.render(s1,True,redd)
    textsurface2=basefont.render(s2,True,redd)
    textsurface3=basefont.render(s3,True,purple)
    textsurface4=basefont.render(s4,True,purple)
    textsurface5=basefont.render(s5,True,purple)
    textsurface6=basefont.render(s6,True,purple)
    textsurface9=basefont.render(r,True,green)

    screen.blit(textsurfaceh,(80,80))
    screen.blit(textsurface1,(80,120))
    screen.blit(textsurface2,(80,160))
    screen.blit(textsurface3,(80,200))
    screen.blit(textsurface4,(80,240))
    screen.blit(textsurface5,(80,280))
    screen.blit(textsurface6,(80,320))
    screen.blit(textsurface9,(80,400))

    inputrect=pygame.Rect(500,400,30,32)

    done = False
    while not(done):
        i=0
        while i<10:
            pygame.draw.rect(screen,colour[i],(0,0,1200,700),50)
            i=i+1
            pygame.display.flip()
            clock.tick(8)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    screen.fill(black, inputrect)
                    usertext=usertext[:-1]
                elif event.key == pygame.K_RETURN:
                    done = True
                else:
                    usertext+=event.unicode
            pygame.draw.rect(screen,aqua,inputrect,3)
            text3=basefont.render(usertext,True,aqua)
            screen.blit(text3,(inputrect.x+5, inputrect.y+5))
            pygame.display.flip()


    screen.fill(black)
    pygame.display.flip()

    no_rounds=int(usertext)
    return no_rounds

def end_screen():
    global score1, score2
    #pygame.mixer.stop()
    #win.play()
    screen.fill(black)
    largefont=pygame.font.Font(None,200)
    text = largefont.render('Game Over!', True, brightyellow)
    text1 = largefont.render('Player1 Wins!', True, aqua)
    text12 = largefont.render('Score:'+str(score1), True, aqua)
    text2 = largefont.render('Player2 Wins!', True, white)
    text22 = largefont.render('Score: '+str(score2), True, white)
    text3 = largefont.render('Game Tied',True, aqua)


    screen.fill((0,0,0))
    screen.blit(text, (100,100))
    print("Game Over")
    if(score1 > score2):
        print("Player 1 wins")
        screen.blit(text1, (100,350))
        screen.blit(text12, (100,500))
    elif(score2 > score1):
        print("Player 2 wins")
        screen.blit(text2, (100,350))
        screen.blit(text22, (100,500))
    else:
        print("Tied")
        screen.blit(text3, (100,350))
    pygame.display.flip()
    clock.tick(0.1)
    return 0
#Game starts here:

game_init()
no_rounds=start_screen()
draw_scores()
draw_buildings()
draw_players()
play_many_rounds(no_rounds)
end_screen()
