import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch

st.header("Mapa de remates de la Copa América 2024")
st.subheader("Filtrá por selección y luego por jugador para ver sus acciones.")
st.write("##### Datos de eventing promovidos por StatsBomb de manera gratuita.")


df = pd.read_csv("eventos_copa_america_2024.csv")
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

team = st.selectbox('Equipo:', df['team'].sort_values().unique(), index=None)
player = st.selectbox(
    'Jugador:', df[df['team'] == team]['player'].sort_values().unique(), index=None)


def filtro(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df


datos_filtrados = filtro(df, team, player)

pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))


def mapa(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['shot_outcome'] == 'Goal' else 0.5,
            zorder=2 if x['shot_outcome'] == 'Goal' else 1,
        )


mapa(datos_filtrados, ax, pitch)

st.pyplot(fig)

st.write("El tamaño de los círculos está determinado por el xG de cada remate \n En verde, los disparos que terminaron en gol. En los mapas están incluidos los penales. Basado en los cursos/videos de McKay Johns.")
st.write("X: @robaboian_")
