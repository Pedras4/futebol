import tkinter as tk
from PIL import Image, ImageTk
import random
#
equipa = {
    "verde": {
        "Michael Olise": "olise.png",
        "Kevin Hart": "hart.png",
        "Breel Embolo": "embolo.png",
        "Nelson Semedo": "nelson.png",
        "Youri Tielemans": "tielemans.png",
        "Homer Simpson": "homer.png"
    },
    "roxo": {
        "Peter Griffin": "peter.png",
        "Aaron Cresswell": "aaron.png",
        "Pizzi": "pizzi.png",
        "Yannick Carrasco": "yannick.png",
        "Lukasz Piszczek": "lucas.png",
        "Mr. Burns": "burns.png"
    }
}

MAX_ACOES = 40 #limite de ações do jogo para 40

janela = tk.Tk() #cria a janela do jogo
janela.title("Futebol") #nome da janela
janela.geometry("1280x720") #proporção da janela
janela.resizable(False, False) #não da para mudar a proporção da janela

golos = {"verde": 0, "roxo": 0} #guarda o resultado do jogo
acao = 0 #guarda o numero de ações realzadas

equipa_atual = random.choice(["verde", "roxo"]) #escolhe a equipa que começa a jogar
jogador = random.choice(list(equipa[equipa_atual].keys())) #escolhe um jogador aleatório da equipa atual

img_ref = None #guardar a referência da imagem para evitar que seja eliminada pelo garbage collector

resultado = tk.Label(janela, font=("Arial", 24, "bold")) #mostra o resultado do jogo
resultado.pack(fill="x") #

acoes = tk.Label(janela, font=("Arial", 16)) #mostra o número de ações realizadas
acoes.pack(pady=10) #cria um espaço entre o resultado e a imagem do jogador

img_label = tk.Label(janela) #coloca a imagem do jogador na tela
img_label.pack(expand=True) #coloca a imagem no centro da tela

texto = tk.Label(janela, font=("Arial", 20, "bold")) #mostra a ação do jogo
texto.pack(pady=20) #cria um espaço entre a imagem do jogador e o texto

def update():
    resultado.config(text=f"Verde {golos['verde']} - {golos['roxo']} Roxo") #calcula o resultado do jogo
    acoes.config(text=f"Ação {acao}/{MAX_ACOES}") #calcula o n de ações

def set_team():
    cor = "#0b3d0b" if equipa_atual == "verde" else "#3d0b3d" #muda a cor
    janela.config(bg=cor) #faz o fundo da janela ser a cor da equipa
    for w in (resultado, acoes, texto, img_label):
        w.config(bg=cor, fg="white") #muda a cor do texto

def show(name):
    global img_ref 
    try:
        file = equipa[equipa_atual].get(name, None) #procura a imagem do jogador na equipa atual

        img = Image.open(file).resize((350, 350)) #redimensiona a imagem
        img_ref = ImageTk.PhotoImage(img) #converte para tkinter
        img_label.config(image=img_ref) #mostra a imagem na tela
    except:
        texto.config(text="Imagem não encontrada") #escreve aonde deveria ficar a imagem que a imagem não foi encontrada


def switch_team(): #muda a equipa atual para a equipa adversária
    global equipa_atual #
    equipa_atual = "roxo" if equipa_atual == "verde" else "verde" #muda a equipa atual para o adversario


def pick_player(): #escolhe um jogador aleatório da equipa atual
    return random.choice(list(equipa[equipa_atual].keys())) #ve a equipa atual, faz os jogadores estarem numa lista e escolhe um jogador aleatório dessa lista


def fim():
    if golos["verde"] > golos["roxo"]: 
        r = "Verde ganhou!" #se a equipa verde tiver mais golos, o resultado é que a equipa verde ganhou
    elif golos["roxo"] > golos["verde"]:
        r = "Roxo ganhou!" #se a equipa roxa tiver mais golos, o resultado é que a equipa roxa ganhou
    else:
        r = "Empate!" #se as duas equipas tiverem o mesmo número de golos, o resultado é empate
    texto.config(text="FIM DO JOGO\n\n" + r) #escreve Fim de jogo e o resultado do jogo na tela

def acao_jogo():
    global jogador, acao #faz com que o python use o jogador e faz a ação

    if acao >= MAX_ACOES: #fim do jogo
        fim()
        return

    set_team() #muda a equipa atual
    show(jogador) #mostra o nome e a imagem do jogador atual

    act = random.choice(["passar", "driblar", "chutar"]) #o jogo escolhe aleatoriamente uma ação
    texto.config(text=f"{jogador} tenta {act}") #mostra a ação do jogador na tela (não é o resultado da ação)

    janela.after(1200, lambda: resultado_acao(act)) #mostra o resultado depois de 1,2 segundos


def resultado_acao(act):
    global jogador, acao #faz com que o python use o jogador e faz a ação

    if act == "passar":
        if random.random() < 0.7: #tem 70% de chance de conseguir passar a bola
            jogador = random.choice([j for j in equipa[equipa_atual] if j != jogador]) #escolhe um jogador aleatório da equipa atual para passar a bola, que não seja o jogador atual
            texto.config(text=f"Passe para {jogador}") #escreve o texto na tela
        else:
            switch_team()
            jogador = pick_player() #escolhe um jogador aleatório da equipa adversária para interceptar a bola
            texto.config(text="Passe interceptado") #escreve o texto na tela

    elif act == "driblar":
        if random.random() < 0.5: #tem 50% de chance de conseguir driblar o adversário
            texto.config(text=f"{jogador} dribla") #escreve o texto na tela
        else:
            switch_team() #muda de equipa
            jogador = pick_player() #escolhe um jogador aleatório da equipa adversária para roubar a bola
            texto.config(text="Perde a bola") #escreve o texto na tela

    elif act == "chutar":
        if random.random() < 0.2: #tem 20% de chance de conseguir marcar um golo
            golos[equipa_atual] += 1 #adiciona 1 ao resultado da equipa atual
            texto.config(text=f"GOLO de {jogador}!") #escreve o texto na tela
        else:
            switch_team() #muda de equipa
            jogador = pick_player() #escolhe um jogador aleatório da equipa adversária para defender o golo
            texto.config(text="Defendido") #escreve o texto na tela

    acao += 1 #quando uma ação é realizada, o número de ações aumenta em 1
    update()

    janela.after(1200, acao_jogo) #faz com que aconteça as ações do jogo

update() 
acao_jogo()
janela.mainloop()