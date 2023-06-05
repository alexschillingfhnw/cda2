#!/usr/bin/env python
# coding: utf-8

# In[20]:


# Import all the helper functions
from helper import *


# ## 2. Explorative Datenanalyse

# ### 2.1 CO₂ Emissionen
# 
# #### 2.1.1 Daten Bereinigung
# 
# Hier lesen wir die CO2 Emissionen ein und bearbeiten die Daten wie folgt:
# 
# 1. Behalte Einträge ab Jahr 1990 im DataFrame.
# 2. Entferne die Spalte "Code".
# 3. Ändere den Spaltennamen "Entity" in "Country".
# 4. Behalte nur Schweiz, Spanien, Deutschland und UK.
# 5. Teile Werte in der Spalte "Annual CO₂ emissions" in miliarde Tonnen um.

# In[21]:


# Read co2 emission data
df_emissions = pd.read_csv("Data/All/CO2/annual-co2-emissions-per-country.csv")

# Wrangle data
df_emissions = wrangle_dataframe(df_emissions, "Annual CO₂ emissions")

# Rename Annual CO₂ emissions to CO2 emissions (billion t)
df_emissions.rename(columns = {'Annual CO₂ emissions': 'CO₂ emissions (billion t)'}, inplace = True)

df_emissions


# ### 2.1.2 CO₂ Emissionen pro Kopf
# 
# Es ist aber nicht sinnvoll, die absoluten CO₂ Emissionen zu betrachten, da die Länder unterschiedlich gross in Landesfläche und Population sind. Deshalb betrachten wir die CO₂-Emissionen pro Kopf und Jahr sowie pro Quadratmeter und Jahr. Dies ermöglicht einen Vergleich der Emissionen, der unabhängig von der Grösse des Landes und der Bevölkerung ist.
# 
# Um die CO₂-Emissionen pro Kopf und Jahr zu berechnen, teilen wir die Gesamtemissionen eines Landes in einem bestimmten Jahr durch die Bevölkerungszahl dieses Landes in diesem Jahr.
# 
# #### 2.1.2.1 Datenaufbereitung

# In[22]:


# Read population data
df_population = pd.read_csv("Data/All/population.csv")

# Rename population column
df_population.rename(columns = {'Population (historical estimates)': 'Population'}, inplace = True)

# Wrangle data
df_population = wrangle_dataframe(df_population, "Population")

df_population


# Wir können nun die beiden Datensätzen verbinden und die Emissionen pro Kopf und Jahr berechnen.

# In[23]:


# Merge dataframes
df_emissions_population = pd.merge(df_emissions, df_population, on = ['Country', 'Year'])

# Create copy of dataframe for emissions per capita
df_em_pop_cap = df_emissions_population.copy()

# Calculate emissions per capita
df_em_pop_cap['CO₂ emissions per capita (t)'] = round(df_em_pop_cap['CO₂ emissions (billion t)'] / df_em_pop_cap['Population'] * 1000000000, 2)

df_em_pop_cap


# Jetzt haben wir die CO₂ Emissionen pro Kopf pro Land und Jahr. Wir können nun die Entwicklung der Emissionen pro Kopf pro Land über die Zeit betrachten (absolute und relative Werte).

# In[24]:


# Create new column and group by country to get value from first row (1990) - add that value to each row
df_em_pop_cap['CO₂ emissions 1990'] = df_em_pop_cap.groupby('Country')['CO₂ emissions (billion t)'].transform(lambda x: x.iloc[0])

# Calculate relative change since 1990
df_em_pop_cap['Relative change CO₂ since 1990'] = round((df_em_pop_cap['CO₂ emissions (billion t)'] - df_em_pop_cap['CO₂ emissions 1990']) / df_em_pop_cap['CO₂ emissions 1990'] * 100, 2)

df_em_pop_cap


# In[25]:


# Create new column and group by country to get value from first row (1990) - add that value to each row
df_em_pop_cap['CO₂ emissions per capita 1990'] = df_em_pop_cap.groupby('Country')['CO₂ emissions per capita (t)'].transform(lambda x: x.iloc[0])

# Calculate relative change since 1990
df_em_pop_cap['Relative change CO₂ per capita since 1990'] = round((df_em_pop_cap['CO₂ emissions per capita (t)'] - df_em_pop_cap['CO₂ emissions per capita 1990']) / df_em_pop_cap['CO₂ emissions per capita 1990'] * 100, 2)

# rename country to Land
df_em_pop_cap.rename(columns = {'Country': 'Land'}, inplace = True)

# rename Year to Jahr
df_em_pop_cap.rename(columns = {'Year': 'Jahr'}, inplace = True)

df_em_pop_cap


# ### 2.1.3 CO2 Emissionen pro Quadratmeter
# 
# Hier die Landesflächen der Länder:
# 
# | Land | Fläche in km2 |
# | --- | --- |
# | Deutschland | 357.386 |
# | Spanien | 505.990 |
# | Schweiz | 41.285 |
# | UK | 242.495 |
# 
# [Quelle](https://de.wikipedia.org/wiki/Liste_von_Staaten_und_Territorien_nach_Fl%C3%A4che)
# 
# Um die CO₂-Emissionen pro Quadratmeter und Jahr zu berechnen, teilen wir die Gesamtemissionen eines Landes in einem bestimmten Jahr durch die Fläche dieses Landes.
# 
# #### 2.1.3.1 Datenaufbereitung

# In[26]:


land_areas = [357386, 505990, 41285, 242495]

# Get list of countries
countries = df_em_pop_cap['Land'].unique().tolist()

# Match countries with land areas
country_land_area = dict(zip(countries, land_areas))

# Create new dataframe for emissions per land area
df_em_land = df_em_pop_cap.copy()

df_em_land['Land Area'] = df_em_land['Land'].map(country_land_area)
df_em_land['CO₂ emissions per land area (t/km²)'] = round(df_em_land['CO₂ emissions (billion t)'] * 1e9 / df_em_land['Land Area'], 2)

# Remove column Land Area
df_em_land.drop(columns = [
    'Land Area', 
    'Population', 
    'CO₂ emissions per capita (t)', 
    'CO₂ emissions 1990',
    'Relative change CO₂ since 1990',
    'CO₂ emissions per capita 1990',
    'Relative change CO₂ per capita since 1990'
    ]
    , inplace = True
)

# rename column CO₂ emissions (billion t) to CO₂ Emissionen (milliard t/km²)
df_em_land.rename(columns = {'CO₂ emissions (billion t)': 'CO₂ emissions (milliard t/km²)'}, inplace = True)

# rename column CO₂ emissions per land area (t/km²) to CO₂ Emissionen pro Landfläche (t/km²)
df_em_land.rename(columns = {'CO₂ emissions per land area (t/km²)': 'CO₂ emissions pro Landfläche (t/km²)'}, inplace = True)

df_em_land


# ## 2.2 Erneuerbare Energien
# ### 2.2.1 Datenaufbereitung
# 
# Diese Daten wurden auf die gleiche Weise wie die CO2-Emissionsdaten aufbereitet. "add_change_columns" berechnet den jährlichen absoluten und relativen Anstieg oder Abstieg der Energieerzeugung aus erneuerbaren Quellen.

# In[27]:


df_renewable_energy = pd.read_csv('Data/All/modern-renewable-prod.csv')

df_renewable_energy = wrangle_dataframe(df_renewable_energy, None)

# rename Country to Land
df_renewable_energy.rename(columns = {'Country': 'Land'}, inplace = True)

# rename column Year to Jahr
df_renewable_energy.rename(columns = {'Year': 'Jahr'}, inplace = True)

# rename Electricity from wind to Produktion Windenergie (TWh)
df_renewable_energy.rename(columns = {'Electricity from wind (TWh)': 'Produktion Windenergie (TWh)'}, inplace = True)

# rename Electricity from solar to Produktion Solarenergie (TWh)
df_renewable_energy.rename(columns = {'Electricity from solar (TWh)': 'Produktion Solarenergie (TWh)'}, inplace = True)

# rename Electricity from hydro to Produktion Wasserkraft (TWh)
df_renewable_energy.rename(columns = {'Electricity from hydro (TWh)': 'Produktion Wasserkraft (TWh)'}, inplace = True)

# rename Electricity from geothermal to Produktion Geothermie (TWh)
df_renewable_energy.rename(columns = {'Other renewables including bioenergy (TWh)': 'Produktion Biomasse (TWh)'}, inplace = True)

df_renewable_energy


# ## 2.3 Energieverbrauch

# In[28]:


# Read energy consumption data
df_energy_cons = pd.read_csv("Data/All/primary-energy-cons.csv")

# Wrangle data
df_energy_cons = wrangle_dataframe(df_energy_cons, "Primary energy consumption (TWh)")

# Rename Country to Land
df_energy_cons.rename(columns = {'Country': 'Land'}, inplace = True)

# Rename Year to Jahr
df_energy_cons.rename(columns = {'Year': 'Jahr'}, inplace = True)

# Rename Primary energy consumption (TWh)
df_energy_cons.rename(columns = {'Primary energy consumption (TWh)': 'Energieverbrauch (TWh)'}, inplace = True)

df_energy_cons


# In[29]:


# Read energy consumption per capita data
df_energy_cons_cap = pd.read_csv("Data/All/per-capita-energy-use.csv")

# Wrangle data
df_energy_cons_cap = wrangle_dataframe(df_energy_cons_cap, "Primary energy consumption per capita (kWh/person)")

# Rename Country to Land
df_energy_cons_cap.rename(columns = {'Country': 'Land'}, inplace = True)

# Rename Year to Jahr
df_energy_cons_cap.rename(columns = {'Year': 'Jahr'}, inplace = True)

# Rename Primary energy consumption per capita (kWh/person)
df_energy_cons_cap.rename(columns = {'Primary energy consumption per capita (kWh/person)': 'Energieverbrauch pro Kopf (kWh/Kopf)'}, inplace = True)

df_energy_cons_cap


# In[30]:


# merge dataframes
df_energy_cons = pd.merge(df_energy_cons, df_energy_cons_cap, on = ['Land', 'Jahr'])
df_energy_cons


# # Widgets

# In[31]:


# Create interactive dataframes
interactive_co2_capita = df_em_pop_cap.interactive()
interactive_co2_land_area = df_em_land.interactive()
interactive_renewable_energy = df_renewable_energy.interactive()
interactive_renewable_energy_new = df_renewable_energy.interactive()
interactive_energy_cons = df_energy_cons.interactive()


# Get list of countries
countries = list(df_renewable_energy["Land"].unique())

# Create country selector widget
country_selector = pn.widgets.CheckButtonGroup(
    name = 'Country selector', 
    value = countries, 
    options = countries,
    button_type = 'primary',
    sizing_mode = 'stretch_both'
)

renewable_energy_selector = pn.widgets.RadioButtonGroup(
    name = 'Renewable energy selector', 
    options = ["Produktion Windenergie (TWh)", "Produktion Wasserkraft (TWh)", "Produktion Solarenergie (TWh)"],
    button_type = 'primary'
)

# Create year slider widget "Fron"
start_year_slider = pn.widgets.IntSlider(
    name = 'Von ',
    start = 1990,
    end = 2020,
    step = 1,
    value = 1990
)

# Create year slider widget "Until"
end_year_slider = pn.widgets.IntSlider(
    name = 'Bis ',
    start = 1990,
    end = 2020,
    step = 1,
    value = 2020
)


# # Pipes

# In[32]:


renewable_energy_pipeline = (
    interactive_renewable_energy[ 
        (interactive_renewable_energy.Land.isin(country_selector)) &
        (interactive_renewable_energy.Jahr.astype('int') >= start_year_slider) &
        (interactive_renewable_energy.Jahr.astype('int') <= end_year_slider)
    ]
    .reset_index(drop=True)

)
co2_capita_pipeline = (
    interactive_co2_capita[
        (interactive_co2_capita.Land.isin(country_selector)) &
        (interactive_co2_capita.Jahr.astype('int') >= start_year_slider) &
        (interactive_co2_capita.Jahr.astype('int') <= end_year_slider)
    ]
    .reset_index(drop=True)
)

co2_land_area_pipeline = (
    interactive_co2_land_area[
        (interactive_co2_land_area.Land.isin(country_selector)) &
        (interactive_co2_land_area.Jahr.astype('int') >= start_year_slider) &
        (interactive_co2_land_area.Jahr.astype('int') <= end_year_slider)
    ]
    .reset_index(drop=True)
)

renewable_energy_pipeline_new = (
    interactive_renewable_energy_new[ 
        (interactive_renewable_energy_new.Land.isin(country_selector)) &
        (interactive_renewable_energy_new.Jahr.astype('int') >= start_year_slider) &
        (interactive_renewable_energy_new.Jahr.astype('int') <= end_year_slider)
    ]
    .reset_index(drop=True)
)

energy_cons_pipeline = (
    interactive_energy_cons[
        (interactive_energy_cons.Land.isin(country_selector)) &
        (interactive_energy_cons.Jahr.astype('int') >= start_year_slider) &
        (interactive_energy_cons.Jahr.astype('int') <= end_year_slider)
    ]
    .reset_index(drop=True)
)


# # Plots

# In[33]:


# Plot Co2 emissions per capita
plot_co2 = co2_capita_pipeline.hvplot(
    x = 'Jahr', 
    y = 'CO₂ emissions per capita (t)',
    by = 'Land', 
    title = 'Entwicklung der CO₂ Emissionen pro Kopf',
    ylabel = 'CO₂ Emissionen pro Kopf (t)',
    width = 700, height = 400)

# Plot Co2 emissions per land area
plot_co2_km2 = co2_land_area_pipeline.hvplot(
    x = 'Jahr', 
    y = 'CO₂ emissions pro Landfläche (t/km²)',
    by = 'Land', 
    title = 'Entwicklung der CO₂ Emissionen pro Landesfläche',
    ylabel = 'CO₂ Emissionen pro Landesfläche (t/km²)',
    width = 700, height = 400)

# Plot Solar Energy Production
plot_solar = renewable_energy_pipeline.hvplot(       
    x = 'Jahr', 
    y = 'Produktion Solarenergie (TWh)',
    by = 'Land',
    title  = 'Solar Energieproduktion',
    xlabel = 'Jahr',
    width = 700, height = 400)

# Plot Wind Energy Production
plot_wind = renewable_energy_pipeline.hvplot(
    x = 'Jahr', 
    y = 'Produktion Windenergie (TWh)',
    by = 'Land',
    title  = 'Wind Energieproduktion',
    width = 700, height = 400)

# Plot Hydro Energy Production
plot_hydro = renewable_energy_pipeline.hvplot(
    x = 'Jahr', 
    y = 'Produktion Wasserkraft (TWh)',
    by = 'Land',
    title  = 'Wasser Energieproduktion',
    width = 700, height = 400)

plot_renewable_energy = renewable_energy_pipeline_new.hvplot(
    x = 'Jahr',
    y = renewable_energy_selector,
    by = 'Land',
    title = 'Produktion erneuerbarer Energien',
    ylabel = 'Energieproduktion (TWh)',
    width = 900, height = 400)

plot_energy_cons = energy_cons_pipeline.hvplot(
    x = 'Jahr',
    y = 'Energieverbrauch (TWh)',
    by = 'Land',
    title = 'Energieverbrauch',
    width = 700, height = 400)

plot_energy_cons_cap = energy_cons_pipeline.hvplot(
    x = 'Jahr',
    y = 'Energieverbrauch pro Kopf (kWh/Kopf)',
    by = 'Land',
    title = 'Energieverbrauch pro Kopf',
    width = 700, height = 400)


# # Texte

# In[34]:


def textblock(text, title = "", subtitle = ""):

    return (
        f"""
        \n### {title}
        \n#### {subtitle}
        \n {text}
        """
    )


# In[35]:


text_allgemeine_infos = """In diesem Dashboard befinden sich Daten bezüglich der Solar-, Wind- und Wasserenergie. Nebenbei werden noch Daten der CO2 Emissionen vorgestellt. Eingeschränkt wurde das Ganze auf die Länder: Deutschland, Spanien, Schweiz und Grossbritannien"""

text_einleitung = """
Willkommen zu unserem interaktiven Dashboard, das sich der Analyse erneuerbarer Energien - insbesondere Solar-, Wasser- und Windenergie - in den Ländern Deutschland, Grossbritannien, Schweiz und Spanien widmet. In einer Ära, in der der Übergang zu erneuerbaren Energien immer wichtiger wird, ist es entscheidend, Daten und Informationen zu erfassen und zu analysieren, um fundierte Entscheidungen und Strategien zu entwickeln.

Dieses Dashboard ist ein tolles Werkzeug, mit dem Sie tiefe Einblicke in die Energiesektoren dieser vier Länder erhalten. Sie können die Daten unabhängig voneinander filtern, um spezifische Trends und Muster zu erkunden. Es ist uns ein grosses Anliegen, dass Sie die Flexibilität haben, Ihre Untersuchungen nach Belieben zu gestalten und zu kontrollieren.

Zusätzlich zu den Daten und Diagrammen, die wir zur Verfügung stellen, haben wir auch eine Datastory erstellt. Diese nimmt Sie mit auf eine Reise durch die Höhen und Tiefen, Siege und Herausforderungen der erneuerbaren Energien in diesen Ländern. Die Datastory kombiniert Datenanalyse mit Narration, um die Daten zum Leben zu erwecken und ein vollständiges Bild der Situation zu zeichnen.

Schliesslich werden wir unsere Policy Advices aufstellen basierend auf unseren Erkenntnissen. Dieser Teil des Dashboards ermöglicht es Ihnen, zukünftige Trends und Entwicklungen im Bereich der erneuerbaren Energien zu prognostizieren. Durch das Verständnis der gegenwärtigen Daten können wir auf mögliche zukünftige Szenarien hinweisen, und wir laden Sie ein, diese Policy Advices mit uns zu erforschen und zu diskutieren.

Wir hoffen, dass dieses Dashboard für Sie sowohl informativ als auch inspirierend ist. Wir freuen uns auf Ihre Erkenntnisse und Diskussionen, die uns dabei helfen, die Zukunft der erneuerbaren Energien in Europa besser zu verstehen und zu gestalten.
"""

text_sidebar = """
Dieser Leitfaden hilft Ihnen dabei, das volle Potenzial unseres interaktiven Dashboards zu nutzen. Hier erfahren Sie, wie Sie die verschiedenen Funktionen und Widgets verwenden können, um Ihre Datenanalyse so effizient und informativ wie möglich zu gestalten.

1. Filtern: Im Dashboards finden Sie eine Reihe von Filtern. Diese ermöglichen Ihnen, die dargestellten Daten nach spezifischen Kriterien einzugrenzen. Wählen Sie beispielsweise ein spezifisches Land aus, um nur Daten für dieses Land anzuzeigen.

2. Jahresanpassung: Unter den Filtern befindet sich ein Schieberegler zur Auswahl des Zeitraums. Bewegen Sie diesen, um Daten für einen bestimmten Zeitraum zu betrachten. Sie können den Schieberegler verschieben, um den Start- und Endpunkt Ihrer Datenauswahl anzupassen.

3. Plots analysieren: Jeder Plot auf dem Dashboard bietet spezifische Informationen zu den ausgewählten Kriterien. Bewegen Sie den Cursor über bestimmte Punkte oder Bereiche im Plot, um detaillierte Informationen anzuzeigen. Diese Funktion ist besonders nützlich, um tiefer in die Daten einzutauchen und spezifische Trends und Muster zu erkennen.
"""

# Textblock CO2 Emissionen
text_co2_emissionen_1 = textblock(
    title = "Wie viel CO₂ wird pro Kopf ausgestossen?",
    text = "Hier wird der jährliche CO₂ Ausstoss pro Einwohner in Tonnen angezeigt. Diese Metrik liefert einen direkten Einblick in die durchschnittliche 'Carbon Footprint' eines Einwohners in jedem der betrachteten Länder. Wir sehen, dass Deutschland am meisten CO₂ pro Kopf ausstösst, während die Schweiz am wenigsten ausstösst."
)

text_co2_emissionen_2 = textblock(
    title = "Wie viel CO₂ wird pro Landesfläche ausgestossen?",
    text = """Dieses Diagramm zeigt die CO₂ Emissionen pro Quadratkilometer für jedes Land. Dies gibt uns eine Vorstellung davon, wie dicht die CO₂ Emissionen in den verschiedenen Ländern sind, unabhängig von der Bevölkerungsdichte. Hier sieht man, dass Deutschland pro Quadratkilometer immer noch am meisten CO₂ ausstösst, aber Grossbritannien ist nahe dahinter. Spanien hat die niedrigsten CO₂ Emissionen pro Quadratkilometer.\n

| Land | Fläche in km2 |
| --- | --- |
| Deutschland | 357.386 |
| Spanien | 505.990 |
| Schweiz | 41.285 |
| Grossbritanien | 242.495 |
"""
)

text_co2_emissionen_3 = textblock(
    title = "Kann über den gesamten Betrachtungszeitraum hinweg ein ermutigender Trend festgestellt werden?",
    text = "Die CO₂ Emissionen haben in allen vier Ländern abgenommen. Dies weist auf erfolgreiche Bemühungen hin, den Kohlenstoffausstoss zu verringern und den Übergang zu einer nachhaltigeren und umweltfreundlicheren Wirtschaftsweise zu gestalten. Diese Diagramme bieten einen umfassenden und vergleichenden Überblick über den CO₂ Ausstoss in diesen Ländern. Sie dienen als wichtiger Indikator für die Fortschritte, die diese Länder bei der Reduzierung ihrer CO₂ Emissionen gemacht haben und bieten wertvolle Einblicke für zukünftige Klimaschutzstrategien."
)

# Textblock Energieverbrauch
text_energieverbrauch_1 = textblock(
    title = "Wie viel Energie verbrauchen die Länder?",
    text = "Dieses interaktive Diagramm zeigt den Energieverbrauch der vier Länder. Er ist die Summe des gesamten Energieverbrauchs, einschliesslich Strom, Verkehr und Heizung. Wir sehen, dass Deutschland den höchsten Energieverbrauch hat, während die Schweiz den niedrigsten Energieverbrauch hat."
)

text_energieverbrauch_2 = textblock(
    title = "Wie stehen die vier Länder im Vergleich, wenn wir den Energieverbrauch pro Person betrachten?",
    text = "Wenn wir jedoch den Energieverbrauch pro Kopf anzeigen, sehen wir grosse Unterschiede der Diagramme, vor allem in der Schweiz. Die Population ist zwar klein in der Schweiz, aber sie verbrauchen mehr Energie pro Kopf wie Spanien und Grossbritannien. In einigen Jahren verbrauchte die Schweiz sogar mehr Energie pro Kopf als Deutschland."
)

text_energieverbrauch_3 = textblock(
    title = "Kann über den gesamten Betrachtungszeitraum hinweg ein ermutigender Trend festgestellt werden?",
    text = "Die CO₂ Emissionen haben seit dem Jahr 2004 in allen vier Ländern abgenommen. Dies liegt an der Entwicklung von erneuerbaren Energien und der Verbesserung der Energieeffizienz."
)

# Textblock Energieproduktion
text_energieveproduktion_1 = textblock(
    title = "Wie viel Energie produzieren die Länder?",
    text=""
)

# Textblock Erneuerbare Energien
text_erneuerbare_energien_1 = textblock(
    text = """In diesem interaktiven Linienplot können Sie die Entwicklungen in der Produktion von erneuerbaren Energien in Deutschland, Grossbritannien, der Schweiz und Spanien nachverfolgen. Es stehen Daten zu den drei wichtigsten Arten von erneuerbaren Energien zur Verfügung: Solarenergie, Wasserkraft und Windenergie.\n
Mit den bereitgestellten Checkboxen können Sie auswählen, welche Art von erneuerbarer Energie in der Grafik angezeigt werden soll. Auf diese Weise können Sie individuell untersuchen, wie sich die Produktion jeder Energieart im Laufe der Zeit in den verschiedenen Ländern entwickelt hat.\n
Der interaktive Plot ermöglicht es Ihnen, die Daten visuell zu erfassen und direkte Vergleiche zwischen den Ländern und den verschiedenen Energiearten zu ziehen. Sie können zum Beispiel die Entwicklung der Solarenergie in Deutschland mit der in Spanien vergleichen, oder betrachten, wie sich die Nutzung der Windenergie in Grossbritannien im Vergleich zur Schweiz entwickelt hat.\n
Diese grafische Darstellung dient als wertvolles Instrument für die Analyse und das Verständnis der Dynamik und Trends im Bereich der erneuerbaren Energien in diesen vier Ländern. Wir hoffen, dass diese Daten Ihnen helfen, fundierte Schlussfolgerungen zu ziehen und ein tieferes Verständnis für den Fortschritt in der Nutzung erneuerbarer Energien zu gewinnen.
"""
)

# Entwicklung der erneuerbaren Energien in Deutschland
text_solar_deutschland = textblock(
    title = "Solarenergie in Deutschland",
    text = ""
)

text_wind_deutschland = textblock(
    title = "Windenergie in Deutschland",
    text = ""
)

text_wasser_deutschland = textblock(
    title = "Wasserkraft in Deutschland",
    text = ""
)

# Entwicklung der erneuerbaren Energien in Grossbritannien
text_solar_grossbritannien_1 = textblock(
    title = "Warum gibt es ab 2010 einen Anstieg?",
    text = """- Feed-in Tariff (FIT) wurde von der Regierung entwickelt, um die Einführung erneuerbarer und kohlenstoffarmer Stromerzeugung zu fördern.
- Das am 1. April 2010 eingeführte System verpflichtet teilnehmende lizenzierte Stromversorger, Zahlungen für Strom zu leisten, der von akkreditierten Anlagen erzeugt und exportiert wird.
"""
)

text_solar_grossbritannien_2 = textblock(
    title = "Warum gibt es ab 2014 einen noch steileren Anstieg?",
    text = """- Contract for Difference (CfD) wurde eingeführt.
- CfD ist eine langfristige vertragliche Vereinbarung zwischen einem Stromerzeuger mit geringem Kohlendioxidausstoss und der Low Carbon Contracts Company (LCCC), die dem Erzeuger während der gesamten Vertragslaufzeit Preissicherheit bieten soll.
- Dieses System schützt erneuerbare Energieerzeuger vor Preisschwankungen auf dem Energiemarkt und gibt ihnen Planungssicherheit für ihre Investitionen. Gleichzeitig schützt es die Verbraucher, da die Energieerzeuger die Differenz zurückzahlen müssen, wenn der Marktpreis höher ist als der Strike-Preis.
"""
)

text_solar_grossbritannien_3 = textblock(
    title = "Warum flacht der Anstieg in 2019 wieder ab?",
    text = """- Schliessung des FIT-Systems: Nach der Schliessung des FIT-Systems für neue Anmeldungen im April 2019 wurde das SEG-System eingeführt.
- Die SEG wurde am 1. Januar 2020 eingeführt und ist eine von der Regierung unterstützte Initiative. Das SEG verpflichtet einige Stromversorger (SEG-Lizenznehmer) kleine Erzeuger (SEG-Generatoren) für kohlenstoffarmen Strom zu bezahlen, den sie in das nationale Stromnetz einspeisen, sofern bestimmte Kriterien erfüllt sind.
- Wirtschaftliche Unsicherheit: 2020 war ein Jahr grosser wirtschaftlicher Unsicherheit aufgrund der COVID-19-Pandemie. Diese Unsicherheit könnte Investitionen in erneuerbare Energien beeinträchtigt haben.
    - Nachfrage nach Energie: Die Pandemie und die damit verbundenen Lockdown-Massnahmen haben zu einer Verringerung der Wirtschaftstätigkeit geführt, was wiederum zu einer Verringerung der Nachfrage nach Energie führen kann. Dies könnte sowohl Auswirkungen auf die Rentabilität von bestehenden erneuerbaren Energieprojekten als auch auf die Aussichten für neue Projekte haben.
    - Verzögerungen bei Projekten: Soziale Distanzierung und andere Gesundheits- und Sicherheitsmassnahmen, die als Reaktion auf die Pandemie eingeführt wurden, könnten zu Verzögerungen bei der Installation und Inbetriebnahme von erneuerbaren Energieprojekten geführt haben. Darüber hinaus könnten Reisebeschränkungen und Störungen in den Lieferketten zu Verzögerungen bei der Beschaffung von Materialien und Ausrüstung geführt haben.
    - Finanzierung und Investitionen: Die wirtschaftliche Unsicherheit, die durch die Pandemie ausgelöst wurde, könnte dazu führen, dass Investoren vorsichtiger bei der Finanzierung von Projekten im Bereich der erneuerbaren Energien sind. Auf der anderen Seite könnte die Suche nach "grünen" Erholungsstrategien nach der Pandemie auch neue Investitionsmöglichkeiten in erneuerbare Energien eröffnen.
    - Politische Prioritäten: Die Notwendigkeit, auf die unmittelbare Gesundheitskrise zu reagieren, könnte dazu führen, dass andere politische Prioritäten, einschliesslich der Förderung von erneuerbaren Energien und der Bekämpfung des Klimawandels, in den Hintergrund treten.
- Brexit: 2020 war auch das Jahr, in dem der Brexit vollzogen wurde. Die damit verbundenen politischen und wirtschaftlichen Veränderungen könnten Auswirkungen auf die Energiebranche gehabt haben, zum Beispiel durch Veränderungen bei den Handelsbedingungen oder durch Unsicherheit bei den Umweltstandards.
    - Investitionen und Finanzierung: Die Unsicherheit im Vorfeld des Brexit könnte potenzielle Investitionen in erneuerbare Energien beeinflusst haben. Zudem könnte der Zugang zu Finanzierungsquellen wie der Europäischen Investitionsbank eingeschränkt sein.
    - Handel: Der Brexit könnte den Handel mit Energie zwischen Grossbritannien und der EU beeinflussen, sowohl direkt (z.B. den Import und Export von Strom) als auch indirekt (z.B. den Handel mit Ausrüstungen für erneuerbare Energien).
    - Regulierung und Standards: Grossbritannien könnte nach dem Brexit entscheiden, von EU-Standards und -Regulierungen in Bezug auf erneuerbare Energien und Klimaschutz abzuweichen. Dies könnte sowohl positive als auch negative Auswirkungen auf den Sektor haben, abhängig von den genauen Entscheidungen, die getroffen werden.
    - Arbeitskräfte: Der Brexit könnte den Zugang zu Arbeitskräften aus der EU beeinflussen, was insbesondere für bestimmte Fachkräfte im Energiesektor relevant sein könnte.
    - Forschung und Entwicklung: Der Brexit könnte Auswirkungen auf die Teilnahme Grossbritanniens an gemeinsamen Forschungs- und Entwicklungsprojekten der EU in Bezug auf erneuerbare Energien und verwandte Technologien haben.
- Energiepreis
    - COVID-19-Pandemie
        - Verringerung der Nachfrage: Aufgrund der globalen wirtschaftlichen Abschwächung und der Reduzierung der Industrietätigkeit während der Lockdowns sank die Nachfrage nach Energie erheblich. Dies könnte zu einem Überangebot führen und dazu, dass die Preise zumindest vorübergehend fallen.
        - Unterbrechung der Lieferketten: Die Pandemie störte die globalen Lieferketten und führte zu Verzögerungen und Unterbrechungen in vielen Sektoren, einschliesslich der Energiebranche. Diese Faktoren könnten dazu führen, dass die Energiepreise steigen.
        - Unsicherheit: Die Unsicherheit rund um die Dauer und die Auswirkungen der Pandemie kann zu Volatilität auf den Energiemärkten führen, was sich auf die Preise auswirken kann.
    - Brexit
        Handelsschranken: Der Brexit könnte Handelshemmnisse zwischen dem Vereinigten Königreich und der EU geschaffen haben, was sich auf die Kosten der Energieversorgung auswirken könnte.
        Währungsschwankungen: Der Brexit hat zu erheblichen Schwankungen im Wert des britischen Pfunds geführt, was Auswirkungen auf die Energiepreise haben kann, insbesondere wenn Energie oder Energiekomponenten importiert werden.
        Regulatorische Unsicherheit: Der Brexit könnte zu Unsicherheiten hinsichtlich zukünftiger Energieregulierung und -politik führen, was sich auf die Investitionen in den Energieinfrastruktursektor und letztendlich auf die Energiepreise auswirken könnte.
- ökologische Perspektive
    - COVID-19-Pandemie
        - Verringerte Emissionen: Während der Lockdowns wurde eine erhebliche Reduzierung der Treibhausgasemissionen verzeichnet, hauptsächlich aufgrund verminderter Industrietätigkeit und Verkehr. Dies könnte jedoch nur ein vorübergehender Effekt sein.
        - Verzögerung von Projekten: Aufgrund von Einschränkungen und wirtschaftlicher Unsicherheit wurden viele Projekte im Bereich der erneuerbaren Energien möglicherweise aufgeschoben oder gestoppt, was die langfristige Umstellung auf erneuerbare Energien verlangsamen könnte.
        - Nachfrage nach grüner Erholung: Die Pandemie hat weltweit ein Bewusstsein für die Notwendigkeit einer grünen Erholung geschaffen. Dies könnte zu verstärkten Investitionen und Politiken zur Förderung erneuerbarer Energien führen, was sich positiv auf die ökologische Nachhaltigkeit auswirken könnte.
    - Brexit
        - Änderungen in Umweltstandards: Nach dem Brexit hat Grossbritannien die Möglichkeit, seine eigenen Umweltstandards und -regelungen festzulegen. Je nachdem, welche Entscheidungen getroffen werden, könnte dies Auswirkungen auf die Umweltverträglichkeit der Energieerzeugung haben.
        - Investitionen und Handel: Änderungen in Handelsvereinbarungen und Investitionsklima nach dem Brexit könnten Auswirkungen auf die erneuerbaren Energien haben, sowohl positiv als auch negativ, je nach den genauen Bedingungen und wie sie die Attraktivität des Sektors für Investoren beeinflussen.
        - Forschung und Zusammenarbeit: Brexit könnte Auswirkungen auf die Beteiligung Grossbritanniens an gemeinsamen Forschungs- und Entwicklungsprojekten und Initiativen im Bereich der erneuerbaren Energien haben, was Auswirkungen auf die langfristige Entwicklung des Sektors haben könnte.
- CO2 Steuern
    - COVID-19-Pandemie
        - Wirtschaftliche Erholung: Die britische Regierung könnte entscheiden, Steuern zu erhöhen oder zu senken, um die wirtschaftliche Erholung nach der Pandemie zu unterstützen. Dies könnte die CO2-Steuer betreffen, je nachdem, welche Auswirkungen die Regierung auf verschiedene Sektoren der Wirtschaft zu steuern versucht.
        - Grüne Erholung: Es gab weltweit Aufrufe zu einer "grünen" Erholung nach der Pandemie, die Investitionen in erneuerbare Energien und andere klimafreundliche Technologien fördert. Die britische Regierung könnte beschliessen, die CO2-Steuer als Teil dieser Strategie zu nutzen.
    - Brexit
        - EU ETS-Austritt: Vor dem Brexit nahm Grossbritannien am Emissionshandelssystem der EU (EU ETS) teil, einem System, das die CO2-Emissionen durch den Handel mit Emissionszertifikaten reguliert. Nach dem Brexit hat Grossbritannien sein eigenes Emissionshandelssystem eingeführt, das das EU-System ersetzen soll.
        - Eigenständige Politikgestaltung: Nach dem Brexit hat Grossbritannien mehr Freiheit, seine eigene Steuerpolitik zu gestalten, einschliesslich der CO2-Steuer. Die genauen Auswirkungen hängen von den Entscheidungen der britischen Regierung ab.
- weltweite Lieferprobleme
    - COVID-19-Pandemie: Die Pandemie führte weltweit zu erheblichen Unterbrechungen in den Lieferketten. Dies könnte die Lieferung von Materialien und Ausrüstungen für erneuerbare Energien beeinträchtigt haben und könnte zu Verzögerungen bei der Fertigstellung einiger Projekte geführt haben.
    - Brexit: Der Austritt Grossbritanniens aus der Europäischen Union könnte möglicherweise zu logistischen Herausforderungen geführt haben, insbesondere in der unmittelbaren Nachwirkung des offiziellen Brexit-Termins. Dies könnte sich auf die Lieferung von Materialien und Ausrüstungen für erneuerbare Energien aus der EU nach Grossbritannien ausgewirkt haben.
"""
)

text_wind_grossbritannien_1 = textblock(
    title = "Wieso gab es erst etwa 2003 einen Aufschwung in der Windenergie?",
    text = """- Die Entwicklung der Windenergie hat sich erst in den 2000er Jahren beschleunigt, insbesondere im Offshore-Bereich.
- Offshore-Windenergie hat im Vereinigten Königreich aufgrund der günstigen geographischen Bedingungen und der starken Windressourcen in der Nordsee und der Irischen See grosses Potenzial.
- Die britische Regierung hat verschiedene politische Massnahmen und Förderinstrumente eingeführt, um Windenergie (sowohl Onshore- als auch Offshore-Wind) zu unterstützen.
- Dazu gehören das oben erwähnte Feed-in Tariff (FIT)-Schema, das Contract for Difference (CfD)-Schema und andere steuerliche Anreize und Zuschüsse.
- In den letzten Jahren hat das Vereinigte Königreich seine Bemühungen zur Förderung von Windenergie weiter intensiviert. Im Jahr 2020 kündigte die Regierung beispielsweise an, dass sie das Ziel verfolgt, bis 2030 die Offshore-Windenergiekapazität auf 40 Gigawatt zu erhöhen, was ausreichen würde, um alle Haushalte im Land mit Strom zu versorgen.
"""
)

text_wind_grossbritannien_2 = textblock(
    title = "Wieso gibt es bei 2020 einen Abstieg?",
    text = """- Wir haben leider ausser dem Offshore-Windenergie-Abkommen nichts diesbezüglich gefunden.
- Im November 2019 versprach der britische Premierminister Boris Johnson während seiner Wahlkampagne, das Offshore-Wind-Sektor-Abkommen von 2019 von 30 GW bis 2030 auf 40 GW zu erhöhen. Im April 2023 wurde das Ziel aufgrund der Energiekrise durch den Krieg in der Ukraine erneut auf 50 GW erhöht, mit zusätzlichen 5 GW aus schwimmendem Wind.
- Die britische Regierung hat sich verpflichtet, die Zustimmungszeiten für Offshore-Windparks von bis zu vier Jahren auf ein Jahr zu verkürzen. Bis 2030 müssen etwa 2.600 Windturbinen für insgesamt 48 Milliarden Pfund errichtet werden, was bedeutet, dass jährlich 260 neue Windturbinen gebaut werden müssen.
- Es gibt jedoch Herausforderungen bei den Lieferketten, der Netzverbindung, den Hafeninvestitionen und der Arbeitskräftebeschaffung. Die Verfügbarkeit idealer Standorte nimmt ab, was dazu führt, dass Entwicklungen weiter draussen im Meer stattfinden müssen. Schwimmende Offshore-Windkraftanlagen könnten eine Lösung bieten, da die britische Regierung ein Ziel von 5 GW schwimmendem Wind bis 2030 hat.
"""
)

text_wasser_grossbritannien_1 = textblock(
    title = "Hat Grossbritannien überhaupt etwas beüzglich der Wasserkraftenergie übernommen?",
    text = """- Ja, das System der Renewables Obligation wurde am 1. April 2017 für alle neuen Erzeugungskapazitäten geschlossen.
- Das System der Renewables Obligation (RO) wurde entwickelt, um die Erzeugung von Strom aus förderfähigen erneuerbaren Quellen im Vereinigten Königreich zu fördern. Die RO-Regelung trat 2002 in Grossbritannien in Kraft, Nordirland folgte im Jahr 2005.
- Die Regelung verpflichtet die Stromversorger, jährlich eine bestimmte Anzahl von Renewables Obligation Certificates (ROCs) pro Megawattstunde (MWh) Strom vorzulegen, die sie in jedem Verpflichtungszeitraum (1. April - 31. März) an ihre Kunden liefern. Die Versorger können ihre jährliche Verpflichtung erfüllen, indem sie ROCs vorlegen, eine Zahlung in einen Buy-out-Fonds leisten oder eine Kombination aus beidem.
"""
)

# Entwicklung der erneuerbaren Energien in der Schweiz
text_solar_schweiz_1 = textblock(
    title = "Warum hat die Schweiz erst später mit der Produktion von Solarenergie begonnen? - oder warum waren sie langsam, verglichen mit anderen Länder?",
    text = """- Früher waren die Kosten für die Installation von Solaranlagen sehr hoch.
- Die begrenzte Verfügbarkeit von Sonnenlicht in einigen Teilen des Landes ist nicht optimal.
- Die Schweiz hat eine stabile Energieversorgung, die hauptsächlich auf Wasserkraft basiert.
- Heute ist die Netzparität erreicht und Solarstrom ist billiger wie früher.
"""
)

text_solar_schweiz_2 = textblock(
    title = "Warum hat die Schweiz im Vergleich zu anderen Länder relativ wenig Solarenergie?",
    text = """- Bergige Regionen erschweren den Einsatz von Solaranlagen
    - Wenig Infrastruktur, Stromleitungen, höhere Kosten
- Landschaftsschutz
- Bürokratie und lange Genehmigungsverfahren verlangsamen den Ausbau
"""
)

text_solar_schweiz_3 = textblock(
    title = "Da wir in der Schweiz teilorts öfters Nebel haben, können Solaranlagen damit umgehen? Lohnt es sich dann überhaupt eine Solaranlage zu installieren?",
    text = """- Generell produzieren Solaranlagen auch im Nebel Strom.
- Investitionen in grosse Solaranlagen an nebeligen Standorten sind nicht empfehlenswert.
- Eine kleine PV-Anlage an sonnigen Standorten kann ökologisch sehr sinnvoll sein
"""
)

text_solar_schweiz_4 = textblock(
    subtitle = "Sonnenschein",
    text = """Anhand dieser Visualisierung kann man erkennen, wo es in der Schweiz am meisten Sonnenschein gibt. Im Allgemeinen gilt: Je südlicher, desto sonniger. Ausserdem zeigt sich, dass es in den Tälern mehr Sonnenschein gibt als auf den Berggipfeln (Rhonental, Engadin, Rheintal).
- Kantone auf der Alpensüdseite
    - Tessin
        - Locarno / Cimetta
    - Graubünden
        - Poschiavo, Brusio
    - Wallis
        - Sion
        - Zermatt, Täsch
"""
)

text_solar_schweiz_5 = textblock(
    subtitle = "Ausbau der Solaranlagen",
    text = """In dieser Grafik sieht man den Fortschritt der jeweiligen Gemeinden bezüglich des Ausbaus von Solaranlagen. Einige Gemeinden liegen vorn, wie Neuendorf, Onnens, Evionnaz und Courgenay, aber auch erkennbare Regionen wie:
- Kanton Luzern
- Kanton Zug
- Kanton Thurgau
- Rheintal
"""
)

text_solar_schweiz_6 = textblock(
    text = """In der Schweiz gibt es Regionen mit viel Sonnenschein, in denen jedoch nur wenig bis gar keine Solaranlagen ausgebaut wurden. Dies liegt zum einen an der schwierigen Topografie und der fehlenden Infrastruktur in den Alpenregionen. Das Bauen von Anlagen auf sonnigen Hängen in den Bergen erfordert eine beträchtliche Menge an Stromleitungen und anderer Infrastruktur für den Betrieb und die Wartung der Anlagen. Darüber hinaus spielt auch der Landschaftsschutz eine Rolle, da der Erhalt der natürlichen Schönheit der alpinen Landschaft Priorität hat.

Um den Ausbau von Solaranlagen in den Bergen zu fördern, hat die Schweizer Berghilfe im Jahr 2023 ein Solarprogramm für Kleinunternehmen in den Bergen ins Leben gerufen. Das Programm zielt darauf ab, den Anreiz für den Bau von Solaranlagen zu erhöhen. Die beteiligten Betriebe können dadurch das ganze Jahr über Strom produzieren, von einer Unterstützung der Investitionskosten von 50 Prozent profitieren, ihre Energiekosten senken und sogar den überschüssigen Strom verkaufen.

Gemäss dem schweizerischen Energiegesetz, Artikel 71.a, Absatz 4, erhalten Anlagen, die bis zum 31. Dezember 2025 mindestens teilweise Elektrizität ins Stromnetz einspeisen, eine Einmalvergütung von maximal 60 Prozent der Investitionskosten vom Bund. Dies hat zu einer regelrechten "Goldgräberstimmung" geführt, da es um Millionen von Bundessubventionen geht. Das Problem dabei ist, dass aufgrund des Zeitdrucks bis 2025 nur die schnellsten und einfachsten Projekte die Subventionen erhalten. Die Kriterien für die Priorisierung der alpinen Solarkraftwerke müssen daher besser festgelegt werden, zum Beispiel sollte bereits eine Strasse und Stromleitung vorhanden sein.

Eine vielversprechende Möglichkeit besteht darin, Solaranlagen auf Stauseen zu errichten, ähnlich wie es bereits am Mutsee oder Albignasee geschieht. Diese Standorte bieten eine bereits vorhandene Infrastruktur und ermöglichen eine effiziente Nutzung der Fläche für die Solarenergiegewinnung und nimmt nichts mehr weg von der natürlichen Schönheit.
"""
)

text_wind_schweiz = textblock(
    title = "Windenergie in der Schweiz",
    text = ""
)

text_wasser_schweiz = textblock(
    title = "Wasserkraft in er Schweiz",
    text = ""
)

# Entwicklung der erneuerbaren Energien in Spanien
text_solar_spanien = textblock(
    title = "Solarenergie in Spanien",
    text = ""
)

text_wind_spanien = textblock(
    title = "Windenergie in Spanien",
    text = ""
)

text_wasser_spanien = textblock(
    title = "Wasserkraft in Spanien",
    text = ""
)

text_hypothesen_einleitung = textblock(
    title = "Welche Hypothesen stellen wir nun anhand dieser Erkenntnissen auf, um die Energiewende voranzutreiben?",
    text = ""
)

# Textblock Policy Advice
text_policy_advice_1 = textblock(
    title = "Hypothese 1",
    text = "Die Erfahrung Spaniens dient in anderen Ländern (insbesondere Deutschland und Grossbritannien) als Warnung, dass eine zu grosszügige Einspeisevergütung ohne entsprechende Kontrollmechanismen zu finanziellen Schwierigkeiten führen kann. Eine konkrete Massnahme könnte darin bestehen, regelmässige Überprüfungen und Anpassungen der Einspeisevergütungen durchzuführen, um sicherzustellen, dass sie die Marktbedingungen widerspiegeln und nicht zu übermässigen Kosten führen."
)

text_policy_advice_2 = textblock(
    title = "Hypothese 2",
    text = "Die Implementierung eines Systems wie SEG in Grossbritannien kann in der Schweiz und in Deutschland den Anreiz für Hausbesitzer und kleine Unternehmen erhöhen könnte, in erneuerbare Energiesysteme zu investieren. Dadurch könnte der Anteil der erneuerbaren Energien insgesamt gesteigert werden."
)

# Textblock Policy Advice
text_policy_advice_3 = textblock(
    title = "Hypothese 3",
    text = "Da die Schweiz noch nicht viel Solarenergie erzeugt hat und ein Platzmangel herrscht, wäre eine vielversprechende Möglichkeit, Solaranlagen auf bereits vorhandener Infrastruktur (z.B. Stauseen, Bahngleisen, Strommasten, Bahnstationen, usw.)  zu errichten, ähnlich wie es bereits am Mutsee oder Albignasee geschieht."
)

text_solar_schweiz_6 = textblock(
    text = """In der Schweiz gibt es Regionen mit viel Sonnenschein, in denen jedoch nur wenig bis gar keine Solaranlagen ausgebaut wurden. Dies liegt zum einen an der schwierigen Topografie und der fehlenden Infrastruktur in den Alpenregionen. Das Bauen von Anlagen auf sonnigen Hängen in den Bergen erfordert eine beträchtliche Menge an Stromleitungen und anderer Infrastruktur für den Betrieb und die Wartung der Anlagen. Darüber hinaus spielt auch der Landschaftsschutz eine Rolle, da der Erhalt der natürlichen Schönheit der alpinen Landschaft Priorität hat.

Um den Ausbau von Solaranlagen in den Bergen zu fördern, hat die Schweizer Berghilfe im Jahr 2023 ein Solarprogramm für Kleinunternehmen in den Bergen ins Leben gerufen. Das Programm zielt darauf ab, den Anreiz für den Bau von Solaranlagen zu erhöhen. Die beteiligten Betriebe können dadurch das ganze Jahr über Strom produzieren, von einer Unterstützung der Investitionskosten von 50 Prozent profitieren, ihre Energiekosten senken und sogar den überschüssigen Strom verkaufen.

Gemäss dem schweizerischen Energiegesetz, Artikel 71.a, Absatz 4, erhalten Anlagen, die bis zum 31. Dezember 2025 mindestens teilweise Elektrizität ins Stromnetz einspeisen, eine Einmalvergütung von maximal 60 Prozent der Investitionskosten vom Bund. Dies hat zu einer regelrechten "Goldgräberstimmung" geführt, da es um Millionen von Bundessubventionen geht. Das Problem dabei ist, dass aufgrund des Zeitdrucks bis 2025 nur die schnellsten und einfachsten Projekte die Subventionen erhalten. Die Kriterien für die Priorisierung der alpinen Solarkraftwerke müssen daher besser festgelegt werden, zum Beispiel sollte bereits eine Strasse und Stromleitung vorhanden sein.

Eine vielversprechende Möglichkeit besteht darin, Solaranlagen auf Stauseen zu errichten, ähnlich wie es bereits am Mutsee oder Albignasee geschieht. Diese Standorte bieten eine bereits vorhandene Infrastruktur und ermöglichen eine effiziente Nutzung der Fläche für die Solarenergiegewinnung und nimmt nichts mehr weg von der natürlichen Schönheit.
"""
)

text_wind_schweiz_1 = textblock(
    title = "Warum hat die Schweiz so wenig Windenergie?",
    text = """ 
- Die Topografie des Landes erschweren den Bau von Windkraftanlagen in Gebieten mit hohen Windgeschwindigkeiten
- Nicht viel Platz
- Warum sind Bau und Wartung der Windräder sind hoch → Beschleunigung Bewilligungsverfahren
    - Planungs- und Bewilligungsverfahren dauern sehr lange → Der Bundesrat schlägt deshalb vor, dass der Bund ein Konzept mit den Standorten der bedeutendsten Wasserkraft- und Windenergieanlagen erarbeitet, das als Vorgabe für die kantonale Richtplanung dient.
- Öffentliche Wahrnehmung von Windkraftanlagen wird als störend gesehen, insbesondere in ländlichen Gebieten, wo sie oft in der Nähe von Wohngebieten aufgestellt werden müssen
- Windgeschwindigkeiten in der Schweiz sind im Vergleich zu Deutschland und England niedriger, ausgenommen auf den Bergspitzen der Alpen. (siehe Visualisierungen unten)
"""
)

text_wind_schweiz_2 = textblock(
    title = "Wird es geplant, weitere Windparks oder Einzelanlagen zu installieren?",
    text = "Ja, es ist 1 Windpark in Bau, 18 Projekte in Bewilligungsverfahren und 35 in Planung. Ein Beispiel ist das Projekt in Mollendruz im Kanton Waadt, das 12 Windkraftanlagen mit einer installierten Leistung von bis zu 50.4 MW umfassen wird (Das Projekt befindet sich momentan bei der Vorbereitung des Baugesuchs)"
)

text_wind_schweiz_3 = textblock(
    text = """Im unten links dargestellten Bild sind die Windgeschwindigkeiten in einer Höhe von 50 Metern zu sehen. Es zeigt sich, dass die Windgeschwindigkeiten auf den Berggipfeln am höchsten sind, gefolgt von den Seeregionen des Genfersees, Neuenburgersees, Zürichsees, Bodensees sowie dem St. Galler Rheintal, dem Jura-Gebiet und dem Luzerner Hinterland bis zum Zürcher Oberland.

Die mittlere Grafik zeigt die Interessen des Bundes und stellt potenzielle Standorte für den Bau von Windkraftanlagen dar. Dabei ist zu beachten, dass die dargestellten Daten nicht zu 100 Prozent genau sind und weitere detaillierte Untersuchungen erforderlich sind. Dennoch liefert die Grafik eine bessere Orientierung, wo der Ausbau von Windkraftanlagen möglich sein könnte. Basierend auf den beiden Grafiken scheinen potenzielle Standorte auf den kleineren Bergen zwischen Aargau und Zürich, in Teilen des Jura-Gebirges, im St. Galler Rheintal und im Gebiet zwischen dem Neuenburgersee und dem Genfersee geeignet zu sein.

Im rechten Bild werden die Windgeschwindigkeiten auf einer Höhe von 100 Metern für ganz Europa dargestellt. Hier ist erkennbar, dass die Schweiz im Vergleich zu den nordischen Ländern niedrigere Windgeschwindigkeiten aufweist.
    
"""
)

text_wasser_schweiz_1 = textblock(
    title = "Warum setzt die Schweiz so viel auf die Wasserkraftwerke?",
    text = """
- Die Schweiz setzt auf Wasserkraftwerke als zuverlässige und erneuerbare Energiequelle.
- Die zahlreichen Seen und Flüsse in der Schweiz begünstigen den Bau von Wasserkraftanlagen.
- Wasserkraft ist eine bewährte Technologie, die der Schweiz ermöglicht, ihre Energiesicherheit zu gewährleisten und Emissionen zu reduzieren.
"""
)

text_wasser_schweiz_2 = textblock(
    title = "Wie können sie die Produktion so konstant hoch behalten?",
    text = """
- Durch Energiespeicher und Wasserkraftpumpen kann die Produktion von Wasserkraftwerken in der Schweiz konstant gehalten werden.
- Überschüssige Energie kann gespeichert und in Zeiten höheren Verbrauchs genutzt werden.
- Wasserkraftpumpen können genutzt werden, um Wasser in höher gelegene Stauseen zu pumpen und so mehr potentielle Energie zu erzeugen.
"""
)

# Entwicklung der erneuerbaren Energien in Spanien
text_solar_spanien_1 = textblock(
    title = "Warum hat Spanien erst spät mit der Produktion von Solarenergie begonnen?",
    text = """
- Fossile Brennstoffe: Spanien hat traditionell einen Grossteil seiner Energie aus fossilen Brennstoffen bezogen, insbesondere aus Kohle und Erdgas. Der Übergang zu erneuerbaren Energien ist ein komplexer Prozess, der Zeit, Investitionen und politischen Willen erfordert.
- Keine Interesse, da die Konzentration auf die Erschliessung von Erdöl- und Erdgasreserven gelegt wurde.
- Keine klare Strategie für den Ausbau erneuerbarer Energien.
"""
)

text_solar_spanien_2 = textblock(
    title = "Warum flachte die Produktion von Solarenergie nach 2009 ab?",
    text = """
- Da Spanien sich noch immer in einer Wirtschaftskrise befand, waren sie gezwungen, Korrekturen vorzunehmen und Subventionen zu kürzen.
- Rückwirkende Änderung auf die Vergütungsbedingungen
    - Ein Gesetz, welche den Herstellern von Solaranlagen auf ein Vierteljahrhundert hinaus einen Strompreis von 45 Cent pro Kilowatt garantierte wurde abgeschafft. Das war das Zehnfache des durchschnittlichen Marktpreises.
- Fast keine Investitionen mehr
- Ausbaustopp: Die Solarinvestitionen, die bis Ende des Jahres 2007 auf geschätzte mehr als 15 Milliarden Euro angeschwollen waren, kamen zwei Jahre später so gut wie zum Stillstand.
"""
)

text_solar_spanien_3 = textblock(
    title = "Was ist in 2015 passiert?",
    text = """
- Die spanische Regierung führte eine "Sonnensteuer" ein, die Besitzer von Solaranlagen dazu verpflichtete, eine Gebühr für die Erzeugung von Strom zu zahlen, den sie selbst verbrauchten.
- Diese Politik wurde stark kritisiert und behinderte das Wachstum der Solarenergie
"""
)

text_solar_spanien_4 = textblock(
    title = "Warum gab es ab 2019 einen so starken Anstieg?",
    text = """
- Abschaffung der “Sonnensteuer”
- Königliche Dekret 244/2019
    - Liberalisierung des spanischen Strommarktes → mehr Akteure können sich am Markt beteiligen (siehe Quelle Seite 20)
- Sinkende Kosten für Solartechnologien und Strompreise
    - Wachsende Nachfrage nach erneuerbaren Energien
"""
)

text_wind_spanien_1 = textblock(
    title = "Warum sank die Produktion von Wind von 2013 bis 2016?",
    text = """
- Einführung neuer Abgaben
- Einschränkung des Ausbaus erneuerbarer Energien
- Erhöhung des Strompreises    
"""
)

text_wind_spanien_2 = textblock(
    title = "Warum ist sie 2016 wieder gestiegen? Was waren die Auslöser?",
    text = """
- Veränderte politische Landschaft
- Internationale Verpflichtungen: Druck von EU
- Sinkende Kosten für die Technologie
- Ausschreibungen: Förderte den Wettbewerb und trieb die Kosten weiter nach unten, was den Ausbau von Windkraftanlagen begünstigte 
"""
)

text_wasser_spanien_1 = textblock(
    title = "Warum schwankt die Energieproduktion bei Wasserkraftwerke so stark?",
    text = """
- Die Produktion von Wasserkraft schwankt aufgrund von Schwankungen in der Verfügbarkeit und dem Volumen des Wassers, das zur Stromerzeugung genutzt wird.
- In regenreichen Jahren kann die Jahreserzeugung 40 Mrd. kWh überschreiten, während sie in trockenen Jahren weniger als 25 Mrd. kWh beträgt.    
"""
)

text_wasser_spanien_2 = textblock(
    title = "Warum nimmt seit 2010 die Produktion regelmässig ab?",
    text = """
- In Spanien hat die Rolle der Wasserkraft in den letzten Jahren abgenommen.
- Das Wetter spielt wahrscheinlich eine grosse Rolle: Da es immer wärmer und trockener wird, gibt es weniger Wasser für die Energieproduktion.
- In Zeiten der Dürre, trinken die Wasserkraftwerke das Wasser von der Landwirtschaft weg.
- Spanien investiert deshalb eher in andere erneuerbare Energiequellen wie Solar- und Windenergie.    
"""
)


# # Dashboard

# In[39]:


width = 900
small_width = 650
margin = 0
template = pn.template.FastListTemplate(
    title = "Policy Advices für eine grüne Zukunft",
    sidebar_width = 375,
    sidebar = [
        textblock(
            title = "Allgemeine Informationen",
            text = text_allgemeine_infos
        ),
        pn.Spacer(height=20),
        textblock(
            title = "Einstellungen",
            text = "Mittels Sliders und Buttons ist es möglich die einzelnen Plots auf das Jahr und das Land zu beschränken"
        ),
        pn.Row(
            country_selector,
            margin=(0, 5)
        ),
        pn.Row(
            start_year_slider,
            margin=(10, 5)
        ),
        pn.Row(
            end_year_slider,
            margin=(10, 5)
        ),
        #pn.pane.PNG('sidebar_image.png', sizing_mode='scale_width'),
        #pn.pane.Markdown("Bildquelle: [Kasakata](https://kasakata.co.id/wp-content/uploads/2022/03/eco-green-thumbnail-kasakata.jpg)"),
    ],
    
    main = [
        pn.Row(
            pn.Column(
                "# Willkommen!",
                pn.Card(
                    text_einleitung,
                    title = "Einleitung",
                    margin = (5,25),
                    sizing_mode = 'stretch_width',
                    collapsed = True
                ),
                pn.Card(
                    text_sidebar,
                    title = "Anleitung",
                    margin = (5,25),
                    sizing_mode = 'stretch_width',
                    collapsed = True
                ),
                pn.Spacer(height=30),
                sizing_mode = 'stretch_width'
            ),
            sizing_mode = 'stretch_width'
        ),
        pn.Row(
            pn.Column(
                "# Datastory",

# ------------- Co2 Emissionen Plots -------------
                pn.Card(
                    pn.Column(
                        pn.Column(
                            pn.Column(
                                pn.pane.Markdown(text_co2_emissionen_1, sizing_mode='stretch_width'),
                                plot_co2.panel(),
                                sizing_mode='stretch_width'
                            ),
                            pn.pane.Markdown("Datenquelle: [Our World in Data - CO₂ Emissions](https://ourworldindata.org/co2-emissions)"),
                            pn.Column(
                                pn.pane.Markdown(text_co2_emissionen_2, sizing_mode='stretch_width'),
                                plot_co2_km2.panel(),
                                sizing_mode='stretch_width'
                            ),
                            pn.pane.Markdown("Datenquelle: [Our World in Data - CO₂ Emissions](https://ourworldindata.org/co2-emissions)"),
                            sizing_mode='stretch_width'
                        ),
                        sizing_mode='stretch_width'
                    ),
                    text_co2_emissionen_3,
                    title="CO₂ Emissionen",
                    margin=(5, 25),
                    sizing_mode='stretch_width',
                    collapsed = True
                ),

# ------------- Energy Consumtion Plots -------------
                pn.Card(
                    pn.Column(
                        pn.Column(
                            pn.pane.Markdown(text_energieverbrauch_1, sizing_mode = 'stretch_width'),
                            plot_energy_cons.panel(),
                            sizing_mode = 'stretch_width'
                        ),
                        pn.pane.Markdown("Datenquelle: [Our World in Data - CO₂ Emissions](https://ourworldindata.org/co2-emissions)"),
                        pn.Column(
                            pn.pane.Markdown(text_energieverbrauch_2, sizing_mode = 'stretch_width'),
                            plot_energy_cons_cap.panel(),
                            sizing_mode = 'stretch_width'
                        ),
                        pn.pane.Markdown("Datenquelle: [Our World in Data - CO₂ Emissions](https://ourworldindata.org/co2-emissions)"),
                        sizing_mode = 'stretch_width'
                    ),
                    text_energieverbrauch_3,
                    title = "Vergleich Energieverbrauch",
                    margin = (5,25),
                    sizing_mode = 'stretch_width',
                    collapsed = True
                ),

# ------------- Vergleich der Länder (erneuerbare Energien) -------------


                pn.Card(
                    pn.Column(
                        pn.pane.Markdown(text_energieveproduktion_1, sizing_mode='stretch_width'),
                        pn.Column(
                            renewable_energy_selector,
                            plot_renewable_energy.panel(),
                            sizing_mode='stretch_width'
                        ),
                        pn.pane.Markdown("Datenquelle: [Our World in Data - CO₂ Emissions](https://ourworldindata.org/co2-emissions)"),
                        pn.pane.Markdown(text_erneuerbare_energien_1, sizing_mode='stretch_width'),
                        margin=(10, 0),
                        sizing_mode='stretch_width'
                    ),
                    title = "Vergleich Energieproduktion",
                    margin = (5,25),
                    sizing_mode = 'stretch_width',
                    collapsed = True
                ),
                
                
# ------------- Entwicklung im Zeitverlauf -------------
                pn.Card(

# ---------------- DEUTSCHLAND ----------------

                    pn.Row(
                        pn.Card(
                            text_solar_deutschland,
                            title = "Solarenergie in Deutschland",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'
                    ),
                    pn.Row(
                        pn.Card(
                            text_wind_deutschland,
                            title = "Windenergie in Deutschland",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'
                    ),
                    pn.Row(
                        pn.Card(
                            text_wasser_deutschland,
                            title = "Wasserkraft in Deutschland",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'              
                    ),

# ---------------- GROSSBRITANNIEN ----------------

                    pn.Row(
                        pn.Card(
                            text_solar_grossbritannien_1,text_solar_grossbritannien_2, text_solar_grossbritannien_3,
                            pn.pane.Markdown("""Textquellen:
                            [About the FIT scheme](https://www.ofgem.gov.uk/environmental-and-social-schemes/feed-tariffs-fit#:~:text=The%20FIT%20scheme%20was%20launched,Capacity%20and%20Functions),
                            [Scheme Closure](https://www.ofgem.gov.uk/environmental-and-social-schemes/feed-tariffs-fit/scheme-closure),
                            [Contracts for Difference (CfD)](https://www.lowcarboncontracts.uk/contracts-for-difference),
                            [About the Smart Export Guarantee (SEG)](https://www.ofgem.gov.uk/environmental-and-social-schemes/smart-export-guarantee-seg#:~:text=About%20the%20Smart%20Export%20Guarantee%20(SEG)&text=The%20SEG%20requires%20some%20electricity,providing%20certain%20criteria%20are%20met.)
                            """                 
                            ),
                            title = "Solarenergie in Grossbritannien",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'
                    ),
                    pn.Row(
                        pn.Card(
                            text_wind_grossbritannien_1, text_wind_grossbritannien_2,
                            pn.pane.Markdown("""Textquellen:
                            [Grossbritannien gibt Ziele für Offshore Windenergie 2030 bekannt](https://www.iwr.de/news/grossbritannien-gibt-ziele-fuer-offshore-windenergie-2030-bekannt-news35869),
                            [Can the UK achieve its 50 GW offshore wind target by 2030?](https://www.dnv.com/article/can-the-uk-achieve-its-50-gw-offshore-wind-target-by-2030--224379)
                            """                 
                            ),
                            title = "Windenergie in Grossbritannien",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'
                    ),
                    pn.Row(
                        pn.Card(
                            text_wasser_grossbritannien_1,
                            pn.pane.Markdown("""Textquellen:
                            [Renewables Obligation (RO) - iea](https://www.iea.org/policies/4182-renewables-obligation-ro),
                            [Renewables Obligation (RO) - ofgem](https://www.ofgem.gov.uk/environmental-and-social-schemes/renewables-obligation-ro)
                            """                 
                            ),
                            title = "Wasserkraft in Grossbritannien",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'     
                    ),

# ---------------- SCHWEIZ ----------------

                    pn.Row(
                        pn.Card(
                            text_solar_schweiz_1,
                            text_solar_schweiz_2,
                            text_solar_schweiz_3,
                            pn.Column(
                                pn.pane.Markdown("### Weitere Daten zur Solarenergie in der Schweiz"),
                                pn.Row(
                                    pn.pane.PNG('schweiz_sonnenschein.png', sizing_mode = 'scale_width'),
                                    pn.pane.PNG('schweiz_ausbau_solaranlagen.png', sizing_mode = 'scale_width'),
                                ),
                                pn.Row(
                                    pn.pane.Markdown("Quelle: MeteoSchweiz - Klimanormwerte Sonnenscheindauer 1981-2010", sizing_mode = 'stretch_width'),
                                    pn.pane.Markdown("Quelle: Bundesamt für Energie - Ausbau der Solaranlagen 2023", sizing_mode = 'stretch_width'),
                                ),
                                pn.Row(
                                    pn.pane.Markdown(text_solar_schweiz_4, sizing_mode = 'stretch_width'),
                                    pn.pane.Markdown(text_solar_schweiz_5, sizing_mode = 'stretch_width'),
                                ),
                                sizing_mode = 'stretch_width'
                            ),
                            text_solar_schweiz_6,
                            pn.pane.Markdown("""Textquellen:
                            [UVEK - Elektrizitätsproduktionsanlagen in der Schweiz](https://www.uvek-gis.admin.ch/BFE/storymaps/EE_Elektrizitaetsproduktionsanlagen/),
                            [SRF - Solaranlagen in den Bergen: Schweizer Berghilfe lanciert Solarprogramm für Kleinunternehmen](https://www.srf.ch/news/schweiz/solaranlagen-in-den-bergen-schweizer-berghilfe-lanciert-solarprogramm-fuer-kleinunternehmen),
                            [SRF - Energiewende in den Alpen: Jetzt beginnt das Wettrennen um die Solar-Bundessubventionen](https://www.srf.ch/news/schweiz/energiewende-in-den-alpen-jetzt-beginnt-das-wettrennen-um-die-solar-bundessubventionen)
                            """
                            ),
                            title = "Solarenergie in der Schweiz",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'
                    ),
                    pn.Row(
                        pn.Card(
                            text_wind_schweiz_1,
                            text_wind_schweiz_2,
                            pn.Column(
                                pn.pane.Markdown("### Weitere Daten zur Windenergie in der Schweiz"),
                                pn.Row(
                                    pn.pane.PNG('schweiz_windgeschwindigkeit.png', sizing_mode = 'scale_width'),
                                    pn.pane.PNG('schweiz_wind_zonen.png', sizing_mode = 'scale_width'),
                                    pn.pane.PNG('schweiz_europa_wind.png', sizing_mode = 'scale_width'),
                                ),
                                pn.Row(
                                    pn.pane.Markdown("Quelle: OpenData Swiss - Windatlas Schweiz", sizing_mode = 'stretch_width'),
                                    pn.pane.Markdown("Quelle: OpenData Swiss - Windatlas Schweiz", sizing_mode = 'stretch_width'),
                                    pn.pane.Markdown("Quelle: Universität Oldenburg - Ein Windatlas für Europa", sizing_mode = 'stretch_width'),
                                ),
                                sizing_mode = 'stretch_width'
                            ),
                            text_wind_schweiz_3,
                            pn.pane.Markdown("""Textquellen:    
                            [Der Bundesrat - Beschleunigung Bewilligungsverfahren](https://www.admin.ch/gov/de/start/dokumentation/medienmitteilungen.msg-id-87045.html),
                            [Suisse EOLE - Kostenvergleiche](https://suisse-eole.ch/de/news/irena-wind-und-solarstrom-schlagen-im-kostenvergleich-selbst-guenstigste-kohlekonkurrenten/),
                            [Suisse EOLE - Windenergie](https://suisse-eole.ch/de/windenergie/windparks/),
                            [Suisse EOLE - Factsheet](https://suisse-eole.ch/wp-content/uploads/2023/04/20_SE_02_FACTSHEET_Anpassung_D_V3_230404.pdf)
                            """
                            ),
                            title = "Windenergie in der Schweiz",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'
                    ),
                    pn.Row(
                        pn.Card(
                            text_wasser_schweiz_1,
                            text_wasser_schweiz_2,
                            pn.pane.Markdown("Textquellen: [BFE - Erneuerbare Energien Wasserkraft](https://www.bfe.admin.ch/bfe/de/home/versorgung/erneuerbare-energien/wasserkraft.html)"),
                            title = "Wasserkraft in der Schweiz",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'            
                    ),

# ---------------- SPANIEN ----------------
                    pn.Row(
                        pn.Card(
                            text_solar_spanien_1,
                            text_solar_spanien_2,
                            text_solar_spanien_3,
                            text_solar_spanien_4,
                            pn.pane.Markdown("""Textquellen:  
                            [FAZ - Spanien Abschied von der Solar-Weltmacht](https://www.faz.net/aktuell/wirtschaft/wirtschaftspolitik/spanien-abschied-von-der-solar-weltmacht-1227724.html),
                            [TAZ - Erneuerbare Energien in Südspanien](https://taz.de/Erneuerbare-Energien-in-Suedspanien/!5830308/),
                            [Energiezukunft - Abschaffung der Sonnensteuer](https://www.energiezukunft.eu/politik/spanien-beschliesst-abschaffung-der-sonnensteuer/),
                            [Idealista - Boom von Solarstrom in Spanien](https://www.idealista.com/de/news/leben-in-spanien/2020/09/23/7761-ein-neues-gesetz-zum-eigenverbrauch-laesst-den-solarstrom-in-spanien-wieder-boomen),
                            [German Energy Solutions - Spanien Marktanalyse](https://www.german-energy-solutions.de/GES/Redaktion/DE/Publikationen/Marktanalysen/2021/zma-spanien-2021-h2.pdf?__blob=publicationFile&v=4),
                            [Mariscal Abogados - Einspeisevergütungen Spanien](https://www.mariscal-abogados.de/die-abschaffung-des-einspeiseverguetung-system-in-spanien/)  
                            """
                            ),
                            title = "Solarenergie in Spanien",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'
                    ),
                    pn.Row(
                        pn.Card(
                            text_wind_spanien_1,
                            text_wind_spanien_2,
                            pn.pane.Markdown("""Textquellen:  
                            [Roedl - Erneuerbare Energien Neue Abgaben](https://www.roedl.de/themen/erneuerbare-energien/neue-abgaben-f%C3%BCr-die-stromerzeuger-in-spanien),
                            [German Energy Solutions - Ausschreibungen in Spanien](https://www.german-energy-solutions.de/GES/Redaktion/DE/Standardartikel/Marktinformationen/Ausschreibungen/2022/20220810-spanien.html),
                            [Climate EC Europa - Climate Energy Framework](https://climate.ec.europa.eu/eu-action/climate-strategies-targets/2030-climate-energy-framework_de)
                            """
                            ),
                            title = "Windenergie in Spanien",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'
                    ),
                    pn.Row(
                        pn.Card(
                            text_wasser_spanien_1,
                            text_wasser_spanien_2,
                            pn.pane.Markdown("""Textquellen:  
                            [Costa Nachrichten - Energiewende](https://www.costanachrichten.com/spanien/politik-wirtschaft/spanien-erneuerbare-energien-energiewende-2022-gas-solarenergie-windkraft-biomasse-strompreis-91737644.html)
                            """
                            ),
                            title = "Wasserkraft in Spanien",
                            margin = (5,25),
                            sizing_mode = 'stretch_width',
                            collapsed = True
                        ),
                        sizing_mode = 'stretch_width'              
                    ),
                    pn.Spacer(height=30),
                    title = "Ereignisse in der Energieproduktion",
                    margin = (5,25),
                    sizing_mode = 'stretch_width',
                    collapsed = True
                ),
                pn.Spacer(height=30),
                sizing_mode = 'stretch_width'
            ),
            sizing_mode = 'stretch_width'
        ),
    ],
    accent_base_color = '#2E8B57',
    header_background = '#2E8B57',
)

#template.show()
pn.serve(template)

