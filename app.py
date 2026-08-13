import feedparser
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Temptation Island Radar",
    page_icon="🏝️",
    layout="wide"
)

# Stile CSS personalizzato
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    h3 {
        color: #1f2937;
        font-weight: 600;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 8px;
        margin-top: 20px;
    }
    .stLinkButton > a {
        background-color: #e11d48;
        color: white;
        border-radius: 8px;
        font-weight: 500;
        text-align: center;
    }
    .stLinkButton > a:hover {
        background-color: #be123c;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# URL del feed RSS mirato esclusivamente a Temptation Island tramite Google News
RSS_URL = "https://news.google.com/rss/search?q=Temptation+Island&hl=it&gl=IT&ceid=IT:it"

# Funzione per scaricare le notizie con cache
@st.cache_data(ttl=600)
def fetch_news(feed_url):
    try:
        parsed_feed = feedparser.parse(feed_url)
        return parsed_feed.entries
    except Exception:
        return []

# Intestazione principale
st.title("🏝️ Temptation Island Radar")
st.markdown("Tutte le ultime news, i falò di confronto, le anticipazioni e il gossip sul reality show più discusso d'Italia.")

# Sidebar per la ricerca e la monetizzazione
with st.sidebar:
    st.image("https://img.icons8.com/color/96/palm-tree.png", width=70)
    st.header("Esplora")
    
    search_query = st.text_input("🔍 Cerca argomento o coppia:", "", placeholder="Es. falò, coppie, anticipazioni...")

    st.divider()
    
    # Sezione Donazioni / Ko-fi
    st.markdown("### ☕ Ti piace l'app?")
    st.write("Sostieni il progetto e mantieni il radar sempre attivo.")
    
    st.markdown("""
        <a href="https://ko-fi.com/repeat98201" target="_blank" style="
            display: block;
            background: linear-gradient(135deg, #ff5e5b 0%, #ff8a5b 100%);
            color: #ffffff;
            padding: 12px 20px;
            text-align: center;
            text-decoration: none;
            font-weight: 700;
            font-size: 16px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(255, 94, 91, 0.4);
            margin-top: 10px;
            margin-bottom: 10px;
        ">
            ☕ Offrimi un caffè
        </a>
    """, unsafe_allow_html=True)

st.divider()

# Caricamento e visualizzazione delle notizie in griglia
st.subheader("🔥 Ultime Notizie in Tempo Reale")
entries = fetch_news(RSS_URL)

if not entries:
    st.warning("Al momento non è possibile recuperare le notizie. Riprova più tardi.")
else:
    cols = st.columns(2)
    count = 0
    
    for entry in entries:
        title = entry.title
        
        # Filtro di ricerca testuale
        if search_query and search_query.lower() not in title.lower():
            continue
            
        with cols[count % 2]:
            with st.container(border=True):
                st.markdown(f"#### {title}")
                
                published = getattr(entry, 'published', 'Data non disponibile')
                st.caption(f"📅 {published}")
                
                raw_summary = getattr(entry, 'summary', 'Nessun sommario disponibile.')
                if len(raw_summary) > 200:
                    raw_summary = raw_summary[:200] + "..."
                
                st.write(raw_summary)
                
                st.link_button("Leggi l'articolo completo", entry.link, use_container_width=True)
        count += 1

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>Temptation Island Radar &bull; Creato con Python e Streamlit</p>", 
    unsafe_allow_html=True
)