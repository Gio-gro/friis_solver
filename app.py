import streamlit as st
import sympy
from sympy import symbols, Eq, solve, pi

num_format = "%.2f"

p_r , p_t, fsl, g_t, g_r , f_r, f_t, wvlen, freq, a_e, eirp, s_r, radius = symbols('p_r p_t fsl g_t g_r f_r f_t wvlen freq a_e eirp s_r radius')

friis_eq = Eq(p_r, p_t*(1/fsl)*g_t*g_r*f_t*f_r)
fsl_eq = Eq(fsl, (4*pi*radius)/wvlen)
freq_eq = Eq(freq, 3e8 / wvlen)
a_e_eq = Eq(a_e, (g_r*(wvlen**2))/(4*pi))
eirp_eq = Eq(eirp, p_t*g_t)
s_r_eq = Eq(s_r, (p_t*g_t)/(4*pi*(radius**2))*f_t)
p_r_eq = Eq(p_r, s_r*a_e*f_r)

st.title("Friis equation solver")

st.subheader("System")

col_sys1, col_sys2 = st.columns(2)
with col_sys1:
    st.number_input("Frequency (Hz)", key='freq', format=num_format)
with col_sys2:
    st.number_input("Wavelength (m)", key='wvlen', format=num_format)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Transmitter")
    st.number_input("Tx Power, $P_t$ (W)", key='p_t', format=num_format)
    st.number_input("Tx Gain, $G_t$ (ratio)", key='g_t', format=num_format)
    st.number_input("Tx Loss Factor, $f_t$ (ratio)", key='f_t', format=num_format)
    st.number_input("EIRP (W)", key='eirp', format=num_format)

with col2:
    st.subheader("Path")
    st.number_input("Distance, $r$ (m)", key='radius', format=num_format)
    st.number_input("Path Loss, $FSL$ (ratio)", key='fsl', format=num_format)
    st.number_input("Power Density, $S_r$ (W/m²)", key='s_r', format=num_format)

with col3:
    st.subheader("Receiver")
    st.number_input("Rx Power, $P_r$ (W)", key='p_r', format=num_format)
    st.number_input("Rx Gain, $G_r$ (ratio)", key='g_r', format=num_format)
    st.number_input("Rx Loss Factor, $f_r$ (ratio)", key='f_r', format=num_format)
    st.number_input("Effective Aperture, $A_e$ (m²)", key='a_e', format=num_format)

st.divider()

st.header("Results")
