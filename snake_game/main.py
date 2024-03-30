import pygame
from random import randint,choice
import supabase
from base64 import b64encode,b64decode
import webbrowser
from json import dumps
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]

        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')

        self.is_vulnerable = True
        self.flashing_list = [True,False]
        self.flashing_index = 0
        self.vulnerable_timer = 0
        self.draw_flashing = True

        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= ground_rect.top or pygame.mouse.get_pressed()[0] and self.rect.bottom >= ground_rect.top:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > ground_rect.top: self.rect.bottom = ground_rect.top
    
    def player_animaiton(self):
        if self.rect.bottom < ground_rect.top:
            self.image = self.player_jump    
        else:
            self.player_index += 0.05
            if self.player_index >= len(self.player_walk) - 1: self.player_index = 0
            self.image = self.player_walk[round(self.player_index)]
    
    def flashing(self):
        flashing = False
        if score >= self.vulnerable_timer:
            self.is_vulnerable = True

        if not self.is_vulnerable:
            self.flashing_index += 0.1
            if self.flashing_index >= len(self.flashing_list) - 1: self.flashing_index = 0
            if self.flashing_list[round(self.flashing_index)]: flashing = True
        else: flashing = True
        self.draw_flashing = flashing  

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animaiton()
        self.flashing()

class Obstcales(pygame.sprite.Sprite):
    def __init__(self,type,speeds):
        super().__init__()
        if type == 'snail':
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos = ground_rect.top
        else:
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = ground_rect.top - 150
        self.speeds = speeds
        self.type = type
        self.animaiton_index = 0
        self.image = self.frames[self.animaiton_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100),y_pos))

    def obstcale_animaiton(self):
        if self.type == 'snail':
            self.animaiton_index += 0.035
        else:
            self.animaiton_index += 0.1
        if self.animaiton_index >= len(self.frames) - 1: self.animaiton_index = 0
        self.image = self.frames[round(self.animaiton_index)]

    def obstcale_movement(self):
        self.rect.x -= self.speeds
        if self.rect.right <= -50: self.kill()

    def update(self):
        self.obstcale_animaiton()
        self.obstcale_movement()

class Button(pygame.sprite.Sprite):
    def __init__(self,surf,x,y):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(center=(x,y))
        self.clicked = False
        self.aciton = False

    def apply_clickabilty(self):
        aciton = False 
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()) and self.clicked == False:
            self.clicked = True
            aciton = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        
        self.aciton = aciton
            
    def update(self):
        self.apply_clickabilty()

class Heart(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        heart = pygame.image.load('graphics/heart/heart.png').convert_alpha()
        empty_heart = pygame.image.load('graphics/heart/empty_heart.png').convert_alpha()
        self.hearts = [heart,empty_heart]
        self.is_empty = 0
        self.image = self.hearts[self.is_empty]
        self.image = pygame.transform.rotozoom(self.image,0,0.1)
        self.rect = self.image.get_rect(midtop=(440,10))

    def empting(self):
       self.image = self.hearts[self.is_empty]
       self.image = pygame.transform.rotozoom(self.image,0,0.1)
    def update(self):
        self.empting()

class PlusHeart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/heart/plus_heart.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,0.1)
        self.rect = self.image.get_rect(center=(randint(900,1100),randint(25,ground_rect.top)))

    def heart_movement(self):
        self.rect.x -= 5
        if self.rect.right <= -50: self.kill()

    def update(self):
        self.heart_movement()

class Label(pygame.sprite.Sprite):
    def __init__(self,surf,x,y):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(center=(x,y))

class InputBox(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, text=''):
        super().__init__()
        self.color = (0,0,0)
        self.entered = False
        self.text = text
        self.image = my_font.render(text, True, self.color)
        self.rect = self.image.get_rect(center=(x,y))
        self.rect.width = w
        self.rect.height = h

        self.active = False

    def handle_event(self, event):
        if not self.entered:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                    self.text = ''
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = (0,0,0) if self.active else (0,0,0)
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.entered = True
                        upsert(self.text,highscore)

                        
                
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.image = my_font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.image.get_width()+10)
        self.rect.w = width

class CheckBox(pygame.sprite.Sprite):
    def __init__(self,type,button=0):
        super().__init__()
        if type:
            self.image = pygame.image.load('graphics/checkbox/checked.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,0.12)
            self.rect = self.image.get_rect(midright=(button.left - 20, button.centery - 8))
        else:
            self.image = pygame.image.load('graphics/checkbox/unchecked.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,0.05)
            self.rect = self.image.get_rect(midright=(button.left - 20, button.centery - 6))
        
        
        self.timer = clock.get_time() / 250
        self.checkbox_timer = 0

    def call_timer(self):
        self.checkbox_timer = self.timer + 3

    def change_symbol(self,type,button):
        if type:
            self.image = pygame.image.load('graphics/checkbox/checked.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,0.12)
            self.rect = self.image.get_rect(midright=(button.rect.left - 20, button.rect.centery - 8))
        else:
            self.image = pygame.image.load('graphics/checkbox/unchecked.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,0.05)
            self.rect = self.image.get_rect(midright=(button.rect.left - 20, button.rect.centery - 6))

    def update(self):
        self.timer = pygame.time.get_ticks() / 250
        

def sprite_collisons(group):
    if pygame.sprite.spritecollide(player.sprite,group,False):
        return True
    return False

def heart_cal(group):
    if group == obstcale_group:
        if player.sprite.is_vulnerable and sprite_collisons(obstcale_group) == True:
            for i in range(len(health_bar)):
                heart = health_bar[i]
                if heart.is_empty == 0:
                    heart.is_empty = 1
                    player.sprite.is_vulnerable = False
                    player.sprite.vulnerable_timer = score + 10
                    return False
            obstcale_group.empty()
            losing_sound.play()
            return True
        return False
    else:
        if sprite_collisons(plus_heart_group):
            for i in range(len(health_bar)):
                heart = health_bar[i]
                if not heart.is_empty:
                    health_bar[i-1].is_empty = 0
                    plus_heart_group.sprite.kill()
                    power_up_sound.play()
                    return
            health_bar[i].is_empty = 0
            plus_heart_group.sprite.kill()
            power_up_sound.play()    


def top_5():
    try:
        global supabase

        data = supabase.rpc('top_5',dumps({'arg1':None,'arg2':None})).execute()
        return list(data)[0][1]
    except:
        return False                  

def upsert(inpname,highscore):
    try:
        global supabase

        account = {'name':inpname ,'highscore': highscore}
        db_account = top_5()[-1]
        if db_account['highscore'] < highscore: 
            supabase.table('score').update(account).eq('id',db_account['id']).execute()
    except:
        return False
    
def update_note():
    try:
        global supabase
        data = list(supabase.table('update').select('*').execute())[0][1][0]

        curr_version = version.split('.')
        db_version = data['version'].split('.')
        for num in range(len(curr_version)):
            if db_version[num] > curr_version[num]:
                return [True,data['link']]
        return [False]
    except:
        return False


def heart_resting(num):
    for i in range(num):
        heart = health_bar[i]
        heart.is_empty = 0

def sound_vol(nf):
    if nf == 'on':
        player.sprite.jump_sound.set_volume(0.3)
        winning_sound.set_volume(0.3)
        losing_sound.set_volume(0.3)
        power_up_sound.set_volume(0.3)
    else:
        player.sprite.jump_sound.set_volume(0)
        winning_sound.set_volume(0)
        losing_sound.set_volume(0)
        power_up_sound.set_volume(0)        

start_time = 0

pygame.init()
pygame.display.set_icon(pygame.image.load('graphics/icon.ico'))
screen = pygame.display.set_mode((800,450))
name = "Pixel runner"
pygame.display.set_caption(name)



clock = pygame.time.Clock()

version = '1.0.0'

game_state = 0


#Player
player = pygame.sprite.GroupSingle()
player.add(Player())
player.sprite.jump_sound.set_volume(0.3)


#Obstcales
obstcale_group = pygame.sprite.Group()

speeds = 5

#heart entity
plus_heart_group = pygame.sprite.GroupSingle()

power_up_sound = pygame.mixer.Sound('audio/power_up.mp3')

plus_heart_timer = 75

#font
my_font = pygame.font.Font('font/Pixeltype.ttf', 50)


#background
background_surface = pygame.image.load('graphics/Sky.png').convert()


#ground
ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(topleft=(0,300))

#settings vars
nf = 'on'

#score
score = 0
winning_sound = pygame.mixer.Sound('audio/wining.wav')
played = False

#main menu title
title_surf = my_font.render(name,False,(64,64,64))
title_rect = title_surf.get_rect(midtop=(400,25))

#main menu buttons
main_menu_group = pygame.sprite.Group()

play_button = Button(my_font.render(f'Play',False,(64,64,64)),400,200)
settings_button = Button(my_font.render(f'Settings',False,(64,64,64)),400,250)

madeby = Label(my_font.render(f'Made by Belal',False,(64,64,64)),450,440)
madeby.image = pygame.transform.rotozoom(madeby.image,0,0.5)

main_menu_group.add(madeby)
main_menu_group.add(play_button)
main_menu_group.add(settings_button)

# speeds buttons

speed_button_10 = Button(my_font.render(' ',False,(64,64,64)),0,0)
speed_button_50 = Button(my_font.render(' ',False,(64,64,64)),400,310)
speed_button_100 = Button(my_font.render(' ',False,(64,64,64)),400,10)

message_group = pygame.sprite.GroupSingle()

main_menu_group.add(speed_button_10)
main_menu_group.add(speed_button_50)
main_menu_group.add(speed_button_100)

#highscore buttton main menu
highscore_button = Button(my_font.render(f'Highscore',False,(64,64,64)),400,300)

checkbox_highscore_group = pygame.sprite.GroupSingle()
checkbox_highscore = CheckBox(False,highscore_button.rect)
checkbox_highscore_group.add(checkbox_highscore)

main_menu_group.add(highscore_button)

#update
check_update = False
update_button = Button(my_font.render(f'Check for updates!',False,(64,64,64)),400,350)

checkbox_update_group = pygame.sprite.GroupSingle()
checkbox_update = CheckBox(True,update_button.rect)
checkbox_update_group.add(checkbox_update)



main_menu_group.add(update_button)

#settings menu text
settings_text_surf = my_font.render('Settings',False,(64,64,64))
settings_text_rect = settings_text_surf.get_rect(midtop=(400,25))

#settings menu buttons
settings_menu_group = pygame.sprite.Group()

sounds_button = Button(my_font.render(f'Sounds:{nf}',False,(64,64,64)),400,200)
settings_back_button = Button(my_font.render('Back',False,(64,64,64)),400,420)

settings_menu_group.add(settings_back_button)
settings_menu_group.add(sounds_button)

#db client
url = "https://zzifsbcyfdhkisttssnx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6aWZzYmN5ZmRoa2lzdHRzc254Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTA5NTUyOTksImV4cCI6MjAyNjUzMTI5OX0.j80QUNK0KQzoD9XxrfVhIZRSgBuL0hyqUH6ondmKq30"
supabase = supabase.create_client(supabase_url=url, supabase_key=key)

#highscore

highscore = 0

with open('data/data.txt','rb') as file:
    highscore = int(b64decode(file.read()).decode('ascii'))

highscore_group = pygame.sprite.Group()

highscore_back_button = Button(my_font.render('Back',False,(64,64,64)),400,420)
top_5_list = []

highscore_group.add(highscore_back_button)

#game over menu
game_over_menu_group = pygame.sprite.Group()

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400,225))


main_menu_button = Button(my_font.render('Main menu',False,(64,64,64)),300,400)
restart_button = Button(my_font.render('Restart',False,(64,64,64)),525,400)

username_input_group = pygame.sprite.GroupSingle()

username_input_group.add(InputBox(400,225,50,20,"Username: (if you don't want leave it empty)"))

game_over_menu_group.add(main_menu_button)
game_over_menu_group.add(restart_button)

#health bar
health_bar = []
health_bar_group = pygame.sprite.Group()
losing_sound = pygame.mixer.Sound('audio/losing.wav')


for i in range(3):
    heart = Heart()
    heart.rect.centerx += (-40 * i)
    health_bar.append(heart)
    health_bar_group.add(heart)




#timers and events
obstcale_spawning_timer = pygame.USEREVENT + 1
heart_spawning_timer = pygame.USEREVENT + 2

pygame.time.set_timer(obstcale_spawning_timer,1200)
 

running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == 1:
            if event.type == obstcale_spawning_timer:
                    obstcale_group.add(Obstcales(choice(['fly','snail','snail']),speeds))
        if not username_input_group.sprite.entered and game_state == 2 :
            username = username_input_group.sprite.handle_event(event)


    sound_vol(nf)

    if game_state == 1:
        
        
        #displaying
        screen.blit(background_surface,(0,0))
        screen.blit(ground_surface,ground_rect)

        #player
        if player.sprite.draw_flashing:
            player.draw(screen)
        player.update()


        #obstcale
        obstcale_group.draw(screen)
        obstcale_group.update()

        #plus heart
        if score >= plus_heart_timer:
            plus_heart_group.add(PlusHeart())
            plus_heart_timer = score + 75
        heart_cal(plus_heart_group)
        plus_heart_group.draw(screen)
        plus_heart_group.update()

        #health bar and collisons
        if heart_cal(obstcale_group):
            game_state = 2
        

        health_bar_group.draw(screen)
        health_bar_group.update()

        #score
        score = round(pygame.time.get_ticks() / 250 - start_time)
        if score > highscore:
            highscore = score
            with open('data/data.txt','wb') as file:
                file.write(b64encode(str(highscore).encode('ascii')))
        if score == highscore and played == False:
          winning_sound.play() 
          played = True
        
        score_surf = my_font.render(f'Score:{score}', False, (64,64,64))
        score_rect = score_surf.get_rect(center=(80,30))
        score_surf = pygame.transform.rotozoom(score_surf,0,0.8)

        highscore_surf = my_font.render(f'HighScore:{str(highscore)}', False, (64,64,64))
        highscore_rect = highscore_surf.get_rect(center=(720,30))
        highscore_surf = pygame.transform.rotozoom(highscore_surf,0,0.8)

        screen.blit(score_surf,score_rect)
        screen.blit(highscore_surf,highscore_rect)

    elif game_state == 2:
        your_score_surf = my_font.render(f'Score:{score}',False,(64,64,64))
        your_score_rect = your_score_surf.get_rect(center=(400,50))

        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(your_score_surf,your_score_rect)

        game_over_menu_group.draw(screen)
        game_over_menu_group.update()
        if not username_input_group.sprite.entered and top_5() != False:
            screen.fill((255,255,255))
            username_input_group.draw(screen)
            username_input_group.update()
        
        start_time = round(pygame.time.get_ticks() / 250)

        if main_menu_button.aciton:
            game_state = 0

        elif restart_button.aciton:
            player.add(Player())
            played = False
            game_state = 1
            #resting
            username_input_group.sprite.text = "Username: (if you don't want leave it empty)"
            username_input_group.sprite.entered = False

            heart_resting(len(health_bar))

    elif game_state == 0:
        if play_button.aciton:
            start_time = round(pygame.time.get_ticks() / 250)
            heart_resting(len(health_bar))
            username_input_group.sprite.text = "Username: (if you don't want leave it empty)"
            username_input_group.sprite.entered = False
            game_state = 1

        elif settings_button.aciton:
            game_state = 3

        elif highscore_button.aciton:
            top_5_list = top_5()
            if top_5_list:
                game_state = 4
            else:
                checkbox_highscore.call_timer()
               
        elif update_button.aciton:
            db_version = update_note()

            if db_version == False:
                checkbox_update.change_symbol(False,update_button)
                checkbox_update.call_timer()

            elif check_update == True:
                webbrowser.open(db_version[1])

            elif db_version[0]:
                update_button.image = my_font.render('Update!',False,(64,64,64))
                update_button.rect.centerx = 400
                
            else:
                checkbox_update.change_symbol(True,update_button)
                checkbox_update.call_timer()

        elif speed_button_10.aciton:
            speeds = 10
            message = CheckBox(True,pygame.Rect(float(randint(61,739)),float(randint(50,400)),20.0,20.0))
            message.image = my_font.render('Oh, You just pressed a button',False,(64,64,64))
            message_group.add(message)
        
        elif speed_button_50.aciton:
            speeds = 50
            message = CheckBox(True,pygame.Rect(float(randint(61,739)),float(randint(50,400)),20.0,20.0))
            message.image = my_font.render('Oh, You just pressed a button',False,(64,64,64))
            message_group.add(message)
        
        elif speed_button_100.aciton:
            speeds = 100
            message = CheckBox(True,pygame.Rect(float(randint(61,739)),float(randint(50,400)),20.0,20.0))
            message.image = my_font.render('Oh, you just pressed a button',False,(64,64,64))
            message_group.add(message)


        checkbox_highscore_group.update()
        checkbox_update_group.update()    
        screen.fill((94,129,162))

        if checkbox_update.timer < checkbox_update.checkbox_timer:            
            checkbox_update_group.draw(screen)

        if checkbox_highscore.timer < checkbox_highscore.checkbox_timer:            
            checkbox_highscore_group.draw(screen)

        screen.blit(title_surf,title_rect)

        message_group.draw(screen)
        message_group.update()
        main_menu_group.draw(screen)
        main_menu_group.update()
    
    elif game_state == 3:
        
        sounds_button.image = my_font.render(f'Sounds:{nf}',False,(64,64,64))
        if sounds_button.aciton:
            if nf == 'on':
                nf = 'off'
                    
            else:
                nf = 'on'
            
        elif settings_back_button.aciton:
            game_state = 0

        screen.fill((94,129,162))
        screen.blit(settings_text_surf,settings_text_rect)
        settings_menu_group.draw(screen)
        settings_menu_group.update()
    
    else:
        screen.fill((245,206,66))
        
        for i in range(len(top_5_list)):
            highscore_group.add(Label(my_font.render(f'#{i +1}- {top_5_list[i]['name']} {top_5_list[i]['highscore']}', False, (64,64,64)),400,100 + i * 50))

        if highscore_back_button.aciton:
            game_state = 0


        highscore_group.draw(screen)
        highscore_group.update()
    

    pygame.display.flip()
    clock.tick(60)
