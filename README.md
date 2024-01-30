# SmartGrid

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

In elk bestand wordt de hillclimber voor N seconden gerund met 5 verschillende kabel verbinding algoritmes. 

Zowel experiment.py als experiment1.py bevat instructies voor gebruik.

Een overzicht met resultaten wordt na afloop geprint.

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

## Auteurs
- Patrick Kools
- Tibbe Blaauboer
- Dyon Plomp