# import matplotlib.pyplot as plt
# from sklearn.preprocessing import StandardScaler
# import seaborn as sns
# import numpy as np
# from IPython.display import clear_output

def plot_scatter(df,columna):
    '''Devuelve un scatter plot de las columnas de df'''
    import matplotlib.pyplot as plt
    columnas = df.select_dtypes(exclude=['object']).columns
    for i in columnas:
        plt.scatter(df[i],df[columna])
        plt.xlabel(i)
        plt.ylabel(columna)
        plt.show()

def standard_scale(df):
    '''Devuelve un dataframe con las columnas escaladas'''
    from sklearn.preprocessing import StandardScaler
    import pandas as pd
    scaler = StandardScaler()
    string = df.select_dtypes(include=['object']).columns #solo vamos a escalar las columnas que no son string
    df_no_string = df.drop(string,axis=1)
    df_no_string = scaler.fit_transform(df_no_string)
    df_no_string = pd.DataFrame(df_no_string,columns=df.drop(string,axis=1).columns)
    df_escaled = df.copy()
    df_escaled[df_no_string.columns] = df_no_string
    return df_escaled

def boxplot(df):
    '''Devuelve un boxplot de df'''
    import seaborn as sns
    df_escaled = standard_scale(df)
    sns.boxplot(data=df_escaled,orient='h')

def rango_outliers(df):
    '''Devuelve el rango de outliers de df, definidas por min y max'''
    df_escaled = standard_scale(df)
    Q1 = df_escaled.quantile(0.25)
    Q3 = df_escaled.quantile(0.75)
    IQR = Q3 - Q1
    min = Q1 - 1.5*IQR
    max = Q3 + 1.5*IQR
    return min,max

def outliers(df):
    '''Devuelve un dataframe con los outliers de df, y una columna llamada outliers con las columnas que son outliers'''
    df_escaled = standard_scale(df)
    min,max = rango_outliers(df)
    columnas_no_string = df.select_dtypes(exclude=['object']).columns
    premisa = (df_escaled[columnas_no_string] < min) | (df_escaled[columnas_no_string] > max)
    indexes = df_escaled[premisa].dropna(axis=0,how='all').index
    df_outliers_bool = df_escaled[premisa].dropna(axis=0,how='all').isna()
    df_outliers = df.loc[indexes]
    columnas = df_outliers.columns
    dict = {i:[j for j in columnas if df_outliers_bool.loc[i][j] == False] for i in indexes}
    df_outliers['outliers'] = dict.values()
    return df_outliers

def ver_Nan(df,columns):
    for column in columns:
        text = f'NaN? - {column.upper()} '
        
        isNa = df[column].isna().any()
        print(f'{text.ljust(50)} {isNa}')

def nearest_square(number):
    '''
    Get nearest whole sqaure from a given number.
    '''
    import numpy as np
    return np.power(np.round(np.sqrt(number)), 2)


def display_histograms(df, exclude=None):
    '''
    Crea histogramas de todas las columnas numéricas (float o int) de un
    dataset.
    '''
    from IPython.display import clear_output
    # nearest_square = lambda number: np.power(np.round(np.sqrt(number)), 2)

    int_columns = df.select_dtypes(include=(int, float))
    sq = int(nearest_square(len(int_columns.columns)))

    int_columns.hist(figsize=(20, 20), layout=(sq, sq))

    clear_output()


def display_barplots(df, exclude=False):
    '''
    Crea bar plots de todas las columnas categóricas de un dataframe.
    '''
    if exclude:
        df = df.drop(columns=exclude)
    cat_columns = df.select_dtypes(include=object)
    for column in cat_columns:
        column.plot.bar
  

