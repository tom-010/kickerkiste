import streamlit as st
import itertools
import pandas as pd
import random
import io


# Titel der App
st.title("⚽ Kicker Kiste Turnierplaner")

# Default-Spieler
DEFAULT_PLAYERS = "Tom, Martin, Augsburer, Jolle, Vivian, Raphi"

# Session State initialisieren
if 'players_input' not in st.session_state:
    st.session_state['players_input'] = DEFAULT_PLAYERS

# Sidebar-Eingabe
st.sidebar.header("Spieler hinzufügen")
players_input = st.sidebar.text_area(
    "Spielernamen (mit Komma trennen)",
    value=st.session_state['players_input']
)

# Spieler speichern
st.session_state['players_input'] = players_input
players = [name.strip() for name in players_input.split(",") if name.strip()]

# Anzahl der Spieler validieren
if len(players) < 4:
    st.warning("Bitte mindestens 4 Spielernamen eingeben, um Teams zu bilden.")
else:
    # Alle möglichen Teams erzeugen (Kombinationen von 2)
    teams = list(itertools.combinations(players, 2))

    # Alle Matches erzeugen und Überschneidungen vermeiden
    matches = list(itertools.combinations(teams, 2))
    valid_matches = [m for m in matches if len(set(m[0]) & set(m[1])) == 0]

    # Matches zufällig mischen für Diversität
    random.shuffle(valid_matches)

    # Daten für die Anzeige vorbereiten
    match_data = []
    for idx, match in enumerate(valid_matches, 1):
        team1, team2 = match
        match_data.append({"Spiel": idx, "Team 1": " & ".join(team1), "Team 2": " & ".join(team2), "Ergebnis Team 1": ""})

    df = pd.DataFrame(match_data)

    # Matchplan mit editierbaren Ergebnissen anzeigen
    st.header("📅 Spielplan")
    edited_df = st.data_editor(df, num_rows="dynamic")

    # Export-Button für CSV
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer := io.BytesIO(), engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Spielplan")
    st.download_button(
        label="📥 Als Excel herunterladen",
        data=buffer.getvalue(),
        file_name="kickerkiste_spielplan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )