import streamlit as st
import os

# Configurazione della pagina (Titolo e Icona)
st.set_page_config(page_title="Tech Daily Briefing", page_icon="☕")

# Funzione per caricare il CSS personalizzato (Opzionale, per renderlo più carino)
def local_css():
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Titolo Principale
st.title("☕ Il tuo Briefing Tech")
st.caption("Le notizie più importanti di ieri, riassunte dall'AI.")

st.divider()

# Logica di lettura
file_report = "report_oggi.md"

if os.path.exists(file_report):
    with open(file_report, "r", encoding="utf-8") as f:
        contenuto = f.read()
    
    # Visualizza il contenuto Markdown
    st.markdown(contenuto)
else:
    # Se il file non esiste ancora (es. è la prima volta che lo apri)
    st.warning("⚠️ Nessun report trovato.")
    st.info("Esegui lo script 'daily_update.py' per generare il primo report!")

# Footer
st.divider()
st.text("Aggiornato automaticamente ogni mattina alle 07:00")