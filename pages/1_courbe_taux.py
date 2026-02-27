import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import streamlit as st

# --- HEADER SECTION ---
st.title("Yield Curve Modeling")
st.subheader("The Nelson-Siegel Framework")

st.markdown("""
This module demonstrates the parametric modeling of the Term Structure of Interest Rates (TSIR). 
Mastering yield curve dynamics is essential for Asset-Liability Management (ALM), 
regulatory solvency capital requirements (SCR), and strategic asset allocation.
""")

# --- MATHEMATICAL FOUNDATION ---
st.markdown("### 1. Mathematical Framework")
st.latex(r"""
y(t) = \beta_0 + \beta_1 \left( \frac{1 - e^{-t/\tau}}{t/\tau} \right) + \beta_2 \left( \frac{1 - e^{-t/\tau}}{t/\tau} - e^{-t/\tau} \right)
""")

# Sidebar for parameters
st.sidebar.header("Model Parameters")
b0 = st.sidebar.slider("Beta 0 (Long-Term Level)", 0.0, 0.10, 0.04, step=0.005)
b1 = st.sidebar.slider("Beta 1 (Slope)", -0.10, 0.10, -0.02, step=0.005)
b2 = st.sidebar.slider("Beta 2 (Curvature)", -0.10, 0.10, 0.01, step=0.005)
tau = st.sidebar.slider("Tau (Scale Factor)", 0.1, 10.0, 2.0)

# Curve calculation
t = np.linspace(0.1, 30, 100)
term1 = (1 - np.exp(-t/tau)) / (t/tau)
term2 = term1 - np.exp(-t/tau)
y = b0 + b1*term1 + b2*term2

# Interactive visualization with Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Nelson-Siegel Curve', line=dict(color='#1f77b4', width=3)))
fig.update_layout(title="Term Structure of Interest Rates", xaxis_title="Maturity (Years)", yaxis_title="Rate", template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.info("""
**Note:** The Nelson-Siegel model is a parsimonious approach that describes the yield curve 
using four key parameters, reflecting the market's expectations of inflation, growth, and liquidity.
""")

# --- PARAMETERS INTERPRETATION ---
st.markdown("### 2. Factor Decomposition")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"""
    **$\\beta_0$ - The Level (Long-Term Rate):** Represents the value of the yield as maturity approaches infinity. 
    A change in $\\beta_0$ indicates a parallel shift in the curve.

    **$\\beta_1$ - The Slope (Short-Term Decay):** Determines the speed at which the curve reaches its long-term level. 
    A negative $\\beta_1$ typically signifies a normal upward-sloping curve.
    """)

with col_b:
    st.markdown(f"""
    **$\\beta_2$ - The Curvature (Medium-Term Hump):** Captures the specific 'bulge' in the 2-to-5-year sector. 
    This is critical for valuing mid-term insurance liabilities.

    **$\\tau$ - The Scale Factor:** Specifies the maturity at which the loading on the curvature is maximized.
    """)

# --- RISK MANAGEMENT INSIGHTS ---
st.markdown("---")
st.markdown("### 3. Risk Management Perspectives")

st.write("""
From a Chief Risk Officer (CRO) perspective, monitoring these parameters allows for:
1. **Scenario Analysis:** Assessing the impact of "Twists" (Slope changes) and "Butterflies" (Curvature changes) on the Net Internal Value.
2. **Stress Testing:** Quantifying the sensitivity of the Solvency II balance sheet to non-parallel shifts.
3. **ALM Steering:** Fine-tuning the duration gap between assets and liabilities.
""")



# Risk Analysis - Head of Risk Vision
st.markdown("---")
st.write("### 🧠 Strategic Analysis")
if b1 < 0:
    st.success("The curve is **normal** (positive slope). Economic expectations are stable.")
else:
    st.error("The curve is **inverted**. Warning: risk of recession or short-term liquidity stress.")