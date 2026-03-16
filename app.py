import streamlit as st
import os
import yt_dlp
from dotenv import load_dotenv

# Importando nossos motores da pasta utils
from utils.video_engine import VideoProcessor
from utils.ai_engine import AICopywriter

# Garante que as pastas de trabalho existam para não dar erro
os.makedirs("downloads", exist_ok=True)
os.makedirs("output", exist_ok=True)

load_dotenv()

st.set_page_config(page_title="Pascale Studio AI", layout="wide", page_icon="🚀")

st.title("🚀 Pascale Studio AI")
st.markdown("Bem-vindo à sua central de automação de marketing.")

with st.sidebar:
    st.header("⚙️ Configurações")
    marca = st.selectbox("Selecione a Marca:", ["Pascale Tours", "Pascale Regularização"])
    api_key = st.text_input("Gemini API Key:", type="password", value=os.getenv("GEMINI_API_KEY", ""))

url = st.text_input("🔗 Link do Vídeo (Instagram/TikTok/YouTube):")

if st.button("🔥 GERAR TUDO", use_container_width=True):
    if not url or not api_key:
        st.error("⚠️ Preencha o link do vídeo e a Chave da API para continuar.")
    else:
        with st.status("🛸 Processando sua automação...", expanded=True) as status:
            try:
                # 1. Download
                status.write("📥 1/3: Baixando o vídeo original na melhor qualidade...")
                ydl_opts = {
                    'format': 'bestvideo[height<=1080]+bestaudio/best', 
                    'outtmpl': 'downloads/raw.mp4', 
                    'overwrites': True,
                    'quiet': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 2. Edição
                status.write("✂️ 2/3: Adaptando para o formato 9:16 e aplicando a marca...")
                video_path = VideoProcessor.processar("downloads/raw.mp4", marca)
                
                # 3. IA Copywriting
                status.write("🤖 3/3: Acionando o Gemini Sênior para escrever as legendas...")
                copywriter = AICopywriter(api_key)
                texto = copywriter.gerar_pacote(marca, url)
                
                status.update(label="✅ Conteúdo Pronto para as Redes!", state="complete")
                st.balloons()
                
                # --- Exibição do Resultado ---
                st.divider()
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📱 Vídeo Finalizado")
                    st.video(video_path)
                    
                with col2:
                    st.subheader("📝 Copy Estratégica")
                    st.write(texto)

            except Exception as e:
                status.update(label="❌ Falha no processamento.", state="error")
                st.error(f"Erro técnico: {str(e)}")