#
import boto3
from decimal import Decimal
from numpy import column_stack
import pandas as pd
from datetime import datetime, timedelta

session = boto3.session.Session(
    profile_name='andre.nicacio', region_name='sa-east-1')
dynamodb = session.resource('dynamodb')

columns = list()
response_flow = dict()

def formated_date_today(hoje):
    data_final = hoje + timedelta(days=2)   

    data_inicial_formated = hoje.strftime('%Y-%m-%dT00:00:%S.%f')   

    data_final_formated = data_final.strftime('%Y-%m-%dT23:59:%S.%f')  

    return data_inicial_formated, data_final_formated 

def formated_date_semana(hoje, wd):
    data_inicial = hoje - timedelta(days=wd)
    data_final = data_inicial + timedelta(days=6)   

    data_inicial_formated = data_inicial.strftime('%Y-%m-%dT00:00:%S.%f')

    data_final_formated = data_final.strftime('%Y-%m-%dT23:59:%S.%f')  

    return data_inicial_formated, data_final_formated 

def formated_date_mes(hoje, month):
    date = hoje   

    data_inicial_formated = date.strftime(f'%Y-{month}-01T00:00:%S.%f')   

    data_final_formated = date.strftime('%Y-%m-%dT23:59:%S.%f')  

    return data_inicial_formated, data_final_formated 
def buscar_tabela():
    value = 'Acompanhamento CCC - SEMANA'
    table = dynamodb.Table('table_micro_task_execution')
    params = None
    if value == "Acompanhamento CCC - GERAL" or value == "Visão GERAL":
        params = dict(
            FilterExpression='#task_info.#name = :task AND #result = :finish',
            ExpressionAttributeNames={"#task_info": "task_info", "#name": "name", "#result": "result"},
            ExpressionAttributeValues={
                ':task': 'CCC',
                ':finish': 'FINISH'
            }
        )
    elif value == "Acompanhamento CCC - HOJE" or value == "Visão de HOJE":
        hoje = datetime.today()
        date_initial, date_finish = formated_date_today(hoje)
        params = dict(
            FilterExpression='#task_info.#name = :task AND #result = :finish AND #when.#start BETWEEN :dtI AND :dtF',
            ExpressionAttributeNames={"#task_info": "task_info", "#name": "name", "#result": "result", "#when": "when", "#start": "start"},
            ExpressionAttributeValues={
                ':task': 'CCC',
                ':finish': 'FINISH',
                ':dtI': date_initial,
                ':dtF': date_finish
            }
        )        
    elif value == "Acompanhamento CCC - SEMANA" or value == "Visão da SEMANA":
        hoje = datetime.today()
        wd = hoje.weekday()
        date_initial, date_finish = formated_date_semana(hoje,wd)
        params = dict(
            FilterExpression='#task_info.#name = :task AND #result = :finish AND #when.#start BETWEEN :dtI AND :dtF',
            ExpressionAttributeNames={"#task_info": "task_info", "#name": "name", "#result": "result", "#when": "when", "#start": "start"},
            ExpressionAttributeValues={
                ':task': 'CCC',
                ':finish': 'FINISH',
                ':dtI': date_initial,
                ':dtF': date_finish
            }
        )       

    elif value == "Acompanhamento CCC - MÊS" or value == "Visão do MÊS":
        hoje = datetime.today()
        today = datetime.now()
        month = today.strftime("%m")
        date_initial, date_finish = formated_date_mes(hoje,month)
        params = dict(
            FilterExpression='#task_info.#name = :task AND #result = :finish AND #when.#start BETWEEN :dtI AND :dtF',
            ExpressionAttributeNames={"#task_info": "task_info", "#name": "name", "#result": "result", "#when": "when", "#start": "start"},
            ExpressionAttributeValues={
                ':task': 'CCC',
                ':finish': 'FINISH',
                ':dtI': date_initial,
                ':dtF': date_finish
            }
        )           
     

    tasks = list()
    finishedTask = list()
    item = dict()

    while True:
        response = table.scan(**params)
        items = response.get("Items")
        if items:
            tasks.extend(items)

        last_key = response.get('LastEvaluatedKey')

        if not last_key:
            break

        params['ExclusiveStartKey'] = last_key

    # CAPTURA DAS QUESTIONS EXECUTION
    
    qtdade_total = len(tasks)

    item['TOTAL'] = qtdade_total


    return tasks

tasks = buscar_tabela()
# %%
def Average(lst):
    if lst != []:
        response = sum(lst) / len(lst)
        return f'{response:.2f}'
    else:
        return 0

res = {}
columns = {}
## TOTAL DE TAREFAS
totalTasks = len(tasks)
res['Total'] = totalTasks

## MEDIA POR DIA
avaragePerDay = len(tasks) / 15
res["Média diária"] = avaragePerDay

## ENDERECOS ERRADOS
insuccess = 0
efective = 0
sticks = 0
addressOf = 0
ecNotReceive = 0
ecNotVisitButExist = 0
responsibleBusy = 0
urgent = 0

motivo = dict()
materials = dict()
products = dict()
productsnum = dict()

def Percent(product):
    num = res.get(f'Produto {product}',None)
    if num and efective >= 1:
        response = (num * 100) / efective
        return f'{response:.2f}'
    else:
        return 0

for task in tasks:
    for question in task['execution']:
        context = question.get('context', '')
        response = question.get('response', '')
        # if context == "Estabelecimento Localizado" and response == "Não":
        #     insuccess +=1
        if context == "Confirmação de endereço" and response == "Não":
            addressOf +=1
        if context == "O que foi localizado?":
            motivo[f'Insucesso: {response}'] = motivo.get(f'Insucesso: {response}', 0) + 1
        if context == "Primeiro contato":
            if response == "O EC está aberto e vai atender a visita." or response == "O EC está aberto e vai atender a visita":
                efective += 1
            elif response == "O EC está aberto mas o responsável está ocupado":
                responsibleBusy += 1
                ecNotVisitButExist += 1
            elif response == "O EC está aberto mas se recusa a atender a visita":
                ecNotReceive += 1
                ecNotVisitButExist += 1
        if context == "Colou adesivo" and response == "Sim":
            sticks += 1
        if context == "Assunto urgente com a Alelo" and "Sim":
            urgent += 1
        if context == "Ofertas oferecidas":
            for item in response:
                products[f'Produto {item}'] = products.get(f'Produto {item}', 0) + 1
        if "Nota interesse em " in context:
            item = context.replace('Nota interesse em ', '')
            item = context.replace('Nota interesse em ', '')
            value = float(response)
            productlist = productsnum.get(item, list())
            productlist.append(value)
            productsnum[item] = productlist
        if context == "Materiais Entregues":
            for item in response:
                materials[f'Material {item}'] = materials.get(f'Material {item}', 0) + 1

# PESQUISAS NÃO EFETIVAS
insuccess = totalTasks - efective
res['Não efetivas'] = insuccess

# ADDRESS NOT FOUND
res['Endereços não confirmados'] = addressOf

## PESQUISAS EFETIVAS
res['Efetivas'] = efective

## ADESIVOS COLADOS
res['Adesivos colados'] = sticks

## ASSUNTOS URGENTES
res['Assuntos urgentes'] = urgent

## PRODUTOS OFERECIDOS
res.update(products)

## MATERIAIS
res.update(materials)

## MOTIVO INSUCESSO
res.update(motivo)
p = f"@*Painel*@-Qtd ECs oferecidos: {res.get('Produto Painel',0)} @-% ECs oferecidos: {Percent('Painel')}%@-Média de interesse: {Average(productsnum.get('Painel', []))} / 10@"
d = f"@*Desenvolve*@-Qtd ECs oferecidos: {res.get('Produto Desenvolve',0)} @-% ECs oferecidos: {Percent('Desenvolve')}%@-Média de interesse: {Average(productsnum.get('Desenvolve',[]))} / 10@"
ar = f"@*Antecipação de recebíveis*@-Qtd ECs oferecidos: {res.get('Produto Antecipação de recebíveis',0)} @-% ECs oferecidos: {Percent('Antecipação de recebíveis')}%@-Média de interesse: {Average(productsnum.get('Antecipação de recebíveis',[]))} / 10@"
pp = f"@*Pede Pronto*@-Qtd ECs oferecidos: {res.get('Produto Pede pronto',0)} @-% ECs oferecidos: {Percent('Pede pronto')}%@-Média de interesse: {Average(productsnum.get('Pede pronto',[]))} / 10@"
mc = f"@*Mais clientes*@-Qtd ECs oferecidos: {res.get('Produto Mais clientes',0)} @-% ECs oferecidos: {Percent('Mais clientes')}%@-Média de interesse: {Average(productsnum.get('Mais clientes',[]))} / 10@"
print(f"""*CONSOLIDADO* @ Visitas Realizadas: {res.get('Total', 0)} @ Visitas - Efetivas: {res.get('Efetivas',0)} @ Visitas - Não efetivas: {res.get('Não efetivas',0)} @ @*EFETIVAS* @ *- Sucesso :* @ Adesivos colados: {res.get('Adesivos colados',0)} @ Endereços atualizados: {res.get('Endereços não confirmados',0)} @ @*NÃO EFETIVAS* @ EC aberto mas se recusa a responder: {ecNotReceive} @ Estabelecimento fechado pra sempre: {res.get('Insucesso: Um estabelecimento fechamento a muito tempo ou para sempre', 0)} @ Residência ou prédio residencial: {res.get('Insucesso: Uma residência ou prédio residencial',0)} @ Terreno baldio: {res.get('Insucesso: Um terreno baldio',0)} @ Não encontrei o endereço: {res.get('Insucesso: Um endereço indicado não localizado', 0)} @ Comércio com outro nome: {res.get('Insucesso: Outro estabelecimento no lugar', 0)} @ @*PRODUTOS* @ {p}{d}{ar}{pp}{mc} @*MATERIAIS ENTREGUES* @ Folder: {res.get('Material Folder',0)} @ Adesivo: {res.get('Material Adesivo',0)} @ Kit: {res.get('Material Kit', 0)} @ Caneta: {res.get('Material Canetas', 0)}""")

res = {k:[v] for k,v in res.items()}
dataFrame = pd.DataFrame(res)
dataFrame.to_excel('./reports_alelo/acompanhamento_ccc.xlsx', index=False)