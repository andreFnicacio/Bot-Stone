# %%
import json
from collections import Counter
from redis import Redis
import pandas as pd

task = "RFA"
conn = Redis('redis.mysofie.com', 5071, decode_responses=True)
keys = conn.keys(f'SOFIE:MICROTASK:IN_PERSON#')
x = conn.georadius('SOFIE:MICROTASK:IN_PERSON#', 1, 1, 99999999999999, 'km')
# %%
tasks = list()
i = 0
pipe = conn.pipeline()
for item in x:
    i += 1
    data = json.loads(item)
    taskid = data['task_id']
    a = pipe.hgetall(f'SOFIE:MICROTASK:{taskid}:DATA#')
res = pipe.execute()
# %%
tasks = list()
for i in res:
    tasks.append(i)

res = tasks
# %%
itens = pd.DataFrame(res)


itens.to_excel('redis.xlsx', index=False)

cities_ccc = list()
cities_rfa = list()
cities_rfa2 = list()
cities_rfa3 = list()
for data in res:
    task_name = data.get('task_name','')
    if task_name == 'CCC':
        cities_ccc.append(data.get('city', 'vip'))
    elif task_name == 'RFA':
        cities_rfa.append(data.get('city', 'vip'))
    elif task_name == 'RFA-2':
        cities_rfa2.append(data.get('city', 'vip'))
    elif task_name == 'RFA-3':
        cities_rfa3.append(data.get('city', 'vip'))


count = {it: freq for it, freq in Counter(cities_ccc).items()}
count_ccc = {k: v for k, v in sorted(
    count.items(), key=lambda item: item[1], reverse=True)}

count = {it: freq for it, freq in Counter(cities_rfa).items()}
count_rfa = {k: v for k, v in sorted(
    count.items(), key=lambda item: item[1], reverse=True)}

count = {it: freq for it, freq in Counter(cities_rfa2).items()}
count_rfa2 = {k: v for k, v in sorted(
    count.items(), key=lambda item: item[1], reverse=True)}

count = {it: freq for it, freq in Counter(cities_rfa3).items()}
count_rfa3 = {k: v for k, v in sorted(
    count.items(), key=lambda item: item[1], reverse=True)}


print("Gerando cidades CCC")
cidades_ccc = pd.DataFrame.from_dict(count_ccc, orient='index').rename(
    columns={0: 'Quantidade de Tarefas CCC'})

print("Gerando cidades RFA")
cidades_rfa = pd.DataFrame.from_dict(count_rfa, orient='index').rename(
    columns={0: 'Quantidade de Tarefas RFA'})

print("Gerando cidades RFA-2")
cidades_rfa2 = pd.DataFrame.from_dict(count_rfa2, orient='index').rename(
    columns={0: 'Quantidade de Tarefas RFA-2'})

print("Gerando cidades RFA-3")
cidades_rfa3 = pd.DataFrame.from_dict(count_rfa3, orient='index').rename(
    columns={0: 'Quantidade de Tarefas RFA-3'})


with pd.ExcelWriter('./reports_sofie/tarefas_por_cidade.xlsx') as writer:  
    cidades_ccc.to_excel(writer,sheet_name="CCC")
    cidades_rfa.to_excel(writer,sheet_name="RFA")
    cidades_rfa2.to_excel(writer,sheet_name="RFA-2")
    cidades_rfa3.to_excel(writer,sheet_name="RFA-3")




# %%