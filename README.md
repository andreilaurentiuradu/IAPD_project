# IAPD — predictia performantei ofensive a jucatorilor

Proiectul foloseste un singur notebook pentru colectarea si pregatirea datelor din FBref si StatsBomb, apoi un notebook separat pentru analiza si compararea modelelor.

## Pornire

Instaleaza dependentele din radacina proiectului:

```bash
python3 -m pip install -r requirements.txt
```

Deschide Jupyter din radacina proiectului sau din directorul `notebooks/`, apoi ruleaza [data_scraper.ipynb](extraction/data_scraper.ipynb) de sus in jos. Notebookul incearca ambele surse si salveaza separat cate un tabel pe jucator–meci:

- `data/raw/fbref/fbref_player_match_stats.csv`
- `data/raw/statsbomb/statsbomb_player_match_stats.csv`

FBref este configurat pentru Premier League, La Liga, Ligue 1, Bundesliga si Serie A 2023/24 si refoloseste paginile de meci deja prezente in cache. Notebookul cere toate meciurile celor cinci ligi selectate si refoloseste paginile din cache, descarcand doar paginile lipsa. Daca nu exista cache compatibil, notebookul cere sezonul complet. StatsBomb este configurat pentru FIFA World Cup 2022. Schimba configuratia din primele celule pentru alte sezoane sau perechi competitie–sezon. StatsBomb pastreaza JSON-urile per meci ca checkpointuri, iar FBref foloseste cache-ul `data/cache/fbref` pentru reluare.

Exportul FBref are 54.231 randuri jucator–meci: Premier League 380 meciuri, La Liga 380, Ligue 1 308, Bundesliga 308 si Serie A 380. Ligue 1 si Bundesliga includ cate doua meciuri de baraj pentru retrogradare. StatsBomb are 1.995 randuri din toate cele 64 meciuri ale Cupei Mondiale 2022. Datele celor doua surse raman separate, deoarece statisticile si acoperirea difera. Notebookul standardizeaza timpul de joc ca `Min` pentru ambele surse si verifica minimum 1.000 de aparitii si 10 campuri statistice numerice pentru fiecare dataset.

## Modelare

Ruleaza [player_performance_modeling.ipynb](notebooks/player_performance_modeling.ipynb) dupa scraper. Notebookul combina automat datele FBref si StatsBomb, pastreaza sursa fiecarui rand si evalueaza rezultatele separat pe sursa. Modelul prezice daca jucatorul va avea cel putin un gol sau assist, folosind statistici din aparitiile anterioare. Comparatia include regresia logistica si padurea aleatoare. Testarea este cronologica separat pentru fiecare sursa, iar metricile se salveaza atat general, cat si pe sursa in `data/processed/`.

StatsBomb Open Data contine competitii si sezoane selectate, nu acoperire completa. Daca publici rezultatele, citeaza StatsBomb si respecta cerintele de atribuire din [repository-ul oficial](https://github.com/hudl/open-data). FBref poate limita cererile automate; notebookul ruleaza initial un singur sezon si pastreaza cache-ul pentru reluare.
