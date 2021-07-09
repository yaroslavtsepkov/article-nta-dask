from typing import List
import pandas as pd
from dask import distributed
from dask import dataframe as dd
from tqdm import tqdm
from time import time
from glob import glob
import os
import csv
import webbrowser

def calc_sum_in_group(df):
    return df.groupby('Category')['Amount'].sum()

def daskProcess(filepath: str, client):
    temp = dd.read_csv(filepath, encoding="windows-1251")
    sent = client.submit(calc_sum_in_group, temp)
    result = sent.result().compute()

def pandasProcess(filepath: str):
    temp = pd.read_csv(filepath, encoding="windows-1251")
    calc_sum_in_group(temp)

def runExps(files:List[str]):
    texp = range(10)
    header = True
    files = tqdm(files,ascii=True, total=len(texp)*len(files))
    columns=["timestamp","experiment","tools","filesize(bytes)"]
    # with distributed.Client() as client:
    #     webbrowser.open(client.dashboard_link)
    for file in files:
        for exp in texp:
            filesize = os.path.getsize(file)
            files.set_description("exp: {}, filesize: {}".format(exp, filesize))
            files.refresh()
            
            # try:
            #     tic = time()
            #     daskProcess(file, client)
            #     dtoc = time()-tic
            # except:
            #     dtoc = None                    
            try:
                tic = time()
                pandasProcess(file)
                pdtoc = time()-tic
                
            except:
                pdtoc = None
            finally:
                files.update(1)
                with open("report.csv", mode="a") as f:
                    writer = csv.writer(f)
                    if header:
                        writer.writerow(columns)
                        header = False
                        # writer.writerow([dtoc, exp, "dask", filesize])
                        writer.writerow([pdtoc, exp, "pandas", filesize])
                    else:
                        # writer.writerow([dtoc, exp, "dask", filesize])
                        writer.writerow([pdtoc, exp, "pandas", filesize])

def main():
    os.chdir("data")
    files = glob("*.csv")
    files.sort()
    runExps(files)

if __name__ == "__main__":
    tic = time()
    main()
    toc = time()-tic
    print("done. Precces time: {}".format(toc))