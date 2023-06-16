# cda2 - Policy Advices zur Energieerzeugung ohne Treibhausgasausstoss

## Dashboard
Das Dashboard wurde mithilfe von Streamlit und Heroku erstellt und kann über den folgenden Link aufgerufen werden: https://cda2-policy-advices.herokuapp.com/

## Datenstory
Unsere Datenstory ist direkt im Dashboard integriert.

## Arbeitsprotokoll
Für unsere Arbeitsorganisation haben wir Notion genutzt. Dort haben wir verschiedene Aufgaben mit dazugehörigen Akzeptanzkriterien definiert und diese entsprechend an unsere Teammitglieder verteilt. Weitere Informationen finden Sie unter folgendem Link: https://www.notion.so/CDA2-Challenge-Policy-Advices-f3ea5a4ed3fc421fa40557ebbdc30d85

## Daten
Die verwendeten Daten finden Sie im Ordner /Data. Die meisten dieser Daten stammen von "Our World in Data", allerdings haben wir auch andere Quellen genutzt.

## Python-Dateien
- app.py: Dieses Skript beinhaltet das Streamlit-Dashboard, welches unser Haupt-Interface bildet.
- EDA.ipynb: In diesem Jupyter Notebook wurden die Rohdaten gesammelt, bereinigt, gefiltert und erste Visualisierungen erstellt.
- Old_Dashboard.ipynb: Dieses Jupyter Notebook diente ursprünglich der Erstellung des Dashboards mittels der Bibliothek Panel. Da jedoch Kompatibilitätsprobleme mit den Deployment-Tools wie Heroku oder Google Colab auftraten, haben wir uns gegen diese Lösung entschieden.
- helper.py: In dieser Datei befinden sich Hilfsfunktionen, die wir geschrieben haben, um redundanten Code zu vermeiden und die Lesbarkeit zu verbessern.

## Weitere Dateien
- Procfile: Wird für die Bereitstellung der Anwendung auf Heroku benötigt.
- setup.sh: Ein Shell-Skript, welches die nötigen Schritte zur Einrichtung des Dashboards auf dem Server automatisiert.
- requirements.txt: Diese Datei enthält alle Python-Bibliotheken, die für das Laufen des Dashboards benötigt werden. Sie ist vor allem für das Deployment auf dem Server wichtig.
- .DS_Store und ipynb_checkpoints: Diese Dateien bzw. Ordner sind systemgeneriert und können ignoriert werden.
