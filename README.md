```markdown
# IronDownloader 4k🎬

Um aplicativo desktop de alta performance desenvolvido em Python para baixar vídeos e áudios do YouTube com qualidade máxima, focado em garantir compatibilidade total e imediata com o Adobe Premiere Pro e outros softwares de edição profissionais.

## 🚀 Principais Funcionalidades

* **Qualidade Máxima (até 4k):** Força o download das melhores trilhas de vídeo e áudio separadas e realiza a união perfeita (merge) utilizando o FFmpeg, garantindo arquivos `.mp4` limpos e sem engasgos.
* **Workflow Otimizado para Edição:** A opção "Apenas Áudio" converte e extrai o arquivo diretamente no formato `.wav` (sem perda de dados) ou `.mp3`, limpando arquivos temporários (`.webm`) para um workflow limpo no Premiere Pro.
* **Seleção Dinâmica de Resolução:** Menu inteligente que se adapta à sua escolha, oferecendo desde 144p até 2160p (4k/Max) para vídeo, e qualidades de estúdio para áudio.
* **Interface Gráfica Moderna (UI):** Desenvolvida com a biblioteca `customtkinter`, oferecendo um Dark Mode elegante, intuitivo e responsivo.
* **Processamento Assíncrono (Threading):** A interface do aplicativo não congela durante downloads pesados, mantendo-se 100% responsiva.
* **Feedback Visual em Tempo Real:** Barra de progresso integrada diretamente ao motor de download, mostrando a porcentagem exata e status da conversão.
* **Gestão Inteligente de Pastas:** Escolha facilmente o diretório de destino dos arquivos ou utilize o atalho rápido para a sua pasta de Downloads padrão.
* **Versão Portátil (.exe):** Pronto para uso como um executável independente (OneFile), sem necessidade de instalação do Python na máquina do usuário final.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x:** Linguagem principal do projeto.
* **yt-dlp:** O motor de extração de mídia mais poderoso e atualizado da atualidade.
* **CustomTkinter:** Framework utilizado para a construção da interface gráfica avançada.
* **FFmpeg:** Ferramenta de linha de comando essencial para renderização, conversão e união de mídia em segundo plano.
* **PyInstaller:** Utilizado para compilar o script em um executável independente.

## ⚙️ Instalação e Uso (Para Desenvolvedores)

### Pré-requisitos
* Ter o Python instalado.
* Ter o [FFmpeg](https://ffmpeg.org/) baixado e extraído no seu computador.

### Passo a passo
1. Clone este repositório no seu terminal:
   ```bash
   git clone [https://github.com/IronVisuals/IronDownloader.git](https://github.com/IronVisuals/IronDownloader.git)
   ```
2. Navegue até a pasta do projeto e crie um ambiente virtual para isolar as dependências:
   ```bash
   cd irondownloader
   python -m venv venv
   ```
3. Ative o ambiente virtual e instale as bibliotecas necessárias:
   ```bash
   pip install yt-dlp customtkinter pyinstaller
   ```
4. **Configuração Crucial de Caminho:** Abra o arquivo `main.py` e altere a variável `ffmpeg_location` para apontar exatamente onde a pasta `bin` do seu FFmpeg está localizada no seu computador.
5. Para executar o script diretamente:
   ```bash
   python main.py
   ```

## 👨‍💻 Autor

Desenvolvido por **Iron**.