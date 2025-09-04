import requests
import csv
import io

def authenticate(token: str, start_date: str, end_date: str) -> str:
    url = "https://us.engagingnetworks.app/ea-dataservice/export.service"
    querystring = {
        "token": token,
        "startDate": start_date, #MMDDYYYY
        "endDate": end_date #MMDDYYYY
    }
    headers = {
        "Accept": "text/html; charset=UTF-8, text/xml; charset=UTF-8, text/csv; charset=UTF-8"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    
    #return response.text

    csv_content = io.StringIO(response.text)
    reader = csv.reader(csv_content)
    rows = list(reader)
    with open("test2.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"CSV saved as 'test2.csv'")
    return rows