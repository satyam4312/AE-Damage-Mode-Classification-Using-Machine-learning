import requests
import streamlit as st
import pandas as pd

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Damage Mode Prediction",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Composite Damage Mode Prediction")

st.write("Predict the damage mode of composite materials using Acoustic Emission (AE) features.")

st.divider()

# ==========================================
# Input Features
# ==========================================

col1, col2 = st.columns(2)

with col1:

    amp = st.number_input(
        "Amplitude (Amp)",
        value=75.4
    )

    rise = st.number_input(
        "Rise Time (RiseT)",
        value=51.0
    )

    duration = st.number_input(
        "Duration (Dur)",
        value=185.2
    )

    energy = st.number_input(
        "Energy (Eny)",
        value=1245.8
    )

with col2:

    counts = st.number_input(
        "Counts",
        value=42
    )

    rms = st.number_input(
        "RMS",
        value=2.3
    )

    ss = st.number_input(
        "Signal Strength (SS)",
        value=480.0
    )

st.divider()

# ==========================================
# Prediction
# ==========================================

if st.button("Predict Damage Mode", use_container_width=True):

    payload = {
        "features": {
            "Amp": amp,
            "RiseT": rise,
            "Dur": duration,
            "Eny": energy,
            "Counts": counts,
            "RMS": rms,
            "SS": ss
        }
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction Successful")

            st.subheader("Predicted Damage Mode")

            st.metric("Damage Mode", result["damage_mode"])

            st.metric("Confidence", f"{result['confidence']*100:.2f}%")

            st.subheader("Class Probabilities")

            probs = pd.DataFrame(
                result["probabilities"].items(),
                columns=["Damage Mode", "Probability"]
            )

            probs["Probability (%)"] = probs["Probability"] * 100

            st.dataframe(probs, use_container_width=True)

            st.bar_chart(probs.set_index("Damage Mode")["Probability (%)"])

        else:
            st.error(response.json())

    except Exception as e:
        st.error(str(e))