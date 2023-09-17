from ssl import VerifyFlags
import boto3
from numpy import column_stack
import pandas as pd
from datetime import datetime

'''
[1] função Listing = recebe stageVariables(pode ser DEV ou PROD) e queryStringParameters(filtros do front)
    [1.1] transforma valores recebidos em querry para o mongodb 
    [1.2] com o resultado da querry do mongo executa a função report alelo e retorna valores como "data" 
    
[2] report_alelo = ler e tratas itens vindos do Mongodb 
    [2.1] retorna uma planilha para download

'''


def listing():

    ids = list()
    
    
    session = boto3.session.Session(
        profile_name='andre.nicacio', region_name='sa-east-1')
    dynamodb = session.resource('dynamodb')
    
    company = 'apsen'
    column_dataframe = ['CNPJ']
    columns = list()
    start = datetime(2022, 10, 4, 0, 0, 0, 0)
    finish = datetime(2022, 10, 26, 0, 0, 0, 0)
    task = 'RFA-2'
    
    final_dataframe = list()
    
    if(company.lower() == 'apsen'):
        if task == 'RFA':
            column_dataframe = [
                    'Data_Execução',
                    'task_id',
                    'BANDEIRA',
                    'GRUPO',
                    'CNPJ',
                    'DESCRICAO_CUP',
                    "Local encontrado",
                    "Encontrou Lactosil Flora",
                    "Diferença entre Lactosil Flora e concorrentes",
                    "Posicionamento das caixas na prateleira Lactosil Flora",
                    "Tinha mensagem LEVE +8 CAPSULAS Lactosil Flora",
                    "Localizou o preço do Lactosil Flora na prateleira",
                    "Havia promoção sinalizada na etiqueta Lactosil",
                    "Localizou o preço do Lactosil na prateleira",
                    "Encontrou Lactosil 10,000 FCC 30tbl",
                    "Posicionamento das caixas na prateleira Lactosil",
                    "Tinha mensagem LEVE +8 CAPSULAS Lactosil",
                    "Localizou o preço do Lactosil na prateleira",
                    "Havia promoção sinalizada na etiqueta Lactosil",
                    "Preço unitário Lactosil",
                    "Foto Lactosil ou prateleira",
                    "Encontrou Inilok 30cpr",
                    "Preço unitário Inilok",
                    "Medicamento oferecido como opção mais barata ao Inilok",
                    "Medicamento oferecido na troca do Inilok",
                    "Medicamento oferecido como opção mais barata ao Inilok",
                    "Preço unitário do produto indicado"]
        elif task == 'RFA-2':
            column_dataframe = [
                    'Data_Execução',
                    'task_id',
                    'BANDEIRA',
                    'GRUPO',
                    'CNPJ',
                    'DESCRICAO_CUP',
                    'O que encontrou no local',
                    'Produto para ansiedade que nao seja medicamento',
                    'Probians esta na prateleira?',            
                    'Ja ouviu falar em probians?',
                    'Tem Probians na loja?',
                    'Produtos proximos ao Probians',
                    'Foto prateleira Probians',
                    'Tem Extima lata?',
                    'Extim esta atras do balcao ou na prateleira ao seu alcance?',
                    'Qual o preço do Extima lata?',
                    'Você foi informado sobre o programa Sou Mais Vida?',
                    'Foto Extima Lata na prateleira',
                    'Tem Inilok 30 cpr comprimidos ?',
                    'Preço do Inilok 30cpr',
                    'Tem algum outro medicamento genérico para o Inilok ?',
                    'O genérico é exatamente a mesma coisa do Inilok ?',
                    'Qual é a diferença entre o Inilok e o genérico ?']            
        elif task == 'RFA-3':
            column_dataframe = [
                    'Data_Execução',
                    'task_id',
                    'BANDEIRA',
                    'GRUPO',
                    'CNPJ',
                    'DESCRICAO_CUP',
                    'O que encontrou no local',
                    'Encontrou Motilex HA com 30 cápsulas na prateleira',
                    'Encontrou preço do Motilex HA na prateleira',            
                    'Preço informado do Motilex HA na prateleira',
                    'Posicionamento da(as) caixa(s) do Motilex HA na prateleira',
                    'Mensagem de Leve + 12 Dias',
                    'Marca sugerida colageno para articulações',
                    'Preço do Motilex HA de acordo com o balconista',
                    'Foi informado sobre programa de desconto do laboratório Sou Mais Vida',
                    'Encontrou alguma comunicação sobre o programa de desconto do laboratório Sou Mais Vida',
                    'Foto prateleira Motilex HA',
                    'Indicação de remédio para enjoo',
                    'Opção que dá menos sonolência e age mais rápido.',
                    'Entao qual a marca indicada?',
                    'Opção mais barato que não causa sonolência',
                    'Meclin é a mesma coisa.']           

    elif(company.lower() == 'alelo'):
        if task.upper() == 'CCC':
            column_dataframe = [
                      "task_id",
                      "EC",
                      "ENDERECO",
                      "CNPJ",
                      "BAIRRO",
                      "DATA",
                      "HORA",
                      "Estabelecimento Localizado",
                      "Primeiro contato",
                      "Detalhes da recusa do EC",
                      "Nome do responsavel",
                      "Nota interesse em Painel",
                      "Nota interesse em Desenvolve",
                      "Nota interesse em Antecipação de recebíveis",
                      "Nota interesse em Pede pronto",
                      "Nota interesse em Mais clientes",
                      "Observação dos produtos oferecidos",
                      "Observação sobre a visita"
                      ]  
    
    task_id = ''
    
    # FUNÇOES RESPONSAVEL POR ACESSAR E TRAZER DADOS DO DYNAMO
    
    
    def buscar_tabela_in_person():
        table = dynamodb.Table('table_micro_task_in_person')
        params = dict(
            FilterExpression='#company = :c and #status.#status = :s and #status.#state = :f',
            ExpressionAttributeNames={'#company': 'company','#status': 'status', '#state': 'state'},
            ExpressionAttributeValues={':c': company.lower(),
                                       ':s': 'SUCCESS', 
                                       ':f': 'FINISHED'}
        )
        tasks = list()
        res = list()
    
        while True:
            response = table.scan(**params)
            items = response.get("Items")
            if items:
                tasks.extend(items)
    
            last_key = response.get('LastEvaluatedKey')
    
            if not last_key:
                break
            
            params['ExclusiveStartKey'] = last_key
    
        for data in tasks:
            if(company.lower() == 'apsen'):
                verify_cnpj = data['original'].get('CNPJ', None)
                if verify_cnpj:
                    item = {
                        'SUBCANAL': data['original'].get('SUBCANAL', ''),
                        'BANDEIRA': data['original'].get('BANDEIRA', ''),
                        'GRUPO': data['original'].get('GRUPO', ''),
                        'CNPJ': verify_cnpj,
                        'DESCRICAO_CUP': data['original'].get('DESCRICAO_CUP', ''),
                        'task_id': data['task_id']
                    }
                else:
                    item = {
                        'SUBCANAL': data['original'].get('SUBCANAL', ''),
                        'BANDEIRA': data['original'].get('BANDEIRA', ''),
                        'GRUPO': data['original'].get('GRUPO', ''),
                        'CNPJ': data['original'].get('CNPJ ', ''),
                        'DESCRICAO_CUP': data['original'].get('DESCRICAO_CUP', ''),
                        'task_id': data['task_id']
                    }                    

                res.append(item)
                ids.append(data['task_id'])
            elif(company.lower() == 'alelo'):
                address = data.get('address',None)
                date_time = data.get('status',None)
                obj = date_time["when"].split("T")
                date = obj[0]
                hora = obj[1]
                if address:
                    item = {
                        'EC': data['original']['NOME_FANTASIA'],
                        'CNPJ': data['original']['CNPJ'],
                        'BAIRRO': data['address']['district'],
                        'DATA': date,
                        'HORA': hora,
                        'AUDITORIA': data['status']['when'],
                        'ENDERECO': address['formatted_address'],
                        'CIDADE': address['city'],
                        'ESTADO': address['state'],
                        'task_id': data['task_id']
                    }
                    res.append(item)   
                else:
                    item = {                        
                        'EC': data['original']['NOME_FANTASIA'],
                        'CNPJ': data['original']['CNPJ'],
                        'BAIRRO': '',                        
                        'DATA': date,
                        'HORA': hora,
                        'AUDITORIA': data['status']['when'],
                        'task_id': data['task_id']
                    }
                    res.append(item)                              
    
        return res
    
    
    def buscar_tabela_execution():
        response_flow = dict()
        count = 0
        table = dynamodb.Table('table_micro_task_execution')
        params = dict(
            FilterExpression='company = :c AND audit.approved = :a AND #audit.#when BETWEEN :dtI AND :dtF AND #result = :f AND #task_info.#name = :name_task',
            ExpressionAttributeNames={"#audit": "audit", "#when": "when", "#result": "result", '#task_info': 'task_info', '#name': 'name'},
            ExpressionAttributeValues={
                ':c': company.lower(),
                ':a': True,
                ':dtI': start.isoformat(),
                ':dtF': finish.isoformat(),
                ':name_task': task.upper(),
                ':f': 'FINISH'
            }
        )
    
        # response = table.cam(**params)
    
        tasks = list()
    
        while True:
            response = table.scan(**params)
            items = response.get("Items")
            if items:
                tasks.extend(items)
    
            last_key = response.get('LastEvaluatedKey')
    
            if not last_key:
                break
            
            params['ExclusiveStartKey'] = last_key
        print(len(tasks))
        # CAPTURA DAS QUESTIONS EXECUTION/PERSON
        
        return tasks
    
    # SEÇAO RESPONSAVEL POR CAPTURAR DADOS DO DYNAMO E ENCAMINHAR PARA O ARQUIVO
    all_execution = buscar_tabela_execution()
    qtd_execution = len(all_execution)
    
    # %%
    def parse_execution(tasks):
        finishedTask = list()
        for data in tasks:
            execution = list()
            for itemExec in data['execution']:
                verify_column = itemExec.get('context', None)     
                verify_response = itemExec.get('response', None)     
                style = itemExec.get('style', None)
                if(company.lower() == 'apsen'):
                    for columns in column_dataframe:
                        if style != 'photo':
                            if verify_column == columns and verify_column != 'O que encontrou no local':
                                    response_flow = {
                                        'resposta': itemExec.get('response', None),
                                        'pergunta': verify_column
                                    }
                                    execution.append(response_flow)  
                            elif verify_column == 'O que encontrou no local' and verify_response != None:
                                    response_flow = {
                                        'resposta': itemExec.get('response', None),
                                        'pergunta': verify_column
                                    }
                                    execution.append(response_flow)  
                            else:
                                response_flow = {
                                    'resposta': '',
                                    'pergunta': ''
                                }
                                execution.append(response_flow)          
                        else:
                            if verify_column:
                                try:
                                    final_dataframe.remove(verify_column)
                                except:
                                    print()
                                response_photos = itemExec.get('response', "vazio")
    
                                for i, foto in enumerate(response_photos):
                                    name = f'{verify_column}_{i+1}'
                                    if name not in final_dataframe:
                                        final_dataframe.append(name)
                                    response_flow = {
                                            f'resposta': foto,
                                            'pergunta': name
                                        }                                  
                                    execution.append(response_flow)
                                
                                                               
                else:
                    for columns in column_dataframe:
                        if verify_column == columns:
                            if verify_column == "Telefone fixo do EC":
                                telefone = itemExec.get('response', None)
                                exec = {
                                    'resposta': str(telefone['phone']),
                                    'pergunta': verify_column
                                }
                                execution.append(exec)
                            elif verify_column == "Telefone celular do EC":
                                telefone = itemExec.get('response', None)
                                exec = {
                                    'resposta': str(telefone['phone']),
                                    'pergunta': verify_column
                                }
                                execution.append(exec)
                            elif verify_column == "Email do EC":
                                email = itemExec.get('response', None)
                                exec = {
                                    'resposta': str(email['email']),
                                    'pergunta': verify_column
                                }
                                execution.append(exec)                        
                            elif verify_column == "CNPJ corrigido do estabelecimento":
                                cnpj = itemExec.get('response', None)
                                if cnpj:
                                    exec = {
                                        'resposta': str(cnpj['cnpj']),
                                        'pergunta': verify_column
                                    }
                                    execution.append(exec)                        
                            else:
                                exec = {
                                    'resposta': str(itemExec.get('response', None)),
                                    'pergunta': verify_column
                                }
                                execution.append(exec)
                        
    
    
            if(company.lower() == 'apsen'):
                item = {
                    'Data_Execução': data['when']['start'],
                    'Finish': data['audit']['when'],
                    'task_id': data['task_id'],
                    'execution_id': data['execution_id']
                }
    
                for execAtual in execution:
                    pergunta = execAtual.get('pergunta', None)
                    resposta = execAtual.get('resposta',None)
                    item[pergunta] = resposta
                finishedTask.append(item)        
    
            elif(company.lower() == 'alelo'):
                date_time = data.get('when',None)
                obj = date_time["finish"].split("T")
                date = obj[0]                
                time = obj[1]                
                item = {
                    'task_id': data['task_id'],
                    'AGENTE RESPONSAVEL': data['who'],
                    'sofier': data['who'],
                    'DATA': date,
                    'HORA': time,
                    'LATITUDE': data['task_info']['location']['lng'],
                    'LONGITUDE': data['task_info']['location']['lat']
                }
    
                for execAtual in execution:
                    pergunta = execAtual['pergunta']
                    item[pergunta] = execAtual['resposta']
                finishedTask.append(item) 
                               
    
        return finishedTask
    
    final_dataframe = list(column_dataframe)
    execution = parse_execution(all_execution)
    print(qtd_execution)
    
    # %%
    print('executuion carregada')
    print('buscando in person')
    inperson = buscar_tabela_in_person()
    
    # %%
    
    data = list()
    
    for exec in range(len(execution)):
        taskid = execution[exec]['task_id']
        #data_inperson = list(filter(lambda item: item['task_id'] == task_id, inperson))
        res = [x for x in inperson if x['task_id'] == taskid]
        if(res != []):
            new_value = {**res[0],**execution[exec]}
            data.append(new_value)
        else:
            continue
        
    print(len(data))
    print('Iniciando DataFrame')        
    dataFrame = pd.DataFrame(data)
    dataFrame.to_excel(f'cru.xlsx', index=False)
    
    dataFrame = dataFrame.reindex(columns=final_dataframe)
    
    dataFrame.to_excel(f'./reports_sofie/execucoes_ccc_report.xlsx', index=False)
    print('Finalizado')
    
listing()

    

    