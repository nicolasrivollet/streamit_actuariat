import streamlit as st
import base64
import os

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
        base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    
    st.download_button(
        label="📥 Télécharger mon CV (PDF)",
        data=pdf_data,
        file_name="CV_Nicolas_Rivollet.pdf",
        mime="application/pdf"
    )
    
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.error(f"Fichier {cv_filename} introuvable.")