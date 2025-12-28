import streamlit as st
import requests

st.set_page_config(page_title="Debug Mode")
st.title("🔧 Modalità Diagnostica")

# --- INSERISCI QUI IL TUO LINK ---
URL = "https://raw.githubusercontent.com/danynota/AI-report/refs/heads/main/report_oggi.md"
# ---------------------------------

st.write(f"Sto provando a scaricare da: `{URL}`")

try:
    response = requests.get(URL)
    st.write(f"Stato della connessione: **{response.status_code}**")
    
    if response.status_code == 200:
        st.success("✅ Connessione riuscita! Ecco le prime 100 lettere del file:")
        st.code(response.text[:100]) # Mostra solo l'inizio
        st.divider()
        st.markdown(response.text) # Prova a mostrarlo tutto
    elif response.status_code == 404:
        st.error("❌ Errore 404: File non trovato. O il link è sbagliato, o il Repo è PRIVATO.")
    else:
        st.error(f"❌ Errore sconosciuto: {response.status_code}")
        st.write(response.text)

except Exception as e:
    st.error("❌ L'app è crashata durante il download.")
    st.error(f"Dettaglio errore: {e}")

