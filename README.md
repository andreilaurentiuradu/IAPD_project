# IAPD - predictia performantei ofensive a jucatorilor

Proiectul colecteaza statistici FBref la nivel de jucator si meci pentru sezonul 2023/24. `extraction/data_scraper.ipynb` extrage si salveaza datele, iar `notebooks/player_performance_modeling.ipynb` le exploreaza si compara doua modele de baza.

## Structura si pornire

Instaleaza dependentele din radacina proiectului:

```bash
python3 -m pip install -r requirements.txt
```

Deschide Jupyter din radacina proiectului sau dintr-un subdirector al acestuia. Ruleaza notebookurile in aceasta ordine:

1. `extraction/data_scraper.ipynb`
2. `notebooks/player_performance_modeling.ipynb`

## Extragerea datelor

Scraperul foloseste FBref pentru sezonul 2023/24 in urmatoarele competitii:

- Premier League
- La Liga
- Ligue 1
- Bundesliga
- Serie A
- Champions League
- Europa League
- Conference League

Datasetul este salvat in `data/raw/fbref/fbref_player_match_stats.csv`. Fiecare rand este o aparitie a unui jucator intr-un meci. Coloana `league` identifica competitia, iar `game_id` identifica meciul. Paginile descarcate sunt pastrate in `data/cache/fbref` si pot fi refolosite daca notebookul este rerulat. CSV-ul final este scris dupa ce extragerea si pregatirea datelor s-au incheiat.

CSV-ul verificat in prezent contine 66.731 de randuri jucator-meci, din 2.163 de meciuri si 8 competitii. La o noua extragere, notebookul afiseaza sumarul curent.

## Explorare si modelare

Notebookul `player_performance_modeling.ipynb` citeste CSV-ul FBref, standardizeaza campurile folosite si afiseaza grafice pentru volumul datelor pe competitie, contributiile la gol, suturi si corelatiile dintre statisticile din acelasi meci. Corelatiile sunt descriptive; statisticile din meciul curent nu sunt folosite ca predictori.

Tinta este daca jucatorul inscrie cel putin un gol sau ofera cel putin un assist in meciul curent. Predictorii sunt calculati din toate aparitiile anterioare disponibile ale jucatorului in dataset, indiferent de competitie, si includ competitia meciului curent. Meciul curent este exclus din aceste rezumate. Sunt comparate regresia logistica si padurea aleatoare. Datele sunt impartite cronologic, pastrand cele mai recente 20% dintre datele distincte pentru test.

Rezultatele sunt salvate in `data/processed/`:

- `model_comparison.csv` - metricile generale ale modelelor
- `test_predictions.csv` - predictiile pentru observatiile de test
- `competition_metrics.csv` - metricile modelului ales, separat pe competitie

Evaluarea foloseste meciuri din sezonul 2023/24. Pentru a estima performanta intr-un sezon urmator, modelul trebuie evaluat si pe date din acel sezon, care nu au fost folosite la antrenare.

## Note

- FBref poate limita cererile automate; cache-ul local permite refolosirea paginilor deja descarcate.
- O corelatie intre doua statistici nu demonstreaza o relatie cauzala.
- Mai multe date sau competitii nu garanteaza automat predictii mai bune; compara metricile si testeaza pe un sezon ulterior.
