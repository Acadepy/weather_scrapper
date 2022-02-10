import requests, datetime
from bs4 import BeautifulSoup


today = datetime.datetime.now()
year_i = today.year
year_f = today.year
month_i = today.strftime("%m")
month_f = today.strftime("%m")
day_i = today.day
day_f = today.day
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        
if __name__ == '__main__':
    url = f"https://www.wunderground.com/dashboard/pws/ITURCI5/table/{year_i}-{month_i}-{day_i}/{year_f}-{month_f}-{day_f}/daily"
    print(f"Obteniendo datos desde el {day_i}/{month_i}/{year_i} al {day_f}/{month_f}/{year_f}")

    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')
    
    #Find the table
    table = soup.find("table", class_="history-table desktop-table")

    #Find all columns titles from the table and convert them to text
    titles_row = table.find("tr")
    titles_list = titles_row.find_all("th")
    titles = [i.text for i in titles_list]
    
    #Find all rows from the table and convert them to text
    table_body = table.find("tbody")
    table_rows = table_body.find_all("tr")
    data_rows = []
    for row in table_rows:
        columns_list = row.find_all("td")
        columns_text = [col.text for col in columns_list]
        data_rows.append(columns_text)
        print(data_rows)
        

    for row in data_rows:
        hour = datetime.datetime.strptime(row[0], "%I:%M %p") 
        #Faltaría seleccionar el día. Ahora mismo está leyendo una hora pero el día es el 01/01/1900
        print(hour)   
