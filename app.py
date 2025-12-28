import streamlit as st
import requests

# Configurazione pagina
st.set_page_config(page_title="Tech Daily Briefing", page_icon="☕")

# ---------------------------------------------------------
# 👇 INCOLLA QUI LO STESSO LINK CHE HAI USATO NEL DEBUG E CHE DAVA "200"
URL_REPORT = "INSERISCI_QUI_IL_TUO_LINK_RAW_FUNZIONANTE"
# ---------------------------------------------------------

def local_css():
    st.markdown("""
    <style>
    .report-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def leggi_report_online():
    try:
        # Scarica il file (disabilita la cache per essere sicuri di avere l'ultimo)
        response = requests.get(URL_REPORT, headers={"Cache-Control": "no-cache"})
        
        if response.status_code == 200:
            return response.text
        else:
            return "⚠️ Errore: Non riesco a scaricare il report. Controlla il link."
    except Exception as e:
        return f"⚠️ Errore di connessione: {e}"

# --- Interfaccia ---
local_css()

st.title("☕ Il tuo Briefing Tech")
st.caption("Le notizie più importanti di ieri, selezionate dall'AI.")
st.divider()

# Carica il report
contenuto = leggi_report_online()

if "⚠️" in contenuto:
    st.error(contenuto)
else:
    # Mostra il report
    st.markdown(contenuto)

# Footer
st.divider()
st.caption("Aggiornato automaticamente ogni mattina alle 07:00 • Powered by Gemini & GitHub")
