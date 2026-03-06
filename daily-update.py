import os
import datetime
from dotenv import load_dotenv
from tavily import TavilyClient
import google.generativeai as genai

# 1. Carica variabili d'ambiente
load_dotenv()

tavily_key = os.getenv("TAVILY_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if not tavily_key or not gemini_key:
    raise ValueError("⚠️ Chiavi API mancanti nel file .env")

# 2. Configura i Client
tavily = TavilyClient(api_key=tavily_key)
genai.configure(api_key=gemini_key)

model = genai.GenerativeModel('gemini-2.5-flash')

def genera_report():
    print("🔍 Cerco le notizie...")
    # 1. Calcola la data di ieri
    ieri = datetime.date.today() - datetime.timedelta(days=1)
    data_str = ieri.strftime("%Y-%m-%d")
    
    # 2. Cerca le notizie (Tavily)
    risultati = tavily.search(
    query="latest AI tech news new model release startup funding",
    search_depth="advanced",
    max_results=15,
    time_range="week"
)
    
    # Creiamo il contesto per l'AI
    unique_titles = set()
    filtered = []

    for r in risultati["results"]:
        if r["title"] not in unique_titles:
            unique_titles.add(r["title"])
            filtered.append(r)

    context_news = "\n".join([
        f"- {r['title']}: {r['content']} (Link: {r['url']})"
        for r in filtered
    ])
    print("🧠 L'AI sta scrivendo il report...")
    
    # 3. Prompt per Gemini
    prompt = f"""
    Sei un curatore editoriale tech esperto. Il tuo compito è filtrare il rumore e fornire solo i fatti.
    
    Analizza queste notizie grezze del {data_str}:
    {context_news}
    Assegna a ogni notizia un punteggio da 1 a 10 di importanza per il settore AI.
    Seleziona solo quelle >=7.
    
    Crea un report essenziale in Italiano (Markdown).
    
    STRUTTURA OBBLIGATORIA:
    # 🗞️ Tech Briefing del {data_str}
    
    ## ⚡ Flash News (Tech, AI)
    (Qui inserisci una lista puntata. OGNI punto deve seguire rigorosamente questo formato:
    * [Titolo della notizia in Italiano](URL_ORIGINALE) - Una singola frase sintetica che spiega la notizia.)
    
    REGOLE:
    - Niente intro o conclusioni ("Ecco il report..."). Vai dritto al punto.
    - Usa SOLO le notizie presenti nel contesto.
    - Il titolo deve essere il link (Markdown syntax).
    - Massimo 10-12 punti totali.
    """

    # 4. Generazione (Google Gemini)
    response = model.generate_content(prompt)
    report_content = response.text

    # 5. Salva il report
    output_path = os.path.join(os.path.dirname(__file__), "report_oggi.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

if __name__ == "__main__":
    genera_report()
    print(f"✅ Fatto! Report salvato in '{os.path.join(os.path.dirname(__file__), 'report_oggi.md')}'")

