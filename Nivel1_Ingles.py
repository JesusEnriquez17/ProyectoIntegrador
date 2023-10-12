import pygame
import pytmx

def draw_tilemap_offset(surface, tmxdata, offset_x, offset_y):
    for layer in tmxdata.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmxdata.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, ((x * tmxdata.tilewidth) - offset_x, (y * tmxdata.tileheight) - offset_y))

def load_pygame(filename, colorkey=None):
    tmxdata = pytmx.util_pygame.load_pygame(filename, colorkey)
    return tmxdata

def draw_collectibles(surface, collectibles, camera_rect):
    for collectible in collectibles:
        # Ajusta el path de tu imagen de coleccionable
        image = pygame.image.load("img/Botones/despensa32b.png")
        rect = pygame.Rect(collectible.x, collectible.y, collectible.width, collectible.height)
        surface.blit(image, rect.move(-camera_rect.x, -camera_rect.y))

def draw_game_over(surface, myfont):
    text = myfont.render("You Lost", True, (255, 0, 0))
    text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 20))

    # Carga la imagen del botón "Reintentar"
    retry_button_image = pygame.image.load("img/Botones/BotonTryAgain.png")
    retry_button_rect = retry_button_image.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 100))

    surface.blit(text, text_rect)
    surface.blit(retry_button_image, retry_button_rect.topleft)  # Dibujar la imagen del botón
    
    return retry_button_rect  # Return the rect to check for clicks



# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((1000, 575))
tmxdata = load_pygame("img/Mapas/MapaBosque.tmx")
collision_objects = [obj for obj in tmxdata.objects if obj.properties.get("collision", False)]
collectibles = [obj for obj in tmxdata.objects if obj.properties.get("collectible", False)]

myfont = pygame.font.Font("fuentes/Minecraft.ttf", 75)

pygame.mixer.init()
pygame.mixer.music.load('sounds/Action 01.WAV')
pygame.mixer.music.set_volume(50.0)
pygame.mixer.music.play(-1)


camera_rect = pygame.Rect(0, 0, 1000, 575)
player_rect = pygame.Rect(50, 50, 30, 60)
player_velocity = [0, 0]
gravity = 1
jump_height = -15
jumping = False

collected_count = 0

running = True
game_over = False
paused = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Cambiar el estado de pausa cuando se presiona Esc
                paused = not paused
    
    # Si el juego está en pausa, muestra un mensaje y continua con el próximo ciclo
    if paused:
        myfont = pygame.font.Font("fuentes/Minecraft.ttf", 75)
        text = myfont.render("PAUSED", True, (255, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.Clock().tick(30)
        continue

    if player_rect.y > tmxdata.height * tmxdata.tileheight:
        game_over = True
    
    if game_over:
        retry_button_rect = draw_game_over(screen, myfont)
        pygame.display.flip()
        
        # Esperar a que ocurra un evento en lugar de procesar todos los eventos en un bucle
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if retry_button_rect.collidepoint(mouse_pos):
                # Reset necessary variables to restart the level
                player_rect.x, player_rect.y = 50, 50
                collected_count = 0
                collectibles = [obj for obj in tmxdata.objects if obj.properties.get("collectible", False)]
                game_over = False
        
        pygame.time.Clock().tick(30)
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_velocity[0] = -5
    elif keys[pygame.K_d]:
        player_velocity[0] = 5
    else:
        player_velocity[0] = 0
    
    if keys[pygame.K_w] and not jumping:
        player_velocity[1] = jump_height
        jumping = True
    
    player_velocity[1] += gravity
    next_rect_x = player_rect.x + player_velocity[0]
    next_rect_y = player_rect.y + player_velocity[1]

    horizontal_collision = False
    for obj in collision_objects:
        obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        if obj_rect.colliderect(pygame.Rect(next_rect_x, player_rect.y, player_rect.width, player_rect.height)):
            horizontal_collision = True
            break

    if not horizontal_collision:
        player_rect.x = next_rect_x
    
    vertical_collision = False
    for obj in collision_objects:
        obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        if obj_rect.colliderect(pygame.Rect(player_rect.x, next_rect_y, player_rect.width, player_rect.height)):
            vertical_collision = True
            jumping = False
            player_velocity[1] = 0
            break

    if not vertical_collision:
        player_rect.y = next_rect_y

    camera_rect.centerx = player_rect.centerx
    camera_rect.centery = player_rect.centery
    camera_rect.x = max(0, min(camera_rect.x, tmxdata.width * tmxdata.tilewidth - camera_rect.width))
    camera_rect.y = max(0, min(camera_rect.y, tmxdata.height * tmxdata.tileheight - camera_rect.height))

    screen.fill((0, 0, 0))
    draw_tilemap_offset(screen, tmxdata, camera_rect.x, camera_rect.y)
    draw_collectibles(screen, collectibles, camera_rect)
  
    # Check collision with collectibles
    collected = []
    for collectible in collectibles:
        rect = pygame.Rect(collectible.x, collectible.y, collectible.width, collectible.height)
        if player_rect.colliderect(rect):
            collected.append(collectible)
            collected_count += 1
    
    collectibles = [c for c in collectibles if c not in collected]
    
    pygame.draw.rect(screen, (255, 0, 0), player_rect.move(-camera_rect.x, -camera_rect.y))
    
    # Draw collectible count
    font = pygame.font.Font(None, 36)
    text = font.render(f"Food: {collected_count}", True, (255, 255, 255))
    screen.blit(text, (screen.get_width() - 200, 20))
    
    pygame.display.flip()
    pygame.time.Clock().tick(144)

pygame.quit()