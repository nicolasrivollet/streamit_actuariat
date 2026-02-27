import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Solvency II Review | Insights", layout="wide")

# --- HEADER ---
st.title("⚖️ Solvency II Modernization (2024/2025 Review)")
st.subheader("Strategic Implications for European Insurers")

st.markdown("""
The ongoing revision of the Solvency II Directive aims to unlock capital for long-term investments while refining the sensitivity of the framework. 
As a **Head of Risk**, understanding these shifts is critical for capital planning and dividend policy.
""")

st.divider()

# --- KEY PILLARS OF THE REFORM ---
st.header("1. The Three Strategic Pillars")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🚀 Capital Relief")
    st.write("""
    * **Risk Margin (RM):** Significant reduction via a new cost-of-capital rate (lowered from 6% to 4.75%) and a floor mechanism.
    * **Impact:** Direct boost to Tier 1 Own Funds, especially for long-tail life business.
    """)

with col2:
    st.markdown("#### 🛡️ Macro-Prudential Tools")
    st.write("""
    * **New Powers:** Supervisors will have tools to address systemic liquidity risks and concentration.
    * **Impact:** Higher reporting burden and potential soft capital buffers during crises.
    """)

with col3:
    st.markdown("#### 🌿 Sustainability (ESG)")
    st.write("""
    * **Article 44:** Integration of climate change transition risk into the ORSA.
    * **Impact:** Pillar 1 could eventually see 'green' supporting or 'brown' penalizing factors.
    """)

st.divider()

# --- INTERACTIVE IMPACT SIMULATOR ---
st.header("2. Risk Margin Sensitivity Simulator")
st.write("Estimate the potential release of capital from the new Risk Margin formula.")

c_col1, c_col2 = st.columns([1, 2])

with c_col1:
    current_rm = st.number_input("Current Risk Margin (€M)", value=100)
    reduction_pct = st.slider("Expected Reduction (%)", 15, 30, 20)
    
    new_rm = current_rm * (1 - reduction_pct/100)
    capital_release = current_rm - new_rm

with c_col2:
    df_impact = pd.DataFrame({
        "Status": ["Current", "Post-Review"],
        "Risk Margin (€M)": [current_rm, new_rm]
    })
    fig = px.bar(df_impact, x="Status", y="Risk Margin (€M)", color="Status", 
                 color_discrete_map={"Current": "#EF553B", "Post-Review": "#00CC96"})
    st.plotly_chart(fig, use_container_width=True)

st.success(f"Estimated Capital Release: **€{capital_release:.2f}M** (This directly increases the Solvency Ratio).")

st.divider()

# --- CRO PERSPECTIVE ---
st.header("3. CRO Strategic Action Plan")
st.markdown("""
To navigate this transition, the Risk Function must prioritize:
1. **Volatility Adjustment (VA) Re-calibration:** Reviewing the impact of the new 'local component' in the VA formula.
2. **Long-Term Equity (LTE):** Assessing the relaxed criteria for LTE to optimize the SCR Equity charge (22% vs 39%/49%).
3. **Proportionality:** Leveraging simplified rules for 'Low-Risk Profile' undertakings to reduce administrative costs.
""")

st.info("💡 **Did you know?** The review also introduces a more phased-in approach for the transition to the new UFR (Ultimate Forward Rate) extrapolated via the Smith-Wilson model.")

st.caption("Strategic Analysis by Nicolas Rivollet - Expert in Insurance Risk Governance")