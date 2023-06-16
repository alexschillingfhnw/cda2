# cda2 - Policy Advices zur Energieerzeugung ohne Treibhausgasausstoss

## Dashboard

Das Dashboard wurde mittels Streamlit und Heroku gemacht und man findet es hier: https://cda2-policy-advices.herokuapp.com/

## Datastory
Der Datastory befindet sich ebenfalls im Dashboard.

## Arbeitsprotokoll
Wir haben [Notion](https://www.notion.so/CDA2-Challenge-Policy-Advices-f3ea5a4ed3fc421fa40557ebbdc30d85) verwendet. Wir haben dort Tasks mit Akzeptanzkriterien definiert und an den jeweiligen Teammitglieder zugeteilt.

## Daten
Die Daten sind im Ordner /Data zu finden. Die meisten Dateien stammen von Our World in Data, gibt jedoch noch andere Quellen.

## Python Dateien
- app.py: Diese Datei ist unser Dashboard, welche mittels Streamlit programmiert wurde. 
- EDA.ipynb: Hier wurden die ersten Daten gesammelt, bereinigt, gefiltert und visualisiert.
- Old_Dashboard.ipynb: Dieser Notebook haben wir verwendet das Dashboard zu erstellen mittels Panel. Wir hatten jedoch Probleme, das Dashboard mit dem Tool Panel zu veröffentlichen, weil es einfach nicht mit Server-Tools wie Heroku oder Google Colab kompatibel war. Wir versuchten das ganze Dashboard von einem Notebook zu einem normalen Python File zu konvertieren, jedoch scheiterten wir auch hier.
- helper.py: Hier haben wir "Hilfe-Funktionen" programmiert, damit wir den gleichen Code nicht überall kopieren mussten. 

## Andere Dateien
- Procfile
- setup.sh: 
- requirements.txt: Beinhaltet alle Bibliotheken, die für das Dashboard verwendet werden (braucht man für das Deployment des Dashboards)
- .DS_Store: Kann man ignorieren
- ipynb_checkpoints: Kann man ignorieren
