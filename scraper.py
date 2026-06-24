import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

# Intestazione per simulare una richiesta da un browser umano ed evitare blocchi di sicurezza
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
}

# Configurazione completa con tutti e 3 i prodotti estratti dal vostro database AURA Tracker
PRODOTTI_TARGET = [
    {
        "Brand": "The Ordinary",
        "Prodotto": "Niacinamide 10% + Zinc 1%",
        "Formato": "60ml",
        "Rivenditore": "Profumerie Galeazzi",
        "Link": "https://profumeriegaleazzi.it/products/niacinamide-10-zinc-1?variant=55978556260725",
        "Selector": {"tag": "span", "class": "price-item--sale"}
    },
    {
        "Brand": "CeraVe",
        "Prodotto": "Detergente Idratante",
        "Formato": "473ml",
        "Rivenditore": "XFarma",
        "Link": "https://www.xfarma.it/it/cerave-detergente-idratante-viso-pelle-da-normale-a-secca-i-acido-ialuronico-e-ceramidi-473ml.html",
        "Selector": {"tag": "span", "class": "price"}
    },
    {
        "Brand": "Cera di Cupra",
        "Prodotto": "Crema Idratante Opacizzante Per Pelli Miste O Grasse",
        "Formato": "50ml",
        "Rivenditore": "Filgi Store",
        "Link": "https://www.filgistore.it/it/creme-viso/4848-cera-di-cupra-ricette-di-miele-crema-idratante-opacizzante-pelli-miste-o-grasse-50-ml-8002140055508.html",
        "Selector": {"tag": "span", "class": "current-price"}
    }
]

def estrai_prezzo(url, selector):
    try:
        # Esegue la richiesta HTTP verso il sito web
        risposta = requests.get(url, headers=HEADERS, timeout=15)
        
        # Se il sito risponde con una protezione anti-bot o errore
        if risposta.status_code != 200:
            print(f" -> Errore di connessione (Codice: {risposta.status_code})")
            return "Errore Connessione"
        
        # Analizza la struttura HTML della pagina
        soup = BeautifulSoup(risposta.text, 'html.parser')
        elemento_prezzo = soup.find(selector["tag"], class_=selector["class"])
        
        if elemento_prezzo:
            testo_prezzo = elemento_prezzo.text.strip()
            
            # Algoritmo di pulizia: converte stringhe come "10,80 €" o " 3.89€ " in numeri decimali puri
            prezzo_pulito = (
                testo_prezzo.replace("€", "")
                            .replace("EUR", "")
                            .replace(",", ".")
                            .replace("da", "") # Rimuove eventuali scritte tipo "da 10,00"
                            .strip()
            )
            return prezzo_pulito
        
        print(" -> Tag HTML del prezzo non individuato.")
        return "N/D"
        
    except Exception as e:
        print(f" -> Errore durante lo scraping: {str(e)}")
        return f"Errore: Spia"

def main():
    # Rileva la data odierna nel formato standard dei vostri file (AAAA-MM-GG)
    data_oggi = datetime.now().strftime("%Y-%m-%d")
    nuove_righe = []

    print(f"=== AVVIO CRONJOB AURA TRACKER - DATA: {data_oggi} ===")

    # Ciclo automatico su tutti e 3 i prodotti configurati nella lista
    for item in PRODOTTI_TARGET:
        print(f"\nScraping in corso per: {item['Brand']} ({item['Formato']}) da {item['Rivenditore']}...")
        
        prezzo_rilevato = estrai_prezzo(item["Link"], item["Selector"])
        print(f" -> Risultato: {prezzo_rilevato}")
        
        # Compilazione della riga rispettando l'ordine esatto delle colonne della vostra tabella Excel
        riga = [
            data_oggi,
            item["Brand"],
            item["Prodotto"],
            item["Formato"],
            item["Rivenditore"],
            prezzo_rilevato,
            "Online",         # Status di default
            "E-commerce",     # Categoria Rivenditore di default
            item["Link"]
        ]
        nuove_righe.append(riga)
        
        # Politica di delay cortese: aspetta 3 secondi tra un sito e l'altro per evitare ban degli IP da parte dei server
        time.sleep(3) 

    # Apertura e scrittura sul database unico prezzi.csv (in modalità Append 'a')
    try:
        with open('prezzi.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for riga in nuove_righe:
                writer.writerow(riga)
        print("\n[SUCCESSO] Tutte le nuove rilevazioni sono state iniettate nel file prezzi.csv!")
    except Exception as e:
        print(f"\n[ERRORE] Impossibile scrivere sul file CSV: {str(e)}")

if __name__ == "__main__":
    main()