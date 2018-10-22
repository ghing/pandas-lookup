pandas-lookup
=============

A port of [agate-lookup](https://github.com/wireservice/agate-lookup) that provides the lookup in Pandas DataFrames instead of Agate Tables.

This uses lookup tables from Wireservice's [lookup](https://github.com/wireservice/lookup) project.

Installation
------------

```
pip install git+https://github.com/ghing/pandas-lookup.git#egg=pandas-lookup
```

Look up a column from a lookup table
------------------------------------

```
>>> import pandaslookup
>>> import pandas as pd
>>> df = pd.DataFrame({'state_abbr': ['CT', 'NY', 'NJ']})
>>> print(df)
  state_abbr
0         CT
1         NY
2         NJ
>>> import pandaslookup
>>> import pandas as pd
>>> df = pd.DataFrame({'state_abbr': ['CT', 'NY', 'NJ']})
>>> print(df)
  state_abbr
0         CT
1         NY
2         NJ
```

Retrieve a table without joining
--------------------------------

```
>>> import pandaslookup
>>> table = pandaslookup.from_lookup(['usps', 'year'], 'population')
>>> print(table.head())
  usps  year  population
0   AL  1970     3454557
1   AL  1971     3497349
2   AL  1972     3540003
3   AL  1973     3580759
4   AL  1974     3627778
```

Installing for development
--------------------------

```
pipenv install --dev -e .
```

Running tests
-------------

```
pipenv run python -m unittest
```

Prior art
---------

- [harbolkn/pandas-lookup](https://github.com/harbolkn/pandas-lookup): This is the same idea, but it relies on the `agate-lookup` package, which createds a needless dependency on Agate. Also, I don't think I like monkey-patching `DataFrame`.
