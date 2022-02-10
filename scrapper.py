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
    print(url)
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')
    
    #Find the table
    table = soup.find("table", class_="history-table desktop-table")
    #Find all columns from the table and convert them to text
    tr_table = table.find("tr")
    ths_table = tr_table.find_all("th")
    ths_table_text = [i.text for i in ths_table]
    
    #Find all rows from the table and convert them to text
    tbody = table.find("tbody")
    trs_body = tbody.find_all("tr")
    rows = []
    for tr_body in trs_body:
        columns = tr_body.find_all("td")
        columns_text = [col.text for col in columns]
        rows.append(columns_text)
    print(rows)

    #Con esto ya tengo listo, las cabeceras en ths_table_text y los datos en una lista de listas, en rows
    