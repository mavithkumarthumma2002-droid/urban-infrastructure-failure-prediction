# Urban Infrastructure Failure Prediction

Machine Learning assignment, Autumn 2026.

Predicting whether a city block will have a localised infrastructure failure
(1) or not (0) from environmental, structural and operational measurements.
Three model types will be compared: logistic regression, a decision tree and
a neural network. The results go on a single A3 infographic poster.

The data is fictional (456 city blocks, `data/urbandata.csv`).

## How to run

Python 3.9 or newer, from the project root:

```
pip install -r requirements.txt
python main.py
```

`python main.py` runs every step in order, or name the steps to run,
e.g. `python main.py explore`. Charts go to `outputs/figures/` and
tables to `outputs/tables/`.

## Tests

```
python -m pytest
```
