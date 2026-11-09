# Extragere date fotbal – pasul 1

Scriptul descarcă statistici la nivel de jucător și meci din FBref și/sau Understat și le salvează ca CSV în `data/raw/`. Păstrează coloanele sursei pentru prelucrarea și verificarea ulterioară. Nu antrenează modele și nu creează încă eticheta „performanță ofensivă ridicată”.

## Instalare și rulare

Din directorul proiectului:

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
python scripts/extract_data.py
```

Implicit descarcă Premier League pentru sezoanele 2023–24 și 2024–25 din FBref.

```bash
# Ambele surse
python scripts/extract_data.py --source both

# Alte ligi și sezoane (numele ligii trebuie să fie recunoscut de soccerdata)
python scripts/extract_data.py --source fbref \
  --leagues "ENG-Premier League" "ESP-La Liga" \
  --seasons 2022-2023 2023-2024

# Alt director de ieșire
python scripts/extract_data.py --source understat --output-dir data/raw
```

Fișierele create implicit:

- `data/raw/fbref_player_match_stats.csv`
- `data/raw/understat_player_match_stats.csv` (când se cere Understat)

## Câmpuri și limite

FBref este sursa principală pentru minute, goluri, pase decisive, șuturi și cartonașe din rapoartele sale de meci. Understat adaugă statistici de șut și indicatori precum xG/xA, dar nu acoperă toate câmpurile. Scriptul nu unește automat rândurile între surse: identificatorii și definițiile pot diferi, iar unirea trebuie verificată înainte de analiză. Forma recentă va trebui calculată într-un pas ulterior din istoricul meciurilor, fără a folosi meciul prezis.

Lista inițială include și alte surse, însă ele nu sunt interschimbabile: StatsBomb Open Data oferă evenimente pentru competiții selectate; football-data.org necesită token și se concentrează pe competiții/meciuri; TheSportsDB oferă date despre evenimente și statistici cu acoperire diferită; Transfermarkt nu este folosit în acest colector. Pentru rezultate reproductibile, începe cu FBref/Understat și notează sursa, liga și sezoanele în lucrare.

Datele pot lipsi sau cererile pot fi limitate de site-uri. soccerdata folosește cache local. Rulează rar și verifică termenii și condițiile fiecărei surse înainte de publicarea datelor extrase.
