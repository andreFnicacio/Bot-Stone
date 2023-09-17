# %%

import time
import threading
from datetime import datetime
import pandas as pd
import boto3

def query_execution(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.session.Session(profile_name='andre.nicacio', region_name='sa-east-1').resource('dynamodb')

    table = dynamodb.Table('table_micro_task_execution')

    scan_kwargs = dict(
        FilterExpression=' #result <> :d',
        ExpressionAttributeNames={
            '#result': 'result',
        },
        ExpressionAttributeValues={
            ':d': 'CANCEL',

        },
    )
    base = []
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)

        for item in (response.get('Items')):
            try:
                dicionario = {}
                dicionario['_id'] = item['task_id']
                dicionario['reprovado'] = item['execution_id']
                dicionario['company'] = item['company']
                dicionario['tarefa'] = item['task_info']['name']
                dicionario['data da tarefa'] = item['when']['finish']
                dicionario['sofier'] = item['who']
                dicionario['status'] = item.get('result')
                if item.get('audit'):
                    dicionario['Auditor'] = item['audit'].get('who')
                    dicionario['data da auditoria'] = item['audit']['when']
                    dicionario['aprovada'] = item['audit']['approved']

                base.append(dicionario)
            except:
                print(item["task_id"])
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    return base


valores_in_execution = query_execution()
# %%

itens = pd.DataFrame(valores_in_execution)
valores = list()

# for item in itens['data da tarefa']:
#     horario = (item.split("T"))[1]
#     valores.append(f'{item[8:10]}-{item[5:8]}{item[0:4]}')
#
# df1 = pd.DataFrame(valores)
# # itens['data da tarefa'].update(valores)


itens.to_excel('./reports_sofie/auditorias_thaylla.xlsx', index=False)