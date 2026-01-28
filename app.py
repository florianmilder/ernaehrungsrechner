import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.image("https://images.squarespace-cdn.com/content/v1/5fabec7705d8847b1502daaa/1617027374785-A9DX36UNU16N635Q7RZH/hipp_das_beste_2x3.jpg")

st.markdown("""
<style>

/* Gesamter Hintergrund */
.stApp {
    background-color: #89CFF0;
}

/* Hauptcontainer */
.block-container {
    padding: 2.5rem 3rem;
    border-radius: 20px;
    background-color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #E6007E,
        #009FE3,
        #F39200,
        #6A2383
    );
    color: white;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Überschriften */
h1, h2, h3 {
    font-family: "Comic Sans MS", "Trebuchet MS", sans-serif;
}

/* Buttons */
button {
    border-radius: 25px !important;
    background-color: #E6007E !important;
    color: white !important;
    font-weight: bold;
}

/* Slider */
div[data-baseweb="slider"] > div {
    color: #E6007E;
}

</style>
""", unsafe_allow_html=True)


# ======================
# TITEL
# ======================
st.title("Enterale Ernährung – Bedarfsrechner")

# ======================
# PATIENT
# ======================
st.header("Patientendaten")

gewicht = st.number_input(
    "Gewicht (kg)",
    min_value=30,
    max_value=200,
    value=70
)

alter = st.number_input(
    "Alter (Jahre)",
    min_value=18,
    max_value=100,
    value=30
)

if alter < 18:
    st.warning("⚠️ Dieser Rechner ist nur für Erwachsene (>18 Jahre) geeignet.") 
    st.stopp()

# Geschlecht auswählen
geschlecht = st.selectbox(
    "Geschlecht",
    options=["Mann", "Frau"]
)

# PAL jetzt bis 2,4
pal = st.slider(
    "Aktivitätslevel (PAL)",
    min_value=1.0,
    max_value=2.4,
    value=1.3,
    step=0.1
)

protein_pro_kg = st.slider(
    "Proteinbedarf (g/kg KG)",
    min_value=0.6,
    max_value=2.0,
    value=1.2,
    step=0.1
)

# ======================
# PRODUKT
# ======================
st.header("Produktdaten (frei wählbar)")

kcal_pro_ml = st.number_input(
    "Energiegehalt (kcal/ml)",
    min_value=0.5,
    max_value=3.0,
    value=1.5,
    step=0.1
)

protein_pro_100ml = st.number_input(
    "Proteingehalt (g/100 ml)",
    min_value=0.0,
    max_value=20.0,
    value=6.3,
    step=0.1
)

wasser_pro_100ml = st.number_input(
    "Wassergehalt der Sondennahrung (g/100 ml)",
    min_value=50.0,
    max_value=100.0,
    value=80.0,
    step=0.1
)


protein_pro_ml = protein_pro_100ml / 100 
wasser_pro_ml = wasser_pro_100ml / 100  # intern für Berechnung

# ======================
# BERECHNUNG
# ======================
# Grundumsatz nach Geschlecht
if geschlecht == "Frau":
    grundumsatz = (0.047 * gewicht - 0.01452 * alter + 3.21) * 239
else: # Mann
    grundumsatz = (0.047 * gewicht + 1.009 - 0.01452 * alter + 3.21) * 239

energiebedarf = grundumsatz * pal
proteinbedarf = protein_pro_kg * gewicht

ml_pro_tag = energiebedarf / kcal_pro_ml
protein_zugeführt = ml_pro_tag * protein_pro_ml

# ======================
# WASSERBEDARF
# ======================
wasserbedarf = 35 * gewicht  # g pro Tag

wasser_aus_sonde = ml_pro_tag * wasser_pro_ml
wasser_ergaenzend = wasserbedarf - wasser_aus_sonde
if wasser_ergaenzend < 0: 
    wasser_ergaenzend = 0  # kein negatives Wasser

# ======================
# ERGEBNISSE
# ======================
st.header("Ergebnisse")

st.write(f"🟠 **Energiebedarf:** {energiebedarf:.0f} kcal/Tag")
st.write(f"🟠 **Proteinbedarf:** {proteinbedarf:.1f} g/Tag")
st.write(f"🟠**Gesamtwasserbedarf:** {wasserbedarf: .0f} g/Tag")
st.write("")
st.write(f"🟠 **Benötigte Sondenmenge:** {ml_pro_tag:.0f} ml/Tag")
st.write(f"🟠 **Proteinzufuhr:** {protein_zugeführt:.1f} g/Tag")
st.write(f"🟠 **Wasser aus Sondennahrung:** {wasser_aus_sonde: .0f} g/Tag")
st.write(f"🟠 **Zu ergänzendes Wasser:** {wasser_ergaenzend: .0f} g/Tag")

# Bewertung Protein
if protein_zugeführt >= proteinbedarf:
    st.success("Proteinbedarf wird gedeckt ✅")
else:
    st.warning("Proteinbedarf wird NICHT gedeckt ⚠️")

# ======================
# ZUFUHRMENGE (für 16, 20, 24 h)
# ======================
stunden_laufzeit = [16, 20, 24]
ml_h_list = [ml_pro_tag / h for h in stunden_laufzeit]

# ======================
# DIAGRAMM: 3 Balken mit Zahlen
# ======================
fig, ax = plt.subplots()
bars = ax.bar([str(h) + " h" for h in stunden_laufzeit], ml_h_list, color=['skyblue','orange','purple'])

# Zahlen über den Balken anzeigen
for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2, # x-Mittelpunkt
        yval + 2, # leicht oberhalb des Balkens
        f'{yval:.1f}', # Zahl formatieren
        ha='center',
        va='bottom',
        fontsize=10
    )

ax.set_xlabel("Laufzeit")
ax.set_ylabel("ml pro Stunde")
ax.set_title("Zufuhrgeschwindigkeit")
ax.grid(axis='y')

st.pyplot(fig)

st.video("https://youtu.be/3i0_-A7iuBk")
st.write()
st.markdown("Entdecke die Vielfalt der enteralen Ernährung unter: [HiPP-Sondennahrung](https://www.hipp.de/hipp-sondennahrung/)")


