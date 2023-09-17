# %%
# listagem de tasks finalizadas
from operator import concat
from ssl import VerifyFlags
import json
from numpy import column_stack
import pandas as pd
from collections import Counter
contacts = input()

with open('./scripts_sofie/contagem_acessos.json', 'r') as openfile:
    json_object = json.load(openfile)

array_contacts = list(contacts.split(","))

count = { it: freq for it, freq in Counter(array_contacts).items() }

c = {k: v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True)}


for key in c.keys():
    if json_object.get(key,key) in c:
        new_value = c[key] + json_object.get(key,0)
        json_object[key] = new_value
    else:
        json_object[key] = c[key]

list_users = "*NÚMERO DE VISITAS (CELULAR):*@"

for key in json_object.keys():
    list_users += f'{key} : {json_object[key]}@'

print(list_users)

with open("./scripts_sofie/contagem_acessos.json", "w") as outfile:
    json.dump(json_object, outfile)

