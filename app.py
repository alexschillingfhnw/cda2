import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit.components.v1 import html
from ipyvizzu import Chart, Data, Config, Style, DisplayTarget

# set page config
#st.set_page_config(layout='wide')

st.write("# Policy Advices zur Erzeugung von Energie ohne Treibhausgasausstoss")
st.write("## Willkommen!")

with st.expander("Einleitung"):
    st.write("""
        Dieses Dashboard verfügt über Analysen der erneuerbarer Energien in Deutschland, Grossbritannien, der Schweiz und Spanien. In einer Zeit, in der die Bedeutung erneuerbarer Energien immer grösser wird, ist es wichtig, Daten zu sammeln und zu analysieren, um fundierte Entscheidungen zu treffen. Unser Dashboard bietet Daten und Diagramme, die gefiltert werden können, um spezifische Trends und Muster zu erkunden. Wir haben auch eine Datastory erstellt, um wichtige Ereignisse in der Entwicklung der erneuerbaren Energien zu zeigen und die Daten zum Leben zu erwecken. Schliesslich bieten wir Policy-Advices basierend auf unseren Erkenntnissen an, um zukünftige Trends im Bereich erneuerbarer Energien zu prognostizieren.
    """)

with st.expander("Anleitung"):
    st.markdown("""
Dieser Leitfaden zeigt Ihnen, wie Sie unser interaktives Dashboard am besten nutzen können. Hier sind einige wichtige Tipps:

1. Filtern: Nutzen Sie die Filter, um Ihre Daten nach bestimmten Kriterien zu sortieren. Zum Beispiel können Sie nach einem bestimmten Land filtern, um nur Daten aus diesem Land anzuzeigen.
2. Zeitraum anpassen: Verwenden Sie den Schieberegler unter den Filtern, um den Zeitraum auszuwählen, für den Sie Daten anzeigen möchten. Sie können den Start- und Endpunkt der Datenauswahl anpassen.
3. Plots analysieren: Jeder Plot auf dem Dashboard bietet spezifische Informationen. Bewegen Sie den Cursor über bestimmte Punkte oder Bereiche im Plot, um detaillierte Informationen anzuzeigen. Diese Funktion ist besonders nützlich, um tiefer in die Daten einzutauchen und Trends zu erkennen.
""")


st.header('Datastory')

with st.expander("1. CO₂ Emissionen"):
    st.write("#### Wie viel CO₂ wird pro Kopf ausgestossen?")
    st.write("""
        Hier wird der jährliche CO₂ Ausstoss pro Einwohner in Tonnen angezeigt. Diese Metrik liefert einen direkten Einblick in die durchschnittliche 'Carbon Footprint' eines Einwohners in jedem der betrachteten Länder. Wir sehen, dass Deutschland am meisten CO₂ pro Kopf ausstösst, während die Schweiz am wenigsten ausstösst.
    """)

    # import co2 emissions per capita data
    df_em_cap = pd.read_csv("Data/emissions_per_capita.csv")

    # create co2 emissions per capita plot
    fig_em_cap = px.line(
        df_em_cap, 
        x = "Jahr", 
        y = "CO2 emissions per capita (t)", 
        color = "Land", 
        title = "Entwicklung der CO₂ Emissionen pro Kopf"
    )

    # show plot
    st.plotly_chart(fig_em_cap)

    st.write("Datenquelle: [Our World in Data - CO₂ Emissions](https://ourworldindata.org/co2-emissions)")

    st.write("#### Wie viel CO₂ wird pro Landesfläche ausgestossen?")
    st.write("""
        Dieses Diagramm zeigt die CO₂ Emissionen in Tonnen pro Quadratkilometer für jedes Land. Dies gibt uns eine Vorstellung davon, wie dicht die CO₂ Emissionen in den verschiedenen Ländern sind, unabhängig von der Bevölkerungsdichte. Hier sieht man, dass Deutschland pro Quadratkilometer immer noch am meisten CO₂ ausstösst, aber Grossbritannien ist nahe dahinter. Spanien hat die niedrigsten CO₂ Emissionen pro Quadratkilometer.
    """)
    
    df_country_size = pd.DataFrame({
        "Land": ["Deutschland", "Spanien", "Schweiz", "UK"],
        "Fläche in km2": [357386, 505990, 41285, 242495],
    })

    st.table(df_country_size)

    # import co2 emissions per land area data
    df_em_land = pd.read_csv("Data/emissions_per_land_area.csv")

    # create co2 emissions per land area plot
    fig_em_land = px.line(
        df_em_land, 
        x = "Jahr", 
        y = "CO2 Emissionen pro Landfläche (t/km2)", 
        color = "Land", 
        title = "Entwicklung der CO₂ Emissionen pro Landesfläche"
    )

    # show plot
    st.plotly_chart(fig_em_land)


# --------- TEST -----------

def create_chart():
    # initialize Chart
 
    chart = Chart(
        width="640px", height="360px", display=DisplayTarget.MANUAL
    )
 
    # create and add data to Chart
 
    data = Data()
    data_frame = pd.read_csv("Data/titanic.csv")

    data.add_data_frame(data_frame)
 
    chart.animate(data)
 
    # add config to Chart
 
    chart.animate(
        Config(
            {
                "x": "Count",
                "y": "Sex",
                "label": "Count",
                "title": "Passengers of the Titanic",
            }
        )
    )
    chart.animate(
        Config(
            {
                "x": ["Count", "Survived"],
                "label": ["Count", "Survived"],
                "color": "Survived",
            }
        )
    )
    chart.animate(Config({"x": "Count", "y": ["Sex", "Survived"]}))
 
    # add style to Chart
 
    chart.animate(Style({"title": {"fontSize": 35}}))
 
    # return generated html code
 
    return chart._repr_html_()
 
 
# generate Chart's html code
 
CHART = create_chart()
 
 
# display Chart
 
html(CHART, width=650, height=370)