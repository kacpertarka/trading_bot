import pandas as pd
from typing import Optional

"""
    Szukanie trendu: porównujemy wartosci - tworzymy granicę górną i dolną a następnie dla każdej kolejnej wartości z df
    porównujemy je z wartościami: max, min i jeśli max przebija górną to zamieniamy, jeśli przebija 2 > razy to 
    dolną zamieniamy na min poprzedniej wartości :)
"""

TREND_TYPE = {
    -1: "DOWN",
    0: "NONE",
    1: "UP"
}


class TrendValue:
    def __init__(self, trend: str, high_border: Optional[float] = None, low_border: Optional[float] = None):
        self._trend = trend
        self._high_border = high_border
        self._low_border = low_border

    @property
    def trend(self) -> str:
        return self._trend

    @trend.setter
    def trend(self, trend: int):
        self._trend = TREND_TYPE.get(trend, 0)

    @property
    def high_border(self) -> float:
        return self._high_border

    @high_border.setter
    def high_border(self, value: float):
        self._high_border = value

    @property
    def low_border(self) -> float:
        return self._low_border

    @low_border.setter
    def low_border(self, value: float):
        self._low_border = value


def find_trend(data: pd.DataFrame) -> TrendValue:
    """
    Find trend in given DataFrame :)
    """
    trend = TrendValue(TREND_TYPE[0])
    # zmienne do przechowywania "starych" wartosci granicznych ? :D
    temp_low_border = 0
    temp_high_border = 0
    # zmienne do sprawdzania czy był podwójny wzrost/spadek
    temp_iter_high = 0
    temp_iter_low = 0
    for _, data in data.iterrows():
        print(f"HIGH: {data.loc['high']}, LOW: {data.loc['low']}")
        # ustawienie zmienncyh pomocniczych
        high_border, is_top_change = top_values(trend, data.loc['high'])
        low_border, is_low_change = low_values(trend, data.loc['low'])
        # dodanie do zmiennych sprawdzajacych wartosci ( 1 - byla zmiana, 0 - nie bylo zmiany )
        temp_iter_low += is_low_change
        temp_iter_high += is_top_change
        if is_low_change and is_top_change:
            # rzadki przypadek - ustawienie obu nowych granic i wyzerowanie obu zmiennych sprzawdzajacych
            trend.high_border = high_border
            trend.low_border = low_border
            temp_high_border = high_border
            temp_low_border = low_border
            temp_iter_low = 0
            temp_iter_high = 0
            trend.trend = 0  # brak zmian trendu?
        elif is_low_change and not is_top_change:
            # zmiana dolnej granicy i sprawdzenie czy nie trzeba zmienic gornej
            if temp_iter_low >= 2:
                """ 
                    jesli zmienna pomocnicza >= 2 to zerujemy ja i zmieniamy obie granice 
                    dolna z aktualnej wartosci a gorna z top swieczki dawnej dolnej granicy xD
                """
                trend.low_border = low_border
                trend.high_border = temp_high_border
                temp_high_border = data.loc['high']
                temp_iter_high = 0
                temp_iter_low = 0
            elif temp_iter_low < 2:
                # podmiana tylko trend.low_border
                trend.low_border = low_border
                temp_high_border = data.loc['high']
            trend.trend = -1  # trend spadajacy?
        elif not is_low_change and is_top_change:
            # zmiana gornej granicy i sprawdzenie czy nie trzeba zmienic dolnej
            if temp_iter_high >= 2:
                """ 
                    jesli zmienna pomocnicza >= 2 to zerujemy ja i zmieniamy obie granice 
                    gorna z aktualnej wartosci a dolna z low swieczki dawnej dolnej granicy xD
                """
                trend.high_border = high_border
                trend.low_border = temp_low_border
                temp_low_border = data.loc['low']
                temp_iter_high = 0
                temp_iter_low = 0
            elif temp_iter_high < 2:
                # podmiana tylko trend.top_bordera ------ ?
                trend.high_border = high_border
                temp_low_border = data.loc['low']
            trend.trend = 1  # trend rosnacy?
        else:  # brak zmian - nie zmieniamy temp_borderow - sa zmiany - ustawiamy  trend.bordery?
            trend.high_border = high_border
            trend.low_border = low_border

        print(f"POPRZEDNIE MAX = {temp_high_border}, POPRZEDNIE MIN = {temp_low_border}")
        print(f"MAX = {trend.high_border}, MIN = {trend.low_border}, aktualny trend = {trend.trend}", end="\n\n")

    return trend


def top_values(trend: TrendValue, value: float) -> tuple[float, bool]:
    """
    Helper function to quick set top values
    Returns:
        tuple of float - new top border, bool - is modified last top border
    """
    if trend.high_border is None:
        return value, False
    elif trend.high_border > value:
        return trend.high_border, False
    else:  # trend.high_border <= value
        return value, True


def low_values(trend: TrendValue, value: float) -> tuple[float, bool]:
    """
    Helper function to quick set low values
    Returns:
        tuple of float - new low border, bool - is modified last low border
    """
    if trend.low_border is None:
        return value, False
    elif trend.low_border < value:
        return trend.low_border, False
    else:  # trend.low_border >= value
        return value, True
