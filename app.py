import streamlit as st
import sympy
from sympy import symbols, Eq, solve, pi

#CONSTANTS
num_format = "%.2f"
eq_keyset = [
    'p_r', 'p_t', 'fsl', 'g_t', 'g_r', 'f_r', 'f_t',
     'wvlen', 'freq', 'a_e', 'eirp', 's_r', 'radius'
]
p_r, p_t, fsl, g_t, g_r , f_r, f_t, wvlen, freq, a_e, eirp, s_r, radius = symbols(' '.join(eq_keyset))

eq_set = {
    'friis_eq' : Eq(p_r, p_t*(1/fsl)*g_t*g_r*f_t*f_r),
    'fsl_eq' : Eq(fsl, (4*pi*radius)/wvlen),
    'freq_eq' : Eq(freq, 3e8 / wvlen),
    'a_e_eq' : Eq(a_e, (g_r*(wvlen**2))/(4*pi)),
    'eirp_eq' : Eq(eirp, p_t*g_t),
    's_r_eq' : Eq(s_r, (p_t*g_t)/(4*pi*(radius**2))*f_t),
    'p_r_eq' : Eq(p_r, s_r*a_e*f_r)
}

#FUNCTION DEFINITIONS
def reset_state() : 
    for symbol in eq_keyset :
        st.session_state[symbol] = None 
    for eq in eq_set :
        st.session_state[eq] = eq_set[eq]

def is_disabled(widget_key) : 
    return st.session_state[widget_key] != None

#INITIALIZATION
if("p_r" not in st.session_state) : 
    reset_state() 

#PAGE UI
st.title("Friis equation solver")

st.button(label="RESET", key="reset_button", on_click=reset_state )

st.subheader("System")

col_sys1, col_sys2 = st.columns(2)
with col_sys1:
    st.number_input("Frequency (Hz)", key='freq', format=num_format, disabled=is_disabled('freq'))
with col_sys2:
    st.number_input("Wavelength (m)", key='wvlen', format=num_format, disabled=is_disabled('wvlen'))

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Transmitter")
    st.number_input("Tx Power, $P_t$ (W)", key='p_t', format=num_format, disabled=is_disabled('p_t'))
    st.number_input("Tx Gain, $G_t$ (ratio)", key='g_t', format=num_format, disabled=is_disabled('g_t'))
    st.number_input("Tx Loss Factor, $f_t$ (ratio)", key='f_t', format=num_format, disabled=is_disabled('f_t'))
    st.number_input("EIRP (W)", key='eirp', format=num_format, disabled=is_disabled('eirp'))

with col2:
    st.subheader("Path")
    st.number_input("Distance, $r$ (m)", key='radius', format=num_format, disabled=is_disabled('radius'))
    st.number_input("Path Loss, $FSL$ (ratio)", key='fsl', format=num_format, disabled=is_disabled('fsl'))
    st.number_input("Power Density, $S_r$ (W/m²)", key='s_r', format=num_format, disabled=is_disabled('s_r'))

with col3:
    st.subheader("Receiver")
    st.number_input("Rx Power, $P_r$ (W)", key='p_r', format=num_format, disabled=is_disabled('p_r'))
    st.number_input("Rx Gain, $G_r$ (ratio)", key='g_r', format=num_format, disabled=is_disabled('g_r'))
    st.number_input("Rx Loss Factor, $f_r$ (ratio)", key='f_r', format=num_format, disabled=is_disabled('f_r'))
    st.number_input("Effective Aperture, $A_e$ (m²)", key='a_e', format=num_format, disabled=is_disabled('a_e'))

st.divider()

st.header("Steps :")
