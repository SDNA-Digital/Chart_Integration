import psycopg2 as pg
import json

try:
    connection = pg.connect(user="postgres", password="SDNA@2022", host="localhost", port="5432", database="Eagle2")
    curs = connection.cursor()
    curs.execute('SELECT processonivelrisco as "Nivel de Risco", mes as "Mes" , COUNT(*) AS "QtdeProcessos" FROM dash_processo GROUP BY processonivelrisco, "Mes" ORDER BY "Mes", "Nivel de Risco"')

    nivel_risco = {
        'MBA': 'Muito Baixo', 
        'BAI': 'Baixo', 
        'MOD': 'Moderado', 
        'ALT': 'Alto', 
        'MAL': 'Muito Alto'
    }
    
    dic_date_mounth = {
        '01': 'Janeiro',
        '02': 'Fevereiro',
        '03': 'Marco',
        '04': 'Abril',
        '05': 'Maio',
        '06': 'Junho',
        '07': 'Julho',
        '08': 'Agosto',
        '09': 'Setembro',
        '10': 'Outubro',
        '11': 'Novembro',
        '12': 'Dezembro'
    }

    results = []
    for row in curs.fetchall():
        result_dict = {}
        result_dict['Mes'] = dic_date_mounth[row[1]]
        result_dict['Nível de Risco'] = nivel_risco[row[0]]
        result_dict['QtdeProcessos'] = row[2]
        results.append(result_dict)

    curs.close()
    connection.close()
    
    results_grouped = {}
    for result in results:
        mes = result['Mes']
        if mes not in results_grouped:
            results_grouped[mes] = {}
        nivel_risco = result['Nível de Risco']
        if nivel_risco not in results_grouped[mes]:
            results_grouped[mes][nivel_risco] = 0
        results_grouped[mes][nivel_risco] += result['QtdeProcessos']
    
    final_results = []
    for mes, data in results_grouped.items():
        data['Mes'] = mes
        final_results.append(data)

    json_result = json.dumps(final_results, indent=4)
    with open('resultado.json', 'w') as arquivo:
        arquivo.write(json_result)

except Exception as e:
    print("Ocorreu um erro:", e)