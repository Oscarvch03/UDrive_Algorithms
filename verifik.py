import requests
import json
import datetime as dt

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRJZCI6IjYyNThiNTYzMmM1MWUzYmQyNzg5NTkzMiIsImRvY3VtZW50VHlwZSI6IkNDIiwiZG9jdW1lbnROdW1iZXIiOiIxMDA3NjU4MDczIiwidiI6MSwicm9sZSI6ImNsaWVudCIsImlhdCI6MTY0OTk4MDc3MX0.LBlt7-KeaEItGQxL0NvGvkstiO_G6dN9TZRwRaPAALM'
print(len(api_key))

def query_verifik(cc, placa):
    headers = {
        'Authorization': 'Bearer ' + api_key
    }

    parameters1 = {
        'documentType': 'CC',
        'documentNumber': cc
    }

    response1 = requests.get('https://api.verifik.co/v2/co/runt/consultarConductor',
                            params=parameters1,
                            headers=headers)

    parameters2 = {
        'documentType': 'CC',
        'documentNumber': cc,
        'plate': placa
    }
    
    response2 = requests.get('https://api.verifik.co/v2/co/runt/consultarVehiculo',
                            params=parameters2,
                            headers=headers)
    if(response1.status_code == 200 and response2.status_code == 200):
        with open(cc + '.json', 'w') as json_file1:
            json.dump(response1.json(), json_file1, indent=4)
        with open(cc + '_' + placa + '.json', 'w') as json_file2:
            json.dump(response2.json(), json_file2, indent=4)
        return (cc + '.json', cc + '_' + placa + '.json')
    else:
        return 'Failed Query. Errors {0} and {1}.'.format(response1.status_code, 
                                                          response2.status_code)


def verifik_json(cc, placa):
    json1 = open('{0}.json'.format(cc))
    json2 = open('{0}_{1}.json'.format(cc, placa))
    persona = json.load(json1)
    vehiculo = json.load(json2)
    val_lic = []
    for l in persona['data']['licencias']:
        vence = [int(i) for i in l['dueDate'].split('/')]
        anho = vence[2]
        mes = vence[1]
        dia = vence[0]
        if(dt.date(anho, mes, dia) > dt.date.today()):
            val_lic.append(l['category'])
    dt_soat = [int(i) for i in vehiculo['data']['soat']['dueDate'].split('/')]
    dt_tech = [int(i) for i in vehiculo['data']['techReview']['dueDate'].split('/')]
    soat = dt.date(dt_soat[2], dt_soat[1], dt_soat[0]) > dt.date.today()
    tech = dt.date(dt_tech[2], dt_tech[1], dt_tech[0]) > dt.date.today()
    if(('A1' in val_lic) or ('B1' in val_lic) or ('B2' in val_lic) or ('C1' in val_lic)):
        if(soat and tech):
            return True
    return False


cc = '5630533'
placa = 'DTZ93E'

# print(query_verifik(cc, placa))
print(verifik_json(cc, placa))

