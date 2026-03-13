import google.generativeai as genai

class AICopywriter:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def gerar_pacote(self, marca, url):
        prompt = f"Crie legendas de alta conversão para a marca {marca} baseada no conteúdo do link {url}. Gere uma versão para Instagram com hashtags e uma curta para WhatsApp Status."
        response = self.model.generate_content(prompt)
        return response.text