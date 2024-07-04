import pygame
from config.colores import * 

pygame.init()

width, height = 853, 650
ventana = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adivina el Pokemon")
fuente = pygame.font.SysFont("Arial", 30)

keys_dict = ["generacion", "nombre", "nombre_ingles", "nombre_frances", "nombre_italiano", "nombre_aleman", "imagen", "imagen_sombreada", "imagen_pixeleada"]

with open("data/pokemon_multilingual_gen1.csv", "r") as pokemons:
    contenido = pokemons.read()

    lista_contenido = contenido.split("\n")
    lista_pokemons = []

    for i in range(1, len(lista_contenido) - 1):
        lista_datos = lista_contenido[i].split(",")
        if len(lista_datos) >= len(keys_dict):
            pokemon = dict()

            for j in range(len(keys_dict)):
                pokemon[keys_dict[j]] = lista_datos[j]

            lista_pokemons.append(pokemon)

generacion_1 = []
generacion_2 = []
generacion_3 = []
generacion_4 = []
generacion_5 = []
generacion_6 = []
generacion_7 = []
generacion_8 = []
generacion_9 = []

for pokemon in lista_pokemons:
    generacion = pokemon["generacion"]
    match generacion:
        case "1":
            generacion_1.append(pokemon)
        case "2":
            generacion_2.append(pokemon)
        case "3":
            generacion_3.append(pokemon)
        case "4":
            generacion_4.append(pokemon)
        case "5":
            generacion_5.append(pokemon)
        case "6":
            generacion_6.append(pokemon)
        case "7":
            generacion_7.append(pokemon)
        case "8":
            generacion_8.append(pokemon)
        case "9":
            generacion_9.append(pokemon)

matriz_generacion = [
    [generacion_1, generacion_2, generacion_3],
    [generacion_4, generacion_5, generacion_6],
    [generacion_7, generacion_8, generacion_9]
]

for fila in matriz_generacion:
    for celda in fila:
        print(f"{len(celda)} pokemones", end=" | ")
    print()

def display_pokemon(pokemon: dict, modo: str) -> None:
    if modo == "facil":
        image_path = pokemon['imagen']
    elif modo == "medio":
        image_path = pokemon['imagen_sombreada']
    elif modo == "dificil":
        image_path = pokemon['imagen_pixeleada']

    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (400, 400))
    ventana.blit(image, (width // 2 - 200, height // 2 - 200))

def render_text(text, position, color, font_size=30):
    fuente = pygame.font.SysFont("Arial", font_size)
    text_surface = fuente.render(text, True, color)
    ventana.blit(text_surface, position)

def mostrar_nombres(nombre_1:str, nombre_2:str, nombre_3:str, nombre_4:str) ->None:
    render_text("Nombres: ",(width // 2 - 415, height // 2 + 50), TEXT,25)
    render_text(f"ingles: {nombre_1}", (width // 2 - 415, height // 2 + 80), TEXT,20)
    render_text(f"frances: {nombre_2}", (width // 2 - 415, height // 2 + 110), TEXT,20)
    render_text(f"italiano: {nombre_3}", (width // 2 - 415, height // 2 + 140), TEXT,20)
    render_text(f"aleman: {nombre_4}", (width // 2 - 415, height // 2 + 170), TEXT,20)

def guess_pokemon(value:dict, guess:str, mensaje:str, modo: str, nombre_1:str, nombre_2:str, nombre_3:str, nombre_4:str) -> None:
    display_pokemon(value, modo)
    render_text("Adivina el Pokémon:", (width // 2 - 150, height // 2 + 160), TEXT)
    render_text(guess, (width // 2 - 150, height // 2 + 240), TEXT)
    render_text(mensaje, (width // 2 - 150, height // 2 + 240), TEXT)
    mostrar_nombres(nombre_1, nombre_2, nombre_3, nombre_4)


def load_global_best_streak(filename="mejor_racha.txt", folder="data"):
    file = open(filename, "a+")
    file.seek(0)
    content = file.read()
    if content:
        return int(content)
    return 0

global_mejor_racha = load_global_best_streak()

def save_global_best_streak(racha, filename="mejor_racha.txt", folder="data"):
    with open(filename, "w") as file:
        file.write(str(racha))

def mostrar_resultados():
    ventana.fill(BLACK)
    render_text("PARTIDA TERMINADA", (width // 2 - 150, height // 2 - 250), TEXT, 40)
    render_text(f"Aciertos: {respuesta_correcta}/{num_questions}", (width // 2 - 150, height // 2 - 100), TEXT)
    render_text(f"Mejor tiempo de la partida: {mejor_tiempo_transcurrido:.2f} segs", (width // 2 - 150, height // 2 - 50), TEXT)
    render_text(f"Tiempo total: {tiempo_total:.2f} segs", (width // 2 - 150, height // 2), TEXT)
    render_text(f"Mejor racha global: {global_mejor_racha}", (width // 2 - 150, height // 2 + 50), TEXT)

    jugar_nuevamente_btn = pygame.Rect(width // 2 - 100, height // 2 + 100, 220, 50)
    pygame.draw.rect(ventana, (SIDE_BOX), jugar_nuevamente_btn)
    render_text("Volver a jugar", (jugar_nuevamente_btn.x + 20, jugar_nuevamente_btn.y + 10), BACKGROUND)

    pygame.display.update()
    return jugar_nuevamente_btn

botones_modo = {
    "facil": pygame.Rect(10, 200, 100, 40),
    "medio": pygame.Rect(10, 250, 100, 40),
    "dificil": pygame.Rect(10, 300, 100, 40)
}

def draw_generation_selection(selected_generations):
    render_text("Generaciones:", (10, 10), TEXT)
    for i in range(rows):
        for j in range(cols):
            gen = i * cols + j + 1
            x = 10 + j * (button_width + spacing)
            y = 50 + i * (button_height + spacing)
            color = SIDE_BOX_SELECTED if gen in selected_generations else SIDE_BOX
            pygame.draw.rect(ventana, color, (x, y, button_width, button_height))
            render_text(f"Gen {gen}", (x + 10, y + 10), TEXT if gen in selected_generations else TEXT, 15)

def get_pokemons_by_generation(selected_generations):
    pokemons = []
    for gen in selected_generations:
        row = (gen - 1) // cols
        col = (gen - 1) % cols
        pokemons += matriz_generacion[row][col]
    return pokemons

button_width = 60
button_height = 30
spacing = 5
rows = 3
cols = 3
bandera = True
jugando = True
pokemon_actual = {}
nombre_ingles = ""
nombre_frances = ""
nombre_italiano = ""
nombre_aleman = ""
user_input = ""
guess = ""
mensaje = ""
tiempo_aux = 1
user_rect = pygame.Rect(200, 520, 140, 32)
input_bool = False
tiempo_entrada = pygame.time.get_ticks()
mejor_tiempo_transcurrido = float('inf')
tiempo_total = 0
tiempo_preguntado = []
calcular_promedio = lambda total, tiempos: total / len(tiempos) if tiempos else 0
respuesta_correcta = 0
racha = 0
mejor_racha = 0
imagenes_mostradas = 0
num_questions = 10
generaciones_seleccionadas = set()
modo = "facil"
preguntas_realizadas = 0