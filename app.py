import pandas as pd
from PIL import Image
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

# -------------- 1. CO2 Emissionen ---------------

st.write("### 1. CO₂ Emissionen")

with st.expander("# CO₂ Emissionen"):
    st.write("#### 1.1 Wie viel CO₂ wird pro Kopf ausgestossen?")
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

    st.divider()

    st.write("#### 1.2 Wie viel CO₂ wird pro Landesfläche ausgestossen?")
    st.write("Dieses Diagramm zeigt die CO₂ Emissionen in Tonnen pro Quadratkilometer für jedes Land. Dies gibt uns eine Vorstellung davon, wie dicht die CO₂ Emissionen in den verschiedenen Ländern sind, unabhängig von der Bevölkerungsdichte. Hier sieht man, dass Deutschland pro Quadratkilometer immer noch am meisten CO₂ ausstösst, aber Grossbritannien ist nahe dahinter. Spanien hat die niedrigsten CO₂ Emissionen pro Quadratkilometer.")
    
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

    st.plotly_chart(fig_em_land)

    st.write("Datenquelle: [Our World in Data - CO₂ Emissions](https://ourworldindata.org/co2-emissions)")

    st.divider()

    st.write("#### 1.3 Kann über den gesamten Betrachtungszeitraum hinweg ein ermutigender Trend festgestellt werden?")
    st.write("Die CO₂ Emissionen haben in allen vier Ländern abgenommen. Dies weist auf erfolgreiche Bemühungen hin, den Kohlenstoffausstoss zu verringern und den Übergang zu einer nachhaltigeren und umweltfreundlicheren Wirtschaftsweise zu gestalten. Diese Diagramme bieten einen umfassenden und vergleichenden Überblick über den CO₂ Ausstoss in diesen Ländern. Sie dienen als wichtiger Indikator für die Fortschritte, die diese Länder bei der Reduzierung ihrer CO₂ Emissionen gemacht haben und bieten wertvolle Einblicke für zukünftige Klimaschutzstrategien.")


# -------------- 2. VERGLEICH ENERGIEVERBRAUCH ---------------

st.write("### 2. Vergleich Energieverbrauch")

with st.expander("# Vergleich Energieverbrauch"):
    st.write("#### 2.1 Wie viel Energie verbrauchen die Länder?")
    st.write("Dieses interaktive Diagramm zeigt den Energieverbrauch der vier Länder. Er ist die Summe des gesamten Energieverbrauchs, einschliesslich Strom, Verkehr und Heizung. Wir sehen, dass Deutschland den höchsten Energieverbrauch hat, während die Schweiz den niedrigsten Energieverbrauch hat.")

    # import energy consumption data
    df_en_cons = pd.read_csv("Data/energy_consumption.csv")

    # create energy consumption per country plot
    fig_en_cons = px.line(
        df_en_cons, 
        x = "Jahr", 
        y = "Energieverbrauch (TWh)", 
        color = "Land", 
        title = "Entwicklung des Energieverbrauchs (TWh)"
    )

    st.plotly_chart(fig_en_cons)

    st.write("Datenquelle: [Our World in Data - Energy Consumption](https://ourworldindata.org/energy-production-consumption)")

    st.divider()

    st.write("#### 2.2 Wie stehen die vier Länder im Vergleich, wenn wir den Energieverbrauch pro Person betrachten?")
    st.write("Wenn wir jedoch den Energieverbrauch pro Kopf anzeigen, sehen wir grosse Unterschiede der Diagramme, vor allem in der Schweiz. Die Population ist zwar klein in der Schweiz, aber sie verbrauchen mehr Energie pro Kopf wie Spanien und Grossbritannien. In einigen Jahren verbrauchte die Schweiz sogar mehr Energie pro Kopf als Deutschland.")

    # create energy consumption per capita per country plot
    fig_en_cons_cap = px.line(
        df_en_cons, 
        x = "Jahr", 
        y = "Energieverbrauch pro Kopf (kWh/Kopf)", 
        color = "Land", 
        title = "Entwicklung des Energieverbrauchs pro Kopf (TWh)"
    )

    st.plotly_chart(fig_en_cons_cap)

    st.write("Datenquelle: [Our World in Data - Energy Consumption](https://ourworldindata.org/energy-production-consumption)")

    st.divider()

    st.write("#### 2.3 Kann über den gesamten Betrachtungszeitraum hinweg ein ermutigender Trend festgestellt werden?")
    st.write("Die CO₂ Emissionen haben seit dem Jahr 2004 in allen vier Ländern abgenommen. Dies liegt an der Entwicklung von erneuerbaren Energien und der Verbesserung der Energieeffizienz.")


# -------------- 3. VERGLEICH ENERGIEPRODUKTION ---------------

st.write("### 3. Vergleich grüne Energieproduktion")

with st.expander("# Vergleich grüne Energieproduktion"):
    st.write("#### 3.1 Wie viel Energie produzieren die Länder aus erneuerbaren Quellen?")
    st.write("In diesem interaktiven Linienplot sieht man die Entwicklungen in der Produktion von erneuerbaren Energien in Deutschland, Grossbritannien, der Schweiz und Spanien nachverfolgen. Es stehen Daten zu den drei wichtigsten Arten von erneuerbaren Energien zur Verfügung: Solarenergie, Wasserkraft und Windenergie.")

    # import renewable energy production data
    df_ren_en_prod = pd.read_csv("Data/renewable_energy_production.csv")

    energy_selector = st.selectbox(
        "###### Selektieren Sie eine Energiequelle",
        ('Wind', 'Wasser', 'Solar', 'Biomasse'))

    if energy_selector == 'Wind':
        
        # show wind plot
        fig_ren_en_prod_wind = px.line(
            df_ren_en_prod, 
            x = "Jahr", 
            y = "Produktion Windenergie (TWh)", 
            color = "Land", 
            title = "Entwicklung der Produktion von Windenergie (TWh)"
        )

        st.plotly_chart(fig_ren_en_prod_wind)


    elif energy_selector == 'Wasser':

        # show water plot
        fig_ren_en_prod_water = px.line(
            df_ren_en_prod, 
            x = "Jahr", 
            y = "Produktion Wasserkraft (TWh)", 
            color = "Land", 
            title = "Entwicklung der Produktion von Wasserkraft (TWh)"
        )

        st.plotly_chart(fig_ren_en_prod_water)

    elif energy_selector == 'Solar':
        # show solar plot
        fig_ren_en_prod_solar = px.line(
            df_ren_en_prod, 
            x = "Jahr", 
            y = "Produktion Solarenergie (TWh)", 
            color = "Land", 
            title = "Entwicklung der Produktion von Solarenergie (TWh)"
        )

        st.plotly_chart(fig_ren_en_prod_solar)
    
    elif energy_selector == 'Biomasse':

        # show biomass plot
        fig_ren_en_prod_biomass = px.line(
            df_ren_en_prod, 
            x = "Jahr", 
            y = "Produktion Biomasse (TWh)", 
            color = "Land", 
            title = "Entwicklung der Produktion von Biomasse (TWh)"
        )

        st.plotly_chart(fig_ren_en_prod_biomass)

    st.write("Datenquelle: [Our World in Data - Renewable Energy](https://ourworldindata.org/renewable-energy)")
    st.divider()
    st.write("Im folgenden Kapitel *4. Ereignisse in der Energieproduktion* beziehen sich die Erkenntnisse auf der interaktiven Visualisierung beim Kapitel *3. Vergleich grüne Energieproduktion*.")


# -------------- 4. EREIGNISSE IN DER ENERGIEPRODUKTION ---------------

st.write("### 4. Ereignisse in der Energieproduktion")

with st.expander("## Ereignisse in der Energieproduktion"):

    col1, col2 = st.columns(2)

    with col1:
        country_selector = st.selectbox(
        "###### Selektieren Sie ein Land ...",
        ('Deutschland', 'Grossbritannien', 'Schweiz', 'Spanien'))

    with col2:
        energy_selector_2 = st.selectbox(
            "###### und eine Energiequelle",
            ('Wind', 'Wasser', 'Solar', 'Biomasse'),
            key = 'unique_key_2')

    st.divider()

    if country_selector == "Deutschland":

        if energy_selector_2 == "Solar":

            st.write("#### 1. Warum stieg die Produktion so stark ab 2009?")
            st.write("""
            - Einführung des Erneuerbare-Energien-Gesetzes (EEG) im Jahr 2000 und Novellierung im Jahr 2004
            - EEG förderte Investitionen in erneuerbare Energien
            - EEG stellte eine Einspeisevergütung für Strom aus erneuerbaren Quellen
            - Einspeisevergütung war höher als der Marktpreis für Strom
            - Betrieb von Solaranlagen wurde dadurch wirtschaftlich rentabel
            """)

            st.write("#### 2. Was sind die Gründe dafür, dass Deutschland im Vergleich zu anderen Ländern eine deutlich höhere Solarenergieproduktion aufweist?")
            st.write("""
            - Attraktive Einspeisevergütungen für Solarstrom seit 2000 → Ansturm auf die Installation von Solarpanels
            - Technologischer Fortschritt im Bereich der Solartechnologie → Kostensenkung & höhere Effizienz
            - Hoher Akzeptanz und Nachfrage nach Solarenergie in der Bevölkerung
            - Frühe Adaption
            """)

            st.divider()

            st.write("##### Weitere Daten zur Solarenergie in Deutschland")

            st.image(Image.open("images/deutschland_solar.png"), caption = "Entwicklung der Zahlen")
            st.write("Quelle: [Bundesnetzagentur](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/ErneuerbareEnergien/ZahlenDatenInformationen/start.html)")

            st.image(Image.open("images/deutschland_solar_2.png"), caption = "Anzahl Anlagen für Solarenergie")
            st.write("Quelle: [Bundesnetzagentur](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/ErneuerbareEnergien/ZahlenDatenInformationen/start.html)")

            st.image(Image.open("images/deutschland_solar_3.png"), caption = "Arbeitsplätze in der Solarbranche")
            st.write("Quelle: [Bundesnetzagentur](https://strom-report.com/photovoltaik/)")
            
            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [Bundesnetzagentur - EEG in Zahlen](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/ErneuerbareEnergien/ZahlenDatenInformationen/start.html)
            - [Bundesnetzagentur - Erneuerbare Energien](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/ErneuerbareEnergien/ZahlenDatenInformationen/start.html)
            - [STROM REPORT - Hoher Akzeptanz und Nachfrage nach Solarenergie](https://strom-report.com/photovoltaik/)
            - [Erneuerbare Energien - Redaktion Dossier](https://www.erneuerbare-energien.de/EE/Redaktion/DE/Dossier/eeg.html)
            """)

        elif energy_selector_2 == "Wind":
            st.write("#### 1. Warum stieg die Produktion so stark ab 2010?")
            st.write("""
            - Das Erneuerbare-Energien-Gesetz (EEG) wurde novelliert, um die Einspeisevergütung für Strom aus erneuerbaren Quellen zu erhöhen.
            - Ein neues System von Ausschreibungen für Windenergie an Land wurde eingeführt, um die Kosten für den Ausbau der Windenergie zu senken.
            - Anstatt einer garantierten Einspeisevergütung wurde ein wettbewerbliches Vergütungssystem eingeführt, bei dem Windkraftanlagenbetreiber um den Zuschlag für den Bau neuer Anlagen konkurrieren.
            """)

            st.divider()

            st.write("##### Weitere Daten zur Windenergie in Deutschland")

            col8, col9 = st.columns(2)


            with col8:
                st.image(Image.open("images/deutschland_wind_an_land_zuwachs.png"), caption = "Wind an Land Zuwachs Deutschland")
                st.write("Quelle: [Bundesnetzagentur - Statistiken erneuerbarer Energieträger](https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/ErneuerbareEnergien/ZahlenDatenInformationen/EEStatistikMaStRBNetzA.pdf?__blob=publicationFile&v=16)")

            with col9:
                st.image(Image.open("images/deutschland_wind_auf_see_zuwachs.png"), caption = "Wind auf See Zuwachs Deutschland")
                st.write("Quelle: [Bundesnetzagentur - Statistiken erneuerbarer Energieträger](https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/ErneuerbareEnergien/ZahlenDatenInformationen/EEStatistikMaStRBNetzA.pdf?__blob=publicationFile&v=16)")

            st.write("##### Ausbau von Windleistungen")
            st.write("Wir sehen, dass Deutschland in den letzten Jahren erhebliche Fortschritte beim Ausbau der Windenergie auf Land und See gemacht hat. Diese Fortschritte zeigen sich in der Zunahme der installierten Kapazität von Windenergieanlagen. Doch Deutschland hat noch grössere Ziele für die Zukunft: Bis zum Jahr 2030 soll die installierte Kapazität von Windenergieanlagen an Land auf 115’000MW und auf See auf 30’000MW erhöht werden, um eine noch grössere Menge an erneuerbarem Strom zu erzeugen und so den Klimawandel zu bekämpfen.")

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [EEG - Das Erneuerbare Energien Gesetz](https://www.erneuerbare-energien.de/EE/Redaktion/DE/Dossier/eeg.html?docId=95221d23-82f7-4dc4-9beb-e5776d5ca7a0)
            - [Wikipedia - Geschichte der Windenergienutzung](https://de.wikipedia.org/wiki/Geschichte_der_Windenergienutzung)
            """)


        elif energy_selector_2 == "Wasser":
            st.write("#### 1. Was ist der Grund für die konstante Wasserenergie?")
            st.write("""
            - Die Stromerzeugung aus Wasserkraft in Deutschland blieb seit den 1990er Jahren relativ konstant.
            - Die meisten geeigneten Standorte für den Bau von Wasserkraftwerken wurden bereits genutzt.
            - Es wurden andere erneuerbare Energien bevorzugt, wie Solar und Wind.
            """)

            st.write("#### 2. Warum konnte man das ganze nicht noch weiter Ausbreiten?")
            st.write("""
            - Schwieriger Zugang zu verbleibenden Standorten
            - Genehmigungsverfahren wurden aufgrund von Umwelt- und Naturschutzbedenken strenger
            """)

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            """)

    elif country_selector == "Grossbritannien":
            
        if energy_selector_2 == "Solar":

            st.write("#### 1. Warum gibt es ab 2010 einen Anstieg?")
            st.write("""
            - Feed-in Tariff (FIT) wurde von der Regierung entwickelt, um die Einführung erneuerbarer und kohlenstoffarmer Stromerzeugung zu fördern.
            - Das am 1. April 2010 eingeführte System verpflichtet teilnehmende lizenzierte Stromversorger, Zahlungen für Strom zu leisten, der von akkreditierten Anlagen erzeugt und exportiert wird.
            """)

            st.write("#### 2. Warum gibt es ab 2014 einen noch steileren Anstieg?")
            st.write("""
            - Contract for Difference (CfD) wurde eingeführt.
            - CfD ist eine langfristige vertragliche Vereinbarung zwischen einem Stromerzeuger mit geringem Kohlendioxidausstoss und der Low Carbon Contracts Company (LCCC), die dem Erzeuger während der gesamten Vertragslaufzeit Preissicherheit bieten soll.
            - Dieses System schützt erneuerbare Energieerzeuger vor Preisschwankungen auf dem Energiemarkt und gibt ihnen Planungssicherheit für ihre Investitionen. Gleichzeitig schützt es die Verbraucher, da die Energieerzeuger die Differenz zurückzahlen müssen, wenn der Marktpreis höher ist als der Strike-Preis.
            """)

            st.write("#### 3. Warum flacht der Anstieg in 2019 wieder ab?")
            st.write("""
            - Schliessung des FIT-Systems: Nach der Schliessung des FIT-Systems für neue Anmeldungen im April 2019 wurde das SEG-System eingeführt.
            - Die SEG wurde am 1. Januar 2020 eingeführt und ist eine von der Regierung unterstützte Initiative. Das SEG verpflichtet einige Stromversorger (SEG-Lizenznehmer) kleine Erzeuger (SEG-Generatoren) für kohlenstoffarmen Strom zu bezahlen, den sie in das nationale Stromnetz einspeisen, sofern bestimmte Kriterien erfüllt sind.
            - Wirtschaftliche Unsicherheit: Die Pandemie hat Unsicherheiten für Investitionen in erneuerbare Energien verursacht, hauptsächlich durch gesenkte Energienachfrage, verzögerte Projekte und vorsichtigere Investoren. Der Brexit könnte zusätzlich Unsicherheiten und Zugangsbeschränkungen zu Finanzierungsquellen verursacht haben.
            - Energiepreise: Sowohl die Pandemie als auch der Brexit könnten Volatilität in den Energiepreisen verursacht haben. Erstere durch Unterbrechung der globalen Lieferketten und gesunkene Nachfrage und der Brexit durch Handelshemmnisse und währungsbedingte Preisschwankungen.
            - Ökologische Perspektive: Die Pandemie hat einerseits zu verringerten Emissionen geführt, andererseits aber erneuerbare Energieprojekte verzögert. Eine "grüne Erholung" könnte dennoch gestärkte Investitionen und Politiken zur Förderung erneuerbarer Energien nach sich ziehen. Der Brexit gibt Grossbritannien die Möglichkeit, eigene Umweltstandards und -regelungen festzulegen, welche die Umweltverträglichkeit der Energieerzeugung beeinflussen könnten.
            - CO2-Steuern: Die Pandemie und der Brexit haben beide die Möglichkeit zur Neugestaltung der CO2-Steuern geboten, sei es zur Unterstützung der wirtschaftlichen Erholung oder als Teil einer "grünen Erholung".
            - Lieferprobleme: Die Pandemie und der Brexit haben beide zu Unterbrechungen in den Lieferketten geführt, welche die Lieferung von Materialien und Ausrüstungen für erneuerbare Energien beeinträchtigt haben könnten.
            """)

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [About the FIT scheme](https://www.ofgem.gov.uk/environmental-and-social-schemes/feed-tariffs-fit#:~:text=The%20FIT%20scheme%20was%20launched,Capacity%20and%20Functions)
            - [Scheme Closure](https://www.ofgem.gov.uk/environmental-and-social-schemes/feed-tariffs-fit/scheme-closure)
            - [Contracts for Difference (CfD)](https://www.lowcarboncontracts.uk/contracts-for-difference)
            - [About the Smart Export Guarantee (SEG)](https://www.ofgem.gov.uk/environmental-and-social-schemes/smart-export-guarantee-seg#:~:text=About%20the%20Smart%20Export%20Guarantee%20(SEG)&text=The%20SEG%20requires%20some%20electricity,providing%20certain%20criteria%20are%20met.)
            """)

        elif energy_selector_2 == "Wind":

            st.write("#### 1. Wieso gab es erst etwa 2003 einen Aufschwung in der Windenergie?")
            st.write("""
            - Die Entwicklung der Windenergie hat sich erst in den 2000er Jahren beschleunigt, insbesondere im Offshore-Bereich.
            - Offshore-Windenergie hat im Vereinigten Königreich aufgrund der günstigen geographischen Bedingungen und der starken Windressourcen in der Nordsee und der Irischen See grosses Potenzial.
            - Die britische Regierung hat verschiedene politische Massnahmen und Förderinstrumente eingeführt, um Windenergie (sowohl Onshore- als auch Offshore-Wind) zu unterstützen.
            - Dazu gehören das oben erwähnte Feed-in Tariff (FIT)-Schema, das Contract for Difference (CfD)-Schema und andere steuerliche Anreize und Zuschüsse.
            - In den letzten Jahren hat das Vereinigte Königreich seine Bemühungen zur Förderung von Windenergie weiter intensiviert. Im Jahr 2020 kündigte die Regierung beispielsweise an, dass sie das Ziel verfolgt, bis 2030 die Offshore-Windenergiekapazität auf 40 Gigawatt zu erhöhen, was ausreichen würde, um alle Haushalte im Land mit Strom zu versorgen.
            """)

            st.write("#### 2. Wieso gibt es bei 2020 einen Abstieg?")
            st.write("""
            - Wir haben leider ausser dem Offshore-Windenergie-Abkommen nichts diesbezüglich gefunden.
            - Im November 2019 versprach der britische Premierminister Boris Johnson während seiner Wahlkampagne, das Offshore-Wind-Sektor-Abkommen von 2019 von 30 GW bis 2030 auf 40 GW zu erhöhen. Im April 2023 wurde das Ziel aufgrund der Energiekrise durch den Krieg in der Ukraine erneut auf 50 GW erhöht, mit zusätzlichen 5 GW aus schwimmendem Wind.
            - Die britische Regierung hat sich verpflichtet, die Zustimmungszeiten für Offshore-Windparks von bis zu vier Jahren auf ein Jahr zu verkürzen. Bis 2030 müssen etwa 2.600 Windturbinen für insgesamt 48 Milliarden Pfund errichtet werden, was bedeutet, dass jährlich 260 neue Windturbinen gebaut werden müssen.
            - Es gibt jedoch Herausforderungen bei den Lieferketten, der Netzverbindung, den Hafeninvestitionen und der Arbeitskräftebeschaffung. Die Verfügbarkeit idealer Standorte nimmt ab, was dazu führt, dass Entwicklungen weiter draussen im Meer stattfinden müssen. Schwimmende Offshore-Windkraftanlagen könnten eine Lösung bieten, da die britische Regierung ein Ziel von 5 GW schwimmendem Wind bis 2030 hat.
            """)

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [Grossbritannien gibt Ziele für Offshore Windenergie 2030 bekannt](https://www.iwr.de/news/grossbritannien-gibt-ziele-fuer-offshore-windenergie-2030-bekannt-news35869)
            - [Can the UK achieve its 50 GW offshore wind target by 2030?](https://www.dnv.com/article/can-the-uk-achieve-its-50-gw-offshore-wind-target-by-2030--224379)
            )
            """)

        elif energy_selector_2 == "Wasser":

            st.write("#### 1. Hat Grossbritannien überhaupt etwas beüzglich der Wasserkraftenergie übernommen?")
            st.write("""
            - Ja, das System der Renewables Obligation wurde am 1. April 2017 für alle neuen Erzeugungskapazitäten geschlossen.
            - Das System der Renewables Obligation (RO) wurde entwickelt, um die Erzeugung von Strom aus förderfähigen erneuerbaren Quellen im Vereinigten Königreich zu fördern. Die RO-Regelung trat 2002 in Grossbritannien in Kraft, Nordirland folgte im Jahr 2005.
            - Die Regelung verpflichtet die Stromversorger, jährlich eine bestimmte Anzahl von Renewables Obligation Certificates (ROCs) pro Megawattstunde (MWh) Strom vorzulegen, die sie in jedem Verpflichtungszeitraum (1. April - 31. März) an ihre Kunden liefern. Die Versorger können ihre jährliche Verpflichtung erfüllen, indem sie ROCs vorlegen, eine Zahlung in einen Buy-out-Fonds leisten oder eine Kombination aus beidem.
            """)

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [Renewables Obligation (RO) - iea](https://www.iea.org/policies/4182-renewables-obligation-ro)
            - [Renewables Obligation (RO) - ofgem](https://www.ofgem.gov.uk/environmental-and-social-schemes/renewables-obligation-ro)
            """)

    elif country_selector == "Schweiz":
            
        if energy_selector_2 == "Solar":

            st.write("#### 1. Warum hat die Schweiz erst später mit der Produktion von Solarenergie begonnen? - oder warum waren sie langsam, verglichen mit anderen Länder?")
            st.write("""
            - Früher waren die Kosten für die Installation von Solaranlagen sehr hoch.
            - Die begrenzte Verfügbarkeit von Sonnenlicht in einigen Teilen des Landes ist nicht optimal.
            - Die Schweiz hat eine stabile Energieversorgung, die hauptsächlich auf Wasserkraft basiert.
            - Heute ist die Netzparität erreicht und Solarstrom ist billiger wie früher.
            """)

            st.write("#### 2. Warum hat die Schweiz im Vergleich zu anderen Länder relativ wenig Solarenergie?")
            st.write("""
            - Bergige Regionen erschweren den Einsatz von Solaranlagen.
                - Wenig Infrastruktur, Stromleitungen, höhere Kosten
            - Landschaftsschutz
            - Bürokratie und lange Genehmigungsverfahren verlangsamen den Ausbau.
            """)

            st.write("#### 3. Da wir in der Schweiz teilorts öfters Nebel haben, können Solaranlagen damit umgehen? Lohnt es sich dann überhaupt eine Solaranlage zu installieren?")
            st.write("""
            - Generell produzieren Solaranlagen auch im Nebel Strom.
            - Investitionen in grosse Solaranlagen an nebeligen Standorten sind nicht empfehlenswert.
            - Eine kleine PV-Anlage an sonnigen Standorten kann ökologisch sehr sinnvoll sein.
            """)

            st.divider()

            st.write("##### Weitere Daten zur Solarenergie in der Schweiz")

            col3, col4 = st.columns(2)


            with col3:
                st.image(Image.open("images/schweiz_sonnenschein.png"), caption = "Sonnenscheindauer in der Schweiz")
                st.write("Quelle: [Opendata - Klimanormwerte Sonnenscheindauer 1981-2010](https://map.geo.admin.ch/?layers=ch.meteoschweiz.klimanormwerte-sonnenscheindauer_aktuelle_periode)")

                st.write("##### Sonnenschein")
                st.write("""Anhand dieser Visualisierung kann man erkennen, wo es in der Schweiz am meisten Sonnenschein gibt. Im Allgemeinen gilt: Je südlicher, desto sonniger. Ausserdem zeigt sich, dass es in den Tälern mehr Sonnenschein gibt als auf den Berggipfeln (Rhonental, Engadin, Rheintal).
- Kantone auf der Alpensüdseite
    - Tessin
        - Locarno / Cimetta
    - Graubünden
        - Poschiavo, Brusio
    - Wallis
        - Sion
        - Zermatt, Täsch
                """)

            with col4:
                st.image(Image.open("images/schweiz_ausbau_solaranlagen.png"), caption = "Ausbau der Solaranlagen 2023")
                st.write("Quelle: [Bundesamt für Energie - Ausbau der Solaranlagen 2023](https://map.geo.admin.ch/?layers=ch.meteoschweiz.klimanormwerte-sonnenscheindauer_aktuelle_periode)")

                st.write("##### Ausbau der Solaranlagen")
                st.write("""In dieser Grafik sieht man den Fortschritt der jeweiligen Gemeinden bezüglich des Ausbaus von Solaranlagen. Einige Gemeinden liegen vorn, wie Neuendorf, Onnens, Evionnaz und Courgenay, aber auch erkennbare Regionen wie:
- Kanton Luzern
- Kanton Zug
- Kanton Thurgau
- Rheintal """)
            st.divider()

            st.write("##### Das Problem:")
            st.write("In der Schweiz gibt es Regionen mit viel Sonnenschein, in denen jedoch nur wenig bis gar keine Solaranlagen ausgebaut wurden. Dies liegt zum einen an der schwierigen Topografie und der fehlenden Infrastruktur in den Alpenregionen. Das Bauen von Anlagen auf sonnigen Hängen in den Bergen erfordert eine beträchtliche Menge an Stromleitungen und anderer Infrastruktur für den Betrieb und die Wartung der Anlagen. Darüber hinaus spielt auch der Landschaftsschutz eine Rolle, da der Erhalt der natürlichen Schönheit der alpinen Landschaft Priorität hat.")

            st.write("##### Was wird unternommen?")
            st.write("""Um den Ausbau von Solaranlagen in den Bergen zu fördern, hat die Schweizer Berghilfe im Jahr 2023 ein Solarprogramm für Kleinunternehmen in den Bergen ins Leben gerufen. Das Programm zielt darauf ab, den Anreiz für den Bau von Solaranlagen zu erhöhen. Die beteiligten Betriebe können dadurch das ganze Jahr über Strom produzieren, von einer Unterstützung der Investitionskosten von 50 Prozent profitieren, ihre Energiekosten senken und sogar den überschüssigen Strom verkaufen.

Gemäss dem schweizerischen Energiegesetz, Artikel 71.a, Absatz 4, erhalten Anlagen, die bis zum 31. Dezember 2025 mindestens teilweise Elektrizität ins Stromnetz einspeisen, eine Einmalvergütung von maximal 60 Prozent der Investitionskosten vom Bund. Dies hat zu einer regelrechten "Goldgräberstimmung" geführt, da es um Millionen von Bundessubventionen geht. Das Problem dabei ist, dass aufgrund des Zeitdrucks bis 2025 nur die schnellsten und einfachsten Projekte die Subventionen erhalten. Die Kriterien für die Priorisierung der alpinen Solarkraftwerke müssen daher besser festgelegt werden, zum Beispiel sollte bereits eine Strasse und Stromleitung vorhanden sein.
            """)

            st.write("##### Was kann man machen?")
            st.write("Eine vielversprechende Möglichkeit besteht darin, Solaranlagen auf dem Wasser von Stauseen zu installieren. Diese Standorte bieten eine bereits vorhandene Infrastruktur und ermöglichen eine effiziente Nutzung der Fläche für die Solarenergiegewinnung und nimmt nicht viel weg von der natürlichen Schönheit. Eine weitere Möglichkeit wäre Solaranlagen oberhalb von Parkplätzen auszubauen.")

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [UVEK - Elektrizitätsproduktionsanlagen in der Schweiz](https://www.uvek-gis.admin.ch/BFE/storymaps/EE_Elektrizitaetsproduktionsanlagen/)
            - [SRF - Solaranlagen in den Bergen: Schweizer Berghilfe lanciert Solarprogramm für Kleinunternehmen](https://www.srf.ch/news/schweiz/solaranlagen-in-den-bergen-schweizer-berghilfe-lanciert-solarprogramm-fuer-kleinunternehmen)
            - [SRF - Energiewende in den Alpen: Jetzt beginnt das Wettrennen um die Solar-Bundessubventionen](https://www.srf.ch/news/schweiz/energiewende-in-den-alpen-jetzt-beginnt-das-wettrennen-um-die-solar-bundessubventionen)
            )
            """)

        if energy_selector_2 == "Wind":

            st.write("#### 1. Warum hat die Schweiz so wenig Windenergie?")
            st.write("""
            - Die Topografie des Landes erschweren den Bau von Windkraftanlagen in Gebieten mit hohen Windgeschwindigkeiten
            - Nicht viel Platz
            - Warum sind Bau und Wartung der Windräder sind hoch → Beschleunigung Bewilligungsverfahren
            - Planungs- und Bewilligungsverfahren dauern sehr lange → Der Bundesrat schlägt deshalb vor, dass der Bund ein Konzept mit den Standorten der bedeutendsten Wasserkraft- und Windenergieanlagen erarbeitet, das als Vorgabe für die kantonale Richtplanung dient.
            - Öffentliche Wahrnehmung von Windkraftanlagen wird als störend gesehen, insbesondere in ländlichen Gebieten, wo sie oft in der Nähe von Wohngebieten aufgestellt werden müssen
            - Windgeschwindigkeiten in der Schweiz sind im Vergleich zu Deutschland und England niedriger, ausgenommen auf den Bergspitzen der Alpen. (siehe Visualisierungen unten)
            """)

            st.write("#### 2. Wird es geplant, weitere Windparks oder Einzelanlagen zu installieren?")
            st.write("Ja, es ist 1 Windpark in Bau, 18 Projekte in Bewilligungsverfahren und 35 in Planung. Ein Beispiel ist das Projekt in Mollendruz im Kanton Waadt, das 12 Windkraftanlagen mit einer installierten Leistung von bis zu 50.4 MW umfassen wird (Das Projekt befindet sich momentan bei der Vorbereitung des Baugesuchs)")

            st.divider()


            st.write("##### Weitere Daten zur Windenergie in der Schweiz")

            col5, col6, col7 = st.columns(3)

            with col5:
                st.image(Image.open("images/schweiz_windgeschwindigkeit.png"), caption = "Windgeschwindigkeit in der Schweiz")
                st.write("Quelle: [OpenData Swiss - Windatlas Schweiz](https://map.geo.admin.ch/?layers=ch.bfe.windenergie-geschwindigkeit_h50)")
            
            with col6:
                st.image(Image.open("images/schweiz_wind_zonen.png"), caption = "Wind: Bundesinteresse")
                st.write("Quelle: [OpenData Swiss - Windatlas Schweiz](https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=ch.swisstopo.pixelkarte-farbe)")
            
            with col7:
                st.image(Image.open("images/schweiz_europa_wind.png"), caption = "Windatlas für Europa")
                st.write("Quelle: [Universität Oldenburg - Ein Windatlas für Europa](https://uol.de/aktuelles/artikel/ein-windatlas-fuer-europa-3435)")

            st.write("Im linken Bild sind die Windgeschwindigkeiten in einer Höhe von 50 Metern zu sehen. Es zeigt sich, dass die Windgeschwindigkeiten auf den Berggipfeln am höchsten sind, gefolgt von den Seeregionen des Genfersees, Neuenburgersees, Zürichsees, Bodensees sowie dem St. Galler Rheintal, dem Jura-Gebiet und dem Luzerner Hinterland bis zum Zürcher Oberland.")
            st.write("Die mittlere Grafik zeigt die Interessen des Bundes und stellt potenzielle Standorte für den Bau von Windkraftanlagen dar. Dabei ist zu beachten, dass die dargestellten Daten nicht zu 100 Prozent genau sind und weitere detaillierte Untersuchungen erforderlich sind. Dennoch liefert die Grafik eine bessere Orientierung, wo der Ausbau von Windkraftanlagen möglich sein könnte. Basierend auf den beiden Grafiken scheinen potenzielle Standorte auf den kleineren Bergen zwischen Aargau und Zürich, in Teilen des Jura-Gebirges, im St. Galler Rheintal und im Gebiet zwischen dem Neuenburgersee und dem Genfersee geeignet zu sein.")
            st.write("Im rechten Bild werden die Windgeschwindigkeiten auf einer Höhe von 100 Metern für ganz Europa dargestellt. Hier ist erkennbar, dass die Schweiz im Vergleich zu den nordischen Ländern niedrigere Windgeschwindigkeiten aufweist.")

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [Der Bundesrat - Beschleunigung Bewilligungsverfahren](https://www.uvek-gis.admin.ch/BFE/storymaps/EE_Elektrizitaetsproduktionsanlagen/)
            - [Suisse EOLE - Kostenvergleiche](https://suisse-eole.ch/de/news/irena-wind-und-solarstrom-schlagen-im-kostenvergleich-selbst-guenstigste-kohlekonkurrenten/)
            - [Suisse EOLE - Windenergie](https://suisse-eole.ch/de/windenergie/windparks/)
            - [Suisse EOLE - Factsheet](https://suisse-eole.ch/wp-content/uploads/2023/04/20_SE_02_FACTSHEET_Anpassung_D_V3_230404.pdf)
            """)

        if energy_selector_2 == "Wasser":

            st.write("#### 1. Warum setzt die Schweiz so viel auf die Wasserkraftwerke?")
            st.write("""
            - Die Schweiz setzt auf Wasserkraftwerke als zuverlässige und erneuerbare Energiequelle.
            - Die zahlreichen Seen und Flüsse in der Schweiz begünstigen den Bau von Wasserkraftanlagen.
            - Wasserkraft ist eine bewährte Technologie, die der Schweiz ermöglicht, ihre Energiesicherheit zu gewährleisten und Emissionen zu reduzieren.
            """)

            st.write("#### 2. Wie können sie die Produktion so konstant hoch behalten?")
            st.write("""
            - Durch Energiespeicher und Wasserkraftpumpen kann die Produktion von Wasserkraftwerken in der Schweiz konstant gehalten werden.
            - Überschüssige Energie kann gespeichert und in Zeiten höheren Verbrauchs genutzt werden.
            - Wasserkraftpumpen können genutzt werden, um Wasser in höher gelegene Stauseen zu pumpen und so mehr potentielle Energie zu erzeugen.
            """)

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [BFE - Erneuerbare Energien Wasserkraft](https://www.bfe.admin.ch/bfe/de/home/versorgung/erneuerbare-energien/wasserkraft.html)
            """)         

    elif country_selector == "Spanien":
            
        if energy_selector_2 == "Solar":

            st.write("#### 1. Warum hat Spanien erst spät mit der Produktion von Solarenergie begonnen?")
            st.write("""
            - Fossile Brennstoffe: Spanien hat traditionell einen Grossteil seiner Energie aus fossilen Brennstoffen bezogen, insbesondere aus Kohle und Erdgas. Der Übergang zu erneuerbaren Energien ist ein komplexer Prozess, der Zeit, Investitionen und politischen Willen erfordert.
            - Keine Interesse, da die Konzentration auf die Erschliessung von Erdöl- und Erdgasreserven gelegt wurde.
            - Keine klare Strategie für den Ausbau erneuerbarer Energien.
            """)

            st.write("#### 2. Warum flachte die Produktion von Solarenergie nach 2009 ab?")
            st.write("""
            - Da Spanien sich noch immer in einer Wirtschaftskrise befand, waren sie gezwungen, Korrekturen vorzunehmen und Subventionen zu kürzen.
            - Rückwirkende Änderung auf die Vergütungsbedingungen
                - Ein Gesetz, welche den Herstellern von Solaranlagen auf ein Vierteljahrhundert hinaus einen Strompreis von 45 Cent pro Kilowatt garantierte wurde abgeschafft. Das war das Zehnfache des durchschnittlichen Marktpreises.
            - Fast keine Investitionen mehr
            - Ausbaustopp: Die Solarinvestitionen, die bis Ende des Jahres 2007 auf geschätzte mehr als 15 Milliarden Euro angeschwollen waren, kamen zwei Jahre später so gut wie zum Stillstand.
            """)

            st.write("#### 3. Was ist in 2015 passiert?")
            st.write("""
            - Die spanische Regierung führte eine "Sonnensteuer" ein, die Besitzer von Solaranlagen dazu verpflichtete, eine Gebühr für die Erzeugung von Strom zu zahlen, den sie selbst verbrauchten.
            - Diese Politik wurde stark kritisiert und behinderte das Wachstum der Solarenergie
            """)

            st.write("#### 4. Warum gab es ab 2019 einen so starken Anstieg?")
            st.write("""
            - Abschaffung der “Sonnensteuer”
            - Königliche Dekret 244/2019
                - Liberalisierung des spanischen Strommarktes → mehr Akteure können sich am Markt beteiligen (siehe Quelle Seite 20)
            - Sinkende Kosten für Solartechnologien und Strompreise
                - Wachsende Nachfrage nach erneuerbaren Energien
            """)

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [FAZ - Spanien Abschied von der Solar-Weltmacht](https://www.faz.net/aktuell/wirtschaft/wirtschaftspolitik/spanien-abschied-von-der-solar-weltmacht-1227724.html)
            - [TAZ - Erneuerbare Energien in Südspanien](https://taz.de/Erneuerbare-Energien-in-Suedspanien/!5830308/)
            - [Energiezukunft - Abschaffung der Sonnensteuer](https://www.energiezukunft.eu/politik/spanien-beschliesst-abschaffung-der-sonnensteuer/)
            - [Idealista - Boom von Solarstrom in Spanien](https://www.idealista.com/de/news/leben-in-spanien/2020/09/23/7761-ein-neues-gesetz-zum-eigenverbrauch-laesst-den-solarstrom-in-spanien-wieder-boomen)
            - [German Energy Solutions - Spanien Marktanalyse](https://www.german-energy-solutions.de/GES/Redaktion/DE/Publikationen/Marktanalysen/2021/zma-spanien-2021-h2.pdf?__blob=publicationFile&v=4)
            - [Mariscal Abogados - Einspeisevergütungen Spanien](https://www.mariscal-abogados.de/die-abschaffung-des-einspeiseverguetung-system-in-spanien/)
            """)    

        if energy_selector_2 == "Wind":

            st.write("#### 1. Warum sank die Produktion von Wind von 2013 bis 2016?")
            st.write("""
            - Einführung neuer Abgaben
            - Einschränkung des Ausbaus erneuerbarer Energien
            - Erhöhung des Strompreises
            """)

            st.write("#### 2. Warum ist sie 2016 wieder gestiegen? Was waren die Auslöser?")
            st.write("""
            - Veränderte politische Landschaft
            - Internationale Verpflichtungen: Druck von EU
            - Sinkende Kosten für die Technologie
            - Ausschreibungen: Förderte den Wettbewerb und trieb die Kosten weiter nach unten, was den Ausbau von Windkraftanlagen begünstigte
            """)

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [Roedl - Erneuerbare Energien Neue Abgaben](https://www.roedl.de/themen/erneuerbare-energien/neue-abgaben-f%C3%BCr-die-stromerzeuger-in-spanien)
            - [German Energy Solutions - Ausschreibungen in Spanien](https://www.german-energy-solutions.de/GES/Redaktion/DE/Standardartikel/Marktinformationen/Ausschreibungen/2022/20220810-spanien.html)
            - [German Energy Solutions - Ausschreibungen in Spanien](https://climate.ec.europa.eu/eu-action/climate-strategies-targets/2030-climate-energy-framework_de)
            """)   

        if energy_selector_2 == "Wasser":

            st.write("#### 1. Warum schwankt die Energieproduktion bei Wasserkraftwerke so stark?")
            st.write("""
            - Die Produktion von Wasserkraft schwankt aufgrund von Schwankungen in der Verfügbarkeit und dem Volumen des Wassers, das zur Stromerzeugung genutzt wird.
            - In regenreichen Jahren kann die Jahreserzeugung 40 Mrd. kWh überschreiten, während sie in trockenen Jahren weniger als 25 Mrd. kWh beträgt.
            """)

            st.write("#### 2. Warum ist sie 2016 wieder gestiegen? Was waren die Auslöser?")
            st.write("""
            - In Spanien hat die Rolle der Wasserkraft in den letzten Jahren abgenommen.
            - Das Wetter spielt wahrscheinlich eine grosse Rolle: Da es immer wärmer und trockener wird, gibt es weniger Wasser für die Energieproduktion.
            - In Zeiten der Dürre, trinken die Wasserkraftwerke das Wasser von der Landwirtschaft weg.
            - Spanien investiert deshalb eher in andere erneuerbare Energiequellen wie Solar- und Windenergie.
            """)

            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [Costa Nachrichten - Energiewende](https://www.costanachrichten.com/spanien/politik-wirtschaft/spanien-erneuerbare-energien-energiewende-2022-gas-solarenergie-windkraft-biomasse-strompreis-91737644.html)
            """)   


# -------------- 5. POLICY ADVICES ---------------

st.write("### 5. Policy Advices")

with st.expander("## Policy Advices"):
    st.write("Hier werden aus den wichtigsten Erkenntnisse aus den vorherigen Abschnitten Handlungsempfehlungen abgeleitet. Diese Empfehlungen sollen den Entscheidungsträgern in der Politik helfen, die richtigen Massnahmen zu ergreifen, um die Energiewende voranzutreiben.")

    st.write("#### Hypothese 1")
    st.write("Die übermässigen Einspeisevergütungen in Spanien führten zu erheblichen finanziellen Belastungen, mit Staatsschulden in Höhe von über 9 Milliarden Euro, hauptsächlich aufgrund der Diskrepanz zwischen der Einspeisevergütung und den Strompreisobergrenzen. Dies hat dazu geführt, dass seit 2016 Betreiber von Photovoltaikanlagen Abgaben auf installierte Leistung und erzeugte Energiemenge zahlen müssen und kleinere Anlagen (<100 kW) keine Vergütung für eingespeisten Überschussstrom erhalten. Diese Erfahrung dient als Warnung für andere Länder, wie Deutschland und Grossbritannien, bei der Gestaltung ihrer Einspeisevergütungen. Eine effektive Massnahme könnte darin bestehen, regelmässige Überprüfungen und Anpassungen der Einspeisevergütungen durchzuführen, um sicherzustellen, dass sie den Marktbedingungen entsprechen und nicht zu übermässigen Kosten führen. (siehe Plot bei 3. Vergleich Energieproduktion, Produktion der Solarenergie in Spanien flacht nach dem Jahr 2015, weil da die Sonnensteuer eingeführt wurde)")

    st.write("#### Hypothese 2")
    st.write("Die Implementierung eines Systems wie SEG in Grossbritannien könnte in der Schweiz und in Deutschland den Anreiz (z.B. Hausbesitzer kann Ausgaben bezüglich erneuerbaren Enerigen in den nächsten 10 Jahren bei den Steuern abziehen) für Hausbesitzer und kleine Unternehmen erhöhen, in erneuerbare Energiesysteme zu investieren. Dadurch könnte der Anteil der erneuerbaren Energien insgesamt gesteigert werden.")
    
    st.write("#### Hypothese 3")
    st.write("Da die Schweiz noch nicht viel Solarenergie erzeugt hat und ein Platzmangel herrscht, wäre eine vielversprechende Möglichkeit, Solaranlagen auf bereits vorhandener Infrastruktur wie z.B. Parkplätze, auf dem Wasser von Stauseen, Fassaden, Strommasten, Bahnstationen, usw. (siehe Plot bei 3. Vergleich Energieproduktion, Produktion der Solarenergie in Deutschland ist vorbildlich)")
    
    st.write("#### Hypothese 4")
    st.write("In der EU gibt es einen Mangel an globalen Massnahmen. Indem Unternehmen wie Repsol freiwillige Massnahmen ergreifen, können sie nicht nur ihren eigenen ökologischen Fussabdruck reduzieren, sondern auch andere Unternehmen zur Nachahmung ermutigen. Diese Vorreiterrolle und der positive Einfluss können einen Dominoeffekt auslösen, bei dem immer mehr Unternehmen ihre eigenen Massnahmen zur Klimaneutralität entwickeln und umsetzen. Dieser kaskadierende Effekt könnte den Übergang zu einer kohlenstoffarmen Wirtschaft beschleunigen und dazu beitragen, den globalen Klimawandel effektiv anzugehen.")
    

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
 
#html(CHART, width=650, height=370)