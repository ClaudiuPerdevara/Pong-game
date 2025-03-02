import pygame, sys,random
from pygame.examples.go_over_there import screen

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock=pygame.time.Clock()

screen_width=1280
screen_height=960
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

ball = pygame.Rect(screen_width/2-15,screen_height/2-15,30,30)
player=pygame.Rect(screen_width-20,screen_height/2-70,10,140)
opponent=pygame.Rect(10,screen_height/2-70,10,140)

background_color=((92, 114, 133))
negru=(9, 18, 44)

ball_speed_x=4*random.choice((-1,1))
ball_speed_y=4*random.choice((-1,1))
player_speed=0
opponent_speed=7

player_score=0
opponent_score=0
game_font=pygame.font.Font("freesansbold.ttf",30)
game_font2=pygame.font.Font("freesansbold.ttf",60)
score_time=True

pong_sound=pygame.mixer.Sound("pong.mp3")
score_sound=pygame.mixer.Sound("score.mp3")

def ball_restart():
    global ball_speed_x
    global ball_speed_y
    global score_time
    current_time=pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)
    if current_time - score_time < 700:
        number_three=game_font2.render("3",False,negru)
        screen.blit(number_three,(screen_width/2-20,screen_height/2+20))
    if 700<current_time - score_time < 1400:
        number_two=game_font2.render("2",False,negru)
        screen.blit(number_two,(screen_width/2-20,screen_height/2+20))
    if 1400<current_time - score_time < 2100:
        number_one=game_font2.render("1",False,negru)
        screen.blit(number_one,(screen_width/2-20,screen_height/2+20))
    if current_time-score_time<2100:
        ball_speed_y=0
        ball_speed_x=0
    else:
        ball_speed_y = 4* random.choice((-1, 1))
        ball_speed_x = 4* random.choice((-1, 1))
        score_time=None

def ball_animation():
    global ball_speed_x
    global ball_speed_y
    global opponent_score
    global player_score
    global score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top<=0 or ball.bottom>=screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y*=-1

    if ball.left<=0:
        pygame.mixer.Sound.play(score_sound)
        player_score+=1
        score_time=pygame.time.get_ticks()

    if ball.right>=screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score+=1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x>0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right-player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom-player.top)<10 and ball_speed_y>10:
            ball_speed_y*=-1
        elif abs(ball.top-player.bottom)<10 and ball_speed_y<10:
            ball_speed_y*=-1
    if ball.colliderect(opponent) and ball_speed_x<0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                opponent_speed = 12
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_DOWN:
               player_speed+=7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_DOWN:
               player_speed-=7
            if event.key == pygame.K_UP:
                player_speed += 7
    ball_animation()
    player_animation()
    opponent_animation()

    screen.fill(background_color)
    pygame.draw.aaline(screen,negru,(screen_width/2,0),(screen_width/2,screen_height))

    pygame.draw.rect(screen,negru,player)
    pygame.draw.rect(screen,negru,opponent)
    pygame.draw.rect(screen,negru,ball)

    if score_time:
        ball_restart()

    player_text=game_font.render(f"{player_score}",False,(negru))
    screen.blit(player_text,(660,470))

    opponent_text=game_font.render(f"{opponent_score}",False,(negru))
    screen.blit(opponent_text,(600,470))

    pygame.display.flip()
    clock.tick(120)
