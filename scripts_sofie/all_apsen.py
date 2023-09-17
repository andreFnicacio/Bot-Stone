# %%
import pandas as pd
import boto3


def query_company(company):
    dynamodb = None
    if not dynamodb:
        dynamodb = boto3.session.Session(profile_name='andre.nicacio', region_name='sa-east-1').resource('dynamodb')

    table = dynamodb.Table('table_micro_task_in_person')

    scan_kwargs = dict(
        FilterExpression='#company = :c',
        ExpressionAttributeNames={'#company': 'company'},
        ExpressionAttributeValues={':c': company, }
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
apsen = query_company("apsen")

itens_apsen = []
for item in apsen:
    dicionario = dict()
    dicionario['task_id'] = item['task_id']
    dicionario['tarefa'] = item['task']['name']
    dicionario['lote'] = item['status']['lot_reference']
    dicionario['data do lote'] = item['status']['when']
    dicionario['status'] = item['status']['status']
    dicionario['state'] = item['status']['state']
    dicionario['visita'] = item['task']['etapa']
    dicionario['onda'] = item['task']['onda']
    dicionario['last movement'] = item.get('last_movement')
    dicionario['bandeira'] = item['original']['BANDEIRA']
    # dicionario['Grupo'] = item['original']['GRUPO']
    # dicionario['subcanal'] = item['original']['SUBCANAL']
    dicionario['Cidade'] = item['original']['CUP_CIDADE']
    dicionario['UF'] = item['original']['CUP_UF']
    dicionario['nome'] = item['original']['DESCRICAO_CUP']
    dicionario['CNPJ'] = item['original'].get('CNPJ')
    dicionario['Endereço'] = item['address']['formatted_address']
    if item['sofie_place'].get('location'):
        dicionario['lat'] = item['sofie_place']['location']['lat']
        dicionario['lng'] = item['sofie_place']['location']['lng']

    itens_apsen.append(dicionario)

print(len(itens_apsen))
excel = pd.DataFrame(itens_apsen)
# excel.to_excel('pontos_apsen.xlsx', index=False)
excel.to_excel('./reports_sofie/all_apsen.xlsx', index=False)
print('fim apsen')