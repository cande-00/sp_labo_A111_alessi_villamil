import pygame
import random
from config.colores import *
from config.funciones import *

pygame.init()

width, height = 853, 650
ventana = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adivina el Pokemon")
fuente = pygame.font.SysFont("Arial", 30)

while bandera:
    if jugando:
        ventana.fill(BACKGROUND)
        draw_generation_selection(generaciones_seleccionadas)

        if pokemon_actual:
            guess_pokemon(pokemon_actual, guess, mensaje, modo, nombre_ingles, nombre_frances, nombre_italiano, nombre_aleman)

        TIEMPO = (pygame.time.get_ticks() - tiempo_entrada) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                bandera = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos
                generation_clicked = False
                for i in range(rows):
                    for j in range(cols):
                        gen = i * 3 + j + 1
                        x = 10 + j * (button_width + spacing)
                        y = 50 + i * (button_height + spacing)
                        if x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height:
                            generation_clicked = True
                            if gen in generaciones_seleccionadas:
                                generaciones_seleccionadas.remove(gen)
                            else:
                                generaciones_seleccionadas.add(gen)
                            filtered_pokemons = get_pokemons_by_generation(generaciones_seleccionadas)
                            if filtered_pokemons:
                                pokemon_index = random.randint(0, len(filtered_pokemons) - 1)
                                pokemon_actual = filtered_pokemons[pokemon_index]
                if generation_clicked:
                    pass
                else:
                    keys = list(botones_modo.keys())
                    for i in range(len(keys)):
                        key = keys[i]
                        rect = botones_modo[key]
                        if rect.collidepoint(evento.pos):
                            modo = key
                            print(f"Modo cambiado a: {modo}")
                            break
                #maneja el clic en el botón "mostrar nombre"
                if boton_mostrar_nombre.collidepoint(evento.pos):  
                    mensaje = f"¡{pokemon_actual['nombre']}!"
                    pokemon_index = random.randint(0, len(filtered_pokemons) - 1)
                    pokemon_actual = filtered_pokemons[pokemon_index]
                    pygame.time.wait(500)
                    if racha > global_mejor_racha:
                        global_mejor_racha = racha
                        save_global_best_streak(global_mejor_racha)
                    racha = 0
                    preguntas_realizadas += 1
                    if preguntas_realizadas == num_questions:
                        jugando = False
                    else:
                        filtered_pokemons = get_pokemons_by_generation(generaciones_seleccionadas)
                        if filtered_pokemons:
                            pokemon_index = random.randint(0, len(filtered_pokemons) - 1)
                            pokemon_actual = filtered_pokemons[pokemon_index]
                        tiempo_entrada = pygame.time.get_ticks()

            if evento.type == pygame.KEYDOWN:
                if input_bool:
                    if evento.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif evento.key == pygame.K_RETURN:
                        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_entrada) / 1000
                        tiempo_preguntado.append(tiempo_transcurrido)
                        tiempo_total += tiempo_transcurrido
                        preguntas_realizadas += 1
                        if user_input.lower() == pokemon_actual["nombre"].lower():
                            mensaje = "¡Correcto!"
                            nombre_ingles = pokemon_actual["nombre_ingles"]
                            nombre_frances = pokemon_actual["nombre_frances"]
                            nombre_italiano = pokemon_actual["nombre_italiano"]
                            nombre_aleman = pokemon_actual["nombre_aleman"]
                            respuesta_correcta += 1
                            racha += 1
                            if racha > mejor_racha:
                                mejor_racha = racha
                            if tiempo_transcurrido < mejor_tiempo_transcurrido:
                                mejor_tiempo_transcurrido = tiempo_transcurrido
                        else:
                            mensaje = f"¡Incorrecto! El Pokémon era {pokemon_actual['nombre']}"
                            nombre_ingles = pokemon_actual["nombre_ingles"]
                            nombre_frances = pokemon_actual["nombre_frances"]
                            nombre_italiano = pokemon_actual["nombre_italiano"]
                            nombre_aleman = pokemon_actual["nombre_aleman"]
                            if racha > global_mejor_racha:
                                global_mejor_racha = racha
                                save_global_best_streak(global_mejor_racha)
                            racha = 0
                        if preguntas_realizadas == num_questions:
                            jugando = False
                        else:
                            filtered_pokemons = get_pokemons_by_generation(generaciones_seleccionadas)
                            if filtered_pokemons:
                                pokemon_index = random.randint(0, len(filtered_pokemons) - 1)
                                pokemon_actual = filtered_pokemons[pokemon_index]
                            tiempo_entrada = pygame.time.get_ticks()
                            user_input = ""
                    else:
                        user_input += evento.unicode
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if user_rect.collidepoint(evento.pos):
                    input_bool = True
                else:
                    input_bool = False

       #definir boton mostrar nombre
        boton_mostrar_nombre = pygame.Rect(width // 2 - 420, height // 2 + 250, 235, 40)

        if tiempo_preguntado:
            render_text(f"Tiempo anterior: {tiempo_preguntado[-1]:.2f} segs", (width // 2 + 150, 10), TEXT, 20)
        render_text(f"Tiempo transcurrido: {TIEMPO:.2f} segs", (width // 2 + 150, 60), TEXT, 20)
        render_text(f"Mejor tiempo: {mejor_tiempo_transcurrido if mejor_tiempo_transcurrido != float('inf') else 0:.2f} segs", (width // 2 + 150, 110), TEXT, 20)
        render_text(f"Promedio de tiempo: {calcular_promedio(tiempo_total, tiempo_preguntado):.2f} segs", (width // 2 + 150, 170), TEXT, 20)
        render_text(f"Racha actual: {racha}", (width // 2 + 150, 230), TEXT, 20)
        render_text(f"Mejor racha global: {global_mejor_racha}", (width // 2 + 150, 290), TEXT, 20)

        keys = list(botones_modo.keys())
        for i in range(len(keys)):
            key = keys[i]
            rect = botones_modo[key]
            color = SIDE_BOX_SELECTED if key == modo else SIDE_BOX
            pygame.draw.rect(ventana, color, rect)
            render_text(key.capitalize(), (rect.x + 10, rect.y + 10), TEXT, 20)

        pygame.draw.rect(ventana, TEXT, user_rect)
        user_text = fuente.render(user_input, True, INPUT_TEXT)
        ventana.blit(user_text, (user_rect.x + 5, user_rect.y + 5))
        user_rect.w = max(450, user_text.get_width() + 10)

        #renderizar el btn de mostrar nombre
        pygame.draw.rect(ventana, SIDE_BOX, boton_mostrar_nombre)
        render_text("Mostrar Nombre", (boton_mostrar_nombre.x + 10, boton_mostrar_nombre.y + 5), TEXT)
        
        pygame.display.update()
    else:
        jugar_nuevamente_btn = mostrar_resultados()
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

if racha > global_mejor_racha:
    global_mejor_racha = racha
    save_global_best_streak(global_mejor_racha)

print("Juego terminado")
print(f"Respuestas correctas: {respuesta_correcta}/{num_questions}")
print(f"Mejor tiempo de la partida: {mejor_tiempo_transcurrido:.2f} segundos")
print(f"Promedio de tiempo: {tiempo_total / len(tiempo_preguntado):.2f} segundos")
print(f"Mejor racha global: {global_mejor_racha}")

pygame.quit()