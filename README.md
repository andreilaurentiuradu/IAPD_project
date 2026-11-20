# IAPD - predictia performantei ofensive a jucatorilor

Proiectul combina statisticile FBref la nivel de jucator-meci cu istorice Transfermarkt despre accidentari/absente raportate. Datele sunt folosite local pentru analiza si laborator.

## Pornire

Instaleaza dependentele din radacina proiectului:

```bash
python3 -m pip install -r requirements.txt
```

Deschide Jupyter din radacina proiectului sau dintr-un subdirector al acestuia. Ruleaza notebookurile in aceasta ordine:

1. `extraction/data_scraper.ipynb`
2. `notebooks/player_performance_modeling.ipynb`

## Surse si fisiere

### FBref

Pentru sezonul 2023/24, scraperul colecteaza statistici jucator-meci din Premier League, La Liga, Ligue 1, Bundesliga, Serie A, Champions League, Europa League si Conference League. CSV-ul este salvat in `data/raw/fbref/fbref_player_match_stats.csv`. Identificatorul meciului este in `game_id`, echipa in `team`, iar competitia in `league`.

### Transfermarkt

Notebookul descarca local istoricul public de accidentari si profilurile jucatorilor din [football-datasets](https://github.com/salimt/football-datasets), care publica fisiere provenite din Transfermarkt. Fisierele brute sunt pastrate in `data/raw/transfermarkt/`; istoricul imbogatit cu aliasurile de nume este salvat in `transfermarkt_player_injury_histories.csv`.

La ultima verificare, sursa continea 143.195 de inregistrari de absente. Potrivirea numelor Transfermarkt cu FBref reuseste pentru aproximativ 85,5% dintre randurile jucator-meci utilizabile. Numele ambigue raman neasociate. Inregistrarile Transfermarkt pot fi incomplete, iar absenta unui eveniment nu confirma ca jucatorul era apt.

Ambele surse folosesc cache/fisiere locale; la rerulare, fisierele deja descarcate sunt refolosite. Datele brute sunt excluse din Git prin `.gitignore`.

## Modelare

Notebookul de modelare:

- deriva adversarul din perechea de echipe asociata fiecarui `game_id`;
- defineste performanta ofensiva ca gol, assist sau cel putin un sut pe poarta in meciul curent;
- calculeaza predictorii statistici din toate aparitiile anterioare ale jucatorului, fara a folosi meciul curent;
- estimeaza minutele pre-meci prin media minutelor din aparitiile anterioare;
- adauga competitia, identitatea adversarului si indicatori Transfermarkt pentru absente raportate active inaintea meciului si absente din ultimele 365 de zile;
- compara regresia logistica si padurea aleatoare folosind o impartire cronologica, cu cele mai recente 20% dintre datele distincte pastrate pentru test.

Predictiile sunt conditionate de aparitie: CSV-ul FBref contine jucatorii cu minute jucate, nu toti jucatorii convocati sau indisponibili. Transfermarkt nu furnizeaza momentul publicarii raportului; absentele sunt reconstruite retrospectiv dupa intervalul datat si nu reprezinta fise medicale complete. `expected_minutes_pre_match` este o medie istorica, nu o estimare bazata pe primul 11 confirmat.

La ultima rulare, setul de modelare a avut 62.611 randuri si 187 de caracteristici pre-meci. Pentru tinta extinsa, media preciziei (PR AUC) a fost 0,525 la regresia logistica si 0,514 la padurea aleatoare. Aceste scoruri nu sunt direct comparabile cu rularea anterioara, deoarece definitia tintei s-a schimbat.

Rezultatele sunt salvate in `data/processed/`:

- `model_comparison.csv` - metricile generale
- `test_predictions.csv` - predictiile de test cu informatii de context
- `competition_metrics.csv` - metricile separate pe competitie

Evaluarea foloseste meciuri din sezonul 2023/24. Pentru a estima performanta intr-un sezon viitor, modelul trebuie evaluat si pe date din acel sezon.
