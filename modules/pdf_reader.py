import streamlit as st
import base64
import os

st.set_page_config(page_title="Lecteur PDF", layout="wide")

st.title("📄 Lecteur de Documents PDF")

st.markdown("""
Cet outil permet de visualiser des documents PDF directement dans l'application, sans avoir à les télécharger.
Il utilise le lecteur natif du navigateur via une intégration HTML.
""")

st.divider()

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Sélection du Document")
    source = st.radio("Source :", ["Mon CV (Portfolio)", "Charger un fichier"])

    pdf_file = None
    
    if source == "Mon CV (Portfolio)":
        # Nom du fichier CV tel que défini dans Accueil.py
        cv_filename = "cv_RivolletNicolas_v2602-5.pdf"
        if os.path.exists(cv_filename):
            with open(cv_filename, "rb") as f:
                pdf_file = f.read()
            st.success("CV chargé avec succès.")
        else:
            st.error(f"Fichier {cv_filename} introuvable.")
            
    else:
        uploaded_file = st.file_uploader("Uploader un PDF", type="pdf")
        if uploaded_file is not None:
            pdf_file = uploaded_file.read()

with col2:
    if pdf_file:
        # Encodage en base64 pour l'intégration HTML
        base64_pdf = base64.b64encode(pdf_file).decode('utf-8')
        
        # Injection de l'iframe
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.info("👈 Veuillez sélectionner ou charger un document pour le visualiser.")