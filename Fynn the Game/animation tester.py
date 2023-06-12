import pygame
pygame.init()
win=pygame.display.set_mode((300,300))
pygame.display.set_caption('animation tester')
frame=1
print('============================================')
inp=input('Enter picture name (e.g. Greg right)\n\n>>')
run=True
while run:
    win.fill((255,255,255))
    image=pygame.image.load(inp+' '+str(frame)+'.png')
    win.blit(image,(20,20))
    pygame.display.update()
    pygame.time.delay(100)
    if frame!=4:
        frame+=1
    else:
        frame=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

pygame.quit()
        
