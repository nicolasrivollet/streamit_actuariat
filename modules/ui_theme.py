import streamlit as st

def apply_theme():
    """
    Applique la charte graphique institutionnelle :
    - Typographie à empattement (Source Serif 4) pour le corps et les titres
    - Typographie sans-serif (Inter) pour les contrôles, métriques et navigation
    - Palette de couleurs sobre (bleu nuit, ardoise, blanc cassé)
    - Style épuré pour les alertes, onglets et cartes
    """
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,300..700;1,8..60,300..700&display=swap');

    /* Typographie globale à empattement */
    html, body, [class*="css"], [data-testid="stAppViewContainer"], .stMarkdown, p, li {
        font-family: 'Source Serif 4', Georgia, 'Times New Roman', serif !important;
        color: #1E293B;
        font-size: 1.02rem;
        line-height: 1.65;
    }

    /* Titres avec empattement noble et couleur ardoise profonde */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Source Serif 4', Georgia, serif !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        letter-spacing: -0.015em !important;
    }

    h1 {
        font-size: 2.2rem !important;
        line-height: 1.25 !important;
        margin-bottom: 0.4rem !important;
    }

    h2 {
        font-size: 1.55rem !important;
        line-height: 1.3 !important;
        margin-top: 1.6rem !important;
        margin-bottom: 0.6rem !important;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 0.35rem;
    }

    h3 {
        font-size: 1.25rem !important;
        line-height: 1.35 !important;
        margin-top: 1.3rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Éléments techniques et interactifs en Inter (sans-serif net) */
    button, input, select, textarea, [data-testid="stSidebarNav"], 
    .stButton, .stTabs [data-baseweb="tab"], [data-testid="stMetricLabel"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Barre latérale (Sidebar) sobre et aérée */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }

    /* Alertes Streamlit (st.info, st.success, etc.) transformées en callouts discrets */
    div[data-testid="stAlert"] {
        border-radius: 4px !important;
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
        border-left: 3px solid #1E3A8A !important;
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        padding: 0.85rem 1.1rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    }

    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
        font-size: 0.95rem !important;
        line-height: 1.55 !important;
    }

    /* Onglets modernes et épurés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        border-bottom: 1px solid #E2E8F0 !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 0.92rem !important;
        padding: 8px 18px !important;
        color: #64748B !important;
        border-radius: 4px 4px 0 0 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #1E3A8A !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #1E3A8A !important;
        background-color: transparent !important;
    }

    /* Métriques (KPI) */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: #64748B !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #0F172A !important;
    }

    /* Cartes exécutives personnalisées */
    .exec-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 1.35rem 1.45rem;
        margin-bottom: 1rem;
        height: 100%;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .exec-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 3px 8px rgba(15, 23, 42, 0.06);
    }

    .exec-card-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.45rem;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid #F1F5F9;
    }

    .exec-card-text {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 0.93rem;
        color: #475569;
        line-height: 1.6;
        margin: 0;
    }

    /* Badges techniques */
    .badge-pill {
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.03em;
        padding: 0.22rem 0.65rem;
        border-radius: 4px;
        background-color: #F1F5F9;
        color: #334155;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        border: 1px solid #E2E8F0;
    }

    /* Séparateur subtil */
    hr {
        margin: 1.75rem 0 !important;
        border: none !important;
        border-top: 1px solid #E2E8F0 !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
