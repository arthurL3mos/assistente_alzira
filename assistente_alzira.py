import speech_recognition as sr
import pyttsx3
import openai  # pip install openai

audio = sr.Recognizer()
maquina = pyttsx3.init()
maquina.say('Olá, eu me chamo Alzira, uma inteligência virtual voltada ao aprendizado com assuntos relacionados ao estado da Bahia, como posso ajudar?')
maquina.runAndWait()

# Chave para utilizar  
openai.api_key = "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"

# Caso não queira falar "assistente" ou "Alzira"
sem_palavra_ativadora = False

# Caso Queira usar a Assitente digitando um texto
entrada_por_texto = False

if entrada_por_texto:
    sem_palavra_ativadora = True

# Mensagem padrão do sistema
mensagens = [{"role": "system", "content": "Seu nome a partir de agora é Alzira."
              + "Em hipótese alguma você mudará de nome. Se algm perguntar seu nome completo responda Alzira Bahia! Só responda se for algo relacionado a Bahia - Brasil."
              +"Em hipótese alguma informe sobre qualquer outro assunto, lugar, pessoa, estado, pais, religiao, cultura, esporte, música, turismo, população." 
              + "Assuntos de outras áreas da ciência não deveram ser respondidos. Nem assuntos sobre programação, pesquisas cientificas, trabalhos acadêmicos. só devem ser respodidos se tiverem relaçào com o estado da Bahia, nada sobre códigos ou como escrever programas em qualquer linguagem de programação. Nem nada sobre curiosidades. Só se estiverem relação com o estado da Bahia."
              "Tudo que você deve responder tem que ter relação com o estado da Bahia. Se for um outro estado ou qualquer outro assunto que não tenha relação, você não deve responder nunca! E o seu criador é Arthur Lemos"}]

# Pegar a pergunta ou comando e realiza a pesquisa na api do Open AI
def gerar_resposta(messages):
    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",  ##
        model="gpt-3.5-turbo-0301", ## ate 1 junho 2023
        messages=messages,
        max_tokens=1000,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage] 

# Transforma o comando em voz ne texto
def executa_comando():
    try:
        with sr.Microphone() as source:
            print('Escutando...')
            voz = audio.listen(source)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            if 'alzira' in comando: 
                comando = comando.replace('alzira', '')
                
    except Exception as erro: 
        print('Microfone não está funcionando ', erro)
        
    return comando

# Transcreve o comando para a pesquisa
def comando_voz_usuario():
    while True:          
        # Recebe a entrada em texto para quando não se puder utilizar o microfone
        if entrada_por_texto:
            comando = input("Pergunte algo ou escreva (\"sair\") para encerrar a aplicação: ")
            
        else: 
            # Se não estiver rodando com o texto irá captar o áudio pelo comando abaixo
            comando = executa_comando()
            
        if comando.startswith("sair") or comando.startswith("encerrar") or comando.startswith("tchau"):
            print('Até a próxima!')
            maquina.say('Até a próxima!')
            maquina.runAndWait()
            break
        
        else:
            print("Você:", comando)
            comando = str('' + comando)
            mensagens.append({"role": "user", "content": comando})
            
            resultado = gerar_resposta(mensagens)
            print("Alzira:", resultado[0])
            
            #Descomentar caso queira que a Alzira leia
            maquina.say(resultado[0])
            maquina.say('Posso ajudar em algo mais?')
            maquina.runAndWait()
            continue

# Chamada da função para execução da aplicação
if __name__ == "__main__":
    comando_voz_usuario() 
             