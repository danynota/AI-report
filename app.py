import streamlit as st
import os
import requests
# Configurazione della pagina (Titolo e Icona)
st.set_page_config(page_title="Tech Daily Briefing", page_icon="☕")
URL_REPORT = https://raw.githubusercontent.com/danynota/AI-report/refs/heads/main/report_oggi.md
#Leggi file da web
def leggi_report_online():
    try:
        # Scarica il file direttamente da GitHub
        response = requests.get(URL_REPORT)
        
        # Se il file esiste (codice 200), restituisce il testo
        if response.status_code == 200:
            return response.text
        else:
            return "⚠️ Errore: Non riesco a scaricare il report da GitHub."
    except Exception as e:
        return f"⚠️ Errore di connessione: {e}"
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

contenuto = leggi_report_online()
st.markdown(contenuto)
# Footer
st.divider()

st.text("Aggiornato automaticamente ogni mattina alle 07:00")
