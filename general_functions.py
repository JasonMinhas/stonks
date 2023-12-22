import pandas as pd
import datetime as dt
import os
import cProfile
import pstats
import io


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


def clean_numeric(currency_series):
    currency_series = currency_series.astype(str)
    for char in [' ', '$', ',', '-']:
        currency_series = currency_series.str.replace(char, '', regex=True)

    return currency_series


def strip_df(df):
    # get list of column headers that are objects
    object_cols = df.select_dtypes(include=object).columns
    # strip all string series
    df[object_cols] = df[object_cols].apply(lambda ser: ser.str.strip())

    return df


def clean_headers(df):
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
    return df


def get_files_in_folder(folder_path, extensions_to_keep='all', include_full_path=False):
    """
    :param folder_path: folder to get files from
    :param extensions_to_keep: list or 'all' if all files should be returned
    :param return_file_paths:  full file paths
    :return:
    """

    file_list = []

    if extensions_to_keep == 'all':
        for f in os.listdir(folder_path):
            file_path = os.path.join(folder_path, f)
            if (os.path.isfile(file_path)) and not (f.startswith('~$')):
                file_list.append(f)
    else:
        extensions_to_keep = tuple([ext.lower() for ext in extensions_to_keep])
        for f in os.listdir(folder_path):
            file_path = f'{folder_path}/{f}'
            file_ext = file_path.split('.')[-1].lower()
            if (os.path.isfile(file_path)) and (file_ext in extensions_to_keep) and not (f.startswith('~$')):
                file_list.append(f)

    if include_full_path is True:
        path_list = [f'{folder_path}/{file}' for file in file_list]
        return path_list
    return file_list


def save_df(df, save_path, df_date_header=None, overwrite=False, save_as_ext='.xlsx'):
    if df_date_header is not None:
        df[df_date_header] = pd.to_datetime(df[df_date_header])
        min_date = df[df_date_header].min().strftime('%m.%d.%Y')
        max_date = df[df_date_header].max().strftime('%m.%d.%Y')
        save_path = save_path + '_' + min_date + '-' + max_date

    directory = os.path.dirname(save_path)
    while not os.path.exists(directory):
        save_path = input(f'"{directory}" path does not exist. Please enter a new one: '
                          f'')
        directory = os.path.dirname(save_path)
    if not overwrite:
        i, save_path_alt = 0, save_path
        while os.path.isfile(f'{save_path_alt}{save_as_ext}'):
            version_num = 'V' + str(i + 2)
            save_path_alt = save_path + '_' + version_num
            i += 1
        if save_as_ext == '.xlsx':
            df.to_excel(f'{save_path_alt}.xlsx', index=False)
        elif save_as_ext == '.csv':
            df.to_csv(path_or_buf=f'{save_path_alt}.csv', index=False)
        else:
            raise ValueError(f'The argument for save_as_ext parameter, {save_as_ext}, is not a ".csv" or ".xlsx" extension')
    elif save_as_ext == '.xlsx':
        df.to_excel(f'{save_path}.xlsx', index=False)
    elif save_as_ext == '.csv':
        df.to_csv(path_or_buf=f'{save_path}.csv', index=False)


def clean_days_of_week(series):
    """
    Clean day of week naming convention in buysheet to match what CORE outputs
    :param series:
    :return:
    """
    # variation in ways analysts enter day of week
    day_of_week_dict = {'0': ['M', 'Mo'],
                        '2': ['W', 'We'],
                        '3': ['Th'],
                        '4': ['F', 'Fr'],
                        '5': ['Sa'],
                        '6': ['Su'],
                        '1': ['T', 'Tu']}

    # replace input day of week variations with integers
    for key in day_of_week_dict:
        for value in day_of_week_dict[key]:
            series = series.str.replace(value, key, regex=False)

    # replace each key with value in series
    for key in day_of_week_dict:
        series = series.str.replace(key, day_of_week_dict[key][0], regex=False)

    return series


def get_list_of_state_abbr():
    state_abbr_list = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
        'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
        'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC']

    return state_abbr_list


def clean_phone_number(phone_number_ser):
    phone_number_ser = phone_number_ser.astype(str)
    for char in [' ', '(', ')', '-']:
        phone_number_ser = phone_number_ser.str.replace(char, '', regex=True)

    return phone_number_ser


def get_mon_date(cur_date, with_period=False):
    days_from_monday = cur_date.weekday()
    mon_date = cur_date - dt.timedelta(days_from_monday)

    if with_period:
        mon_date = str(mon_date).replace('-', '.')

    return mon_date


def get_sun_date(cur_date, with_period=False):
    days_from_sunday = 6 - cur_date.weekday()
    sun_date = cur_date + dt.timedelta(days_from_sunday)

    if with_period:
        sun_date = str(sun_date).replace('-', '.')

    return sun_date

