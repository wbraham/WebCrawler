import requests
import json
from bs4 import BeautifulSoup


links = []


def url_crawler():
    url = 'http://www.ordre-medecins.org.tn/components/com_annuaires/annuaires.php'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="lxml")
    for link in soup.findAll("area"):
        x = 'http://www.ordre-medecins.org.tn/components/com_annuaires/annuaires.php'+link.get('href')
        global links
        links.append(x)


def crawler(total_pages):
    for ville in links:
        page = 1
        print("url"+ville)
        mon_url = ville
        nom_ville = mon_url.split("?ville=")
        nom_fichier = nom_ville[1]
        print("nom ville:"+nom_fichier)
        while page <= total_pages:
            url = mon_url+'&page='+str(page)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, features="lxml")
            doctors_list = []
            for link in soup.select("tr"):
                cells = link.findAll('td')
                if len(cells)>0:
                    name = cells[0].text.strip()
                    speciality = cells[1].text.strip()
                    address = cells[3].text.strip()
                    phone = cells[4].text.strip()
                    description = cells[2].text.strip()
                    doctor = {'nom': name, 'specialité':speciality, 'adresse':address, 'telephone':phone}
                    if (len(phone)!=0 and (description!="Médecin à l\'étranger") and (description!="Médecin Sans Activité")
                            and (description!="Médecin Contractuel") and (description!="Décédé") and (description!="Résident[e]")):
                        doctors_list.append(doctor)

            for dr in doctors_list:
                with open(nom_fichier + '.json', 'a+', encoding='utf-8') as jsonfile:
                    json.dump(dr, jsonfile, ensure_ascii=False)

            page += 1


url_crawler()
crawler(2)
