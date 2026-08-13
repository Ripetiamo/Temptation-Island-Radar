import re
import feedparser
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Temptation Island Radar",
    page_icon="🏝️",
    layout="wide"
)

# Stile CSS per i titoli
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    h3 { color: #1f2937; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# URL del feed RSS
RSS_URL = "https://news.google.com/rss/search?q=Temptation+Island&hl=it&gl=IT&ceid=IT:it"

@st.cache_data(ttl=600)
def fetch_news(feed_url):
    try:
        parsed_feed = feedparser.parse(feed_url)
        return parsed_feed.entries
    except Exception:
        return []

# Intestazione
st.title("🏝️ Temptation Island Radar")
st.markdown("Tutte le ultime news, falò di confronto e gossip in tempo reale.")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/palm-tree.png", width=70)
    st.header("Esplora")
    
    search_query = st.text_input("🔍 Cerca argomento:", "", placeholder="Es. falò, coppie...")

    st.divider()
    
    st.markdown("### ☕ Ti piace l'app?")
    st.write("Sostieni il progetto.")
    
    st.link_button("☕ Offrimi un caffè", "https://ko-fi.com/repeat98201", use_container_width=True)

st.divider()

# Notizie
st.subheader("🔥 Ultime Notizie")
entries = fetch_news(RSS_URL)

if not entries:
    st.warning("Nessuna notizia disponibile.")
else:
    cols = st.columns(2)
    count = 0
    
    for entry in entries:
        if search_query and search_query.lower() not in entry.title.lower():
            continue
            
        with cols[count % 2]:
            with st.container(border=True):
                st.markdown(f"**{entry.title}**")
                published = getattr(entry, 'published', 'Data non disp.')
                st.caption(f"📅 {published}")
                
                # Pulizia totale del sommario da qualsiasi tag HTML/href
                raw_summary = getattr(entry, 'summary', '')
                summary = re.sub('<.*?>', '', raw_summary)
                
                if len(summary) > 150: 
                    summary = summary[:150] + "..."
                st.write(summary)
                
                st.link_button("Leggi", entry.link, use_container_width=True)
        count += 1
