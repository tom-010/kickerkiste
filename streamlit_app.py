import streamlit as st
import itertools
import pandas as pd
import random

# Titel der App
st.title("⚽ Tischfußball Turnierplaner")

# Eingabe der Spielernamen
st.sidebar.header("Spieler hinzufügen")
default_players = "Tom, Martin, Augsburer, Jolle, Vivian, Raphi"
players_input = st.sidebar.text_area("Spielernamen (mit Komma trennen)", value=default_players)
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
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Als CSV herunterladen",
        data=csv,
        file_name="tischfussball_spielplan.csv",
        mime="text/csv",
    )
