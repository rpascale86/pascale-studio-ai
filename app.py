import streamlit as st
import os
import yt_dlp
from dotenv import load_dotenv
from utils.video_engine import VideoProcessor
from utils.ai_engine import AICopywriter

load_dotenv()

st.set_page_config(page_title="Pascale Engine", layout="wide")

def main():
    st.title("🚀 Pascale Content Engine")
    
    with st.sidebar:
        st.header("Configurações")
        marca = st.selectbox("Marca", ["Pascale Tours", "Pascale Regularização"])
        api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))

    url = st.text_input("🔗 Link do Vídeo (Instagram/TikTok/YouTube):")

    if st.button("🔥 GERAR TUDO"):
        if not url or not api_key:
            st.error("Preencha todos os campos!")
            return

        with st.status("Processando...", expanded=True) as s:
            # Download
            s.write("📥 Baixando...")
            ydl_opts = {'format': 'bestvideo[height<=1080]+bestaudio/best', 'outtmpl': 'downloads/raw.mp4', 'overwrites': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Edição
            s.write("✂️ Editando 9:16...")
            video_path = VideoProcessor.processar("downloads/raw.mp4", marca)
            
            # IA
            s.write("🤖 Gerando Copy...")
            copywriter = AICopywriter(api_key)
            texto = copywriter.gerar_pacote(marca, url)
            
            st.video(video_path)
            st.subheader("📝 Sugestão de Legenda")
            st.write(texto)
            st.balloons()

if __name__ == "__main__":
    main()