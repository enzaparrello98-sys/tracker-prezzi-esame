import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

# Intestazioni per simulare un browser umano
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
}

PRODOTTI_TARGET = [
    # --- 1. THE ORDINARY ---
    {
        "Brand": "The Ordinary",
        "Prodotto": "Niacinamide 10% + Zinc 1%",
        "Formato": "60ml",
        "Rivenditore": "Sephora",
        "Link": "https://www.sephora.it/p/niacinamide-10%25---zinc-1%25---siero-anti-imperfezioni-P3220023.html",
        "Selector": {"tag": "span", "class": "price-sales"}
    },
    {
        "Brand": "The Ordinary",
        "Prodotto": "Niacinamide 10% + Zinc 1%",
        "Formato": "60ml",
        "Rivenditore": "Notino",
        "Link": "https://www.notino.it/the-ordinary/niacinamide-10-zinc-1-high-strength-vitamin-and-mineral-blemish-formula-siero-viso-leggero-contro-le-imperfezioni-della-pelle/",
        "Selector": {"tag": "span", "class": "price"}
    },
    
    # --- 2. CERAVE ---
    {
        "Brand": "CeraVe",
        "Prodotto": "Detergente Idratante",
        "Formato": "473ml",
        "Rivenditore": "Douglas",
        "Link": "https://www.douglas.it/it/p/5002931180",
        "Selector": {"tag": "span", "class": "product-price__price"}
    },
    {
        "Brand": "CeraVe",
        "Prodotto": "Detergente Idratante",
        "Formato": "473ml",
        "Rivenditore": "XFarma",
        "Link": "https://www.xfarma.it/it/cerave-detergente-idratante-viso-pelle-da-normale-a-secca-i-acido-ialuronico-e-ceramidi-473ml.html",
        "Selector": {"tag": "span", "class": "price"}
    },

    # --- 3. CERA DI CUPRA ---
    {
        "Brand": "Cera di Cupra",
        "Prodotto": "Crema Idratante Opacizzante",
        "Formato": "50ml",
        "Rivenditore": "FarmaSave",
        "Link": "https://www.farmasave.it/cera-di-cupra-crema-idratante-opacizzante-pelli-miste-grasse-50-ml.html",
        "Selector": {"tag": "span", "class": "price"}
    },
    {
        "Brand": "Cera di Cupra",
        "Prodotto": "Crema Idratante Opacizzante",
        "Formato": "50ml",
        "Rivenditore": "Profumeria Web",
        "Link": "https://www.profumeriaweb.com/cera-di-cupra-crema-idratante-opacizzante-pelli-miste-o-grasse-50ml",
        "Selector": {"tag": "span", "class": "regular-price"}
    }
]

def estrai_prezzo(url, selector):
    # Usiamo un blocco TRY/EXCEPT totale per proteggere il programma dai crash
    try:
        risposta = requests.get(url, headers=HEADERS, timeout=15)
        if risposta.status_code != 200:
            return "Bloccato da Anti-Bot"
        
        soup = BeautifulSoup(risposta.text, 'html.parser')
        elemento_prezzo = soup.find(selector["tag"], class_=selector["class"])
        
        if elemento_prezzo:
            testo_prezzo = elemento_prezzo.text.strip()
            prezzo_pulito = (
                testo_prezzo.replace("€", "")
                            .replace("EUR", "")
                            .replace(" ", "")
                            .replace(",", ".")
                            .replace("da", "")
                            .strip()
            )
            return prezzo_pulito
        return "N/D (Layout cambiato)"
    except Exception:
        # Se un sito va in errore, restituisce questa scritta invece di far fallire GitHub
        return "Errore Connessione"

def main():
    data_oggi = datetime.now().strftime("%Y-%m-%d")
    nuove_righe = []

    print("--- INIZIO MONITORAGGIO ---")

    for item in PRODOTTI_TARGET:
        print(f"Estrazione da {item['Rivenditore']}...")
        prezzo_rilevato = estrai_prezzo(item["Link"], item["Selector"])
        print(f"-> Risultato: {prezzo_rilevato}")
        
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
        time.sleep(4)

    # Scrittura finale protetta
    try:
        with open('prezzi.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for riga in nuove_righe:
                writer.writerow(riga)
        print("Scrittura completata!")
    except Exception as e:
        print(f"Errore scrittura CSV: {e}")

if __name__ == "__main__":
    main()
