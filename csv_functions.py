import pandas as pd
COLUMN_NAMES_LIST: list[str] = ['open', 'close', 'high', 'low', 'RSI', 'time']


def create_file(file: str) -> None:
    """ Create csv file if not exists """
    data_to_create: pd.DataFrame = pd.DataFrame(columns=COLUMN_NAMES_LIST)
    data_to_create.to_csv(file, index=False, header=True, sep=";")


def to_file(file: str, current_data: pd.DataFrame, data_to_add: pd.DataFrame) -> None:
    """ Write dataframe to csv file """
    new_data: pd.DataFrame = pd.concat([current_data, data_to_add], axis=0, ignore_index=True)
    new_data.to_csv(file, index=False, header=True, sep=";")


def from_file(file: str) -> pd.DataFrame:
    """ Read from csv file & return DataFrame"""
    data_from_file: pd.DataFrame = pd.read_csv(file, sep=";")
    return data_from_file
