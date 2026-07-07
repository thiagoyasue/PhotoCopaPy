import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime

# ----------------------------
# CONFIGURAÇÕES
# ----------------------------

TEMPLATE = "template.png"
PASTA_TIMES = "images"
PASTA_OUTPUT = "output"

LARGURA_IMAGEM = 125
ALTURA_IMAGEM = 125

# posição das imagens
POSICOES_IMAGENS = [
    (70, 10),
    (300, 10),
    (550, 10),
    (770, 10),
    (1000, 10)
]

# posição dos textos
POSICOES_TEXTOS = [
    (135, 150),
    (365, 150),
    (615, 150),
    (835, 150),
    (1065, 150)
]

TIMES = [
    "altador",
    "brightvale",
    "dacardia",
    "darigan",
    "faerieland",
    "hauntedwoods",
    "kikolake",
    "krawk",
    "kreludor",
    "lostdesert",
    "maraqua",
    "meridell",
    "moltara",
    "mysteryisland",
    "neopiacentral",
    "rooisland",
    "shenkuu",
    "terrormountain",
    "tyrannia",
    "virtupets"
]

# ----------------------------

os.makedirs(PASTA_OUTPUT, exist_ok=True)

try:
    fonte = ImageFont.truetype("Barlow-ExtraBold.ttf", 56)
except:
    fonte = ImageFont.load_default()

janela = tk.Tk()
janela.title("PhotoCopaPy by thiagoyasue - Cronicas da Copa de Altador - acopadealtador.blogspot.com")
janela.geometry("1200x800")

combos = []
pontuacoes = []

frame_esquerda = tk.Frame(janela)
frame_esquerda.pack(side="left", padx=15, pady=15)

frame_direita = tk.Frame(janela)
frame_direita.pack(side="right", padx=15, pady=15)

tk.Label(
    frame_esquerda,
    text="PhotoCopaPy by thiagoyasue",
    font=("Barlow-ExtraBold.ttf",16,"bold")
).pack(pady=10)

for i in range(5):

    bloco = tk.LabelFrame(frame_esquerda, text=f"Mini-game {i+1}")
    bloco.pack(fill="x", pady=8)

    tk.Label(bloco, text="Time").pack()

    combo = ttk.Combobox(
        bloco,
        values=TIMES,
        state="readonly"
    )

    combo.current(0)
    combo.pack(fill="x", padx=5)

    combos.append(combo)

    tk.Label(bloco, text="Pontuação").pack()

    entrada = tk.Entry(bloco)

    entrada.insert(0, "0-0")

    entrada.pack(fill="x", padx=5, pady=5)

    pontuacoes.append(entrada)

preview_label = tk.Label(frame_direita)
preview_label.pack()


def gerar_preview():

    imagem = Image.open(TEMPLATE).convert("RGBA")

    draw = ImageDraw.Draw(imagem)

    for i in range(5):

        time = combos[i].get()

        caminho = os.path.join(PASTA_TIMES, time + ".png")

        if os.path.exists(caminho):

            logo = Image.open(caminho).convert("RGBA")

            logo = logo.resize(
                (LARGURA_IMAGEM, ALTURA_IMAGEM)
            )

            imagem.paste(
                logo,
                POSICOES_IMAGENS[i],
                logo
            )

        texto = pontuacoes[i].get()

        draw.text(
            POSICOES_TEXTOS[i],
            texto,
            fill="black",
            font=fonte,
            anchor="mm"
        )

    preview = imagem.copy()

    preview.thumbnail((700,700))

    tkimg = ImageTk.PhotoImage(preview)

    preview_label.configure(image=tkimg)

    preview_label.image = tkimg

    return imagem


def salvar():

    try:

        imagem = gerar_preview()

        nome = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png")

        caminho = os.path.join(
            PASTA_OUTPUT,
            nome
        )

        imagem.save(caminho)

        messagebox.showinfo(
            "Pronto",
            f"Imagem salva em:\n{caminho}"
        )

    except Exception as e:

        messagebox.showerror(
            "Erro",
            str(e)
        )


def atualizar(event=None):

    try:
        gerar_preview()
    except:
        pass


for c in combos:
    c.bind("<<ComboboxSelected>>", atualizar)

for e in pontuacoes:
    e.bind("<KeyRelease>", atualizar)

botao = tk.Button(
    frame_esquerda,
    text="GERAR IMAGEM",
    font=("Arial",14,"bold"),
    command=salvar,
    height=2
)

botao.pack(fill="x", pady=20)

atualizar()

janela.mainloop()