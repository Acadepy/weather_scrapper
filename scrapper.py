from ntpath import join
import requests, datetime
from bs4 import BeautifulSoup


today = datetime.datetime.now()
YEAR = today.year
MONTH = today.strftime("%m")
DAY = today.day
#DAY = (today - datetime.timedelta(days = 1)).day
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

#ILLAMA3
#ITURCI5

STATION = "ITURCI5"

# units:
# N/A  °F  °F  %  N/A  mph  mph  in  in  in  N/A  w/m²


def data_scraped(station=STATION, day=DAY, month=MONTH, year=YEAR):
    '''Devuelve todos los datos de un día concreto para una estación dada.'''

    url = f"https://www.wunderground.com/dashboard/pws/{station}/table/{year}-{month}-{day}/{year}-{month}-{day}/daily"
    print(f"Estación: {STATION}.")
    print(f"Obteniendo datos del {day}/{month}/{year}.")

    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')

    print(f"Datos descargados.")
    
    #Find the table
    table = soup.find("table", class_="history-table desktop-table")

    #Find all columns titles from the table and convert them to text
    titles_row = table.find("tr")
    titles_list = titles_row.find_all("th")
    #titles = [i.text for i in titles_list]
    
    #Find all rows from the table and convert them to text
    table_body = table.find("tbody")
    table_rows = table_body.find_all("tr")
    data_rows = []
    for row in table_rows:
        columns_list = row.find_all("td")
        columns_text = [col.text for col in columns_list]
        data_rows.append(columns_text)
        
    all_day_data = []
    for row in data_rows:
        date_string = f"{day}/{month}/{year} " + row[0]
        hour = datetime.datetime.strptime(date_string, "%d/%m/%Y %I:%M %p")

        row_formated = []
        for data in row[1:]:
            try:
                row_formated.append(data.split()[0])
            except:
                row_formated.append("No data")
        row_formated.insert(0, hour.strftime("%d/%m/%Y %H:%M"))
        all_day_data.append(row_formated)

    return all_day_data

def write_data_in_file(data, filename='weather_data.txt'):
    '''Escribe los datos que recibe en un archivo, separando las columnas con tabuladores.'''
    print(f'Escribiendo datos en {filename}...')
    with open(filename, 'a') as writer:
        for r in data:
            writer.write('\t'.join(r))
            writer.write('\n')

def menu():
    '''Menú que te pide un día y una estación, obtiene sus datos y los guarda en un archivo.'''

    print('\n\n\n' + "Rastreador de datos en WunderMaps".center(50, '*') + '\n\n\n')
    station_to_scrape = input('Introduce el nombre de la estación: ')
    station_to_scrape = station_to_scrape if station_to_scrape else STATION

    try:
        day_to_scrape = datetime.datetime.strptime(input('Introduce el día para obtener los datos (dd/mm/aaaa): '), "%d/%m/%Y")
    except:
        print("Ha habido un error con la fecha. No tiene el formato correcto.")
        return
    
    try:
        data = data_scraped(station=station_to_scrape, day=day_to_scrape.day, month=day_to_scrape.month, year=day_to_scrape.year)
        print("Se han obtenido correctamente los datos.")
    except:
        print("Ha habido un error al obtener los datos.")
        return
    
    try:
        write_data_in_file(data=data)
        print("Se han escrito los datos correctamente.")
    except:
        print("Ha habido un error al escribir los datos.")   
        return

def main():
    pass
            
if __name__ == '__main__':
    main()






