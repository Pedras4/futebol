import tkinter as tk
from PIL import Image, ImageTk
import random

# =========================
# JOGADORES E IMAGENS
# =========================

equipa_verde = {
    "Michael Olise": "olise.png",
    "Kevin Hart": "hart.png",
    "Breel Embolo": "embolo.png",
    "Nelson Semedo": "nelson.png",
    "Youri Tielemans": "tielemans.png",
    "Homer Simpson": "homer.png"
}

equipa_roxa = {
    "Peter Griffin": "peter.png",
    "Aaron Cresswell": "aaron.png",
    "Pizzi": "pizzi.png",
    "Yannick Carrasco": "yannick.png",
    "Lukasz Piszczek": "lucas.png",
    "Mr. Burns": "burns.png"
}

MAX_ACOES = 40

# =========================
# JANELA
# =========================

janela = tk.Tk()
janela.title("Simulador de Futebol")
janela.geometry("1280x720")
janela.resizable(False, False)

# =========================
# ESTADO DO JOGO
# =========================

golos_verde = 0
golos_roxo = 0

acao_atual = 0

equipa_com_bola = random.choice(["verde", "roxo"])

if equipa_com_bola == "verde":
    jogador_atual = random.choice(list(equipa_verde.keys()))
else:
    jogador_atual = random.choice(list(equipa_roxa.keys()))

imagem_atual = None

# =========================
# INTERFACE
# =========================

resultado_label = tk.Label(
    janela,
    text="Equipa Verde 0 - 0 Equipa Roxa",
    font=("Arial", 24, "bold"),
    bg="black",
    fg="white"
)

resultado_label.pack(fill="x")

acoes_label = tk.Label(
    janela,
    text=f"Ação 0/{MAX_ACOES}",
    font=("Arial", 16)
)

acoes_label.pack(pady=10)

imagem_label = tk.Label(janela)
imagem_label.pack(expand=True)

texto_label = tk.Label(
    janela,
    text="",
    font=("Arial", 20, "bold"),
    wraplength=800
)

texto_label.pack(pady=20)

# =========================
# FUNÇÕES
# =========================

def atualizar_resultado():
    resultado_label.config(
        text=f"Equipa Verde {golos_verde} - {golos_roxo} Equipa Roxa"
    )

def atualizar_fundo():

    if equipa_com_bola == "verde":
        cor = "#0b3d0b"
    else:
        cor = "#3d0b3d"

    janela.config(bg=cor)
    imagem_label.config(bg=cor)
    texto_label.config(bg=cor, fg="white")
    acoes_label.config(bg=cor, fg="white")

def mostrar_imagem(nome_jogador):

    global imagem_atual

    if nome_jogador in equipa_verde:
        ficheiro = equipa_verde[nome_jogador]
    else:
        ficheiro = equipa_roxa[nome_jogador]

    try:
        img = Image.open(ficheiro)
        img = img.resize((350, 350))
        imagem_atual = ImageTk.PhotoImage(img)

        imagem_label.config(image=imagem_atual)

    except:
        imagem_label.config(image="")
        texto_label.config(
            text=f"Imagem não encontrada:\n{ficheiro}"
        )

def fim_do_jogo():

    if golos_verde > golos_roxo:
        vencedor = "Equipa Verde venceu!"
    elif golos_roxo > golos_verde:
        vencedor = "Equipa Roxa venceu!"
    else:
        vencedor = "Empate!"

    texto_label.config(
        text=f"FIM DO JOGO\n\n{vencedor}"
    )

def iniciar_acao():

    global acao_atual

    if acao_atual >= MAX_ACOES:
        fim_do_jogo()
        return

    atualizar_fundo()

    mostrar_imagem(jogador_atual)

    acao = random.choice([
        "passar",
        "driblar",
        "chutar"
    ])

    texto_label.config(
        text=f"{jogador_atual} tenta {acao}."
    )

    janela.after(
        2000,
        lambda: resultado_acao(acao)
    )

def resultado_acao(acao):

    global jogador_atual
    global equipa_com_bola
    global golos_verde
    global golos_roxo
    global acao_atual

    if acao == "passar":

        sucesso = random.random() < 0.7

        if sucesso:

            if equipa_com_bola == "verde":
                opcoes = [
                    j for j in equipa_verde
                    if j != jogador_atual
                ]
            else:
                opcoes = [
                    j for j in equipa_roxa
                    if j != jogador_atual
                ]

            receptor = random.choice(opcoes)

            mostrar_imagem(receptor)

            texto_label.config(
                text=f"Passe bem sucedido para {receptor}"
            )

            jogador_atual = receptor

        else:

            if equipa_com_bola == "verde":

                interceptor = random.choice(
                    list(equipa_roxa.keys())
                )

                equipa_com_bola = "roxo"

            else:

                interceptor = random.choice(
                    list(equipa_verde.keys())
                )

                equipa_com_bola = "verde"

            mostrar_imagem(interceptor)

            texto_label.config(
                text=f"Passe interceptado por {interceptor}"
            )

            jogador_atual = interceptor

    elif acao == "driblar":

        sucesso = random.random() < 0.5

        if sucesso:

            mostrar_imagem(jogador_atual)

            texto_label.config(
                text=f"{jogador_atual} dribla com sucesso"
            )

        else:

            if equipa_com_bola == "verde":

                roubador = random.choice(
                    list(equipa_roxa.keys())
                )

                equipa_com_bola = "roxo"

            else:

                roubador = random.choice(
                    list(equipa_verde.keys())
                )

                equipa_com_bola = "verde"

            mostrar_imagem(roubador)

            texto_label.config(
                text=f"{roubador} rouba a bola"
            )

            jogador_atual = roubador

    elif acao == "chutar":

        golo = random.random() < 0.2

        if golo:

            mostrar_imagem(jogador_atual)

            texto_label.config(
                text=f"GOLO DE {jogador_atual.upper()}!"
            )

            if equipa_com_bola == "verde":
                golos_verde += 1
            else:
                golos_roxo += 1

            atualizar_resultado()

        else:

            if equipa_com_bola == "verde":

                defensor = random.choice(
                    list(equipa_roxa.keys())
                )

                equipa_com_bola = "roxo"

            else:

                defensor = random.choice(
                    list(equipa_verde.keys())
                )

                equipa_com_bola = "verde"

            mostrar_imagem(defensor)

            texto_label.config(
                text=f"Remate falhado. {defensor} recupera a bola"
            )

            jogador_atual = defensor

    acao_atual += 1

    acoes_label.config(
        text=f"Ação {acao_atual}/{MAX_ACOES}"
    )

    janela.after(
        2000,
        iniciar_acao
    )

# =========================
# INICIAR
# =========================

atualizar_resultado()
iniciar_acao()

janela.mainloop()
