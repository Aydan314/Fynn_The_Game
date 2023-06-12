import pygame
import random
pygame.init()
win=pygame.display.set_mode((800,800))
pygame.display.set_caption('Fynn The Game')

class player(object):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.speed=4
        self.grav=8
        self.rect=pygame.Rect(self.x+50,self.y,self.width-20,self.height)
        self.j_rect=pygame.Rect(self.x+40,self.y,self.width,self.height)
        self.attackrect=pygame.Rect(self.x+80,self.y,self.width,self.height)
        self.moving=False
        self.left=False
        self.dead=False
        self.key=False
        self.health=3
        self.frame=1
        self.cooldown=0
        self.attack=False
        self.attackno=0
    def draw(self,win):
        if self.attack:
            self.attackno=16
        self.j_rect=pygame.Rect(self.x+50,self.y,self.width-25,self.height+8)
        self.rect=pygame.Rect(self.x+50,self.y,self.width-20,self.height)
        if not self.dead:
            if self.key:
                key=pygame.image.load('key.png')
                win.blit(key,(self.x+40,self.y-60))
            if self.left:
                self.attackrect=pygame.Rect(self.x-20,self.y,100,self.height)
                if self.attackno!=0:
                    image=pygame.image.load('Character left attack '+str(self.frame)+'.png')
                else:
                    if not self.moving:
                        image=pygame.image.load('Character left idle.png')
                    else:
                        image=pygame.image.load('Character left moving '+str(self.frame)+'.png')
            else:
                self.attackrect=pygame.Rect(self.x+80,self.y,100,self.height)
                if self.attackno!=0:
                    image=pygame.image.load('Character right attack '+str(self.frame)+'.png')
                else:
                    if not self.moving:
                        image=pygame.image.load('Character right idle.png')
                    else:
                        image=pygame.image.load('Character right moving '+str(self.frame)+'.png')

            if self.cooldown==0:
                if self.frame!=4:
                    self.frame+=1
                else:
                    self.frame=1
                if self.attackno!=0:
                    self.cooldown=5
                else:
                    self.cooldown=10
            else:
                self.cooldown-=1
            if self.attackno != 0 or self.attack:            
                win.blit(image,(self.x-20,self.y))
            else:
                win.blit(image,(self.x,self.y))

            if self.attackno != 0:
                self.attackno-=1
        #pygame.draw.rect(win,(0,0,200),(self.attackrect),1)
        #pygame.draw.rect(win,(0,250,200),(self.rect),1)

class block(object):
    def __init__(self,x,y,width,height,varient):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.varient=varient
        self.cooldown=0
        self.hit_limit=30
        self.frame=1
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.s_rect=pygame.Rect(self.x+10,self.y,self.width-20,self.height)
        self.render=True
        self.strength=4
    def draw(self,win):
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.s_rect=pygame.Rect(self.x+10,self.y,self.width-20,self.height)
        if self.x > -80:
            if self.x < 800:
                if self.varient=='volcano':
                    if self.cooldown < 60:
                        flame=pygame.image.load('flame '+str(self.frame)+'.png')
                        win.blit(flame,(self.x,self.y-140))
                        fire=pygame.Rect(self.x+20,self.y-140,60,160)
                        self.frame+=1
                        if self.frame==4:
                            self.frame=1
                        if player.rect.colliderect(fire):
                            if self.hit_limit==0:
                                if player.health != 0:
                                    player.health-=1
                                    self.hit_limit=30
                                else:
                                    if not player.dead:
                                        death()
                        if self.hit_limit!=0:   
                              self.hit_limit-=1
                        if player.health==0:
                            if not player.dead:
                                death()
                    if self.cooldown==120:
                        self.cooldown=0
                    self.cooldown+=1
                if self.varient=='pitfall':
                    if player.j_rect.colliderect(self.rect):
                        if self.cooldown==0:
                            self.strength-=1
                            self.cooldown=20
                        else:
                            self.cooldown-=1
                    else:
                        if self.cooldown==0:
                            if self.strength!=4:
                                self.strength+=1
                                self.cooldown=30
                        else:
                            self.cooldown-=1
                                
                    if self.strength==0:
                        self.render=False
                    tile=pygame.image.load('pitfall '+str(self.strength)+'.png')
                    
                elif self.varient=='crate':
                        if self.strength==4:
                            tile=pygame.image.load('crate.png')
                        else:
                            tile=pygame.image.load('crate broken.png')
                    
                else:
                    tile=pygame.image.load(self.varient+'.png')
                win.blit(tile,(self.x,self.y))
                        
                    
                #pygame.draw.rect(win,(250,0,0),(self.rect),1)
                #pygame.draw.rect(win,(0,250,250),(self.s_rect),1)
                
class enemy(object):
    def __init__(self,x,y,width,height,varient):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.varient=varient
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.speed=3
        self.cooldown=0
        self.neg=1
        self.frame=1
        self.frame_cooldown=0
        self.shootcooldown=0
        self.health=3
        self.attack=False
    def draw(self,win):
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        if self.x > -80:
            if self.x < 800:
                if self.varient=='saw':
                    self.rect=pygame.Rect(self.x+30,self.y+30,self.width-40,self.height-40)
                    tile=pygame.image.load('saw '+str(self.frame)+'.png')
                    if self.frame_cooldown==0:
                        if self.frame == 4:
                            self.frame=1
                        else:
                            self.frame+=1
                            self.frame_cooldown=2
                    else:
                        self.frame_cooldown-=1
                    self.y+=self.speed*self.neg
                    if player.rect.colliderect(self.rect):
                        if player.health==0:
                            if not player.dead:
                                death()
                        else:
                            if self.cooldown==0:
                                player.health-=1
                                self.cooldown=60
                    if self.cooldown !=0:
                        self.cooldown-=1
                    for item in level_list:
                        if item.rect.colliderect(self.rect):
                            if item.y < self.y:
                                self.neg=1
                            else:
                                self.neg=-1
                            
                else:
                    pygame.draw.rect(win,(250,0,0),(self.x,self.y,self.width,10))
                    pygame.draw.rect(win,(0,250,0),(self.x,self.y,round((self.width/3)*self.health),10))
                    if self.varient=='Greg':
                        if self.shootcooldown==0:
                            projectile_list.append(projectile(self.x,self.y+10,self.neg,'shot arrow'))
                            self.shootcooldown=150
                        else:
                            self.shootcooldown-=1
                    if player.rect.colliderect(self.rect):
                        self.attack=True
                        self.speed=0
                        if self.neg==1:
                            tile=pygame.image.load(self.varient+' attack right '+str(self.frame)+'.png')
                        else:
                            tile=pygame.image.load(self.varient+' attack left '+str(self.frame)+'.png')
                        if self.frame_cooldown==0:
                            if self.frame!=4:
                                self.frame+=1
                                self.frame_cooldown=10
                            else:
                                self.frame=1
                        else:
                            self.frame_cooldown-=1
                    
                        if player.health==0:
                            if not player.dead:
                                death()
                        else:
                            if self.cooldown==0:
                                player.health-=1
                                self.cooldown=40
                            else:
                                self.cooldown-=1
                    else:
                        self.speed=3
                        self.attack=False
                    for item in level_list:
                        if item.rect.colliderect(self.rect):
                            if item.y >= self.y:
                                if item.x < self.x:
                                    self.neg=1
                                else:
                                    self.neg=-1
                                    
                    if not self.attack:
                        if self.neg==1:
                            tile=pygame.image.load(self.varient+' right '+str(self.frame)+'.png')
                        else:
                            tile=pygame.image.load(self.varient+' left '+str(self.frame)+'.png')
                        if self.frame_cooldown==0:
                            if self.frame!=4:
                                self.frame+=1
                                self.frame_cooldown=10
                            else:
                                self.frame=1
                        else:
                            self.frame_cooldown-=1
                        self.x+=self.speed*self.neg
                    
                                    
                win.blit(tile,(self.x,self.y))
                

                
class decor(object):
    def __init__(self,x,y,width,height,varient):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.varient=varient
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.checkpoint=False
    def draw(self,win):
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        if self.x > -80:
            if self.x < 800:
                tile=pygame.image.load(self.varient+'.png')
                if self.varient=='checkpoint':
                    if self.rect.colliderect(player.rect):
                        self.checkpoint=True
                        global dist_travel
                        dist_travel=0
                    if self.checkpoint:
                        tile=pygame.image.load('checkpoint active.png')
                    else:
                        tile=pygame.image.load('checkpoint.png')
                win.blit(tile,(self.x,self.y))
                        

class world(object):
    def __init__(self,x,y,biome,number):
        self.x=x
        self.y=y
        self.biome=biome
        self.number=number
        self.radius=40
    def draw(self,win):
        global unlocked_level
        outer_colour=(20,150,255)
        inner_colour=(0,100,255)
        if unlocked_level >= self.number:
            outer_colour=(20,250,255)
            inner_colour=(20,200,255)
        self.rect=pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
        mouse_pos=pygame.mouse.get_pos()
        pygame.draw.circle(win,(inner_colour),(self.x,self.y),self.radius)
        pygame.draw.circle(win,(outer_colour),(self.x,self.y),self.radius+1,3)
        if self.rect.collidepoint(mouse_pos):
            if not end_game:
                if self.number == unlocked_level:
                    pygame.draw.circle(win,(25,50,255),(self.x,self.y),self.radius+1,3)
                    if pygame.mouse.get_pressed()[0]:
                        load_level(self.number,self.biome) 
                        global menu
                        menu=False
                else:
                     pygame.draw.circle(win,(255,50,25),(self.x,self.y),self.radius,3)

        font=pygame.font.SysFont('callabri',80)
        num=font.render(str(self.number),1,(255,255,255))
        win.blit(num,(self.x-15,self.y-22))
            
        if self.number > unlocked_level:
            lock=pygame.image.load('lock.png')
            win.blit(lock,(self.x+3,self.y+3))

class projectile(object):
    def __init__(self,x,y,facing,varient):
        self.x=x
        self.y=y
        self.facing=facing
        self.varient=varient
        self.speed=6
        self.rect=pygame.Rect(self.x,self.y,40,10)
    def draw(self,win):
        self.rect=pygame.Rect(self.x,self.y,40,10)
        if self.facing==1:
            picture=pygame.image.load(self.varient+' right.png')
            self.x+=self.speed
        else:
            picture=pygame.image.load(self.varient+' left.png')
            self.x-=self.speed
        win.blit(picture,(self.x,self.y))
        

def game_window():
    global coins
    win.blit(background,(0,0))
    for item in nonCol_list:
        item.draw(win)

    index=0
    for item in projectile_list:
        if item.x < -20:
            projectile_list.pop(index)
        elif item.x > 820:
            projectile_list.pop(index)
        elif item.rect.colliderect(player.rect):
            projectile_list.pop(index)
            player.health-=1
            if player.health==0:
                death()
        else:
            for block in level_list:
                if block.rect.colliderect(item.rect):
                    projectile_list.pop(index)
        index+=1
        item.draw(win)
        
    player.draw(win)
    for item in level_list:
        if item.render:
            item.draw(win)
    for item in enemy_list:
        item.draw(win)
    heart_full=pygame.image.load('heart full.png')
    heart_empty=pygame.image.load('heart empty.png')
    if player.health < 3:
        win.blit(heart_empty,(710,5))
    else:
        win.blit(heart_full,(710,5))
    if player.health < 2:
        win.blit(heart_empty,(610,5))
    else:
        win.blit(heart_full,(610,5))
    if player.health < 1:
        win.blit(heart_empty,(510,5))
    else:
        win.blit(heart_full,(510,5))
    coin=pygame.image.load('coin.png')
    win.blit(coin,(5,5))
    font=pygame.font.SysFont('calabri',(80))
    coin_text=font.render('X'+str(coins),1,(255,250,0))
    win.blit(coin_text,(90,18))
    pygame.display.update()

def death():
    global dist_travel
    grave=pygame.image.load('tombstone.png')
    player.dead=True
    game_window()
    if player.y > 880:
        win.blit(grave,(player.x,720))
    else:
        win.blit(grave,(player.x,player.y+80))
    font=pygame.font.SysFont('calabri',200)
    dead_text=pygame.image.load('dead text.png')
    win.blit(dead_text,(0,300))
    pygame.display.update()
    pygame.time.delay(2400)
    player.x=400
    player.y=400
    for item in level_list:
        item.x-=dist_travel
        if item.varient=='pitfall':
            item.strength=4
            item.render=True
    for item in nonCol_list:
        item.x-=dist_travel
    for item in enemy_list:
        item.x-=dist_travel
    projectile_list=[]
    dist_travel=0
    player.dead=False
    player.health=3

def level_complete():
    global unlocked_level
    global level_num
    win_text=pygame.image.load('win text.png')
    win.blit(win_text,(0,300))
    player.health=3
    pygame.display.update()
    pygame.time.delay(2400)
    for item in nonCol_list:
        item.checkpoint=False
    if level_num == unlocked_level:
        unlocked_level+=1
    player.x=400
    player.y=400

isJump = False
max_jump=32
jumpCount = max_jump
global dist_travel
dist_travel=0
global coins
coins=0
global unlocked_level
unlocked_level=1

def load_level(number,biome):
    global background
    background=pygame.image.load(biome+' background.png')
    global level_list
    global nonCol_list
    global enemy_list
    global level_num
    global projectile_list
    level_num=number
    enemy_list=[]
    level_list=[]
    nonCol_list=[]
    projectile_list=[]
    file=open('game levels.txt','r')
    read_file=file.readlines()
    ind=0
    found_no=0
    for line in read_file:
        if 'level '+str(number) in line:
            found_no=ind
        ind+=1
    level1=read_file[found_no+1:found_no+11]
    level_y=0
    while level_y < len(level1):
        item=level1[level_y]
        level_x=0
        while level_x < len(item):
            tile=item[level_x]
            if tile=='#':
                if biome=='tundra':
                    level_list.append(block((level_x*80),(level_y*80),80,80,'snow block'))
                elif biome=='dessert':
                    level_list.append(block((level_x*80),(level_y*80),80,80,'sand'))
                else:
                    level_list.append(block((level_x*80),(level_y*80),80,80,'grass'))
            if tile=='@':
                if biome=='tundra':
                    level_list.append(block((level_x*80),(level_y*80),80,80,'ice'))
                elif biome=='dessert':
                    level_list.append(block((level_x*80),(level_y*80),80,80,'sandstone'))
                else:
                    level_list.append(block((level_x*80),(level_y*80),80,80,'dirt'))
            if tile=='-':
                level_list.append(block((level_x*80),(level_y*80),80,80,'platform'))
            if tile=='D':
                level_list.append(block((level_x*80),(level_y*80),80,160,'door'))
            if tile=='I':
                nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'support'))
            if tile=='H':
                nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'health'))
            if tile=='C':
                nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'coin'))
            if tile=='K':
                nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'key'))
            if tile=='~':
                if biome=='tundra':
                    nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'iceicle'))
                elif biome=='dessert':
                    nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'tumbleweed'))
                else:
                    nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'grass tuft'))
            if tile=='o':
                if biome=='tundra':
                    nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'artic bush'))
                elif biome=='dessert':
                    nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'cactus'))
                else:
                    nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'bush'))
            if tile=='e':
                nonCol_list.append(decor((level_x*80),(level_y*80),160,160,'exit'))
            if tile=='0':
                if biome=='tundra':
                    nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'ice rock'))
                else:
                    nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'rock'))
            if tile=='!':
                level_list.append(block((level_x*80),(level_y*80),80,80,'pitfall'))
            if tile=='c':
                level_list.append(block((level_x*80),(level_y*80),80,80,'crate'))
            if tile=='s':
                enemy_list.append(enemy((level_x*80),(level_y*80),80,80,'Stevey'))
            if tile=='g':
                enemy_list.append(enemy((level_x*80),(level_y*80),80,80,'Greg'))
            if tile=='S':
                enemy_list.append(enemy((level_x*80),(level_y*80),60,60,'saw'))
            if tile=='V':
                level_list.append(block((level_x*80),(level_y*80),80,80,'volcano'))
            if tile=='P':
                nonCol_list.append(decor((level_x*80),(level_y*80),80,80,'checkpoint'))
            
            level_x+=1
        level_y+=1

def load_menu(page):
    global biome
    global world_list
    world_list=[]
    if page==1:
        biome='plains'
        position_list=((100,360),(350,590),(675,455))
        index=0
    elif page==2:
        biome='dessert'
        position_list=((130,350),(400,590),(650,320))
        index=3
    elif page==3:
        biome='tundra'
        position_list=((130,350),(370,530),(650,330))
        index=6
    world_list=[]
    for item in position_list:
        world_list.append(world(item[0],item[1],biome,index+1))
        index+=1

player=player(400,400,80,160)
size=80
run=True
arrow_cooldown=0
start_screen=True
global menu
menu=False
size_down=False
menu_page=1
facing=0
frm_cooldown=0
rand_cooldown=0
attack_limit=0
frm=1
font=pygame.font.SysFont('calabri',80)
show_text=300
show_enemy_stat=150
show_coin_stat=150
show_grade=150
global end_game
end_game=False
killcount=0

delay=0
controls=pygame.image.load('controls.png')
while delay < 600:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            break
    win.blit(controls,(0,0))
    pygame.display.update()
    delay+=1

while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    key=pygame.key.get_pressed()
    if start_screen:
        start_bg=pygame.image.load('start background.png')
        st_font=pygame.font.SysFont('calabri',(size))
        
        if rand_cooldown==0:
            if random.randint(1,80)==1:
                facing=random.randint(0,1)
                rand_cooldown=300
        else:
            rand_cooldown-=1
            
        if frm_cooldown==0:
            frm+=1
            frm_cooldown=20
            if frm==5:
                frm=1
        else:
            frm_cooldown-=1
        if facing==0:
            start_pic=pygame.image.load('character right moving '+str(frm)+'.png')
        else:
            start_pic=pygame.image.load('character left moving '+str(frm)+'.png')

        win.blit(start_bg,(0,0))
        win.blit(start_pic,(140,17))
        start_text=st_font.render('-Press Space-',1,(255,255,255))
        if size == 80:
            size_down=True
        if size == 40:
            size_down=False
        if size_down:
            size-=1
        else:
            size+=1
        win.blit(start_text,(390-size*2,600))
        pygame.time.delay(1)
        pygame.display.update()
        if key[pygame.K_SPACE]:
            load_menu(1)
            menu=True
            start_screen=False
    elif menu:
        mouse_pos=pygame.mouse.get_pos()
        global biome
        bg=pygame.image.load(biome+' levels.png')
        win.blit(bg,(0,0))
        for item in world_list:
            item.draw(win)
        menu_text=pygame.image.load('menu text.png')
        
        if unlocked_level==10:
            end_game=True
            if show_text!=0:
                g_comp=pygame.image.load('game complete.png')
                win.blit(g_comp,(0,400))
                show_text-=1
            else:
                if show_coin_stat!=0:
                    end_font=pygame.font.SysFont('calabri',100)
                    stat_text=end_font.render('Coins collected: '+str(coins)+'/90',1,(250,250,0))
                    transparent=pygame.image.load('transparent.png')
                    win.blit(transparent,(0,400))
                    win.blit(stat_text,(10,410))
                    show_coin_stat-=1
                else:
                    if show_enemy_stat!=0:
                        end_font=pygame.font.SysFont('calabri',100)
                        stat_text=end_font.render('Enemies killed: '+str(killcount)+'/30',1,(200,20,20))
                        transparent=pygame.image.load('transparent.png')
                        win.blit(transparent,(0,400))
                        win.blit(stat_text,(10,410))
                        show_enemy_stat-=1
                    else:
                        if show_grade!=0:
                            score=coins+killcount
                            if score in range(0,20):
                                grade='F'
                            elif score in range(20,40):
                                grade='E'
                            elif score in range(40,60):
                                grade='D'
                            elif score in range(60,80):
                                grade='C'
                            elif score in range(80,100):
                                grade='B'
                            elif score in range(100,120):
                                grade='A'
                            else:
                                grade='A+'
                            end_font=pygame.font.SysFont('calabri',100)
                            stat_text=end_font.render('Final grade: '+grade,1,(0,0,0))
                            transparent=pygame.image.load('transparent.png')
                            win.blit(transparent,(0,400))
                            win.blit(stat_text,(10,410))
                            show_grade-=1
                        else:
                            pygame.time.delay(300)
                            run=False
                            
                        
                
        

        if menu_page==1:
            next_button_show=True
            prev_button_show=False
        elif menu_page==3:
            next_button_show=False
            prev_button_show=True
        else:
            next_button_show=True
            prev_button_show=True
            
        if next_button_show:
            button_rect=pygame.Rect(590,680,200,100)
            pygame.draw.rect(win,(200,200,200),(button_rect))
            pygame.draw.rect(win,(100,100,100),button_rect,2)
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(win,(255,255,255),button_rect,2)
                if pygame.mouse.get_pressed()[0]:
                    if arrow_cooldown==0:
                        menu_page+=1
                        load_menu(menu_page)
                        arrow_cooldown=30
            arrow=pygame.image.load('arrow right.png')
            win.blit(arrow,(button_rect[0],button_rect[1]))
            
        if prev_button_show:
            button_rect=pygame.Rect(10,680,200,100)
            pygame.draw.rect(win,(200,200,200),(button_rect))
            pygame.draw.rect(win,(100,100,100),button_rect,2)
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(win,(255,255,255),button_rect,2)
                if pygame.mouse.get_pressed()[0]:
                    if arrow_cooldown==0:
                        menu_page-=1
                        load_menu(menu_page)
                        arrow_cooldown=30
                    
            arrow=pygame.image.load('arrow left.png')
            win.blit(arrow,(button_rect[0],button_rect[1]))
        if arrow_cooldown != 0:
            arrow_cooldown-=1
            
        win.blit(menu_text,(0,0))
        pygame.display.update()

    else:     
        player.moving=False
        player.attack=False
        
        if key[pygame.K_SPACE]:
            if attack_limit==0:
                player.attack=True
                index=0
                attack_limit=30
                for item in enemy_list:
                    if item.rect.colliderect(player.attackrect):
                        if item.varient != 'saw':
                            item.health-=1
                            if item.health==0:
                                enemy_list.pop(index)
                                killcount+=1
                    index+=1
                    
                index=0
                for item in level_list:
                    if item.varient=='crate':
                        if item.rect.colliderect(player.attackrect):
                            item.strength-=2
                        if item.strength==0:
                            level_list.pop(index)
                    index+=1
                    
        if attack_limit!=0:
            attack_limit-=1

        if key[pygame.K_LEFT]:
            if player.attackno==0:
                can_left=True
                player.left=True
                for tile in level_list:
                    if tile.render:
                        if tile.varient != 'platform':
                            if tile.rect.colliderect(player.rect):
                                if tile.y-80 <= player.y:
                                    if tile.x <= player.x:
                                        can_left=False
                if can_left:
                    player.moving=True
                    dist_travel+=player.speed
                    for item in level_list:
                        item.x+=player.speed
                    for item in nonCol_list:
                        item.x+=player.speed
                    for item in enemy_list:
                        item.x+=player.speed
                    for item in projectile_list:
                        item.x+=player.speed
           
        elif key[pygame.K_RIGHT]:
            if player.attackno==0:
                player.left=False
                can_right=True
                for tile in level_list:
                    if tile.render:
                        if tile.varient != 'platform':
                            if tile.rect.colliderect(player.rect):
                                if tile.y-80 <= player.y:
                                    if tile.x >= player.x: 
                                        can_right=False
                if can_right:
                    player.moving=True
                    dist_travel-=player.speed
                    for item in level_list:
                        item.x-=player.speed
                    for item in nonCol_list:
                        item.x-=player.speed
                    for item in enemy_list:
                        item.x-=player.speed
                    for item in projectile_list:
                        item.x-=player.speed

        if player.y > 880:
            player.health=0
            death()
        if player.health==0:
            death()


        if key[pygame.K_UP]:
            if not isJump:
                touch_block=False
                for tile in level_list:
                    if tile.render:
                        if tile.rect.colliderect(player.j_rect):
                            if tile.y-80 < player.y:
                                touch_block=False
                            else:
                                touch_block=True
                if touch_block:
                    isJump=True
        if isJump:
            if jumpCount >= max_jump*-1:
                 isJump = True
                 neg = 1
                 if jumpCount < 0:
                    neg = -1
                 can_jump=True
                 if player.y < 0:
                     can_jump=False
                     isJump=False
                     jumpCount = max_jump
                 player.j_rect[1]=player.j_rect[1] - round((jumpCount ** 2) * 0.025 * neg)
                 for tile in level_list:
                    if tile.rect.colliderect(player.j_rect):
                        if tile.y < player.y:
                            if tile.render:
                                if tile.varient != 'platform':
                                    can_jump=False
                                    isJump=False
                                    jumpCount = max_jump
                        
                        else:
                            if tile.varient != 'platform':
                                if tile.render:
                                    isJump=False
                                    jumpCount = max_jump
                            else:
                                if neg==-1:
                                    if tile.y > player.y+80:
                                        if tile.render:
                                            isJump=False
                                            jumpCount = max_jump
                                            can_jump=False
                            
                 if can_jump:
                     player.y -= round((jumpCount ** 2) * 0.025 * neg)
                 jumpCount -= 1
            else:
                isJump = False
                jumpCount = max_jump
        index=0
        for item in level_list:
            if item.varient=='door':
                if item.rect.colliderect(player.rect):
                    if player.key:
                        level_list.pop(index)
                        player.key=False
            index+=1

        index=0
        for item in nonCol_list:
            if item.varient=='coin':
                if item.rect.colliderect(player.rect):
                    coins+=1
                    nonCol_list.pop(index)
            if item.varient=='health':
                if item.rect.colliderect(player.rect):
                    if player.health!=3:
                        player.health+=1
                        nonCol_list.pop(index)
            if item.varient=='exit':
                if item.rect.colliderect(player.rect):
                    level_complete()
                    dist_travel=0
                    menu=True
            if item.varient=='key':
                if item.rect.colliderect(player.rect):
                    if player.key==False:
                        player.key=True
                        nonCol_list.pop(index)
            index+=1


        can_down=True
        for tile in level_list:
            if tile.render:
                if tile.s_rect.colliderect(player.j_rect):
                    if tile.y > player.y+80:
                        can_down=False
        if can_down:
            if not isJump:
                player.y+=player.grav
        else:
            if not isJump:
                player.y=(round(player.y/80))*80
        game_window()
pygame.quit()
