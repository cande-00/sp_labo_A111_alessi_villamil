import pygame
from config.colores import * 

pygame.init()

global respuesta_correcta
global mejor_tiempo_transcurrido
global tiempo_total
global tiempo_preguntado
global global_mejor_racha


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
user_rect = pygame.Rect(200, 520, 140, 32)
input_bool = False

tiempo_aux = 1
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

width, height = 853, 650
ventana = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adivina el Pokemon")
fuente = pygame.font.SysFont("Arial", 30)

#se define una lista con las claves que se usan para los diccionarios
keys_dict = ["generacion", "nombre", "nombre_ingles", "nombre_frances", "nombre_italiano", "nombre_aleman", "imagen", "imagen_sombreada", "imagen_pixeleada"]


with open("data/pokemon_multilingual_gen1.csv", "r") as pokemons:
#Descripcion:
            #se abre y se lee el archivo, se guarda en la variable contenido,
            #se divide el contenido en lineas individuales creando una lista con cada linea
            #se itera en cada linea exceptuando la primera y ultima linea
            #si la cantidad de valores es suficiente se crea un dict pokemon y se asigna los valores a las claves definidas key_dict
            #se agrega pokemon a la lista_pokemons
    contenido = pokemons.read()

    lista_contenido = contenido.split("\n")    
    lista_pokemons = []

    for i in range(1, len(lista_contenido) - 1):
        #cada linea se divide por comas
        lista_datos = lista_contenido[i].split(",")
        if len(lista_datos) >= len(keys_dict):
            pokemon = dict()

            for j in range(len(keys_dict)):
                pokemon[keys_dict[j]] = lista_datos[j]
            lista_pokemons.append(pokemon)

#se crean los dicts para ser usados 
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

#se crea una matriz que contiene en cada elemento, las lista con la generacion correspondiente
matriz_generacion = [
    [generacion_1, generacion_2, generacion_3],
    [generacion_4, generacion_5, generacion_6],
    [generacion_7, generacion_8, generacion_9]
]

def display_pokemon(pokemon: dict, modo: str) -> None:
#Descripcion:
            #dependiendo de cada modo, la variable image_path cambia a un tipo de imagen diferente
            #se lodea la imagen de la generacion correspondiente
            #se escala para que todas tengan el mismo tamaño
            #se blitea en la mitad de la pantalla
#Parametros:
            #pokemons: diccionario general donde se encuentran los pokemones
            #modo: string que delimita que modo va a ser
#Return:
            #None

    if modo == "facil":
        image_path = pokemon['imagen']
    elif modo == "medio":
        image_path = pokemon['imagen_sombreada']
    elif modo == "dificil":
        image_path = pokemon['imagen_pixeleada']

    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (400, 400))
    ventana.blit(image, (width // 2 - 200, height // 2 - 200))

def render_text(text:str, position, color, font_size=30) -> None:
#Descripcion:
            #se renderiza cada texto que es pasado en una font size determinado
#Parametros:
            #text: string que es pasado para sar mostrado
            #position: tupla que significa el lugar donde va a ser mostrado
            #color: color del texto
            #font_size: entero que establece el tamaño del texto
#Return:
            #None

    fuente = pygame.font.SysFont("Arial", font_size)
    text_surface = fuente.render(text, True, color)
    ventana.blit(text_surface, position)

def mostrar_nombres(nombre_1:str, nombre_2:str, nombre_3:str, nombre_4:str) -> None:
#Descripcion:
            #renderiza los nombres en otros idiomas que son usados para los pokemones
#Parametros:
            #nombre del 1 al 4 que son strings y la cantidad de nombres que se necesitan mostrar
#Return:
            #None

    render_text("Nombres: ",(width // 2 - 415, height // 2 + 50), TEXT,25)
    render_text(f"ingles: {nombre_1}", (width // 2 - 415, height // 2 + 80), TEXT,20)
    render_text(f"frances: {nombre_2}", (width // 2 - 415, height // 2 + 110), TEXT,20)
    render_text(f"italiano: {nombre_3}", (width // 2 - 415, height // 2 + 140), TEXT,20)
    render_text(f"aleman: {nombre_4}", (width // 2 - 415, height // 2 + 170), TEXT,20)

def guess_pokemon(value:dict, guess:str, mensaje:str, modo: str, nombre_1:str, nombre_2:str, nombre_3:str, nombre_4:str) -> None:
#Descripcion:
            #se muestra el pokemon del dict y el modo elegido
            #se renderiza el texto, lo que el user va a adivinar y el mensaje correspondiente a si es correcto o incorrecto
            #después se muestran los nombres correspondientes al pokemon en pantalla
#Parametros:
            #value: diccionario general donde se encuentran los pokemones
            #guess: string la adivinanza actual del jugador
            #mensaje: string que se muestra dependiendo de si es correcto o incorrecto
            #modo: string, el modo que se muestra del juego (facil, medio, dificil)
            #nombres del 1 al 4 que representan los nombres en distintos idiomas (ingles, frances, italiano, aleman)
#Return:
            #None

    display_pokemon(value, modo)
    render_text("Adivina el Pokémon:", (width // 2 - 150, height // 2 + 160), TEXT)
    render_text(guess, (width // 2 - 150, height // 2 + 240), TEXT)
    render_text(mensaje, (width // 2 - 150, height // 2 + 240), TEXT)
    mostrar_nombres(nombre_1, nombre_2, nombre_3, nombre_4)


def load_global_best_streak(filename="mejor_racha.txt", folder="data"):
    #Descripción: carga la mejor racha global de aciertos desde un archivo.
    #Parámetros:
    #filename (str): nombre del archivo que contiene la mejor racha global.
    #folder (str): nombre de la carpeta donde se encuentra el archivo.
    #Retorno: 
    # int: devuelve la mejor racha global.   
    file = open(filename, "a+")
    file.seek(0)
    content = file.read()
    if content:
        return int(content)
    return 0

global_mejor_racha = load_global_best_streak()

def save_global_best_streak(racha, filename="mejor_racha.txt", folder="data"):
    #Descripción: guarda la mejor racha global en un archivo.
    #Parámetros:
    #racha (int): es la mejor racha global que se guardará.
    #filename (str): nombre del archivo que contiene la mejor racha global. 
    #folder (str): Carpeta donde se encuentra el archivo.
    with open(filename, "w") as file:
        file.write(str(racha))

def mostrar_resultados():
    global respuesta_correcta, mejor_tiempo_transcurrido, tiempo_total, tiempo_preguntado, global_mejor_racha
    #Descripción:
    #muestra los resultados de la partida cuando finaliza y muestra un botón para "volver a jugar".
    #Retorno:
    #jugar_nuevamente_btn (pygame.Rect):devulve el rectángulo del botón "volver a jugar".
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
    #Descripción: dibuja las generaciones seleccionadas por el usuario en la pantalla.
    #Parámetros:
    #selected_generations (list): es la lista de generaciones seleccionadas.
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
    #Descripción: obtiene una lista de Pokémon a partir de las generaciones seleccionadas.
    #Parámetros:
    #selected_generations (list): es la lista de las generaciones seleccionadas.
    #Retorno:
    #list: devuelve una lista de Pokémon de las generaciones seleccionadas.
    pokemons = []
    for gen in selected_generations:
        row = (gen - 1) // cols
        col = (gen - 1) % cols
        pokemons += matriz_generacion[row][col]
    return pokemons

