import google.generativeai as genai

class AICopywriter:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        
        # Sistema anti-falhas para achar o modelo correto
        modelo_correto = 'gemini-1.5-flash'
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    modelo_correto = m.name
                    break
        except Exception:
            pass
            
        self.model = genai.GenerativeModel(modelo_correto)

    def gerar_pacote(self, marca, url_original):
        # PROMPT OTIMIZADO: Estratégia profunda e minuciosa de conversão
        prompt = f"""
        Aja como o Diretor de Marketing Sênior da '{marca}', a empresa que é a maior referência em passeios de buggy em Natal, RN.
        Seu objetivo número um é o crescimento agressivo e estratégico no Instagram e TikTok.
        
        Escreva uma legenda magnética e altamente conversiva para o nosso novo Reels. 
        Referência de contexto do vídeo: {url_original}
        
        Siga RIGOROSAMENTE esta estrutura:
        1. Gancho Retentivo (Linha 1): Uma frase de impacto que gere curiosidade ou desejo imediato (ex: "Você teria coragem de descer essa duna?").
        2. Corpo do Texto (Storytelling): Venda a emoção, a segurança e a exclusividade de fazer o passeio com a nossa frota pelas praias e lagoas do RN.
        3. CTA de Vendas (Chamada para Ação): Uma instrução clara, mandando o cliente curtir, salvar o vídeo para o roteiro de viagem e clicar no link da bio (ou mandar Direct) para agendar.
        4. SEO/Hashtags: 5 a 8 hashtags estratégicas para o turismo no RN e passeios de buggy.
        
        Tom de voz: Envolvente, seguro, profissional e com energia lá em cima. Use emojis estratégicos, mas sem poluir a leitura.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Erro ao gerar o texto com a IA: {str(e)}"