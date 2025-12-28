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
    query = f"Top innovative Tech and AI news released on {data_str}. Focus on breakthroughs, new models, and industry shifts."
    risultati = tavily.search(query=query, search_depth="advanced", max_results=7)
    
    # Creiamo il contesto per l'AI
    context_news = "\n".join([f"- {r['title']}: {r['content']} (Link: {r['url']})" for r in risultati['results']])

    print("🧠 L'AI sta scrivendo il report...")
    
    # 3. Prompt per Gemini
    prompt = f"""
    Sei un esperto giornalista tech. Analizza queste notizie grezze del giorno {data_str}:
    
    {context_news}
    
    Scrivi un report sintetico in Italiano usando la formattazione Markdown.
    Struttura richiesta:
    # 🗞️ Tech Report del {data_str}
    
    ## 🚀 Top News
    (Descrivi le 2-3 notizie più importanti in dettaglio)
    
    ## ⚡ In Breve
    (Elenco puntato rapido delle altre notizie)
    
    ---
    *Fonti incluse nel testo.*
    """

    # 4. Generazione (Google Gemini)
    response = model.generate_content(prompt)
    report_content = response.text

    # 5. Salva il report
    output_path = os.path.join(os.path.dirname(__file__), "report_oggi.md")
    with open("report_oggi.md", "w", encoding="utf-8") as f:
        f.write(report_content)

if __name__ == "__main__":
    genera_report()

    print(f"✅ Fatto! Report salvato in '{os.path.join(os.path.dirname(__file__), 'report_oggi.md')}'")
