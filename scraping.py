import requests
from bs4 import BeautifulSoup
import csv

url = 'https://id.wikipedia.org/wiki/Daftar_lukisan_termahal'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'class': 'wikitable'})

    painting_data = []
    rows = table.find_all('tr')[1:]  # Lewati baris pertama (header tabel)
    for row in rows:
        columns = row.find_all(['td', 'th'])
        pelukis = columns[2].text.strip()
        seniman = columns[4].text.strip()
        tahun = columns[5].text.strip()
        penjual = columns[8].text.strip()

        painting_data.append({'pelukis': pelukis, 'seniman': seniman, 'tahun': tahun, 'penjual': penjual})

    with open('hasil_scraping_lukisan_termahal.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['pelukis', 'seniman', 'tahun','penjual']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for data in painting_data:
            writer.writerow(data)

else:
    print(f'Gagal mengambil halaman web. Kode status: {response.status_code}')
