#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Print out simple moving average of the relative strategy index of closing
prices as they are processed.
"""

from trade import Feed, BaseStrategy


class RSIStrategy(BaseStrategy):

    def __init__(self, sma_window_size, rsi_window_size):
        assert sma_window_size > 0
        assert rsi_window_size > 0

        super().__init__()

        self.__sma_window = []
        self.__sma_window_size = sma_window_size
        self.__gain_window = []
        self.__loss_window = []
        self.__rsi_window_size = rsi_window_size
        self.__last_close = None
        self.__last_gain_avg = None
        self.__last_loss_avg = None

    def on_bar(self, bar):
        sma_window = self.__sma_window
        gain_window = self.__gain_window
        loss_window = self.__loss_window
        sma_window_size = self.__sma_window_size
        rsi_window_size = self.__rsi_window_size

        sma = None
        rsi = None
        if self.__last_close is not None:
            loss = gain = 0
            change = bar.close - self.__last_close
            if change > 0:
                gain = change
            elif change < 0:
                loss = -change

            gain_avg = loss_avg = None
            if self.__last_gain_avg is None:
                gain_window.append(gain)
                loss_window.append(loss)
                if len(gain_window) >= rsi_window_size:
                    gain_avg = sum(gain_window) / rsi_window_size
                    loss_avg = sum(loss_window) / rsi_window_size
            else:
                gain_avg = (self.__last_gain_avg * (rsi_window_size - 1) +
                            gain) / rsi_window_size
                loss_avg = (self.__last_loss_avg * (rsi_window_size - 1) +
                            loss) / rsi_window_size

            if gain_avg is not None:
                rs = gain_avg / loss_avg
                rsi = 100 - (100 / (1 + rs))

                sma_window.append(rsi)
                if len(sma_window) > sma_window_size:
                    del sma_window[0]
                if len(sma_window) == sma_window_size:
                    sma = sum(sma_window) / sma_window_size
                self.__last_gain_avg = gain_avg
                self.__last_loss_avg = loss_avg

        self.__last_close = bar.close
        print(bar.datetime, bar.close, rsi, sma)


def main():
    # Load the yahoo feed from the CSV file
    feed = Feed()
    feed.add_file("orcl_2000.jsonl.gz")

    # Evaluate the strategy with the feed's data
    strategy = RSIStrategy(15, 14)
    strategy.run(feed)


if __name__ == "__main__":
    main()

