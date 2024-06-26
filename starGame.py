import pygame
import tkinter as tk
from tkinter import simpledialog
import os
import pickle

pygame.init()

# tela
tamanho = (1080, 720)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Mapa de Estrelas")
icon_path = os.path.join("assets", "icone.png")
if os.path.isfile(icon_path):
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
branco = (255, 255, 255)
preto = (0, 0, 0)
fonte = pygame.font.SysFont("helvetica", 20)
fonte_info = pygame.font.SysFont("helvetica", 15)
relogio = pygame.time.Clock()
caminho_fundo = os.path.join("assets", "imagemFundo.jpg")
if not os.path.isfile(caminho_fundo):
    raise FileNotFoundError(f"Imagem de fundo não encontrada: {caminho_fundo}")
fundo = pygame.image.load(caminho_fundo)
fundo = pygame.transform.scale(fundo, tamanho)
estrelas = []
nomes_estrelas = []
nome_atual = ""
adicionando_nome = False

# Funções para salvar, carregar e excluir marcações
def salvar_marcacoes():
    with open("marcacoes.pkl", "wb") as f:
        pickle.dump({"estrelas": estrelas, "nomes_estrelas": nomes_estrelas}, f)

def carregar_marcacoes():
    if os.path.exists("marcacoes.pkl"):
        with open("marcacoes.pkl", "rb") as f:
            dados = pickle.load(f)
            return dados["estrelas"], dados["nomes_estrelas"]
    return [], []

def excluir_marcacoes():
    global estrelas, nomes_estrelas
    estrelas = []
    nomes_estrelas = []
    if os.path.exists("marcacoes.pkl"):
        os.remove("marcacoes.pkl")

# nome da estrela
def get_star_name():
    root = tk.Tk()
    root.withdraw()
    nome = simpledialog.askstring("Nome da Estrela", "Digite o nome da estrela:")
    root.destroy()
    return nome if nome else "Desconhecido"

def desenhar_estrelas():
    if len(estrelas) > 1:
        pygame.draw.lines(tela, branco, False, estrelas, 2)
    for i, (pos, nome) in enumerate(zip(estrelas, nomes_estrelas)):
        pygame.draw.circle(tela, preto, pos, 5)
        texto_nome = fonte.render(nome, True, branco)
        tela.blit(texto_nome, (pos[0] + 10, pos[1] - 10))

def desenhar_info_controles():
    info_textos = [
        "Controles:",
        "Salvar Marcações: Ctrl+S",
        "Carregar Marcações: Ctrl+C",
        "Excluir Marcações: Ctrl+E",
        "Sair: ESC"
    ]
    for i, texto in enumerate(info_textos):
        texto_renderizado = fonte_info.render(texto, True, branco)
        tela.blit(texto_renderizado, (10, 10 + i * 20))


def main():
    global adicionando_nome, nome_atual
    rodando = True

    global estrelas, nomes_estrelas
    estrelas, nomes_estrelas = carregar_marcacoes()

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salvar_marcacoes()
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                # Ctrl+S para salvar
                if evento.mod & pygame.KMOD_CTRL and evento.key == pygame.K_s:
                    salvar_marcacoes()
                # Cotrl+C para carregar
                elif evento.mod & pygame.KMOD_CTRL and evento.key == pygame.K_c:
                    estrelas, nomes_estrelas = carregar_marcacoes()
                # Ctrl+E para excluir
                elif evento.mod & pygame.KMOD_CTRL and evento.key == pygame.K_e:
                    excluir_marcacoes()
                elif evento.key == pygame.K_ESCAPE:
                    salvar_marcacoes()
                    rodando = False
                elif adicionando_nome:
                    if evento.key == pygame.K_RETURN:
                        nomes_estrelas[-1] = nome_atual
                        nome_atual = ""
                        adicionando_nome = False
                    elif evento.key == pygame.K_BACKSPACE:
                        nome_atual = nome_atual[:-1]
                    else:
                        nome_atual += evento.unicode
            elif evento.type == pygame.MOUSEBUTTONDOWN and not adicionando_nome:
                pos = evento.pos
                estrelas.append(pos)
                nomes_estrelas.append("")
                adicionando_nome = True

        
        tela.blit(fundo, (0, 0))
        desenhar_estrelas()
        desenhar_info_controles()

        if adicionando_nome:
            pos = estrelas[-1]
            pygame.draw.rect(tela, (128, 0, 128), (pos[0], pos[1] - 30, 200, 30))
            texto_input = fonte.render(nome_atual, True, branco)
            tela.blit(texto_input, (pos[0] + 5, pos[1] - 30))


        pygame.display.update()
        relogio.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()