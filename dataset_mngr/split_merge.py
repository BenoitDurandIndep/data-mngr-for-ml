import numpy as np
import pandas as pd
import random as rd


def add_split_dataset(df_in: pd.DataFrame, split_timeframe: str = "Q", split_pattern: tuple = (60, 20, 20), clean_na: bool = True, fix_end_val: bool = True) -> pd.DataFrame:
    """Add a column split_value in a time index dataframe,
    used to split a dataframe into train 0, validation 1, confirmation 2

    Args:
        df_in (pd.DataFrame): input dataframe, must be timestamp index
        split_timeframe (str, optional): timeframe used to split (H, D, M, Q, Y). Defaults to "Q".
        split_pattern (tuple, optional): split %, must be equal to 100. Defaults to (60, 20, 20).
        clean_na (bool, optional): if a dropna is done. Defaults to True.
        fix_end_val (bool, optional): if confirmation must be at the end of dataframe. Defaults to True.

    Returns:
        pd.DataFrame: Same dataframe with a column splut_value at the end
    """

    df_split = df_in.copy()

    if clean_na:
        df_split.dropna(inplace=True)

    df_split['split_group_ut'] = pd.PeriodIndex(
        df_split.index, freq=split_timeframe)
    df_split['split_group_num'] = df_split.groupby(
        by=['split_group_ut']).ngroup()
    nb_groups = df_split['split_group_num'].max()+1
    nb_conf = (round(nb_groups*split_pattern[2]/100, 0)).astype(int)
    nb_val = (round(nb_groups*split_pattern[1]/100, 0)).astype(int)

    if (fix_end_val):
        df_split['split_value'] = np.where(
            df_split['split_group_num'] < nb_groups-nb_conf, 0, 2)
        df_split['split_value'] = np.where(df_split['split_group_num'].isin(
            rd.sample(range(0, nb_groups-nb_conf-1), nb_val)), 1, df_split['split_value'])
    else:
        df_split['split_value'] = np.where(df_split['split_group_num'].isin(
            rd.sample(range(0, nb_groups-1), nb_conf)), 2, 0)
        df_split['split_value'] = np.where(df_split['split_group_num'].isin(rd.choices(
            (df_split['split_group_num'][df_split['split_value'] == 0]).unique(), k=nb_val)), 1, df_split['split_value'])

    df_split.drop(axis=1, columns=[
                  'split_group_ut', 'split_group_num'], inplace=True)
    return df_split


def split_df_by_split_value(df_in: pd.DataFrame, column_name: str = "split_value", drop_column:bool=True) -> list:
    """ split a df in 3 df (train, validation, confirmation) according a "split column"
    The values must be 0=train , 1=validation, 2=confirmation

    Args:
        df_in (pd.DataFrame): dataframe to split
        column_name (str, optional): name of the column containing the value used to split. Defaults to "split_value".
        drop_column (bool, optional): if it drops the cloumn column_name after split. Defaults to True.

    Raises:
        ValueError: if clumn_name is not found

    Returns:
        list: list of 3 dataframes [train, validation, confirmation]
    """
    df_tmp=df_in.copy()
    nb_split=(df_tmp[column_name].max())+1
    df_splitted = ["empty",]*nb_split

    if column_name in df_in.columns:
        for i in range(0, nb_split):
            df_splitted[i] = df_in.loc[df_in[column_name] == i].copy(deep=True)
            if drop_column:
                df_splitted[i].drop(axis=1,columns=[column_name],inplace=True)
    else:
        raise ValueError(f"column {column_name} not in dataframe !")

    return df_splitted


if __name__ == "__main__":
    nb_groups = 4
    nb_val = 10
    ut = "D"

    open, close = rd.sample(range(10, 20), k=nb_val), rd.sample(
        range(10, 20), k=nb_val)

    idx = pd.date_range("2022-01-01", periods=nb_val, freq=ut)
    frame = {'DATE': idx, 'OPEN': open, 'CLOSE': close}

    df = pd.DataFrame(frame)
    df.set_index('DATE', inplace=True)

    df = add_split_dataset(df_in=df, split_timeframe="D", split_pattern=(
        60, 20, 20), clean_na=True, fix_end_val=True)
    df_train,df_val,df_conf=split_df_by_split_value(df)
    print(df_train)
    print("**********")
    print(df_val)
    print("**********")
    print(df_conf)
