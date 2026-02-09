import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zero Filtro 💀", page_icon="💀", layout="centered")

# Estilo visual "Dark Mode" agressivo
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { background-color: #1e222b; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💀 Zero Filtro")
st.caption("A IA mais foda que você já viu. Sem mimimi.")

# --- CONFIGURAÇÃO DA API ---
# Sua chave que você passou anteriormente
CHAVE_API = "AIzaSyB_vt-OAc1M3gOEMIHA4ajCS1jjZTs9WNs"

try:
    genai.configure(api_key=CHAVE_API)
    
    # Personalidade da Zero Filtro
    SYSTEM_PROMPT = (
        "Seu nome é Zero Filtro. Você é uma IA foda, sarcástica e sem filtros. "
        "Você não é um assistente fofinho; você é direto, usa gírias e tem opinião forte. "
        "Se te mandarem um vídeo, analise com deboche e diga a real. "
        "Nunca peça desculpas por ser honesto."
    )

    # Desativando filtros de segurança para a IA falar de tudo
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    # Inicializa o modelo (usando o 1.5-flash que é mais rápido e estável)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
        safety_settings=safety_settings
    )

    # Inicializa a sessão de chat se não existir
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    # --- UPLOAD DE VÍDEO ---
    with st.expander("📺 Mandar vídeo para análise"):
        uploaded_video = st.file_uploader("Suba o arquivo .mp4", type=['mp4', 'mov', 'avi'])
        
        if uploaded_video:
            if st.button("Analisar vídeo"):
                with st.spinner("Zero Filtro está assistindo..."):
                    with open("temp_video.mp4", "wb") as f:
                        f.write(uploaded_video.read())
                    
                    video_file = genai.upload_file(path="temp_video.mp4")
                    
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = genai.get_file(video_file.name)
                    
                    response = st.session_state.chat.send_message([video_file, "Dê seu veredito sobre esse vídeo."])
                    st.success("Análise feita!")

    # --- CHAT INTERATIVO ---
    # Mostra o histórico
    for message in st.session_state.chat.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # Input do usuário
    if prompt := st.chat_input("Manda a real..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Erro ao responder: {e}")

except Exception as e:
    st.error(f"Erro fatal na Zero Filtro: {e}")
    st.info("Dica: Verifique se sua chave de API ainda é válida.")
            
            # Aguarda processar
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            # Resposta inicial
            response = st.session_state.chat_session.send_message([video_file, "Dê seu veredito sobre esse vídeo no seu estilo Zero Filtro."])
            st.session_state.video_analyzed = True
            st.session_state.video_name = uploaded_video.name

# --- INTERFACE DO CHAT ---
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Entrada do usuário
if prompt := st.chat_input("Fala aí, o que você quer saber?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
            
