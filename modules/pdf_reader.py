import streamlit as st
import os
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="Mon CV", layout="wide")

st.title("📄 Mon Curriculum Vitae")

st.markdown("""
Vous pouvez visualiser mon parcours et mes compétences directement ci-dessous, ou télécharger le document pour le conserver.
""")

st.divider()

# Nom du fichier CV tel que défini dans Accueil.py
cv_filename = "cv_RivolletNicolas_v2602-5.pdf"
if os.path.exists(cv_filename):
    with open(cv_filename, "rb") as f:
        pdf_data = f.read()
    
    st.download_button(
        label="📥 Télécharger mon CV (PDF)",
        data=pdf_data,
        file_name="CV_Nicolas_Rivollet.pdf",
        mime="application/pdf"
    )
    
    pdf_viewer(input=pdf_data, width=700)
else:
    st.error(f"Fichier {cv_filename} introuvable.")