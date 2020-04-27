import pygame

pygame.init()

clock_tick_rate=20

screen = pygame.display.set_mode((400,400))

pygame.display.set_caption("Image")

done=False

clock = pygame.time.Clock()
background_image = pygame.image.load("foto.jpeg").convert()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.blit(background_image, [0,0])

    pygame.display.flip()
    clock.tick(clock_tick_rate)
