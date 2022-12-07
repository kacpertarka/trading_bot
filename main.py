import os
import time
import pandas as pd
from datetime import datetime
from tradingview_ta import TA_Handler, Interval  # ,  Exchange

from csv_functions import create_file, to_file, from_file

# RSI[1], open[1], close[1], low[1], high[1]

FILE: str = "./test.csv"
COLUMN_NAMES_LIST: list[str] = ['open', 'close', 'high', 'low', 'RSI', 'time']
DEFAULT_SIZE_OF_DATA: int = 100

handler = TA_Handler(
    symbol="ETHBUSD",  # TSLA
    exchange="BINANCE",  # NASDAQ
    screener="crypto",  # america
    interval=Interval.INTERVAL_5_MINUTES,
    # timeout=None
)


class Container:

    def __init__(self):
        self._open = None
        self._close = None
        self._high = None
        self._low = None
        self._rsi = None
        self._time = None

    def data_frame(self) -> pd.DataFrame:
        list_of_data: list[float|str] = [self._open, self._close, self._high, self._low, self._rsi, self._time]
        data_to_frame: dict[str: float|str] = {key: [val] for key, val in zip(COLUMN_NAMES_LIST, list_of_data)}
        df: pd.DataFrame = pd.DataFrame.from_dict(data=data_to_frame)
        return df

    def get_data_from_handler(self, handler: TA_Handler) -> None:
        self._open = handler.get_indicators(['open[1]'])['open[1]']
        self._close = handler.get_indicators(['close[1]'])['close[1]']
        self._high = handler.get_indicators(['high[1]'])['high[1]']
        self._low = handler.get_indicators(['low[1]'])['low[1]']
        self._rsi = handler.get_indicators(['RSI[1]'])['RSI[1]']
        self._time = datetime.now().strftime("%H:%M:%S")


container = Container()


def sleeper(curr_time: datetime.time) -> None:
    """ Calculete the difference between current time and the next time divided by 5 ? :) """
    minute: int = curr_time.minute  # np.  4
    if minute == 4 and current_time.second > 40:
        time.sleep(20)
    delta_minute: int = minute % 5
    minute_to_add: int = 5 - delta_minute
    sleep_time: int = minute_to_add * 60
    print(f"Ide spac na {sleep_time} sekund!!")
    time.sleep(sleep_time)


while True:

    current_time: datetime.time = datetime.now().time()
    if not current_time.minute % 5 == 0:  # 00, 05, 10, 15, 20 ... - minutes
        sleeper(current_time)
    # !!!!
    try:
        container.get_data_from_handler(handler)
    except Exception:
        print("Connection Error - sleep!!")
        sleeper(current_time)
    if not os.path.exists(FILE):
        create_file(FILE)

    data: pd.DataFrame = from_file(FILE)  # data from csv file
    adding_data: pd.DataFrame = container.data_frame()  # DataFrame with current data
    if len(data) > 10:  # 100 - default - DEFAULT_SIZE_OF_DATA
        """ if true -> delete first row, add last -> repeat xD """
        data = data.drop(0)
    to_file(FILE, data, adding_data)  # save DataFrame to csv file
    time.sleep(60)  
