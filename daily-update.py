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

model = genai.GenerativeModel('gemini-3-flash-preview')

def genera_report():
    print("🔍 Cerco le notizie...")
    # 1. Calcola la data di ieri
    ieri = datetime.date.today() - datetime.timedelta(days=1)
    data_str = ieri.strftime("%Y-%m-%d")
    
    # 2. Cerca le notizie (Tavily)
    queries = [
    "new AI model release or breakthrough",
    "AI startup funding or tech company AI announcement",
    "new AI tools or product launch"
    ]

    all_results = []

    for q in queries:
        res = tavily.search(
            query=q,
            search_depth="advanced",
            max_results=15,
            time_range="week"
        )
        all_results.extend(res["results"])
    
    # Creiamo il contesto per l'AI
    unique_titles = set()
    filtered = []

    for r in all_results:
        norm = normalize(r["title"])
        if norm not in unique_titles:
            unique_titles.add(norm)
            filtered.append(r)

    context_text = "\n".join(
    f"- {r['title']}: {r['content'][:300]} (Link: {r['url']})"
    for r in filtered
    )
    print("🧠 L'AI sta scrivendo il report...")
    
    # 3. Prompt per Gemini
    prompt = f"""
    Sei un curatore editoriale tech esperto. Il tuo compito è filtrare il rumore e fornire solo i fatti.
    
    Analizza queste notizie grezze del {data_str}:
    {context_text}
    Seleziona le 8 notizie più importanti per il settore AI tra quelle fornite.
    Preferisci notizie riguardanti:
    - nuovi modelli AI
    - startup AI funding
    - nuovi tool AI
    - breakthrough di ricerca

    Ignora:
    - tutorial
    - opinioni
    - guide
    Scarta fonti poco affidabili o clickbait.
    Preferisci fonti tech riconosciute.
    Crea un report essenziale in Italiano (Markdown).
    
    STRUTTURA OBBLIGATORIA:
    # Tech Briefing del {data_str}
    
    ## Flash News (Tech, AI)
    (Qui inserisci una lista puntata. OGNI punto deve seguire rigorosamente questo formato:
    * [Titolo della notizia in Italiano](URL_ORIGINALE) - Una singola frase sintetica che spiega la notizia.)
    
    REGOLE:
    - Niente intro o conclusioni ("Ecco il report..."). Vai dritto al punto.
    - Usa SOLO le notizie presenti nel contesto.
    - Il titolo deve essere il link (Markdown syntax).
    - Massimo 8 punti totali.
    """

    # 4. Generazione (Google Gemini)
    response = model.generate_content(prompt)
    report_content = response.text

    # 5. Salva il report
    output_path = os.path.join(os.path.dirname(__file__), "report_oggi.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)


def normalize(title):
    return title.lower().strip()

if __name__ == "__main__":
    genera_report()
    print(f"✅ Fatto! Report salvato in '{os.path.join(os.path.dirname(__file__), 'report_oggi.md')}'")
