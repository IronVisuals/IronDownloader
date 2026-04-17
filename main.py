import customtkinter as ctk
from tkinter import filedialog
import yt_dlp
import threading
import os

# 1. Configurações da Janela Principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("650x550")
app.title("IronDownloader 4k - Pro Edition")
app.iconbitmap("youtube.ico")
app.resizable(False, False)

pasta_downloads_padrao = os.path.join(os.path.expanduser('~'), 'Downloads')

# 2. Funções de Suporte
def selecionar_pasta():
    pasta_selecionada = filedialog.askdirectory(initialdir=entrada_pasta.get())
    if pasta_selecionada:
        entrada_pasta.delete(0, ctk.END)
        entrada_pasta.insert(0, pasta_selecionada)

def restaurar_downloads():
    entrada_pasta.delete(0, ctk.END)
    entrada_pasta.insert(0, pasta_downloads_padrao)

def atualizar_menu_qualidade():
    if tipo_var.get() == "Vídeo":
        combo_qualidade.configure(values=["144p", "240p", "360p", "480p", "720p", "1080p", "1440p (2K)", "2160p (4K/Max)"])
        combo_qualidade.set("1080p")
    else:
        combo_qualidade.configure(values=["WAV (Sem Perda - Premiere)", "MP3 (320kbps)", "MP3 (192kbps)"])
        combo_qualidade.set("WAV (Sem Perda - Premiere)")

def atualizar_progresso_ui(percentual):
    barra_progresso.set(percentual)
    label_porcentagem.configure(text=f"{int(percentual * 100)}%")

def hook_progresso(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if total_bytes:
            percentual = downloaded / total_bytes
            app.after(0, atualizar_progresso_ui, percentual)
    elif d['status'] == 'finished':
        app.after(0, atualizar_progresso_ui, 1.0)
        # CORREÇÃO APLICADA AQUI COM O LAMBDA
        app.after(0, lambda: label_status.configure(text="Convertendo e finalizando arquivo...", text_color="yellow"))

# 3. Lógica de Download
def iniciar_download():
    url = entrada_url.get()
    tipo = tipo_var.get()
    qualidade = combo_qualidade.get()
    pasta_destino = entrada_pasta.get()
    
    if not url:
        label_status.configure(text="Insira um link válido.", text_color="red")
        return

    barra_progresso.set(0)
    label_porcentagem.configure(text="0%")
    label_status.configure(text="Iniciando...", text_color="yellow")
    botao_baixar.configure(state="disabled") 

    def processo_em_segundo_plano():
        try:
            opcoes_yt = {
                'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'ffmpeg_location': r'C:\Users\Henrique\Documents\FFmpeg\ffmpeg-8.1-essentials_build\bin', 
                'progress_hooks': [hook_progresso],
                'keepvideo': False, 
            }

            if tipo == "Vídeo":
                resolucoes = {"144": 144, "240": 240, "360": 360, "480": 480, "720": 720, "1080": 1080, "1440": 1440, "2160": 2160}
                h = next((v for k, v in resolucoes.items() if k in qualidade), 1080)
                opcoes_yt.update({
                    'format': f'bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/best[height<={h}][ext=mp4]/best',
                    'merge_output_format': 'mp4'
                })
            else:
                opcoes_yt.update({'format': 'bestaudio/best'})
                codec = 'wav' if "WAV" in qualidade else 'mp3'
                bitrate = '320' if "320" in qualidade else '192'
                
                opcoes_yt.update({
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': codec,
                        'preferredquality': bitrate,
                    }]
                })

            with yt_dlp.YoutubeDL(opcoes_yt) as ydl:
                ydl.download([url])
            
            # CORREÇÃO APLICADA AQUI COM O LAMBDA
            app.after(0, lambda: label_status.configure(text="Download Concluído com Sucesso!", text_color="#00FF00"))
        
        except Exception as e:
            # CORREÇÃO APLICADA AQUI COM O LAMBDA
            app.after(0, lambda: label_status.configure(text="Erro no download.", text_color="red"))
            print(f"Erro detalhado: {e}") 
        
        finally:
            # CORREÇÃO APLICADA AQUI COM O LAMBDA
            app.after(0, lambda: botao_baixar.configure(state="normal")) 

    threading.Thread(target=processo_em_segundo_plano).start()

# 4. Interface (UI)
titulo = ctk.CTkLabel(app, text="IronDownloader 4k", font=("Arial", 24, "bold"), text_color="#1f538d")
titulo.pack(pady=(20, 10))

entrada_url = ctk.CTkEntry(app, width=500, placeholder_text="Cole o link do YouTube aqui...")
entrada_url.pack(pady=10)

frame_opcoes = ctk.CTkFrame(app, fg_color="transparent")
frame_opcoes.pack(pady=5)

tipo_var = ctk.StringVar(value="Vídeo")
radio_video = ctk.CTkRadioButton(frame_opcoes, text="Vídeo", variable=tipo_var, value="Vídeo", command=atualizar_menu_qualidade)
radio_video.grid(row=0, column=0, padx=15)
radio_audio = ctk.CTkRadioButton(frame_opcoes, text="Apenas Áudio", variable=tipo_var, value="Áudio", command=atualizar_menu_qualidade)
radio_audio.grid(row=0, column=1, padx=15)

combo_qualidade = ctk.CTkComboBox(app, width=250)
combo_qualidade.pack(pady=10)
atualizar_menu_qualidade()

frame_pasta = ctk.CTkFrame(app, fg_color="transparent") 
frame_pasta.pack(pady=15)
entrada_pasta = ctk.CTkEntry(frame_pasta, width=300)
entrada_pasta.grid(row=0, column=0, padx=(0, 10))
entrada_pasta.insert(0, pasta_downloads_padrao) 

botao_procurar = ctk.CTkButton(frame_pasta, text="Pasta", width=60, command=selecionar_pasta)
botao_procurar.grid(row=0, column=1, padx=(0, 5))
botao_restaurar = ctk.CTkButton(frame_pasta, text="Reset", width=60, fg_color="#454545", hover_color="#2b2b2b", command=restaurar_downloads)
botao_restaurar.grid(row=0, column=2)

botao_baixar = ctk.CTkButton(app, text="INICIAR DOWNLOAD", command=iniciar_download, font=("Arial", 16, "bold"), height=50, fg_color="#1f538d", hover_color="#14375e")
botao_baixar.pack(pady=20)

barra_progresso = ctk.CTkProgressBar(app, width=450, height=15)
barra_progresso.pack(pady=(5, 0))
barra_progresso.set(0)

label_porcentagem = ctk.CTkLabel(app, text="0%", font=("Arial", 12, "bold"))
label_porcentagem.pack(pady=2)

label_status = ctk.CTkLabel(app, text="", font=("Arial", 14, "bold"))
label_status.pack(pady=5)

app.mainloop()