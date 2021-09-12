import pygame
import random

pygame.init()

preto = (0,0,0)
vermelho = (255,0,0)
branco = (255,255,255)
fonte = pygame.font.SysFont("Comic Sams MS" , 30)

lado_celula = 50
tela = pygame.display.set_mode((9*lado_celula, 10*lado_celula))
pygame.display.set_caption( "Campo minado" )
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

#tela inicial
tela.fill(branco)
for i in range(0,9):
   for j in range(0,9):
      pygame.draw.rect(tela, preto, (i*lado_celula,j*lado_celula,lado_celula,lado_celula), 1)
pygame.display.update()

num_bombas = 0
conteudo_celula = [[None for i in range(9)] for j in range(9)]
for i in range(0,9):
   for j in range(0,9):
      if random.randint(1,100) > 90:
         conteudo_celula[i][j] = "X"
         num_bombas += 1
for i in range(0,9):
   for j in range(0,9):
      if conteudo_celula[i][j] != "X":
         nb_bombas_ao_redor = 0
         if i - 1 >= 0 and conteudo_celula[i - 1][j] == "X":
            nb_bombas_ao_redor += 1

         if j - 1 >= 0 and conteudo_celula[i][j - 1] == "X":
            nb_bombas_ao_redor += 1
         if j + 1 < 9 and conteudo_celula[i][j + 1] == "X":
            nb_bombas_ao_redor += 1
         if i + 1 < 9 and conteudo_celula[i + 1][j] == "X":
            nb_bombas_ao_redor += 1
         conteudo_celula[i][j] = str(nb_bombas_ao_redor)
 
celula_revelada = [[False for i in range(9)] for j in range(9)]

jogo_cancelado = False
perdeu = False
ganhou = False
num_celulas_abertas = 0

while not jogo_cancelado:

   for evento in pygame.event.get(): 
      
      if (evento.type == pygame.QUIT): 
         jogo_cancelado = True
         break
      
      if perdeu or ganhou:
         continue

      tela_mudou = False

      if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
          #pega as coordenadas do ponto de clique e calcula a celula
          mouse_x, mouse_y = evento.pos
          celula_x = mouse_x//lado_celula
          celula_y = mouse_y//lado_celula

          #entra no if se a celula foi clicada pela primeira vez
          if not celula_revelada[celula_x][celula_y]:
             tela_mudou = True
             num_celulas_abertas += 1
             celula_revelada[celula_x][celula_y] = True
             #verifica se perdeu
             if conteudo_celula[celula_x][celula_y] == "X":
                pygame.mixer.music.load('explosion.ogg')
                pygame.mixer.music.play(1)
                perdeu = True
             #verifica se ganhou
             elif num_celulas_abertas + num_bombas == 81:
                pygame.mixer.music.load('applause.ogg')
                pygame.mixer.music.play(1)
                ganhou = True

      if tela_mudou:

         tela.fill(branco)
         for i in range(0,9):
            for j in range(0,9):
               pygame.draw.rect(tela, preto, (i*lado_celula,j*lado_celula,lado_celula,lado_celula), 1)
               if celula_revelada[i][j]:
                  if conteudo_celula[i][j] == "X":
                     bomba = pygame.image.load('bomba.jpeg')
                     bomba = pygame.transform.scale(bomba, (lado_celula - 3, lado_celula - 3))
                     tela.blit(bomba, (lado_celula*i + 1, lado_celula*j + 1))
                  else:
                     texto = fonte.render(conteudo_celula[i][j], False, (0,0,0))
                     tela.blit(texto, (lado_celula*i + 0.4*lado_celula, lado_celula*j + 0.4*lado_celula))

         if ganhou:
            texto = fonte.render("Ganhou!", True, preto)
            tela.blit(texto, (0, lado_celula*9))
         elif perdeu:
            texto = fonte.render("Perdeu!", True, preto)
            tela.blit(texto, (0, lado_celula*9))

         pygame.display.update()

pygame.quit()
