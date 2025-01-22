import subprocess
import os

# Caminho para o modelo Piper
PIPER_EXECUTABLE = "D:\Repositories\DS\GlaDos\piper_windows_amd64\piper\piper.exe"
PIPER_MODEL = "D:\Repositories\DS\GlaDos\piper_windows_amd64\piper-voices\en_US-kristin-medium.onnx"
MODEL_JSON = "D:\Repositories\DS\GlaDos\piper_windows_amd64\piper\en_en_US_kristin_medium_en_US-kristin-medium.onnx.json"
OUTPUT_FILE = "output.wav"



def piper_speak(text):
    """Gera áudio com Piper e reproduz"""
    try:
        
        # Excluir o arquivo antigo, se existir
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
                    
        # Comando para sintetizar a fala
        subprocess.run([
        PIPER_EXECUTABLE,  
        "--model", PIPER_MODEL, 
        "--config", MODEL_JSON,
        "--output_file", OUTPUT_FILE, 
        "--sentence_silence 0.4",
        "--length_scale 1",
        "--noise_w 1",
        "--noise_scale 1",
        "--text", text
        ], 
        input=text.encode('utf-8'),
        check=True)
        
        # Reproduzir o áudio gerado
        #os.system(f"aplay {OUTPUT_FILE}")  # Para Linux
        # os.system(f"afplay {OUTPUT_FILE}")  # Para macOS
        os.system(f"start {OUTPUT_FILE}")  # Para Windows
    except Exception as e:
        print(f"Erro ao usar Piper: {e}")

# Exemplo de uso
if __name__ == "__main__":
    piper_speak("Waaaaaait! Who do you think you are to give me any commands?")
