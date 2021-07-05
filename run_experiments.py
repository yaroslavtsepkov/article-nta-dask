from lib_generate_transactions import generate_files, generate_files2
from itertools import product
from datetime import datetime
from os import stat
import pandas as pd
import dask.dataframe as dd
import os

# load/import classes
# python -m pip install "dask[distributed]"
from dask.distributed import Client



def process_pandas(fname):
    '''reads file into pandas dataframe: fname (str) -> '''
    start = datetime.now()

    df = pd.read_csv(fname, encoding='windows-1251')
    result = df.groupby('Category')['Amount'].sum()

    stop = datetime.now()
    duration = (stop - start).total_seconds()
    return duration

def calc_sum_in_group(x):
    return x.groupby('Category')['Amount'].sum()
    

def process_dask(fname):
    '''docstring'''
    start = datetime.now()    

    ddf = dd.read_csv(fname, encoding='windows-1251')

    sent = client.submit(calc_sum_in_group, ddf)
    result = sent.result().compute()
    #result = df.groupby('Category')['Amount'].sum().compute()

    stop = datetime.now()
    duration = (stop - start).total_seconds()
    return duration

def fnames_from_file(fname_csv_list, path):

    with open(fname_csv_list, 'r') as f:
        fnames = f.readlines()

    fnames = [os.path.join(path, fname.strip()) for fname in fnames]

    return fnames

    

n_rep = 5
n_rows_list = [20000, 40000, 100000, 200000, 400000, 1000000, 2000000, 4000000, 10000000, 20000000]
#, 40000000, 80000000]
#tools = ['pandas', 'dask']
tools = ['dask']
experiments = range(1, n_rep + 1)

#
#path = 'D:/dask/csv'
path = 'csv'
#fnames = generate_files(0, n_rows_list, path)
fnames = fnames_from_file('files.txt', path)

print(fnames)

#a = 1 / 0



fname_exp_data = 'notebook-ssd-all_sizes-dask-memory_limit.csv'

with open(fname_exp_data, 'w') as log:
    line = '{},{},{},{},{},{}\n'.format('i', 'n_rows', 'mbytes', 'tool', 'run', 'duration')
    log.write(line)

for i, experiment in enumerate(product(fnames, tools, experiments), 1):
    fname, tool, run = experiment

    #
    mbytes = round(stat(fname).st_size / 1024 / 1024, 3)
    duration = -1
    n_rows = int(fname.split('.')[0].split('_')[1])

    # pandas
    if tool == 'pandas':
        duration = process_pandas(fname)
    else:
        client = Client(n_workers=2,
                        threads_per_worker=1,
                        memory_limit='4GB',
                        processes=False)
        duration = process_dask(fname)
        client.close()

    # result
    result = '{} {} {} {} {} {}'.format(i, n_rows, mbytes, tool, run, duration)
    print(result)
    
    with open(fname_exp_data, 'a') as log:
        line = '{},{},{},{},{},{}\n'.format(i, n_rows, mbytes, tool, run, duration)
        log.write(line)




