from config.colores import *
import pygame

pygame.init()

width, height = 853, 650
ventana = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adivina el Pokemon")

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

Fuente = pygame.font.SysFont("Arial", 30)
aux = 1
bandera = True

while bandera:
    ventana.fill((BACKGROUND))
    TIEMPO = pygame.time.get_ticks()/1000
    if aux  == TIEMPO:  
        aux += 1
        print(TIEMPO)

    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            bandera = False

    contador = Fuente.render("Time Taken: "+str(TIEMPO),0,(TEXT))
    ventana.blit(contador,(100,100))
    pygame.display.update()

pygame.quit()