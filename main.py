import requests
import bs4
from bs4 import BeautifulSoup
import csv
import sys

def scrape_results(url, output_file):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Najdeme odkaz na výběr okrsku
    link = soup.find('a', string='Výběr okrsku')
    if link is None:
        print("Odkaz na výběr okrsku nebyl nalezen.")
        return

    okrsky_url = link['href']
    response = requests.get(okrsky_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Nalezení odkazu pro všechny obce
    obce_links = soup.find_all('a', string='X')
    if not obce_links:
        print("Odkazy na obce nebyly nalezeny.")
        return

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Obec', 'Registrovaní voliči', 'Vydané obálky', 'Platné hlasy'])

        for obec_link in obce_links:
            obec_url = obec_link['href']
            response = requests.get(obec_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            obec_name = soup.find('h3').text.strip()
            volici = soup.find_all('td', class_='cislo')[:3]
            volici_data = [int(vol.text.replace('\xa0', '')) for vol in volici]

            writer.writerow([obec_name] + volici_data)

        print(f"Výsledky byly uloženy do souboru {output_file}.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Chybné použit")

