import os
from PIL import Image as PILImage, ImageDraw, ImageFont

# O "curativo" para o Python novo e o Pillow
if not hasattr(PILImage, 'ANTIALIAS'):
    PILImage.ANTIALIAS = PILImage.LANCZOS

# Importamos o módulo "vfx" que contém os efeitos de Hollywood do MoviePy
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx.all as vfx

class VideoProcessor:
    @staticmethod
    def processar(input_path, brand_name):
        output_path = f"output/post_{brand_name.replace(' ', '_').lower()}.mp4"
        
        clip = VideoFileClip(input_path)
        
        # Otimização 9:16 (Vertical) - Redimensiona e corta o centro
        target_h, target_w = 1920, 1080
        clip_resized = clip.resize(height=target_h)
        x_center = clip_resized.w / 2
        clip_final = clip_resized.crop(x_center=x_center, width=target_w, height=target_h)
        
        # 🔥 O COMBO VIRAL (O Drible do Algoritmo) 🔥
        # 1. Espelhamento (Inverte direita com esquerda para zerar o código do vídeo)
        clip_final = clip_final.fx(vfx.mirror_x)
        
        # 2. Aceleração (Deixa o vídeo 15% mais rápido, prendendo a atenção da geração TikTok)
        clip_final = clip_final.fx(vfx.speedx, 1.15)
        
        # 3. Contraste e Cor (Deixa as paisagens de Natal 10% mais vivas)
        clip_final = clip_final.fx(vfx.colorx, 1.1)
        
        # Etiqueta da marca
        img = PILImage.new('RGBA', (800, 100), color=(0, 0, 0, 200)) 
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except IOError:
            font = ImageFont.load_default()
            
        draw.text((40, 15), brand_name, font=font, fill="white")
        temp_img_path = "downloads/temp_brand.png"
        img.save(temp_img_path)
        
        # Coloca a etiqueta pelo tempo exato do novo vídeo acelerado
        txt_clip = ImageClip(temp_img_path).set_duration(clip_final.duration).set_pos(("center", 1700))
        
        # Junta o vídeo editado com a etiqueta da marca
        main_video = CompositeVideoClip([clip_final, txt_clip])
        
        # 🔥 TELA FINAL DE VENDAS (End Screen) 🔥
        end_img = PILImage.new('RGB', (1080, 1920), color=(20, 20, 20))
        draw_end = ImageDraw.Draw(end_img)
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 90)
            font_sub = ImageFont.truetype("arial.ttf", 60)
        except IOError:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            
        draw_end.text((200, 800), "Gostou do vídeo?", font=font_title, fill="white")
        draw_end.text((150, 950), f"Siga a {brand_name}\ne clique no Link da Bio!", font=font_sub, fill="#00FF00")
        
        temp_end_path = "downloads/temp_endscreen.png"
        end_img.save(temp_end_path)
        
        # 2,5 segundos de tela final para as pessoas conseguirem ler
        end_clip = ImageClip(temp_end_path).set_duration(2.5)
        
        # Cola o vídeo de ação com a tela final de vendas
        final_movie = concatenate_videoclips([main_video, end_clip], method="compose")
        
        # Renderiza a máquina de vendas
        final_movie.write_videofile(
            output_path, 
            fps=30, 
            codec="libx264", 
            audio_codec="aac", 
            preset="ultrafast", 
            threads=4, 
            logger=None
        )
        
        # Limpeza de memória
        clip.close()
        txt_clip.close()
        main_video.close()
        end_clip.close()
        final_movie.close()
        
        return output_path