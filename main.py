import customtkinter as ctk
from tkinter import filedialog
import yt_dlp
import threading
import os
import json
import subprocess
import requests
from PIL import Image
from io import BytesIO
import datetime
import sys

def resolver_caminho(nome_arquivo):
    """ Retorna o caminho absoluto do arquivo, seja no modo Dev ou no .exe """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, nome_arquivo)
    return os.path.join(os.path.abspath("."), nome_arquivo)

# 1. Configurações Globais
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("750x700")
app.title("IronDownloader 4k - Pro Edition")
app.resizable(False, False)

try:
    app.iconbitmap(resolver_caminho("youtube.ico"))
except Exception:
    pass 

pasta_downloads_padrao = r"C:\Users\Henrique\Downloads"
arquivo_historico = "historico.json"
ffmpeg_path = r'C:\Users\Henrique\Documents\FFmpeg\ffmpeg-8.1-essentials_build\bin'

# 2. Funções de Suporte (Histórico e Atualização)
def carregar_historico():
    if os.path.exists(arquivo_historico):
        with open(arquivo_historico, "r") as f:
            return json.load(f)
    return []

def salvar_historico(titulo, tipo):
    hist = carregar_historico()
    hist.append({"data": str(datetime.date.today()), "titulo": titulo, "tipo": tipo})
    with open(arquivo_historico, "w") as f:
        json.dump(hist[-10:], f)
    atualizar_lista_historico()

def atualizar_motor():
    app.after(0, lambda: label_status.configure(text="Atualizando yt-dlp... aguarde.", text_color="yellow"))
    def rodar_update():
        try:
            subprocess.run(["pip", "install", "--upgrade", "yt-dlp"], check=True)
            app.after(0, lambda: label_status.configure(text="Motor atualizado com sucesso!", text_color="#00FF00"))
        except Exception as e:
            app.after(0, lambda: label_status.configure(text="Erro ao atualizar.", text_color="red"))
    threading.Thread(target=rodar_update).start()

# --- NOVAS FUNÇÕES PARA ATUALIZAR OS MENUS DINAMICAMENTE ---
def atualizar_menu_unico():
    if tipo_var.get() == "Vídeo":
        combo_qualidade.configure(values=["144p", "240p", "360p", "480p", "720p", "1080p", "1440p (2K)", "2160p (4K/Max)"])
        combo_qualidade.set("1080p")
    else:
        combo_qualidade.configure(values=["WAV (Sem Perda - Premiere)", "MP3 (320kbps)", "MP3 (192kbps)"])
        combo_qualidade.set("WAV (Sem Perda - Premiere)")

def atualizar_menu_lote():
    if tipo_var_lote.get() == "Vídeo":
        combo_qualidade_lote.configure(values=["144p", "240p", "360p", "480p", "720p", "1080p", "1440p (2K)", "2160p (4K/Max)"])
        combo_qualidade_lote.set("1080p")
    else:
        combo_qualidade_lote.configure(values=["WAV (Sem Perda - Premiere)", "MP3 (320kbps)", "MP3 (192kbps)"])
        combo_qualidade_lote.set("WAV (Sem Perda - Premiere)")
# -------------------------------------------------------------

# 3. Lógica de UI (Miniatura e Pastas)
def selecionar_pasta():
    pasta = filedialog.askdirectory(initialdir=entrada_pasta.get())
    if pasta:
        entrada_pasta.delete(0, ctk.END)
        entrada_pasta.insert(0, pasta)

def buscar_info_video():
    url = entrada_url_unico.get()
    if not url: return
    
    label_titulo_preview.configure(text="Buscando informações...")
    
    def fetch():
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                titulo = info.get('title', 'Vídeo Desconhecido')
                thumb_url = info.get('thumbnail')
                
                app.after(0, lambda: label_titulo_preview.configure(text=titulo[:50] + "..."))
                
                if thumb_url:
                    response = requests.get(thumb_url)
                    img_data = Image.open(BytesIO(response.content))
                    img_ctk = ctk.CTkImage(img_data, size=(160, 90))
                    app.after(0, lambda: label_thumb.configure(image=img_ctk, text=""))
        except Exception:
            app.after(0, lambda: label_titulo_preview.configure(text="Erro ao buscar vídeo. Link privado ou inválido?"))
    threading.Thread(target=fetch).start()

# 4. Motor de Download
def hook_progresso(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        eta = d.get('eta', 0)
        
        if total:
            percentual = downloaded / total
            eta_str = str(datetime.timedelta(seconds=eta)) if eta else "Calculando..."
            app.after(0, barra_progresso.set, percentual)
            app.after(0, lambda: label_porcentagem.configure(text=f"{int(percentual * 100)}% (Faltam {eta_str})"))
            
    elif d['status'] == 'finished':
        app.after(0, barra_progresso.set, 1.0)
        app.after(0, lambda: label_status.configure(text="Arquivo baixado. Otimizando no FFmpeg...", text_color="yellow"))

def executar_download(urls, tipo, qualidade, pasta, usar_trim=False):
    app.after(0, lambda: label_status.configure(text="Iniciando download...", text_color="yellow"))
    app.after(0, lambda: botao_baixar_unico.configure(state="disabled"))
    app.after(0, lambda: botao_baixar_lote.configure(state="disabled"))

    try:
        opcoes_yt = {
            'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s'),
            'ffmpeg_location': ffmpeg_path,
            'progress_hooks': [hook_progresso],
            'keepvideo': False,
            'ignoreerrors': True, 
        }

        if tipo == "Vídeo":
            res = {"144": 144, "240": 240, "360": 360, "480": 480, "720": 720, "1080": 1080, "1440": 1440, "2160": 2160}
            h = next((v for k, v in res.items() if k in qualidade), 1080)
            opcoes_yt.update({'format': f'bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/best[height<={h}][ext=mp4]/best', 'merge_output_format': 'mp4'})
        else:
            opcoes_yt.update({'format': 'bestaudio/best'})
            codec = 'wav' if "WAV" in qualidade else 'mp3'
            bitrate = '320' if "320" in qualidade else '192'
            opcoes_yt.update({'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': codec, 'preferredquality': bitrate}]})

        if usar_trim:
            inicio = entrada_trim_inicio.get()
            fim = entrada_trim_fim.get()
            if inicio and fim:
                opcoes_yt['postprocessor_args'] = ['-ss', inicio, '-to', fim]

        with yt_dlp.YoutubeDL(opcoes_yt) as ydl:
            for url in urls:
                info = ydl.extract_info(url, download=True)
                if info:
                    titulo = info.get('title', 'Lote/Playlist')
                    salvar_historico(titulo, tipo)
        
        app.after(0, lambda: label_status.configure(text="Processo Concluído com Sucesso!", text_color="#00FF00"))
    
    except Exception as e:
        app.after(0, lambda: label_status.configure(text=f"Erro crítico: {e}", text_color="red"))
    finally:
        app.after(0, lambda: botao_baixar_unico.configure(state="normal"))
        app.after(0, lambda: botao_baixar_lote.configure(state="normal"))

def disparar_unico():
    url = entrada_url_unico.get()
    if not url: return
    threading.Thread(target=executar_download, args=([url], tipo_var.get(), combo_qualidade.get(), entrada_pasta.get(), True)).start()

def disparar_lote():
    texto = textbox_lote.get("1.0", ctk.END).strip()
    if not texto: return
    urls = [linha.strip() for linha in texto.split("\n") if linha.strip()]
    threading.Thread(target=executar_download, args=(urls, tipo_var_lote.get(), combo_qualidade_lote.get(), entrada_pasta.get(), False)).start()


# 5. Interface Gráfica (U.I.)
titulo = ctk.CTkLabel(app, text="IronDownloader 4k", font=("Arial", 26, "bold"), text_color="#1f538d")
titulo.pack(pady=(15, 5))

frame_pasta = ctk.CTkFrame(app, fg_color="transparent") 
frame_pasta.pack(pady=5)
entrada_pasta = ctk.CTkEntry(frame_pasta, width=300)
entrada_pasta.grid(row=0, column=0, padx=5)
entrada_pasta.insert(0, pasta_downloads_padrao) 
ctk.CTkButton(frame_pasta, text="Mudar Destino", width=100, command=selecionar_pasta).grid(row=0, column=1)

abas = ctk.CTkTabview(app, width=650, height=380)
abas.pack(pady=10)

aba_unico = abas.add("Vídeo Único")
aba_lote = abas.add("Lote / Playlists")
aba_hist = abas.add("Histórico & Sistema")

# --- ABA 1: VÍDEO ÚNICO ---
ctk.CTkLabel(aba_unico, text="Link do YouTube:").pack(pady=(10,0))
frame_url = ctk.CTkFrame(aba_unico, fg_color="transparent")
frame_url.pack()
entrada_url_unico = ctk.CTkEntry(frame_url, width=400)
entrada_url_unico.grid(row=0, column=0, padx=5)
ctk.CTkButton(frame_url, text="Buscar Info", width=80, command=buscar_info_video).grid(row=0, column=1)

label_thumb = ctk.CTkLabel(aba_unico, text="[ Miniatura ]", width=160, height=90, fg_color="#2b2b2b")
label_thumb.pack(pady=10)
label_titulo_preview = ctk.CTkLabel(aba_unico, text="Cole o link e busque as informações", font=("Arial", 12))
label_titulo_preview.pack()

frame_opcoes = ctk.CTkFrame(aba_unico, fg_color="transparent")
frame_opcoes.pack(pady=10)

tipo_var = ctk.StringVar(value="Vídeo")
# ATENÇÃO AQUI: Adicionado o command=atualizar_menu_unico
ctk.CTkRadioButton(frame_opcoes, text="Vídeo", variable=tipo_var, value="Vídeo", command=atualizar_menu_unico).grid(row=0, column=0, padx=10)
ctk.CTkRadioButton(frame_opcoes, text="Áudio", variable=tipo_var, value="Áudio", command=atualizar_menu_unico).grid(row=0, column=1, padx=10)

combo_qualidade = ctk.CTkComboBox(frame_opcoes, width=200)
combo_qualidade.grid(row=0, column=2, padx=10)
atualizar_menu_unico() # Carrega as opções na inicialização

frame_trim = ctk.CTkFrame(aba_unico, fg_color="transparent")
frame_trim.pack(pady=5)
ctk.CTkLabel(frame_trim, text="Corte (Opcional):").grid(row=0, column=0, padx=5)
entrada_trim_inicio = ctk.CTkEntry(frame_trim, width=80, placeholder_text="00:00:00")
entrada_trim_inicio.grid(row=0, column=1, padx=5)
ctk.CTkLabel(frame_trim, text="até").grid(row=0, column=2)
entrada_trim_fim = ctk.CTkEntry(frame_trim, width=80, placeholder_text="00:01:30")
entrada_trim_fim.grid(row=0, column=3, padx=5)

botao_baixar_unico = ctk.CTkButton(aba_unico, text="BAIXAR", command=disparar_unico, fg_color="#1f538d", font=("Arial", 14, "bold"))
botao_baixar_unico.pack(pady=10)


# --- ABA 2: LOTE E PLAYLISTS ---
ctk.CTkLabel(aba_lote, text="Cole vários links (um por linha) ou o link de uma Playlist:").pack(pady=(10,5))
textbox_lote = ctk.CTkTextbox(aba_lote, width=500, height=150)
textbox_lote.pack()

frame_opcoes_lote = ctk.CTkFrame(aba_lote, fg_color="transparent")
frame_opcoes_lote.pack(pady=15)

tipo_var_lote = ctk.StringVar(value="Vídeo")
# ATENÇÃO AQUI: Adicionado o command=atualizar_menu_lote
ctk.CTkRadioButton(frame_opcoes_lote, text="Vídeo", variable=tipo_var_lote, value="Vídeo", command=atualizar_menu_lote).grid(row=0, column=0, padx=10)
ctk.CTkRadioButton(frame_opcoes_lote, text="Áudio", variable=tipo_var_lote, value="Áudio", command=atualizar_menu_lote).grid(row=0, column=1, padx=10)

combo_qualidade_lote = ctk.CTkComboBox(frame_opcoes_lote, width=200)
combo_qualidade_lote.grid(row=0, column=2, padx=10)
atualizar_menu_lote() # Carrega as opções na inicialização

botao_baixar_lote = ctk.CTkButton(aba_lote, text="INICIAR FILA DE DOWNLOADS", command=disparar_lote, fg_color="#8d1f1f", hover_color="#5e1414", font=("Arial", 14, "bold"))
botao_baixar_lote.pack(pady=10)


# --- ABA 3: HISTÓRICO E SISTEMA ---
ctk.CTkButton(aba_hist, text="Atualizar Motor (yt-dlp)", command=atualizar_motor, fg_color="#2b8d1f").pack(pady=15)
ctk.CTkLabel(aba_hist, text="Últimos 10 Downloads:").pack()
caixa_historico = ctk.CTkTextbox(aba_hist, width=500, height=200, state="disabled")
caixa_historico.pack()

def atualizar_lista_historico():
    caixa_historico.configure(state="normal")
    caixa_historico.delete("1.0", ctk.END)
    for item in reversed(carregar_historico()):
        caixa_historico.insert(ctk.END, f"[{item['data']}] ({item['tipo']}) {item['titulo']}\n")
    caixa_historico.configure(state="disabled")
atualizar_lista_historico()

# 6. Rodapé Global (Status e Progresso)
barra_progresso = ctk.CTkProgressBar(app, width=600, height=15)
barra_progresso.pack(pady=(10, 5))
barra_progresso.set(0)

label_porcentagem = ctk.CTkLabel(app, text="0% (Aguardando...)", font=("Arial", 12, "bold"))
label_porcentagem.pack()

label_status = ctk.CTkLabel(app, text="Sistema Pronto.", font=("Arial", 14, "bold"))
label_status.pack(pady=5)

app.mainloop()