import streamlit as st
import sympy
from sympy import symbols, Eq, solve, pi

p_r , p_t, fsl, g_t, g_r , f_r, f_t, wvlen, freq, a_e, eirp, s_r, radius = symbols('p_r p_t fsl g_t g_r f_r f_t wvlen freq a_e eirp s_r radius')

friis_eq = Eq(p_r, p_t*(1/fsl)*g_t*g_r*f_t*f_r)
fsl_eq = Eq(fsl, (4*pi*radius)/wvlen)
freq_eq = Eq(freq, 3e8 / wvlen)
a_e_eq = Eq(a_e, (g_r*(wvlen**2))/(4*pi))
eirp_eq = Eq(eirp, p_t*g_t)
s_r_eq = Eq(s_r, (p_t*g_t)/(4*pi*(radius**2))*f_t)
p_r_eq = Eq(p_r, s_r*a_e*f_r)

st.title("Friis equation solver")

st.header("Inputs")

st.subheader("System")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Transmitter")

with col2:
    st.subheader("Path")

with col3:
    st.subheader("Receiver")

st.divider()

st.header("Results")
