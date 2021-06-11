# Генератор транзакций

import random
from datetime import datetime, timedelta

def generate_transaction(min_date, max_date, avg_interval, customers, min_amount, max_amount, categories):
    '''generate single transaction record (str)'''

    timestamp = min_date
    i = 0

    while True:
        i += 1
        interval = round(random.triangular(low=0.001, high=0.001+avg_interval, mode=avg_interval), 3)        
        timestamp += timedelta(seconds=interval)
        name = random.choice(customers)
        amount = min_amount + round((max_amount - min_amount) * random.random() * 100) / 100
        category = random.choice(categories)
        
        t_str = timestamp.strftime('%Y-%m-%d %H-%M-%S.%f')
        row = '{},{},{},{:.2f},{}\n'.format(i, t_str, name, amount, category)

        yield row

def generate_files(seed=0, n_rows_list=[1000]):
    '''generates file with transactions'''
    
    min_date, max_date = datetime(2011, 1, 1), datetime(2021, 1, 1)
    min_amount, max_amount = 1.00, 100.00
    customers = ['Маша', 'Вася', 'Коля', 'Миша', 'Таня']
    categories = ['Продукты', 'Одежда', 'Коммунальные услуги', 'Путешествия', 'Транспорт', 'Развлечения', 'Ремонт']

    spread = (max_date - min_date).total_seconds()

    fnames = []

    for n_rows in n_rows_list:

        fname = 'transactions_{}.csv'.format(n_rows)

        random.seed(seed)
        avg_interval = spread / n_rows

        gen = generate_transaction(min_date, max_date, avg_interval, customers, min_amount, max_amount, categories)
        with open(fname, 'w') as f:
            f.write('Id,Timestamp,Customer,Amount,Category\n')
            for _ in range(n_rows):
                row = next(gen)
                f.write(row)

        fnames.append(fname)

    return fnames

def generate_files2(seed=0, n_rows_list=[1000]):
    '''generates file with transactions'''
    
    min_date, max_date = datetime(2011, 1, 1), datetime(2021, 1, 1)
    min_amount, max_amount = 1.00, 100.00
    customers = ['Маша', 'Вася', 'Коля', 'Миша', 'Таня']
    categories = ['Продукты', 'Одежда', 'Коммунальные услуги', 'Путешествия', 'Транспорт', 'Развлечения', 'Ремонт']

    spread = (max_date - min_date).total_seconds()

    fnames = []

    for n_rows in n_rows_list:

        fname = 'transactions_{}.csv'.format(n_rows)

        random.seed(seed)
        avg_interval = spread / n_rows

        
        chunk_size = 10000
        n_chunks = n_rows // chunk_size

        gen = generate_transaction(min_date, max_date, avg_interval, customers, min_amount, max_amount, categories)

        with open(fname, 'w') as f:
            f.write('Id,Timestamp,Customer,Amount,Category\n')

        for _ in range(n_chunks):
            chunk = []
            for _ in range(chunk_size):
                row = next(gen)
                chunk.append(row)
            with open(fname, 'a') as f:
                f.writelines(chunk)

        fnames.append(fname)

    return fnames
