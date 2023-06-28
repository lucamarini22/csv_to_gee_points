import csv
import numpy as np
import pandas as pd


def csv_to_gee_points(
        csv_file: str,
        out_file: str,
        lat_col_name: str,
        long_col_name: str,
        num_rows_before_header: int = 0,
        points_col_name: str = None,
        sep: str = ',',
) -> None:
    """Generates a text file with each row corresponding to the definition in 
    Javascript of a point that can be imported in the Code Editor of Google 
    Earth Engine.   

    Args:
        csv_file (str): path of the csv file.
        out_file (str): path of the output text file containing the javascript
          definition of geometry points.
        lat_col_name (str): name of the latitude column in the csv file.
        long_col_name (str): name of the longitude column in the csv file.
        num_rows_before_header (int, optional): number of rows before the 
          header in the csv file. Defaults to 0.
        points_col_name (str, optional): name of the column containing point 
          names in the csv file. If points_col_name is None then points will 
          be defined as point_n, with n an increasing number starting from 0. 
          Defaults to None.
        sep: separator of the csv file. Defaults to ','.
    """
    df = pd.read_csv(csv_file, sep=sep)
    df.columns = df.iloc[num_rows_before_header - 1]
    # Drops rows before header
    df = df.iloc[num_rows_before_header:]
    
    df[lat_col_name] = _replace_comma_with_dot_in_col(df, lat_col_name)
    df[long_col_name] = _replace_comma_with_dot_in_col(df, long_col_name)
    
    points_def_col_name = 'points_def'
    
    if points_col_name is not None:   
        df[points_def_col_name] = 'var ' \
            + df[points_col_name] \
                + _get_second_part_of_def(df, lat_col_name, long_col_name)
    else:
        df['index'] = [str(i) for i in np.arange(len(df))]
        df[points_def_col_name] = 'var point_' \
            + df['index'] \
                + _get_second_part_of_def(df, lat_col_name, long_col_name)

    df[points_def_col_name].to_csv(
        out_file, 
        index=False, 
        header=False, 
        doublequote=False,
        quoting=csv.QUOTE_NONE,
        escapechar='\\',
        sep = '\n'
    )


def _get_second_part_of_def(
    df: pd.DataFrame,
    lat_col_name: str,
    long_col_name: str,
) -> str:
    """Gets the second part of the definition in Javascript of a point that
    can be imported in the Code Editor of Google Earth Engine.  

    Args:
        df (pd.DataFrame): dataframe that contains latitude and longitude of 
          points.
        lat_col_name (str): name of the latitude column in the csv file.
        long_col_name (str): name of the longitude column in the csv file.

    Returns:
        str: second part of the definition of a point.
    """
    return ' = ee.Geometry.Point([' \
        + df[long_col_name] \
        + ',' \
        + df[lat_col_name] \
        + ']);'


def _replace_comma_with_dot_in_col(
    df: pd.DataFrame, 
    col_name: str
) -> pd.Series:
    """Replaces every comma with a dot in each element of the column col_name
    of dataframe df.

    Args:
        df (pd.DataFrame): dataframe containing column col_name.
        col_name (str): name of the column.

    Returns:
        pd.Series: column col_name with dots instead of commas in its elements.
    """
    return df[col_name].str.replace(',', '.')


if __name__ == "__main__":
    lat_col_name = 'Lat'
    long_col_name = 'Long'
    csv_file = './csv_file.csv'
    out_file = './out_file.txt'
    points_col_name = 'Points_Col_Name'
    num_rows_before_header = 2
    sep = ';'

    csv_to_gee_points(
        csv_file, 
        out_file, 
        lat_col_name, 
        long_col_name, 
        points_col_name=points_col_name,
        sep=sep,
        num_rows_before_header=num_rows_before_header
    )
