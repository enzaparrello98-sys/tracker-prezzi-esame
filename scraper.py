import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
}

# LISTA AMPLIATA: Puoi aggiungere quanti blocchi vuoi qui dentro seguendo lo stesso schema!
PRODOTTI_TARGET = [
    # --- THE ORDINARY ---
    {
        "Brand": "The Ordinary",
        "Prodotto": "Niacinamide 10% + Zinc 1%",
        "Formato": "60ml",
        "Rivenditore": "Profumerie Galeazzi",
        "Link": "https://profumeriegaleazzi.it/products/niacinamide-10-zinc-1?variant=55978556260725",
        "Selector": {"tag": "span", "class": "price-item--sale"}
    },
    # --- CERAVE ---
    {
        "Brand": "CeraVe",
        "Prodotto": "Detergente Idratante",
        "Formato": "473ml",
        "Rivenditore": "XFarma",
        "Link": "https://www.xfarma.it/it/cerave-detergente-idratante-viso-pelle-da-normale-a-secca-i-acido-ialuronico-e-ceramidi-473ml.html",
        "Selector": {"tag": "span", "class": "price"}
    },
    # --- CERA DI CUPRA ---
    {
        "Brand": "Cera di Cupra",
        "Prodotto": "Crema Idratante Opacizzante Per Pelli Miste O Grasse",
        "Formato": "50ml",
        "Rivenditore": "Filgi Store",
        "Link": "https://www.filgistore.it/it/creme-viso/4848-cera-di-cupra-ricette-di-miele-crema-idratante-opacizzante-pelli-miste-o-grasse-50-ml-8002140055508.html",
        "Selector": {"tag": "span", "class": "product-price"} # AGGIORNATO selettore per Filgi
    },
    {
        "Brand": "Cera di Cupra",
        "Prodotto": "Crema Idratante Opacizzante Per Pelli Miste O Grasse",
        "Formato": "50ml",
        "Rivenditore": "FarmaSave",
        "Link": "https://www.farmasave.it/cera-di-cupra-crema-idratante-opacizzante-pelli-miste-grasse-50-ml.html",
        "Selector": {"tag": "span", "class": "price"}
    },
    {
        "Brand": "Cera di Cupra",
        "Prodotto": "Crema Idratante Opacizzante Per Pelli Miste O Grasse",
        "Formato": "50ml",
        "Rivenditore": "IdeaBellezza",
        "Link": "https://www.ideabellezza.it/crema-idratante-opacizzante/",
        "Selector": {"tag": "span", "class": "price"}
    },
    {
        "Brand": "Cera di Cupra",
        "Prodotto": "Crema Idratante Opacizzante Per Pelli Miste O Grasse",
        "Formato": "50ml",
        "Rivenditore": "Profumeria Web",
        "Link": "https://www.profumeriaweb.com/cera-di-cupra-crema-idratante-opacizzante-pelli-miste-o-grasse-50ml",
        "Selector": {"tag": "span", "class": "regular-price"}
    }
]

def estrai_prezzo(url, selector):
    try:
        risposta = requests.get(url, headers=HEADERS, timeout=15)
        if risposta.status_code != 200:
            return "Errore Connessione"
        
        soup = BeautifulSoup(risposta.text, 'html.parser')
        elemento_prezzo = soup.find(selector["tag"], class_=selector["class"])
        
        if elemento_prezzo:
            testo_prezzo = elemento_prezzo.text.strip()
            prezzo_pulito = (
                testo_prezzo.replace("€", "")
                            .replace("EUR", "")
                            .replace(",", ".")
                            .replace("da", "")
                            .strip()
            )
            return prezzo_pulito
        return "N/D"
    except Exception:
        return "Errore"

def main():
    data_oggi = datetime.now().strftime("%Y-%m-%d")
    nuove_righe = []

    for item in PRODOTTI_TARGET:
        prezzo_rilevato = estrai_prezzo(item["Link"], item["Selector"])
        
        riga = [
            data_oggi,
            item["Brand"],
            item["Prodotto"],
            item["Formato"],
            item["Rivenditore"],
            prezzo_rilevato,
            "Online",         
            "E-commerce",     
            item["Link"]
        ]
        nuove_righe.append(riga)
        time.sleep(3) # Pausa防ban

    with open('prezzi.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for riga in nuove_righe:
            writer.writerow(riga)

if __name__ == "__main__":
    main()
