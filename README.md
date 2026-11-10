# Extragere date fotbal

Proiectul folosește notebook-ul [notebooks/football_data_extraction.ipynb](notebooks/football_data_extraction.ipynb) pentru a extrage date din API-ul football-data.org.

## Notebook pentru FBref

Notebook-ul [notebooks/fbref_extraction.ipynb](notebooks/fbref_extraction.ipynb) descarcă jurnale de meci pentru jucători și, opțional, programul/resultatele. Îl poți rula în același mediu Jupyter după instalarea `requirements.txt`. FBref poate răspunde cu 403; în acest caz folosește exportul manual sau încearcă din nou mai târziu.

## Rulare

Din directorul proiectului, instalează dependențele și deschide notebook-ul în VS Code sau Jupyter:

```bash
python3 -m pip install -r requirements.txt
```

Rulează celulele de sus în jos. Notebook-ul cere tokenul API fără să-l afișeze. Poți seta și variabila de mediu `FOOTBALL_DATA_TOKEN`. Modifică `COMPETITION_CODE` și `SEASON_START_YEAR` în celula de configurare.

Rezultatele se salvează în `data/raw/football_data/`: răspunsul brut JSON și fișiere CSV pentru meciuri, goluri, cartonașe și schimbări.

Competițiile și datele disponibile depind de token și de nivelul API. Vezi [documentația football-data.org](https://www.football-data.org/documentation/quickstart) pentru endpoint-urile și filtrele disponibile.

## Notebook pentru TheSportsDB gratuit

Notebook-ul [notebooks/thesportsdb_free_extraction.ipynb](notebooks/thesportsdb_free_extraction.ipynb) folosește API-ul V1 și cheia publică gratuită `123`. Schimbă ID-ul ligii și sezonul în celula de configurare. Outputul se salvează în `data/raw/thesportsdb/`. Planul gratuit are limite per endpoint și nu asigură statistici individuale complete.


## Notebook pentru StatsBomb Open Data

Notebook-ul [notebooks/statsbomb_open_data_extraction.ipynb](notebooks/statsbomb_open_data_extraction.ipynb) descarcă competiții, sezoane, meciuri, evenimente și line-up-uri din depozitul public Hudl/StatsBomb. Selectează perechea ID competiție:ID sezon din catalog. Fișierele ajung în `data/raw/statsbomb/`.

