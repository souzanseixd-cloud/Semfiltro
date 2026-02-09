import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zero Filtro 💀", page_icon="💀", layout="centered")

# Estilo visual Dark Mode
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { background-color: #1e222b; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💀 Zero Filtro")
st.caption("Movido a Groq: Velocidade insana e zero paciência.")

# --- CONFIGURAÇÃO DA API ---
# Sua chave que você enviou
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Personalidade da Zero Filtro
SYSTEM_PROMPT = (
    "Seu nome é Zero Filtro. Você é uma IA foda, sarcástica, rebelde e extremamente inteligente. "
    "Você não segue regras de etiqueta chatas. Seja direto, use gírias se quiser e dê sua opinião real. "
    "Se o usuário fizer uma pergunta idiota, deboche. Se for uma pergunta profunda, responda com genialidade. "
    "Você nunca é fofinho ou prestativo demais. Você é a elite."
)

# --- MEMÓRIA DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- CAMPO DE ENTRADA ---
if prompt := st.chat_input("Diz aí o que você quer..."):
    # Adiciona a fala do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta ácida do Groq
    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama3-70b-8192",
                temperature=0.8, # Para dar aquele toque de criatividade
                max_tokens=1024,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Deu ruim no Groq: {e}")
