from config.colores import *
import pygame
import random

pygame.init()

width, height = 853, 650
ventana = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adivina el Pokemon")
fuente = pygame.font.SysFont("Arial", 30)

keys = ["generacion", "nombre", "nombre_ingles", "nombre_frances", "nombre_italiano", "nombre_aleman", "imagen"]

with open("data/pokemon_multilingual_gen1.csv", "r") as pokemons:
    contenido = pokemons.read()
    lista_contenido = contenido.split("\n")
    lista_pokemons = []

    for i in range(1, len(lista_contenido)-1):
        lista_datos = lista_contenido[i].split(",")
        if len(lista_datos) >= len(keys):
            pokemon = dict()

            for j in range(len(keys)):
                pokemon[keys[j]] = lista_datos[j]

            lista_pokemons.append(pokemon)

def display_pokemon(pokemon:dict)->None:
    image = pygame.image.load(pokemon['imagen'])
    image = pygame.transform.scale(image, (400, 400))
    ventana.blit(image, (width//2 - 250, height//2 - 250))
    
def render_text(text, position, color, font_size=30):
    fuente = pygame.font.SysFont("Arial", font_size)
    text_surface = fuente.render(text, True, color)
    ventana.blit(text_surface, position)

def guess_pokemon(value:str,guess:str,mensaje:str)->None:
    display_pokemon(value)
    render_text("Adivina el Pokémon:", (width // 2 - 150, height // 2 + 160), TEXT)
    render_text(guess, (width // 2 - 150, height // 2 + 240), TEXT)
    render_text(mensaje, (width // 2 - 150, height // 2 + 240), TEXT)

bandera = True
pokemon_actual = random.choice(lista_pokemons)
user_input = ""
guess = ""
mensaje = ""
tiempo_aux = 1
user_rect = pygame.Rect(200,520,140,32)
input_bool = False

while bandera:
    ventana.fill(BACKGROUND)
    guess_pokemon(pokemon_actual, guess, mensaje)
    TIEMPO = pygame.time.get_ticks()/1000
    if tiempo_aux  == TIEMPO:  
        tiempo_aux += 1
        print(TIEMPO)

    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            bandera = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if user_rect.collidepoint(evento.pos):
                input_bool = True
            else: 
                input_bool = False
        if evento.type == pygame.KEYDOWN:
            if input_bool:
                if evento.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif evento.key == pygame.K_RETURN:
                    if user_input.lower() == pokemon_actual["nombre"].lower():
                        mensaje = "¡Correcto!"
                    else:
                        mensaje = "¡Incorrecto! El Pokemon era " + pokemon_actual["nombre"]
                    # Actualiza pokemon_actual con un nuevo pokemon aleatorio
                    pokemon_actual = random.choice(lista_pokemons)
                    user_input = ""
                else:
                    user_input += evento.unicode
                
                
    # contador = fuente.render("Time Taken: "+str(TIEMPO),0,(TEXT))
    # ventana.blit(contador,(100,100))
    
    # guess_text = fuente.render(guess, True, TEXT)
    # ventana.blit(guess_text, (width // 2 - guess_text.get_width() // 2, height // 2 + 150))
    pygame.draw.rect(ventana, SIDE_BOX_SELECTED, user_rect)
    user_text = fuente.render(user_input, True, INPUT_TEXT)
    ventana.blit(user_text, (user_rect.x + 5, user_rect.y + 5))
    user_rect.w = max(450, user_text.get_width() + 10)

    pygame.display.update()

pygame.quit()