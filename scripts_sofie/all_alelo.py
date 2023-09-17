
import pandas as pd
import boto3


def query_company(company):
    dynamodb = None
    if not dynamodb:
        dynamodb = boto3.session.Session(profile_name='andre.nicacio', region_name='sa-east-1').resource('dynamodb')

    table = dynamodb.Table('table_micro_task_in_person')

    scan_kwargs = dict(
        FilterExpression='#company = :c AND #task.#name = :tsk_name',
        ExpressionAttributeNames={'#company': 'company', '#task': 'task', '#name': 'name'},
        ExpressionAttributeValues={':c': company, ':tsk_name': 'CCC'}
    )

    saidas = list()
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        for item in (response.get('Items')):
            saidas.append((item))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    return saidas
# %%
alelo = query_company("alelo")
# %%
item_alelo = []
for item in alelo:
    try:
        dicionario = dict()
        dicionario['task_id'] = item['task_id']
        dicionario['lote'] = item['status'].get('lot_reference')
        dicionario['data do lote'] = item['status']['when']
        dicionario['status'] = item['status']['status']
        dicionario['state'] = item['status']['state']
        dicionario['last movement'] = item.get('last_movement')
        dicionario['Cidade'] = item['original']['CIDADE']
        dicionario['UF'] = item['original']['ESTADO']
        dicionario['nome'] = item['original']['NOME_FANTASIA']
        dicionario['CNPJ'] = item['original']['CNPJ']
        dicionario['Endereço'] = item['address']['formatted_address']
        dicionario['reward'] = item['task'].get('reward', 0)
        if item['sofie_place'].get('location'):
            dicionario['lat'] = item['sofie_place']['location']['lat']
            dicionario['lng'] = item['sofie_place']['location']['lng']

        item_alelo.append(dicionario)
    except Exception as e:
        print(item['task_id'])
        print(e)

excel = pd.DataFrame(item_alelo)
excel.to_excel('./reports_sofie/all_alelo.xlsx', index=False)
print('fim alelo')