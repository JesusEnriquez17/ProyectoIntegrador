import pygame
import sys

# Inicializar pygame y configurar ventana
pygame.init()
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
    pygame.quit()
    sys.exit()

# Crear botones
main_buttons = [
    Button("<~~", 25, 25, 100, 50, (4, 184, 242), (3, 145, 191), quit_game)
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

pygame.quit()
sys.exit()