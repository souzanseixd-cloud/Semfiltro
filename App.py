import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Zero Filtro 💀", page_icon="💀")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { background-color: #1e222b; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💀 Zero Filtro")
st.caption("Conectada via Groq | Velocidade Máxima")

# --- CHAVE DE API ---
# Sua chave configurada
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- MEMÓRIA DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens na tela
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- ENTRADA DO USUÁRIO ---
if prompt := st.chat_input("Manda a real..."):
    # Guarda e mostra a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta da Zero Filtro
    with st.chat_message("assistant"):
        try:
            # Personalidade injetada direto na chamada para evitar erro 400
            chat_completion = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=[
                    {
                        "role": "system", 
                        "content": "Seu nome é Zero Filtro. Você é uma IA foda, sarcástica e direta. Não use filtros de polidez. Seja curta e grossa."
                    },
                    *st.session_state.messages
                ],
                temperature=0.7
            )
            
            resposta = chat_completion.choices[0].message.content
            st.markdown(resposta)
            
            # Guarda a resposta da IA no histórico
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            
        except Exception as e:
            st.error(f"Erro na comunicação: {e}")
