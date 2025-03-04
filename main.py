# Skriv din kod här för att skapa spelet! Följ dessa steg:
'''
Steg 1 - Skapa en skärm och rita ett skepp
Steg 2 - Lägga till en scrollande stjärnbakgrund
Steg 3 - Sätt jetmotorer på rymdskeppet
Steg 4 - Gör så rymdskeppet kan skjuta
Steg 5 - Slumpa fram Asteroider 
Steg 6 - Detektera kollisioner mellan rymdskeppet och asteroiden
Steg 7 - Skapa explosionseffekten (samt lär dig partikeleffekter)
Steg 8 - Gör så att rymdskeppet kan explodera i kollision med asteroiden
Steg 9 - Gör så att rymdskeppet kan skjuta ner asteroider
Steg 10 - Lägg till musik och ljudeffekter
'''

import pygame

skärmens_bredd = 800
skärmens_höjd = 600

skärm = pygame.display.set_mode((skärmens_bredd, skärmens_höjd))

pygame.display.set_caption("Space Shooter")

spelet_körs = True

original_bild = pygame.image.load("assets/sprites/SpaceShip.png")
backgrund_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
backgrund_stjärnor = pygame.image.load("assets/backgrounds/stars-A.png")
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png") 

backgrund_y = 0

sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))

spelare_x = skärmens_bredd // 2 - 120
spelare_y = skärmens_höjd - 200
spelarens_hastighet = 2

jetstråle_x = spelare_x + 40
jetstråle_y = spelare_y + 100

while (spelet_körs == True):

    skärm.fill((0, 0, 30))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            spelet_körs = False

    skärm.blit(backgrund_mörkblå, (0, 0))
    skärm.blit(backgrund_stjärnor, (0, backgrund_y))
    skärm.blit(backgrund_stjärnor, (0, backgrund_y - skärmens_höjd))

    backgrund_y += 2

    if backgrund_y > skärmens_höjd:
        backgrund_y = 0

    skärm.blit(sprite_spelare, (spelare_x, spelare_y))
    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and spelare_x > 0:
        spelare_x = spelare_x - spelarens_hastighet
    if keys[pygame.K_d] and spelare_x < skärmens_bredd - sprite_spelare.get_width():
        spelare_x = spelare_x + spelarens_hastighet
    if keys[pygame.K_w] and spelare_y > 0:
        spelare_y = spelare_y - spelarens_hastighet
    if keys[pygame.K_s] and spelare_y < skärmens_höjd - sprite_spelare.get_width() + 26:
        spelare_y = spelare_y + spelarens_hastighet

pygame.quit()