# IAPD — predictia performantei ofensive a jucatorilor

Proiectul foloseste un singur notebook pentru colectarea si pregatirea datelor din FBref si StatsBomb, apoi un notebook separat pentru analiza si compararea modelelor.

## Pornire

Instaleaza dependentele din radacina proiectului:

```bash
python3 -m pip install -r requirements.txt
```

Deschide Jupyter din directorul `notebooks/`, apoi ruleaza [data_scraper.ipynb](notebooks/data_scraper.ipynb) de sus in jos. Notebookul incearca ambele surse si salveaza separat cate un tabel pe jucator–meci:

- `notebooks/data/raw/fbref/fbref_player_match_stats.csv`
- `notebooks/data/raw/statsbomb/statsbomb_player_match_stats.csv`

FBref este configurat initial pentru Premier League 2023/24 si refoloseste paginile de meci deja prezente in cache. Exportul curent include 244 din cele 380 de meciuri ale sezonului; seteaza `FBREF_USE_CACHED_MATCHES_ONLY = False` pentru a cere intregul sezon. Daca nu exista cache compatibil, notebookul cere sezonul complet. StatsBomb este configurat pentru FIFA World Cup 2022. Schimba configuratia din primele celule pentru alte sezoane sau perechi competitie–sezon. StatsBomb pastreaza JSON-urile per meci ca checkpointuri, iar FBref foloseste cache-ul `notebooks/data/cache/fbref` pentru reluare.

Datele celor doua surse raman separate, deoarece statisticile si acoperirea difera. Notebookul standardizeaza timpul de joc ca `Min` pentru ambele surse si verifica minimum 1.000 de aparitii si 10 campuri statistice numerice pentru fiecare dataset.

## Modelare

Ruleaza [player_performance_modeling.ipynb](notebooks/player_performance_modeling.ipynb) dupa scraper. Variabila `MODEL_SOURCE` alege `statsbomb` sau `fbref`; ambele exporturi au campurile comune necesare modelului. Modelul prezice daca jucatorul va avea cel putin un gol sau assist, folosind statistici din aparitiile anterioare. Comparatia include Logistic Regression si Random Forest, cu split cronologic si metrici potrivite clasei pozitive rare.

StatsBomb Open Data contine competitii si sezoane selectate, nu acoperire completa. Daca publici rezultatele, citeaza StatsBomb si respecta cerintele de atribuire din [repository-ul oficial](https://github.com/hudl/open-data). FBref poate limita cererile automate; notebookul ruleaza initial un singur sezon si pastreaza cache-ul pentru reluare.
