import pygame
import random
from config.colores import *
from config.funciones import *

pygame.init()

width, height = 853, 650
ventana = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adivina el Pokemon")
fuente = pygame.font.SysFont("Arial", 30)

#bandera principal de pygame
while bandera:
    #bandera si el juego esta activo o no
    if jugando:
        ventana.fill(BACKGROUND)
        
        #se dibuja las generaciones seleccionadas
        draw_generation_selection(generaciones_seleccionadas)

        #si no es none (pokemon_actual contiene los datos del pokemon que el jugador debe adivinar) se llama a la funcion guess_pokemon
        if pokemon_actual:
            guess_pokemon(pokemon_actual, guess, mensaje, modo, nombre_ingles, nombre_frances, nombre_italiano, nombre_aleman)
        
        #devuelve el tiempo en milisegundos desde que inicio pygame
        TIEMPO = (pygame.time.get_ticks() - tiempo_entrada) / 1000

        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                bandera = False
            #si el evento es un click en la posicion mouse_x, mouse_y el la var bool es False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos
                generation_clicked = False
                #se itera sobre las posiciones de los botones de generacion en cuadricula
                for i in range(rows):
                    for j in range(cols):
                        #se calcula el num de gen basado en la posicion de la cuadricula
                        gen = i * 3 + j + 1
                        #calcula las cordenadas
                        x = 10 + j * (button_width + spacing)
                        y = 50 + i * (button_height + spacing)
                        #si la posicion del raton esta dentro de los limites del boton la var bool vuelve a true
                        if x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height:
                            generation_clicked = True
                            #se quita la gen si ya esta seleccionada si no se añade
                            if gen in generaciones_seleccionadas:
                                generaciones_seleccionadas.remove(gen)
                            else:
                                generaciones_seleccionadas.add(gen)
                            #filtramos los pokemones segun las gens seleccionadas
                            pokemones_filtrados = get_pokemons_by_generation(generaciones_seleccionadas)
                            #se comprueba que hay pokemones disponibles despues del filtrado
                            if pokemones_filtrados:
                                #seleccionamos un indice aleatorio de la lista y se asigna a pokemon_actual
                                pokemon_index = random.randint(0, len(pokemones_filtrados) - 1)
                                pokemon_actual = pokemones_filtrados[pokemon_index]
                if generation_clicked:
                    pass
                #si no se hace click en el boton generation_clicked se ejecuta el codigo
                else:
                    #creamos una lista con las key de la lista botones_modo e iteramos para recorrer las claves
                    keys = list(botones_modo.keys())
                    for i in range(len(keys)):
                        #en key se obtiene la clave en posicion i y rect se obtiene el rect asociado a esa clave
                        key = keys[i]
                        rect = botones_modo[key]
                        #si existe un click dentro del rect
                        if rect.collidepoint(evento.pos):
                            #cambiamos el modo a la clave correspondiente
                            modo = key
                            print(f"Modo cambiado a: {modo}")
                            break
                #maneja el clic en el botón "mostrar nombre"
                if boton_mostrar_nombre.collidepoint(evento.pos):  
                    mensaje = f"¡El pokemon era {pokemon_actual['nombre']}!"
                    nombre_ingles = pokemon_actual["nombre_ingles"]
                    nombre_frances = pokemon_actual["nombre_frances"]
                    nombre_italiano = pokemon_actual["nombre_italiano"]
                    nombre_aleman = pokemon_actual["nombre_aleman"]
                    #se vuelve a elegir un indice aleatorio y se manda a pokemon_actual
                    pokemon_index = random.randint(0, len(pokemones_filtrados) - 1)
                    pokemon_actual = pokemones_filtrados[pokemon_index]
                    #se espera medio segundo entre cada pokemon
                    pygame.time.wait(500)
                    #si la racha es mayor a la racha global, racha global pasa a tener el valor de racha y se salva en el .txt
                    if racha > global_mejor_racha:
                        global_mejor_racha = racha
                        save_global_best_streak(global_mejor_racha)
                    racha = 0
                    preguntas_realizadas += 1
                    #si preguntas realizadas es del mismo valor que num_questions el juego se para pero no se cierra
                    if preguntas_realizadas == num_questions:
                        jugando = False
                    else:
                        #volvemos a filtrar los pokemones
                        pokemones_filtrados = get_pokemons_by_generation(generaciones_seleccionadas)
                        #si la lista no esta vacia, se genera un indice aleatorio entre 1 y el tamaño de la lista menos 1 y asignamos el pokemon correspondiente indice a pokemon_actual
                        if pokemones_filtrados:
                            pokemon_index = random.randint(0, len(pokemones_filtrados) - 1)
                            pokemon_actual = pokemones_filtrados[pokemon_index]
                        #registramos el timepo
                        tiempo_entrada = pygame.time.get_ticks()
            #si se presiona una tecla y si la entrada de texto esta activa, y si el evento es borrar, se borrar el ultimo caracter de user input
            #esta parte sirve para borrar si es que el jugador se equivoco
            if evento.type == pygame.KEYDOWN:
                if input_bool:
                    if evento.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    #en cambio si se presiona enter, calculamos el tiempo transcurrido que se incio, se agrega el tiempo transcurrido a la lista y se suma a tiempo_total
                    #se incrementa el contador de preguntas
                    elif evento.key == pygame.K_RETURN:
                        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_entrada) / 1000
                        tiempo_preguntado.append(tiempo_transcurrido)
                        tiempo_total += tiempo_transcurrido
                        preguntas_realizadas += 1
                        #si lo que escribio el jugador es igual al nombre del pokemon en pantalla:
                        #se muestra el mensaje y los nombres del pokemon en distintos idiomas, se incrementa la respuesta y la racha
                        if user_input.lower() == pokemon_actual["nombre"].lower():
                            mensaje = "¡Correcto!"
                            nombre_ingles = pokemon_actual["nombre_ingles"]
                            nombre_frances = pokemon_actual["nombre_frances"]
                            nombre_italiano = pokemon_actual["nombre_italiano"]
                            nombre_aleman = pokemon_actual["nombre_aleman"]
                            respuesta_correcta += 1
                            racha += 1
                            #si racha es mayor que mejor_racha, mejor_racha toma el valor de racha
                            if racha > mejor_racha:
                                mejor_racha = racha
                            #si tiempo_transcurrido es menor al mejor_tiempo, mejor_tiempo toma el valor de tiempo 
                            if tiempo_transcurrido < mejor_tiempo_transcurrido:
                                mejor_tiempo_transcurrido = tiempo_transcurrido
                        else:
                            #si el jugador se equivoca, se muestra el mensaje con el pokemon correcto mas sus nombres en distintos idiomas
                            #si la racha es mayor a la global_mejor_racha, global_mejor_racha toma el valor de racha y se llama a la funcion para ser guardada en el .txt
                            mensaje = f"¡Incorrecto! El Pokémon era {pokemon_actual['nombre']}"
                            nombre_ingles = pokemon_actual["nombre_ingles"]
                            nombre_frances = pokemon_actual["nombre_frances"]
                            nombre_italiano = pokemon_actual["nombre_italiano"]
                            nombre_aleman = pokemon_actual["nombre_aleman"]
                            if racha > global_mejor_racha:
                                global_mejor_racha = racha
                                save_global_best_streak(global_mejor_racha)
                            #racha vuelve a cero
                            racha = 0
                        #si preguntas realizadas es del mismo valor que num_questions el juego se para pero no se cierra
                        if preguntas_realizadas == num_questions:
                            jugando = False
                        else:
                            #de no ser asi, se filtran los pokemones y se llama a la funcion para tener los pokemones de las gens seleccionadas
                            pokemones_filtrados = get_pokemons_by_generation(generaciones_seleccionadas)
                            if pokemones_filtrados:
                                #si la lista no esta vacia, se elije el indice de un pokemon al azar y lo asignamos a pokemon actual
                                pokemon_index = random.randint(0, len(pokemones_filtrados) - 1)
                                pokemon_actual = pokemones_filtrados[pokemon_index]
                            #el tiempo de entrada vuelve a ser llamado y se "limpia" donde escribe el jugador
                            tiempo_entrada = pygame.time.get_ticks()
                            user_input = ""
                    else:
                        #obtiene el caracter correspondiente de cada tecla
                        user_input += evento.unicode
            #si se hace click dentro del area se activa donde escribe el jugador, si no, se desactiva
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if user_rect.collidepoint(evento.pos):
                    input_bool = True
                else:
                    input_bool = False

       #definir boton mostrar nombre
        boton_mostrar_nombre = pygame.Rect(width // 2 - 420, height // 2 + 250, 235, 40)

        #se muestra en pantalla los distintos tiempos, la racha y la racha global
        if tiempo_preguntado:
            render_text(f"Tiempo anterior: {tiempo_preguntado[-1]:.2f} segs", (width // 2 + 150, 10), TEXT, 20)
        render_text(f"Tiempo transcurrido: {TIEMPO:.2f} segs", (width // 2 + 150, 60), TEXT, 20)
        render_text(f"Mejor tiempo: {mejor_tiempo_transcurrido if mejor_tiempo_transcurrido != float('inf') else 0:.2f} segs", (width // 2 + 150, 110), TEXT, 20)
        render_text(f"Promedio de tiempo: {calcular_promedio(tiempo_total, tiempo_preguntado):.2f} segs", (width // 2 + 150, 170), TEXT, 20)
        render_text(f"Racha actual: {racha}", (width // 2 + 150, 230), TEXT, 20)
        render_text(f"Mejor racha global: {global_mejor_racha}", (width // 2 + 150, 290), TEXT, 20)

        #convierto las claves en una lista e itero sobre cada clave de la lista
        keys = list(botones_modo.keys())
        for i in range(len(keys)):
            key = keys[i]
            rect = botones_modo[key]
            #determino el color del rect segun el modo seleccionado
            color = SIDE_BOX_SELECTED if key == modo else SIDE_BOX
            #dibujo el rect en la pantalla
            pygame.draw.rect(ventana, color, rect)
            #renderuzi ek texto del boton
            render_text(key.capitalize(), (rect.x + 10, rect.y + 10), TEXT, 20)

        #dibujo el rect donde escribe el jugador
        pygame.draw.rect(ventana, TEXT, user_rect)
        #renderizo el texto introducido por el usuario
        user_text = fuente.render(user_input, True, INPUT_TEXT)
        ventana.blit(user_text, (user_rect.x + 5, user_rect.y + 5))
        user_rect.w = max(450, user_text.get_width() + 10)

        #renderizar el btn de mostrar nombre
        pygame.draw.rect(ventana, SIDE_BOX, boton_mostrar_nombre)
        render_text("Mostrar Nombre", (boton_mostrar_nombre.x + 10, boton_mostrar_nombre.y + 5), TEXT)
        
        pygame.display.update()
    #si el juego no esta activo
    else:
        #se muestran los resultados totales de la partida
        jugar_nuevamente_btn = mostrar_resultados(respuesta_correcta, mejor_tiempo_transcurrido, tiempo_total, global_mejor_racha)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                bandera = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if jugar_nuevamente_btn.collidepoint(evento.pos):
                    #reiniciar variables para una nueva partida
                    preguntas_realizadas = 0
                    respuesta_correcta = 0
                    racha = 0
                    tiempo_total = 0
                    tiempo_preguntado = []
                    mejor_tiempo_transcurrido = float('inf')
                    pokemon_actual = {}
                    user_input = ""
                    mensaje = ""
                    jugando = True
#si racha es mayor a global_mejor_racha, esta toma el valor de racha y es guardada en el .txt
if racha > global_mejor_racha:
    global_mejor_racha = racha
    save_global_best_streak(global_mejor_racha)

print("Juego terminado")
print(f"Respuestas correctas: {respuesta_correcta}/{num_questions}")
print(f"Mejor tiempo de la partida: {mejor_tiempo_transcurrido:.2f} segundos")
print(f"Promedio de tiempo: {tiempo_total / len(tiempo_preguntado):.2f} segundos")
print(f"Mejor racha global: {global_mejor_racha}")

pygame.quit()