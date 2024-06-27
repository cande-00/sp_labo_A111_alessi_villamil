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

#Leer la mejor racha global desde un archivo
#valor por defecto mechor_racha
def load_global_best_streak(filename="mejor_racha.txt",folder="data"):
    #a+ lectura y escritura, si no existe se crea el archivo
    file = open(filename, "a+")
    #mueve el puntero al inicio para 
    file.seek(0)
    #guardo en content la lectura del archivo
    content = file.read()
    #si el archivo tiene contenido, convierte el contenido, a un entero y lo retorna.
    if content:
        return int(content)
    return 0

#guardar la mejor racha global en un archivo
def save_global_best_streak(racha, filename="mejor_racha.txt",folder="data"):
    #w para leer el archivo
    with open(filename, "w") as file:
        #escribo en forma de cadena la racha en el archivo
        file.write(str(racha))

# Variables del juego
bandera = True
pokemon_actual = random.choice(lista_pokemons)
user_input = ""
guess = ""
mensaje = ""
tiempo_aux = 1
user_rect = pygame.Rect(200, 520, 140, 32)
input_bool = False
#almacena el tiempo transcurrido desde que se inicializo pygame
tiempo_entrada = pygame.time.get_ticks()
mejor_tiempo_transcurrido = float('inf')
tiempo_total = 0
respuesta_correcta = 0
tiempo_preguntado = []
racha = 0
mejor_racha = 0
global_mejor_racha = load_global_best_streak()
num_questions = 10

while bandera:
    ventana.fill(BACKGROUND)
    guess_pokemon(pokemon_actual, guess, mensaje)
    
    #calcula el tiempo transcurrido
    TIEMPO = (pygame.time.get_ticks() - tiempo_entrada) / 1000

    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            bandera = False
        #verifica si el evento donde se hizo click es la area del rectangulo 
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if user_rect.collidepoint(evento.pos):
                #permite la entrada del usuario 
                input_bool = True
            else: 
                input_bool = False
        if evento.type == pygame.KEYDOWN:
            if input_bool:
                #si se presionan teclas y es true la variable input_bool
                if evento.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif evento.key == pygame.K_RETURN:
                    #si se presiona enter, se calcula el tiempo transcurrido, se asigna a la variable y despues se añade a la lista
                    tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_entrada) / 1000
                    tiempo_preguntado.append(tiempo_transcurrido)
                    tiempo_total += tiempo_transcurrido
                    if user_input.lower() == pokemon_actual["nombre"].lower():
                        mensaje = "¡Correcto!"
                        respuesta_correcta += 1
                        racha += 1
                        if racha > mejor_racha:
                            mejor_racha = racha
                        if tiempo_transcurrido < mejor_tiempo_transcurrido:
                            mejor_tiempo_transcurrido = tiempo_transcurrido
                        if len(tiempo_preguntado) >= num_questions:
                            bandera = False
                        else:
                            pokemon_actual = random.choice(lista_pokemons)
                            tiempo_entrada = pygame.time.get_ticks()
                            user_input = ""
                    else:
                        mensaje = "¡Incorrecto! El Pokemon era " + pokemon_actual["nombre"]
                        if racha > global_mejor_racha:
                            global_mejor_racha = racha
                            save_global_best_streak(global_mejor_racha)
                        racha = 0
                        pokemon_actual = random.choice(lista_pokemons)
                        tiempo_entrata = pygame.time.get_ticks()
                        user_input = ""
                        
                else:
                    user_input += evento.unicode

    #mostrar tiempos y rachas en pantalla
    if tiempo_preguntado:
        render_text(f"Tiempo anterior: {tiempo_preguntado[-1]:.2f} segs", (width // 2 +150, 10), TEXT, 20)
    render_text(f"Mejor tiempo: {mejor_tiempo_transcurrido if mejor_tiempo_transcurrido != float('inf') else 0:.2f} segs", (width // 2 +150, 60), TEXT,20)
    render_text(f"Promedio de tiempo: {tiempo_total / len(tiempo_preguntado) if tiempo_preguntado else 0:.2f} segs", (width // 2 +150, 110), TEXT,20)
    render_text(f"Racha actual: {racha}", (width // 2 +150, 170), TEXT,20)
    render_text(f"Mejor racha global: {global_mejor_racha}", (width // 2 +150, 230), TEXT,20)

    pygame.draw.rect(ventana, SIDE_BOX_SELECTED, user_rect)
    user_text = fuente.render(user_input, True, INPUT_TEXT)
    ventana.blit(user_text, (user_rect.x + 5, user_rect.y + 5))
    user_rect.w = max(450, user_text.get_width() + 10)

    pygame.display.update()

#actualizar la mejor racha global al finalizar la partida
if racha > global_mejor_racha:
    global_mejor_racha = racha
    save_global_best_streak(global_mejor_racha)

# Mostrar resultados finales
print("Juego terminado")
print(f"Respuestas correctas: {respuesta_correcta}/{num_questions}")
print(f"Mejor tiempo de la partida: {mejor_tiempo_transcurrido:.2f} segundos")
print(f"Promedio de tiempo: {tiempo_total / len(tiempo_preguntado):.2f} segundos")
print(f"Mejor racha global: {global_mejor_racha}")

# Cerrar Pygame
pygame.quit()