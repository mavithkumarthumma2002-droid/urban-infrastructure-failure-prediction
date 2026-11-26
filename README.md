# Urban Infrastructure Failure Prediction

Machine Learning assignment, Autumn 2026.

Predicting whether a city block will have a localised infrastructure failure
(1) or not (0) from environmental, structural and operational measurements.
Three model types will be compared: logistic regression, a decision tree and
a neural network. The results go on a single A3 infographic poster.

The data is fictional (456 city blocks, `data/urbandata.csv`).

## Data cleaning

Problems found while exploring the data and what was done about them:

- `inspection_season` had one "sumer" and `inspection_window` one "morni7ng".
  Both fixed, and any other unknown category now stops the run with an error.
- Two blocks had `material_flexibility` = 91.16 when every other value is
  between 25 and 40.5. Set to missing (the rest of those rows is kept).
- `inspector_id` is only the ID of the engineer who checked the record, so
  it is dropped.
- 13 cells are missing after this. They are filled with the training-set
  median inside the model pipeline later, so the test data can't leak in.

## How to run

Python 3.9 or newer, from the project root:

```
pip install -r requirements.txt
python main.py
```

`python main.py` runs every step in order, or name the steps to run,
e.g. `python main.py explore clean`. Charts go to `outputs/figures/` and
tables to `outputs/tables/`.

## Tests

```
python -m pytest
```
