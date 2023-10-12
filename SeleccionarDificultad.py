import pygame
import sys

# Inicializar pygame y configurar ventana
pygame.init()
screen_size = (1000, 575)
screen = pygame.display.set_mode(screen_size)

# Cargar recursos
background_image_original = pygame.image.load('img/Botones/FondoDificultad.png')
background_image = pygame.transform.scale(background_image_original, screen_size)
button1__image = pygame.image.load('img/Botones/Nivel1.png')
button3__image = pygame.image.load('img/Botones/Nivel3.png')
close_button_image_original = pygame.image.load('img/Botones/Regresar.png')
close_button_image = pygame.transform.scale(close_button_image_original, (128, 128))

# Para la música
seleccionar = pygame.mixer.Sound('sounds/Selec.wav')

# Clase Button
class Button:
    def __init__(self, image, x, y, text, callback=None):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.text = text
        self.callback = callback

    def display(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
            print(f'{self.text} seleccionado')
            seleccionar.play()
            if self.callback:
                self.callback()



# Funciones callback para los botones
def on_button1_click():
    print("Facil")
   

def on_button3_click():
    print("Dificil")

def on_close_button_click():
    global running
    running = False

# Inicializar botones individualmente
button1 = Button(button1__image, 250, 300, 'Facil', on_button1_click)
button3 = Button(button3__image, 750, 300, 'Dificil', on_button3_click)
close_button = Button(close_button_image, 80, 35, 'Cerrar', on_close_button_click)

# Bucle principal
running = True
while running:
    screen.blit(background_image, (0, 0))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Interactuar con botones
        button1.handle_event(event)
        
        button3.handle_event(event)
        close_button.handle_event(event)

    # Dibujar botones
    button1.display(screen)
    
    button3.display(screen)
    close_button.display(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
