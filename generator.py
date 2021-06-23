import pandas as pd
import numpy as np 
import dask.dataframe as dd
import os
import dask
from tqdm import trange
import argparse
import sys
import time

@dask.delayed
def generateData(size: int):
    """
    This function generated syntetic transaction by client 
    Args:
    size int-like
    """
    cat = ("sport","alcohol","work","education","heatlh","travel")
    names = ("James Ford","Eric Bachman","Jack Shepard","Kate Ostin")
    date = pd.date_range(start="2001-01-01", end="2002-01-01", freq='D')
    df = pd.DataFrame({
        "client":np.random.choice(names,size),
        "category": np.random.choice(cat,size),
        "timestamp":np.random.choice(date,size),
        "amount": np.random.randint(low=10,high=255,size = size,dtype=np.uint8)
    })
    return df

def generateBatch(size):
    batch = dd.from_delayed(generateData(size=size))
    return batch

def main(args):
    os.chdir(args.path)
    header = True
    for _ in trange(args.size):
        tempdf = generateBatch()
        tempdf.compute().to_csv(args.filename+".csv", mode="a", header=header, index=False)
        header = False

def argsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--size",default=1, type=int)
    parser.add_argument("-p","--path",default=os.getcwd(), type=str)
    parser.add_argument("-f","--filename",default="temp",type=str)
    parser.add_argument("-bs","--batchsize",default=1_000_000, type=int)
    return parser

if __name__=="__main__":
    parser = argsParser()
    args = parser.parse_args(sys.argv[1:])
    print(f"memory usage: {generateBatch(args.batchsize).compute().memory_usage(index=True,deep=True).sum()/1024/1024}")
    # start = time.time()
    # main(args)
    # end = time.time() - start
    # print("finished.")
    # print(f"processor time: {end}")