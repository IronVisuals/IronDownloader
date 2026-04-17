```markdown
# IronDownloader 4k🎬

Um aplicativo desktop de alta performance desenvolvido em Python para baixar vídeos e áudios do YouTube com qualidade máxima, focado em garantir compatibilidade total e imediata com o Adobe Premiere Pro e outros softwares de edição profissionais.

## 🚀 Principais Funcionalidades

* **Qualidade Máxima (até 4K):** Força o download das melhores trilhas de vídeo e áudio separadas e realiza a união perfeita (merge) utilizando o FFmpeg, garantindo arquivos `.mp4` limpos e sem engasgos.
* **Workflow Otimizado para Edição:** A opção "Apenas Áudio" extrai o arquivo diretamente no formato `.wav` (sem perda de dados), evitando os tradicionais problemas de compressão e dessincronização causados por arquivos `.mp3` dentro do Premiere Pro.
* **Seleção Dinâmica de Resolução:** Menu inteligente que se adapta à sua escolha, oferecendo desde 144p até 2160p (4K/Max) para vídeo, e qualidades de estúdio para áudio.
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
   git clone [https://github.com/SEU_USUARIO/irondownloader.git](https://github.com/SEU_USUARIO/irondownloader.git)
   ```
2. Navegue até a pasta do projeto e crie um ambiente virtual para isolar as dependências:
   ```bash
   cd irondownloader
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   * **Windows:** `.\venv\Scripts\activate`
   * **Linux/Mac:** `source venv/bin/activate`
4. Instale as bibliotecas necessárias:
   ```bash
   pip install yt-dlp customtkinter pyinstaller
   ```
5. **Configuração Crucial de Caminho:** Abra o arquivo `main.py` e altere a variável `ffmpeg_location` para apontar exatamente onde a pasta `bin` do seu FFmpeg está localizada no seu computador.
6. Para executar o script diretamente:
   ```bash
   python main.py
   ```

## 📦 Como gerar o Executável (.exe)

Caso queira compilar o aplicativo para distribuir, certifique-se de estar com o ambiente virtual ativado e execute o comando abaixo no terminal:

```bash
pyinstaller --noconsole --onefile --name "IronDownloader" main.py
```

O arquivo `IronDownloader.exe` será gerado dentro da pasta `dist` do seu projeto. 

*(Aviso: Como o projeto depende do FFmpeg localmente, certifique-se de que a máquina que for rodar o `.exe` tenha acesso ao caminho especificado no código, ou adapte o código para usar um caminho relativo/global).*

## 👨‍💻 Autor

Desenvolvido por **Henrique**.
```

Para atualizar o seu GitHub com essas novidades, basta ir no terminal do VS Code (na pasta do projeto) e rodar estes três comandos:

1. `git add README.md` (Para adicionar a versão nova do arquivo)
2. `git commit -m "Atualiza README com novo nome e instruções do executável"`
3. `git push`

Com isso feito, seu projeto de portfólio estará com um visual super profissional!