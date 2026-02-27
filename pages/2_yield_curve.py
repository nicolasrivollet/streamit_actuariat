import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Yield Curve Modeling | Portfolio", layout="wide")

# --- HEADER ---
st.title("🛡️ Strategic Yield Curve Modeling")
st.markdown("""
**Executive Summary:** This module demonstrates the parametric modeling of the Term Structure of Interest Rates (TSIR) using the **Nelson-Siegel framework**. 
In insurance and risk management, the yield curve is the heartbeat of the balance sheet, governing the valuation of **Best Estimate Liabilities (BEL)** and the calibration of **Asset-Liability Management (ALM)** strategies.
""")

st.divider()

# --- SIDEBAR: CONTROLS ---
st.sidebar.header("🕹️ Model Parameters")
st.sidebar.markdown("Adjust the factors to simulate economic shifts.")

b0 = st.sidebar.slider("Beta 0 (Level - Long Term)", 0.0, 0.10, 0.04, step=0.005, help="Represents the long-term value of the interest rate.")
b1 = st.sidebar.slider("Beta 1 (Slope - Short Term)", -0.10, 0.10, -0.02, step=0.005, help="Determines the slope of the curve.")
b2 = st.sidebar.slider("Beta 2 (Curvature - Medium Term)", -0.10, 0.10, 0.02, step=0.005, help="Captures the 'hump' in the 2-5 year maturity range.")
tau = st.sidebar.slider("Tau (Scale Factor)", 0.5, 10.0, 2.0, help="Controls the position of the curvature peak.")

# --- CALCULATION ---
t = np.linspace(0.1, 30, 100)
term1 = (1 - np.exp(-t/tau)) / (t/tau)
term2 = term1 - np.exp(-t/tau)
y = b0 + b1*term1 + b2*term2

# --- VISUALIZATION ---
fig = go.Figure()

# Main Curve
fig.add_trace(go.Scatter(x=t, y=y*100, mode='lines', name='Nelson-Siegel Curve', 
                         line=dict(color='#1f77b4', width=4)))

fig.update_layout(
    title="Projected Yield Curve (Spot Rates)",
    xaxis_title="Maturity (Years)",
    yaxis_title="Yield (%)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

col_chart, col_math = st.columns([2, 1])

with col_chart:
    st.plotly_chart(fig, use_container_width=True)

with col_math:
    st.markdown("### 📐 Mathematical Foundation")
    st.latex(r"y(t) = \beta_0 + \beta_1 \left( \frac{1 - e^{-t/\tau}}{t/\tau} \right) + \beta_2 \left( \frac{1 - e^{-t/\tau}}{t/\tau} - e^{-t/\tau} \right)")
    st.info("""
    **Factor Interpretation:**
    * **Level ($\beta_0$):** Parallel shifts.
    * **Slope ($\beta_1$):** Short-term expectations.
    * **Curvature ($\beta_2$):** Medium-term hump.
    """)

# --- STRATEGIC ANALYSIS SECTIONS ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏛️ Connection to Best Estimate (BEL)")
    st.write("""
    Under **Solvency II**, the yield curve is the fundamental tool for discounting future cash flows.
    * **Discounting:** Every projected claim or expense is discounted using the risk-free rate corresponding to its maturity.
    * **Smith-Wilson vs. Nelson-Siegel:** While Nelson-Siegel is ideal for internal risk steering, the **EIOPA** mandates the Smith-Wilson model for regulatory reporting to ensure convergence towards the **Ultimate Forward Rate (UFR)** beyond the Last Liquid Point (LLP).
    """)

with col2:
    st.markdown("### 🔍 Model Governance & Selection")
    st.write("""
    Selecting a yield curve model is a trade-off between **Smoothness** and **Fitness**:
    * **Nelson-Siegel:** Best for stability and economic interpretability. Ideal for ALM and CRO dashboards.
    * **Svensson Extension:** Used when the curve exhibits two humps (complex economic environments).
    * **Cubic Splines:** Preferred by Front-Office traders to perfectly match market prices, despite the risk of overfitting.
    """)

# --- RISK ANALYTICS ---
st.markdown("### 📊 Risk Management Perspectives")
risk_col1, risk_col2, risk_col3 = st.columns(3)

with risk_col1:
    st.metric("Long Term Level", f"{b0*100:.2f}%")
    st.caption("Asymptotic rate for infinite maturity.")

with risk_col2:
    slope_status = "Normal" if b1 < 0 else "Inverted"
    st.metric("Curve Shape", slope_status, delta=f"{b1:.3f}", delta_color="inverse" if b1 > 0 else "normal")
    st.caption("Negative slope ($\beta_1 < 0$) indicates a healthy term structure.")

with risk_col3:
    st.metric("Curvature Peak", f"{tau} Years")
    st.caption("Maturity where the $\\beta_2$ loading is maximized.")

st.markdown("---")
st.caption("Developed by Nicolas Rivollet - Actuarial & Risk Expertise Portfolio")