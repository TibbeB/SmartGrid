# SmartGrid

Veel huizen hebben zonnepanelen. Soms produceren deze meer dan ze gebruiken. Om dit overschot op te vangen moeten er batterijen aan gelegd worden. Deze worden dan via een grid (kabels) verbonden met de huizen. Daarnaast hebben batterijen hebben een maximale hoeveelheid stroom die ze kunnen opvangen. Dit creeert de nodigheid voor meerdere batterijen. Het probleem is nu dat het aanleggen van kabels en batterijen geld kosten. Dit creert de noodzaak voor de creatie van een zo'n efficient mogelijk grid, en dat is wat wij gaan proberen te doen.

## Experiment

### Vereisten

In requirements.txt staan alle benodigde packages. Deze kan je installeren via het volgende commando

```
pip install -r requirements.txt
```

### Gebruik Experiment

Bij het experiment wordt er gebruikt van 2 verschillende hillclimbers die de huizen verdelen over de batterijen.

De hillclimbers staan in hun respectievelijke bestanden, experiment.py en experiment1.py.

experiment.py bevat een standaard hillclimber en experiment1.py bevat een simulated annealing hillclimber.

In elk bestand kan de hillclimber voor N seconden of N iteraties gerund afhankelijk van welke functie aangeroepen wordt.

De hillclimber wordt aan geroepen in combinatie met 3 verschillende huis verdelings en 8 verschillende kabel verbinding algoritmes. 

Zowel experiment.py als experiment1.py bevat instructies voor gebruik.

Een overzicht met resultaten wordt na afloop geprint.

Daarnaast wordt er een ook een json file van de het grid configuratie gemaakt.

Om experiment.py aan te roepen gebruik je de volgende code:

```
python3 experiment.py
```

Om experiment.py aan te roepen gebruik je de volgende code:

```
python3 experiment1.py
```

na afloop kunnen de resulaten gevisualiseerd worden via json_reader.py

deze roep je aan met de volgende code:

```
python3 json_reader.py
```

### Structuur

De lijst hieronder weergeeft de structuur van het project:

- **/Huizen&Batterijen**: bevat alle dummy-woonwijken
- **/algorithms**: bevat alle algorithmes met betrekken tot het oplossen van SmartGrid
  - **/algorithms/cable_algoritmes**: bevat alle algoritmes voor het leggen van kabels
  - **/algorithms/initial_state_algorithms**: bevat alle algoritmes voor het optimaal verdelen van de huizen
  - **/algorithms/iterative_algorithms**: bevat alle verschillende hillclimbers voor het verdelen van huizen
  - **/algorithms/not_used_algorithms**: bevat alle ongebruikte/onafgemaakte code die eventueel nog wat zouden kunnen toevoegen aan het project
- **/experiment_results**: bevat alle json files die geproduceert zijn in de experimenten
- **/pictures**: bevat alle afbeeldingen die gebruikt zijn in de code

in de root staat de code voor de experimenten en de visualisatie

## Auteurs
- Patrick Kools
- Tibbe Blaauboer
- Dyon Plomp