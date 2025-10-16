import streamlit as st
import pandas as pd
import time

# --- Configuração da página ---
st.set_page_config(page_title="Desafio da Energia Sustentável", page_icon="⚡", layout="centered")

# --- CSS de estilo ---
st.markdown("""
<style>
body {
    background-color: #f0fdf4;
    background-image: url('https://img.icons8.com/ios/452/solar-panel.png');
    background-size: 100px;
    background-repeat: repeat;
    background-attachment: fixed;
    opacity: 0.97;
}
h1 {
    text-align: center;
    color: #1a4d2e;
    text-shadow: 1px 1px 4px #9be79d;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 800;
    font-size: 2.5em;
    animation: brilho 2s infinite alternate;
}
@keyframes brilho {
    from { text-shadow: 0 0 8px #7ffb6c; }
    to { text-shadow: 0 0 20px #24d64d; }
}
.stButton button {
    background-color: #1a4d2e;
    color: white;
    font-size: 1.2em;
    padding: 10px 30px;
    border-radius: 12px;
    border: none;
    transition: 0.3s;
}
.stButton button:hover {
    background-color: #2ecc71;
    transform: scale(1.05);
}
.stRadio > div {
    background-color: #000000;
    padding: 15px;
    border-radius: 10px;
}
.dataframe {
    border-radius: 10px !important;
    border: 1px solid #b6f1c3;
}
.stTextInput>div>div>input {
    background-color: #000000;
    border-radius: 10px;
    border: 2px solid #2ecc71;
    padding: 8px;
    font-size: 1.1em;
}
</style>
""", unsafe_allow_html=True)

# --- Título ---
st.title("⚡ Desafio da Energia Sustentável ⚡")
st.markdown("<p style='text-align:center; color:#1a4d2e;'>Descubra quanto você entende sobre energia limpa e sustentabilidade! 🌿</p>", unsafe_allow_html=True)

# --- Arquivo de ranking ---
RANKING_FILE = "ranking.csv"

# Cria o arquivo se não existir
try:
    ranking_df = pd.read_csv(RANKING_FILE)
except FileNotFoundError:
    ranking_df = pd.DataFrame(columns=["Nome","Curso", "Pontuação"])
    ranking_df.to_csv(RANKING_FILE, index=False)

# --- Funções ---
def tocar_som(tipo):
    """Som de acerto ou erro"""
    if tipo == "acerto":
        sound = "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg"
    else:
        sound = "https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg"
    st.markdown(f"""
        <audio autoplay>
        <source src="{sound}" type="audio/ogg">
        </audio>
        """, unsafe_allow_html=True)

def salvar_ranking(nome, curso, pontos):
    global ranking_df
    novo = pd.DataFrame([[nome, curso, pontos]], columns=["Nome","Curso", "Pontuação"])
    ranking_df = pd.concat([ranking_df, novo], ignore_index=True)
    ranking_df.to_csv(RANKING_FILE, index=False)

# --- Perguntas ---
perguntas = [
    {
        "pergunta": "Qual destas opções é uma fonte de energia renovável?",
        "opcoes": ["Carvão Mineral", "Energia Solar", "Petróleo"],
        "correta": "Energia Solar"
    },
    {
        "pergunta": "O que ajuda a economizar mais energia elétrica?",
        "opcoes": ["Deixar aparelhos em stand-by", "Usar lâmpadas LED", "Ligar vários aparelhos na mesma tomada"],
        "correta": "Usar lâmpadas LED"
    },
    {
        "pergunta": "O que significa 'energia limpa'?",
        "opcoes": [
            "Energia que não polui o meio ambiente",
            "Energia usada apenas em casas",
            "Energia mais barata"
        ],
        "correta": "Energia que não polui o meio ambiente"
    },
    {
        "pergunta": "Como a energia solar ajuda a reduzir o aquecimento global?",
        "opcoes": ["Diminuindo a emissão de gases poluentes", "Aumentando o consumo de energia elétrica", "Evitando o uso de painéis em áreas urbanas", "Gerando calor para o planeta"],
        "correta": "Diminuindo a emissão de gases poluentes"
    },
    {
        "pergunta": "Qual dessas atitudes também contribui para o uso sustentável de energia?",
        "opcoes": ["Desligar aparelhos da tomada quando não estão em uso", "Deixar luzes acesas em todos os cômodos", "Usar ar-condicionado o máximo o tempo todo", "Lavar roupas com pouca carga várias vezes ao dia"],
        "correta": "Desligar aparelhos da tomada quando não estão em uso"
    }
]

# --- Criação de Abas --- #
aba_quiz, aba_ranking, aba_sobre_projeto = st.tabs(["⚡ Desafio da Energia Sustentável", "🏆 Ranking Geral", "⚙️ Sobre o Projeto"])

# --- Aba do Quiz --- #

with aba_quiz:
    st.subheader("👤 Digite seu nome e curso para começar")
    nome = st.text_input("Seu nome:")
    curso = st.text_input("Seu curso:")

    if nome and curso:
        if "pontos" not in st.session_state:
            st.session_state.pontos = 0
            st.session_state.pergunta_atual = 0

        # Pergunta atual
        if st.session_state.pergunta_atual < len(perguntas):
            p = perguntas[st.session_state.pergunta_atual]
            st.markdown(f"### ❓ {p['pergunta']}")
            resposta = st.radio("Escolha uma opção:", p["opcoes"], index=None)

            if st.button("Responder"):
                if resposta == p["correta"]:
                    st.success("✅ Resposta correta!")
                    tocar_som("acerto")
                    st.session_state.pontos += 1
                else:
                    st.error(f"❌ Errado! A resposta certa é: **{p['correta']}**.")
                    tocar_som("erro")

                st.session_state.pergunta_atual += 1
                time.sleep(1)
                st.rerun()

        else:
            # --- Resultado final ---
            st.markdown("## 🏁 Resultado Final")
            st.write(f"Você acertou **{st.session_state.pontos} de {len(perguntas)} perguntas!**")

            if st.session_state.pontos == 3:
                st.balloons()
                st.success("🌞 Incrível! Você é um **Guardião da Energia Sustentável!**")
            elif st.session_state.pontos == 2:
                st.info("⚡ Muito bem! Você está no caminho certo!")
            else:
                st.warning("💡 Continue aprendendo sobre energia limpa!")

            # Ranking
            salvar_ranking(nome,curso, st.session_state.pontos)
            st.markdown("---")
            st.markdown("### 🏆 Ranking do Dia")
            ranking_df = pd.read_csv(RANKING_FILE).sort_values(by="Pontuação", ascending=False)
            st.dataframe(ranking_df, hide_index=True)

            if st.button("🔁 Jogar Novamente"):
                st.session_state.pontos = 0
                st.session_state.pergunta_atual = 0
                st.rerun()
    else:
        st.info("✏️ Digite seu nome e curso acima para começar o quiz.")

with aba_ranking:
    st.title("🏆 Ranking Geral")
    st.markdown("<p style='text-align:center; color:#1a4d2e;'>Acompanhe o ranking do desafio!</p>", unsafe_allow_html=True)

    try:
        ranking_df = pd.read_csv(RANKING_FILE).sort_values(by="Pontuação", ascending=False)
        st.dataframe(ranking_df, hide_index=True, use_container_width=True)
    except FileNotFoundError:
        st.warning("Ainda não há pontuações registradas.")

    st.markdown("---")
    st.caption("Atualize a página para ver novos resultados em tempo real. 🔄")

with aba_sobre_projeto:
    st.title("🌞 Sobre o Projeto")
    st.markdown("""
    **Objetivo Principal:**  
    Desenvolver um sistema de **carregamento de celular movido à energia solar**, promovendo o uso de fontes renováveis e acessíveis em espaços públicos.

    **Descrição:**  
    O projeto foi aplicado em uma **maquete de ponto de ônibus**, onde instalamos uma **placa solar** conectada a um **regulador de tensão LM2596**, responsável por ajustar a corrente elétrica e carregar o celular com segurança.  
    Nosso objetivo é mostrar como a tecnologia pode ser usada de forma sustentável no dia a dia.

    **Curso:**  
    Técnico em Eletrotécnica — FORTEC

    **Integrantes:**  
    - Deivison Dias  
    - Davi Fernandes  
    - Leonam Santos
    - Felipe Mota
    - Lucas dos Santos
    - Raphael Elias
    - Thiago Carvalho
    """)


    st.image("maquete.png", caption="Maquete do ponto de ônibus com carregador solar", width=350)
