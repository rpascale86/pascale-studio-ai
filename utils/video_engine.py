import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class VideoProcessor:
    @staticmethod
    def processar(input_path, brand_name):
        output_path = f"output/post_{brand_name.replace(' ', '_').lower()}.mp4"
        
        clip = VideoFileClip(input_path)
        
        # Otimização 9:16 (Vertical)
        target_h, target_w = 1920, 1080
        clip_resized = clip.resize(height=target_h)
        x_center = clip_resized.w / 2
        clip_final = clip_resized.crop(x_center=x_center, width=target_w, height=target_h)
        
        # Branding
        txt = TextClip(f" {brand_name} ", fontsize=50, color='white', bg_color='black', font='Arial-Bold')
        txt = txt.set_pos(("center", "bottom")).set_margin(bottom=100).set_duration(clip.duration)
        
        final = CompositeVideoClip([clip_final, txt])
        final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, logger=None)
        
        clip.close()
        return output_path