import streamlit as st
import sympy
from sympy import symbols, Eq, solve, pi

# CONSTANTS
num_format = "%.2e"
eq_keyset = [
    "p_r",
    "p_t",
    "fsl",
    "g_t",
    "g_r",
    "f_r",
    "f_t",
    "wvlen",
    "freq",
    "a_e",
    "eirp",
    "s_r",
    "radius",
]
p_r, p_t, fsl, g_t, g_r, f_r, f_t, wvlen, freq, a_e, eirp, s_r, radius = symbols(
    " ".join(eq_keyset)
)

eq_set = {
    "friis_eq": Eq(p_r, p_t * (1 / fsl) * g_t * g_r * f_t * f_r),
    "fsl_eq": Eq(fsl, (4 * pi * radius) / wvlen),
    "freq_eq": Eq(freq, 3e8 / wvlen),
    "a_e_eq": Eq(a_e, (g_r * (wvlen**2)) / (4 * pi)),
    "eirp_eq": Eq(eirp, p_t * g_t),
    "s_r_eq": Eq(s_r, (p_t * g_t) / (4 * pi * (radius**2)) * f_t),
    "p_r_eq": Eq(p_r, s_r * a_e * f_r),
}


# FUNCTION DEFINITIONS
def reset_state():
    for symbol in eq_keyset:
        st.session_state[symbol] = None
    for eq in eq_set:
        st.session_state[eq] = eq_set[eq]
    st.session_state['steps'] = []


def is_disabled(widget_key):
    return st.session_state[widget_key] != None


def react(symbol):
    value = st.session_state[symbol.name]
    if value is None:
        return
    for eq_key in eq_set:
        free_syms = st.session_state[eq_key].free_symbols
        if symbol in free_syms:
            st.session_state[eq_key] = st.session_state[eq_key].subs(symbol, value)
            free_syms = st.session_state[eq_key].free_symbols
            if len(free_syms) == 1:
                solvend = next(iter(free_syms))
                solution = solve(st.session_state[eq_key], solvend)[0]
                st.session_state[solvend.name] = solution
                st.session_state['steps'].append(f"* Solved for **{solvend.name}** = `{solution:.2e}` (using `{eq_set[eq_key]}`)")
                react(solvend)


# INITIALIZATION
if "p_r" not in st.session_state:
    reset_state()

# PAGE UI
st.title("Friis equation solver")

st.button(label="RESET", key="reset_button", on_click=reset_state)

st.subheader("System")

col_sys1, col_sys2 = st.columns(2)
with col_sys1:
    st.number_input(
        "Frequency (Hz)",
        key="freq",
        format=num_format,
        disabled=is_disabled("freq"),
        on_change=react,
        kwargs={"symbol": freq},
    )
with col_sys2:
    st.number_input(
        "Wavelength (m)",
        key="wvlen",
        format=num_format,
        disabled=is_disabled("wvlen"),
        on_change=react,
        kwargs={"symbol": wvlen},
    )

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Transmitter")
    st.number_input(
        "Tx Power, $P_t$ (W)",
        key="p_t",
        format=num_format,
        disabled=is_disabled("p_t"),
        on_change=react,
        kwargs={"symbol": p_t},
    )
    st.number_input(
        "Tx Gain, $G_t$ (ratio)",
        key="g_t",
        format=num_format,
        disabled=is_disabled("g_t"),
        on_change=react,
        kwargs={"symbol": g_t},
    )
    st.number_input(
        "Normalized $f_t$",
        key="f_t",
        format=num_format,
        disabled=is_disabled("f_t"),
        on_change=react,
        kwargs={"symbol": f_t},
    )
    st.number_input(
        "EIRP (W)",
        key="eirp",
        format=num_format,
        disabled=is_disabled("eirp"),
        on_change=react,
        kwargs={"symbol": eirp},
    )

with col2:
    st.subheader("Path")
    st.number_input(
        "Distance, $r$ (m)",
        key="radius",
        format=num_format,
        disabled=is_disabled("radius"),
        on_change=react,
        kwargs={"symbol": radius},
    )
    st.number_input(
        "Free Space Loss, $FSL$",
        key="fsl",
        format=num_format,
        disabled=is_disabled("fsl"),
        on_change=react,
        kwargs={"symbol": fsl},
    )
    st.number_input(
        "Power Density, $S_r$ (W/m²)",
        key="s_r",
        format=num_format,
        disabled=is_disabled("s_r"),
        on_change=react,
        kwargs={"symbol": s_r},
    )

with col3:
    st.subheader("Receiver")
    st.number_input(
        "Rx Power, $P_r$ (W)",
        key="p_r",
        format=num_format,
        disabled=is_disabled("p_r"),
        on_change=react,
        kwargs={"symbol": p_r},
    )
    st.number_input(
        "Rx Gain, $G_r$",
        key="g_r",
        format=num_format,
        disabled=is_disabled("g_r"),
        on_change=react,
        kwargs={"symbol": g_r},
    )
    st.number_input(
        "Normalized $f_r$",
        key="f_r",
        format=num_format,
        disabled=is_disabled("f_r"),
        on_change=react,
        kwargs={"symbol": f_r},
    )
    st.number_input(
        "Effective Aperture, $A_e$ (m²)",
        key="a_e",
        format=num_format,
        disabled=is_disabled("a_e"),
        on_change=react,
        kwargs={"symbol": a_e},
    )

st.divider()

st.header("Steps :")

for step in st.session_state['steps'] :
    st.write(step)

st.header("STATE")

st.write(st.session_state)