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
            # bild 

            st.write("#### 2. Was sind die Gründe dafür, dass Deutschland im Vergleich zu anderen Ländern eine deutlich höhere Solarenergieproduktion aufweist?")
            st.write("""
            - Attraktive Einspeisevergütungen für Solarstrom seit 2000 → Ansturm auf die Installation von Solarpanels
            - Technologischer Fortschritt im Bereich der Solartechnologie → Kostensenkung & höhere Effizienz
            - Hoher Akzeptanz und Nachfrage nach Solarenergie in der Bevölkerung
            - Frühe Adaption
            """)
            # bild
            
            st.divider()

            st.write("##### Textquellen:")
            st.write("""
            - [EEG förderte Investitionen in erneuerbare Energien](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/ErneuerbareEnergien/ZahlenDatenInformationen/start.html)
            - [Attraktive Einspeisevergütungen für Solarstrom seit 2000 → Ansturm auf die Installation von Solarpanels](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/ErneuerbareEnergien/ZahlenDatenInformationen/start.html)
            - [Hoher Akzeptanz und Nachfrage nach Solarenergie in der Bevölkerung](https://strom-report.com/photovoltaik/)
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
            - [SRF - Solaranlagen in den Bergen: Schweizer Berghilfe lanciert Solarprogramm für Kleinunternehmen,](https://www.srf.ch/news/schweiz/solaranlagen-in-den-bergen-schweizer-berghilfe-lanciert-solarprogramm-fuer-kleinunternehmen)
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

            st.write("#### 2. Warum hat die Schweiz im Vergleich zu anderen Länder relativ wenig Solarenergie?")
            st.write("""
            - Bergige Regionen erschweren den Einsatz von Solaranlagen.
                - Wenig Infrastruktur, Stromleitungen, höhere Kosten
            - Landschaftsschutz
            - Bürokratie und lange Genehmigungsverfahren verlangsamen den Ausbau.
            """)

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