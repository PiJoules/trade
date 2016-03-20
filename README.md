# Backtesting and Trading

Module for backtesting strategies and trading with these strategies.

This module was developed in **Python 3.4**.


## Setup
Create and activate a virtualenv for isolating dependencies.
```sh
$ virtualenv -p python3 venv  # Create
$ source venv/bin/activate  # Activate
(venv) $ pip install -r requirements.txt  # Install dependencies
```

Build the package and install scripts.
```sh
(venv) $ python setup.py bdist_wheel  # Create wheel distribution
(venv) $ wheel install dist/trade-0.0.1-py3-none-any.whl  # Install the wheel
(venv) $ wheel install-scripts trade  # Install scripts
```


## Example usage
Download daily data from yahoo for `ORCL` in `2000` and save into `orcl_2000.jsonl.gz`
where `orcl_2000.jsonl.gz` is a gzip'd jsonl file.
```sh
(venv) $ download_yahoo_daily ORCL 2000 orcl_2000.jsonl.gz
```

Download intra day data for the latest trading day for `ORCL` and save into `orcl_intra_day.jsonl.gz`.
```sh
(venv) $ download_yahoo_intra_day ORCL orcl_intra_day.jsonl.gz
```

### Strategies
Example strategies are in the `example/` dir.
```sh
(venv) $ python example/smastrategy.py
2000-02-14 00:00:00: BUY at $62.19 (balance $1000.00)
2000-03-30 00:00:00: SELL at $78.44 (balance $378.12)
2000-04-06 00:00:00: BUY at $82.19 (balance $1162.50)
2000-04-11 00:00:00: SELL at $77.38 (balance $340.62)
2000-04-27 00:00:00: BUY at $77.31 (balance $1114.38)
2000-05-03 00:00:00: SELL at $75.81 (balance $341.25)
2000-05-05 00:00:00: BUY at $76.81 (balance $1099.38)
2000-05-08 00:00:00: SELL at $72.31 (balance $331.25)
2000-05-12 00:00:00: BUY at $74.19 (balance $1054.38)
2000-05-18 00:00:00: SELL at $73.06 (balance $312.50)
2000-05-30 00:00:00: BUY at $74.19 (balance $1043.12)
2000-06-23 00:00:00: SELL at $79.50 (balance $301.25)
2000-06-26 00:00:00: BUY at $82.69 (balance $1096.25)
2000-06-29 00:00:00: SELL at $80.88 (balance $269.38)
2000-06-30 00:00:00: BUY at $84.06 (balance $1078.12)
2000-07-03 00:00:00: SELL at $80.19 (balance $237.50)
2000-07-20 00:00:00: BUY at $78.12 (balance $1039.38)
2000-07-21 00:00:00: SELL at $75.44 (balance $258.12)
2000-07-26 00:00:00: BUY at $76.75 (balance $1012.50)
2000-07-27 00:00:00: SELL at $75.06 (balance $245.00)
2000-08-03 00:00:00: BUY at $77.44 (balance $995.62)
2000-09-11 00:00:00: SELL at $83.44 (balance $221.25)
2000-11-30 00:00:00: BUY at $26.50 (balance $1055.62)
2000-12-29 00:00:00: SELL at $29.06 (balance $790.62)
Final portfolio value: $1081.25
```

This strategy simulates a strategy where you buy 10 shares of Oracle if the simple moving
average (SMA) if the closing price is less than the current day's close and sell 10 shares
if the closing price is greater than the current day's close.


### Plots
Plot latest intra day data for ORCL. Save the output in `orcl.png`.
The plot should show automatically, but in case it doesn't, the plot is saved
in the specified output.
```sh
(venv) $ plot_intra_day orcl_intra_day.jsonl.gz -o orcl.png  # Create plot
(venv) $ eog orcl.png  # SHow plot if it didn't appear in the last command
```

### Miscellaneous Scripts
- `clean.sh`
  - Remove built/compiled files from the current directory.
  - **Do not use this if the virtualenv is in the current directory since it may remove any binary
    files/executables in the virtualenv. I include and use this script beacuse I store all my venvs
    [in a dedicated venv directory](https://github.com/PiJoules/python-dev-scripts).**


## Todo
- Plots
  - Add candlestick plot generation.
  - Support plotting multiple symbols on the same plot.
- Strategies
  - Add more strategies.
  - Add platform for testing different values for different strategies.
    - Ex. Test multiple values for SMA duration in the the smastrategy.py example.
      A profit is made for SMA of 20 days, but not 15 or 30.
- Tests
  - Add unit testing.
- Cleanup possibly unused code.
  - `trade/barfeed/`
  - `trade/parser/`

