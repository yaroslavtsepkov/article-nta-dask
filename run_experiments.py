from lib_generate_transactions import generate_files, generate_files2
from itertools import product
from datetime import datetime
from os import stat
import pandas as pd
import dask.dataframe as dd



def process_pandas(fname):
    '''reads file into pandas dataframe: fname (str) -> '''
    start = datetime.now()

    df = pd.read_csv(fname, encoding='windows-1251')
    #result = df.shape[0]
    result = df.groupby('Category')['Amount'].sum()

    stop = datetime.now()
    duration = (stop - start).total_seconds()
    return duration

def process_dask(fname):
    '''docstring'''
    start = datetime.now()    

    df = dd.read_csv(fname, encoding='windows-1251')
    #result = df.shape[0].compute()
    result = df.groupby('Category')['Amount'].sum().compute()

    stop = datetime.now()
    duration = (stop - start).total_seconds()
    return duration    
    

n_rep = 5
n_rows_list = [100000, 1000000, 10000000, 100000000, 1000000000]
#n_rows_list = [1000, 3000, 10000]
approaches = ['pandas', 'dask']
experiments = range(1, n_rep + 1)

#
fnames = generate_files2(0, n_rows_list)

a = 1 / 0

for i, experiment in enumerate(product(fnames, approaches, experiments), 1):
    fname, approach, run = experiment

    #
    mbytes = round(stat(fname).st_size / 1024 / 1024, 3)
    duration = -1
    n_rows = int(fname.split('.')[0].split('_')[1])

    # pandas
    if approach == 'pandas':
        duration = process_pandas(fname)
    else:
        duration = process_dask(fname)

    # result
    result = '{} {} {} {} {} {}'.format(i, n_rows, mbytes, approach, run, duration)
    print(result)
    


