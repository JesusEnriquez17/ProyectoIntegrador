import pygame
import sys
import pytmx

def set_all_volume(sounds, mult):
    for sound in sounds:
        vol = sound.get_volume()
        sound.set_volume(min(vol * mult, 1.0))



# Inicialización
pygame.init()
size = (1000, 575) 
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Hungers Hero")
logo = pygame.image.load("img/FondosMapas/Background3.png")
pygame.display.set_icon(logo)
white = (255, 255, 255)

# Carga de imagen y sonido
bg_image = pygame.image.load("img/FondosMapas/Background3.png")
bg_music = pygame.mixer.Sound("sounds/intro.mp3")

seleccionar = pygame.mixer.Sound('sounds/Selec.wav')

pygame.mixer.Sound.play(bg_music, loops=-1)
bg_image = pygame.image.load("img/FondosMapas/background3.png"). convert() #Convertir el formato de la imagen
bg_image = pygame.transform.scale(bg_image,(1000, 575))

music = [bg_music, seleccionar]
set_all_volume(music, 1.0)

# Estado de idioma actual y última vez que se hizo clic
current_language = "spanish"
last_click_time = 0

# Cadena de texto de idiomas
languages = {
    "english": {
        "play": "Play",
        "options": "Options",
        "controls": "Controls",
        "exit": "Exit",
        "spanish": "Spanish",
        "english": "English",
        "sound": "Sound",
        "back": "<~~",
        "lvl1": "Level 1",
        "lvl2": "Level 2",
        "lvl3": "Level 3"
    },
    "spanish": {
        "play": "Jugar",
        "options": "Opciones",
        "controls": "Controles",
        "exit": "Salir",
        "spanish": "Espanol",
        "english": "Ingles",
        "sound": "Sonido",
        "back": "<~~",
        "lvl1": "Nivel 1",
        "lvl2": "Nivel 2",
        "lvl3": "Nivel 3"
    }
}

# Estado de menú actual
menu_state = "main"

# Diccionario para almacenar los volúmenes previos de los sonidos
previous_volumes = {bg_music: 1.0, seleccionar: 0.5}

#FUNCION DE NIVEL 1 EN ESPAÑOL
def Nivel1Español():
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
        text = myfont.render("Has perdido", True, (255, 0, 0))
        text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 20))

        # Carga la imagen del botón "Reintentar"
        retry_button_image = pygame.image.load("img/Botones/BotonReitentar.png")
        retry_button_rect = retry_button_image.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 100))

        surface.blit(text, text_rect)
        surface.blit(retry_button_image, retry_button_rect.topleft)  # Dibujar la imagen del botón
        
        return retry_button_rect 

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
    level_complete = False 

    try:
        meta_object = [obj for obj in tmxdata.objects if obj.properties.get("meta", False)][0]  
    except IndexError:
        raise Exception("Error: No se pudo encontrar un objeto con la propiedad 'meta' en el mapa TMX.")

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
            text = myfont.render("PAUSADO", True, (255, 0, 0))
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

        meta_rect = pygame.Rect(meta_object.x, meta_object.y, meta_object.width, meta_object.height)
        if player_rect.colliderect(meta_rect):
            level_complete = True

        if level_complete:
            myfont = pygame.font.Font("fuentes/Minecraft.ttf", 75)
            text = myfont.render("Has pasado el nivel", True, (255, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.Clock().tick(30)
            continue

        
        pygame.draw.rect(screen, (255, 0, 0), player_rect.move(-camera_rect.x, -camera_rect.y))
        
        # Draw collectible count
        font = pygame.font.Font(None, 36)
        text = font.render(f"Comida: {collected_count}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() - 200, 20))
        
        pygame.display.flip()
        pygame.time.Clock().tick(144)
#FUNCION DE NIVEL 1 EN ESPAÑOL

#FUNCION DE NIVEL 1 EN INGLES
def Nivel1Ingles():
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
        
        return retry_button_rect 

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
    level_complete = False 

    try:
        meta_object = [obj for obj in tmxdata.objects if obj.properties.get("meta", False)][0]  
    except IndexError:
        raise Exception("Error: No se pudo encontrar un objeto con la propiedad 'meta' en el mapa TMX.")

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

        meta_rect = pygame.Rect(meta_object.x, meta_object.y, meta_object.width, meta_object.height)
        if player_rect.colliderect(meta_rect):
            level_complete = True

        if level_complete:
            myfont = pygame.font.Font("fuentes/Minecraft.ttf", 75)
            text = myfont.render("YOU HAVE PASSED THE LEVEL", True, (255, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.Clock().tick(30)
            continue

        
        pygame.draw.rect(screen, (255, 0, 0), player_rect.move(-camera_rect.x, -camera_rect.y))
        
        # Draw collectible count
        font = pygame.font.Font(None, 36)
        text = font.render(f"Food: {collected_count}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() - 200, 20))
        
        pygame.display.flip()
        pygame.time.Clock().tick(144)     
#FUNCION DE NIVEL 1 EN INGLES

#FUNCION PARA MOSTRAR CONTROLES EN INGLES
def show_controls_english():
    
    screen_size = (1000, 575)
    screen = pygame.display.set_mode(screen_size)

    white = (255, 255, 255)  # Definir el color blanco

    last_click_time = pygame.time.get_ticks()  # Para prevenir múltiples clics en un solo evento

    background_image_original = pygame.image.load('img/Botones/ControlesIngles.jpg')
    background_image = pygame.transform.scale(background_image_original, screen_size)

    # Clase para los botones
    class Button:
        def __init__(self, text, x, y, width, height, color, active_color, action=None):
            self.text = text
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.active_color = active_color
            self.action = action

        def draw(self, screen):
            global last_click_time
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if (self.x+self.width > mouse[0] > self.x and
                self.y+self.height > mouse[1] > self.y):
                pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))

                current_time = pygame.time.get_ticks()
                if click[0] == 1 and current_time - last_click_time > 500 and self.action is not None:
                    self.action()
                    last_click_time = current_time
            else:
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

            font = pygame.font.Font("fuentes/minecraft.ttf", 30)
            text = font.render(self.text, True, white)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    # Funciones callback para los botones

    def quit_game():
        nonlocal running
        running = False
        seleccionar.play()
    # Crear botones
    main_buttons = [
        Button("<~~", 25, 25, 150, 50, (128, 0, 0), (255, 0, 0), quit_game)
    ]

    # Bucle principal
    running = True
    while running:
        # Dibuja la imagen de fondo
        screen.blit(background_image, (0, 0))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar botones
        for button in main_buttons:
            button.draw(screen)

        pygame.display.flip()

#FUNCION PARA MOSTRAR CONTROLES EN ESPAÑOL
def show_controls_spanish():
    
    screen_size = (1000, 575)
    screen = pygame.display.set_mode(screen_size)

    white = (255, 255, 255)  # Definir el color blanco

    last_click_time = pygame.time.get_ticks()  # Para prevenir múltiples clics en un solo evento

    background_image_original = pygame.image.load('img/Botones/ControlesEspañol.jpg')
    background_image = pygame.transform.scale(background_image_original, screen_size)

    # Clase para los botones
    class Button:
        def __init__(self, text, x, y, width, height, color, active_color, action=None):
            self.text = text
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.active_color = active_color
            self.action = action

        def draw(self, screen):
            global last_click_time
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if (self.x+self.width > mouse[0] > self.x and
                self.y+self.height > mouse[1] > self.y):
                pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))

                current_time = pygame.time.get_ticks()
                if click[0] == 1 and current_time - last_click_time > 500 and self.action is not None:
                    self.action()
                    last_click_time = current_time
            else:
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

            font = pygame.font.Font("fuentes/minecraft.ttf", 30)
            text = font.render(self.text, True, white)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    # Funciones callback para los botones

    def quit_game():
        nonlocal running
        running = False
        seleccionar.play()
    # Crear botones
    main_buttons = [
        Button("<~~", 25, 25, 150, 50, (128, 0, 0), (255, 0, 0), quit_game)
    ]

    # Bucle principal
    running = True
    while running:
        # Dibuja la imagen de fondo
        screen.blit(background_image, (0, 0))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar botones
        for button in main_buttons:
            button.draw(screen)

        pygame.display.flip()
  
# FUNCION DE SELECCIONAR NIVEL
def SeleccionarNivel():

    pygame.init()
    screen_size = (1000, 575)
    screen = pygame.display.set_mode(screen_size)

    white = (255, 255, 255)  # Definir el color blanco

    last_click_time = pygame.time.get_ticks()  # Para prevenir múltiples clics en un solo evento

    background_image_original = pygame.image.load('img/Botones/NivelesSeleccionar.png')
    background_image = pygame.transform.scale(background_image_original, screen_size)

    # Clase para los botones
    class Button:
        def __init__(self, text_key, x, y, width, height, color, active_color, action=None):
            self.text_key = text_key  # Guarda la clave del texto
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.active_color = active_color
            self.action = action
    
        def draw(self, screen):
            global last_click_time
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
    
            if (self.x+self.width > mouse[0] > self.x and
                self.y+self.height > mouse[1] > self.y):
                pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
    
                current_time = pygame.time.get_ticks()
                if click[0] == 1 and current_time - last_click_time > 500 and self.action is not None:
                    self.action()
                    last_click_time = current_time
            else:
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
            font = pygame.font.Font("fuentes/minecraft.ttf", 30)
            text = font.render(languages[current_language][self.text_key], True, white)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
        
    # Funciones callback para los botones
    def Nivel1():
        print("1")

        if current_language == "english":
            Nivel1Ingles()
        elif current_language == "spanish":
           Nivel1Español()
        else:
            print("Error")
       

    def Nivel2():
        print("2")
        seleccionar.play()

    def Nivel3():
        print("3")
        seleccionar.play()

    def quit_game():
        seleccionar.play()
        nonlocal running
        running = False

    # Crear botones
    main_buttons = [
        Button("lvl1", 130, 427, 240, 82, (4, 184, 242), (3, 145, 191), Nivel1),
        Button("lvl2", 380, 427, 240, 82, (4, 184, 242), (3, 145, 191), Nivel2),
        Button("lvl3", 630, 427, 240, 82, (4, 184, 242), (3, 145, 191), Nivel3),
        Button("back", 25, 25, 150, 50, (128, 0, 0), (255, 0, 0), quit_game)
    ]

    # Bucle principal
    running = True
    while running:
        # Dibuja la imagen de fondo
        screen.blit(background_image, (0, 0))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar botones
        for button in main_buttons:
            button.draw(screen)

        pygame.display.flip()  
# FUNCION DE SELECCIONAR NIVEL


def start_game():

    print("Juego Iniciado")
    seleccionar.play()
    SeleccionarNivel()   

def show_options():
    global menu_state
    print("Mostrando Opciones")
    menu_state = "options"
    seleccionar.play()

def show_controls():
    seleccionar.play()
    if current_language == "english":
        show_controls_english()
    elif current_language == "spanish":
        show_controls_spanish()
    else:
        print("Language not supported")

def mute_all(sounds):
    global previous_volumes
    # Verificamos si ya está muteado (si el volumen de todos los sonidos es 0)
    is_muted = all(sound.get_volume() == 0 for sound in sounds)

    if is_muted:
        # Si ya está muteado, recuperamos los volúmenes previos y limpiamos el diccionario de volúmenes previos
        for sound in sounds:
            sound.set_volume(previous_volumes[sound])
        previous_volumes.clear()
    else:
        # Si no está muteado, guardamos los volúmenes actuales y establecemos todos los sonidos a volumen 0
        for sound in sounds:
            previous_volumes[sound] = sound.get_volume()
            sound.set_volume(0)

def go_back():
    global menu_state
    menu_state = "main"
    seleccionar.play()

def quit_game():
    pygame.quit()
    sys.exit()

def set_language(language):
    global current_language
    current_language = language
    seleccionar.play()

# Clase para los botones
class Button:
    def __init__(self, text, x, y, width, height, color, active_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active_color = active_color
        self.action = action

    def draw(self, screen):
        global last_click_time
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (self.x+self.width > mouse[0] > self.x and
            self.y+self.height > mouse[1] > self.y):
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))

            current_time = pygame.time.get_ticks()
            if click[0] == 1 and current_time - last_click_time > 500 and self.action is not None:
                self.action()
                last_click_time = current_time
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        font = pygame.font.Font("fuentes/minecraft.ttf", 30)
        text = font.render(self.text, True, white)
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

# Crear botones
main_buttons = [
    Button("Play", 400, 260, 200, 50, (0, 128, 0), (0, 255, 0), start_game),
    Button("Options", 400, 320, 200, 50, (0, 128, 128), (0, 255, 255), show_options),
    Button("Controls", 400, 380, 200, 50, (128, 0, 128), (255, 0, 255), show_controls),
    Button("Exit", 400, 440, 200, 50, (128, 0, 0), (255, 0, 0), quit_game)
]

option_buttons = [
    Button("Español", 400, 260, 200, 50, (0, 128, 0), (0, 255, 0), lambda: set_language("spanish")),
    Button("English", 400, 320, 200, 50, (0, 128, 128), (0, 255, 255), lambda: set_language("english")),
    Button("Sound", 400, 380, 200, 50, (128, 0, 128), (255, 0, 255), lambda: mute_all(music)),
    Button("Back", 400, 440, 200, 50, (128, 0, 0), (255, 0, 0), go_back)
]

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_image, (0, 0))

    # Actualiza el texto de los botones de acuerdo al idioma actual
    for i, text_key in enumerate(["play", "options", "controls", "exit"]):
        main_buttons[i].text = languages[current_language][text_key]
    for i, text_key in enumerate(["spanish", "english", "sound", "back"]):
        option_buttons[i].text = languages[current_language][text_key]

    if menu_state == "main":
        for button in main_buttons:
            button.draw(screen)
    elif menu_state == "options":
        for button in option_buttons:
            button.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

