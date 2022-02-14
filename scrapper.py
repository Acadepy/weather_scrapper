import requests, datetime
from bs4 import BeautifulSoup


today = datetime.datetime.now()
YEAR = today.year
MONTH = today.strftime("%m")
DAY = today.day
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        
if __name__ == '__main__':
    url = f"https://www.wunderground.com/dashboard/pws/ITURCI5/table/{YEAR}-{MONTH}-{DAY}/{YEAR}-{MONTH}-{DAY}/daily"
    print(f"Obteniendo datos del {DAY}/{MONTH}/{YEAR}")

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
        date_string = f"{DAY}/{MONTH}/{YEAR} " + row[0]
        hour = datetime.datetime.strptime(date_string, "%d/%m/%Y %I:%M %p")
        borrar = [data.split()[0] for data in row[1:]]
        borrar.insert(0, hour.strftime("%d/%m/%Y %I:%M %p"))
        print(borrar)