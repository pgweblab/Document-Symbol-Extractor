import os
import cv2
import json
import logging
import numpy as np
from pdf2image import convert_from_path
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PDFProcessor:
    def __init__(self, pdf_path, output_dir, json_db_path):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.json_db_path = json_db_path
        self.symbols = []

    def process_pdf(self):
        logging.info(f"Elaborazione del PDF: {self.pdf_path}")
        pages = convert_from_path(self.pdf_path)
        for i, page in enumerate(pages):
            page_path = os.path.join(self.output_dir, f'page_{i+1}.png')
            page.save(page_path, 'PNG')
            logging.info(f"Pagina {i+1} salvata: {page_path}")
            self.extract_symbols(page_path, i+1)

    def extract_symbols(self, image_path, page_num):
        logging.info(f"Estraendo simboli dalla pagina {page_num}")
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Miglioramento del contrasto
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)
        
        # Riduzione del rumore con Non-Local Means Denoising
        gray = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)
        
        # Sogliatura adattiva
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, blockSize=15, C=10)
        
        # Operazioni morfologiche per pulire l'immagine
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        # Trova i contorni
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        orb = cv2.ORB_create()
        symbol_count = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            if area < 50 or area > 5000:
                continue
            aspect_ratio = float(w)/h
            if aspect_ratio > 5 or aspect_ratio < 0.2:
                continue
            
            # Estrarre l'immagine del simbolo
            symbol = img[y:y+h, x:x+w]
            symbol_gray = gray[y:y+h, x:x+w]
            
            # Calcolo dei descrittori ORB
            keypoints, descriptors = orb.detectAndCompute(symbol_gray, None)
            
            # Salva l'immagine del simbolo
            symbol_path = os.path.join(self.output_dir, f'symbol_p{page_num}_s{symbol_count+1}.png')
            cv2.imwrite(symbol_path, symbol)
            
            # Aggiungi il simbolo alla lista
            self.symbols.append({
                'page': page_num,
                'symbol_id': f'p{page_num}_s{symbol_count+1}',
                'path': symbol_path,
                'position': {'x': x, 'y': y, 'width': w, 'height': h},
                'descriptors': descriptors.tolist() if descriptors is not None else None
            })
            symbol_count += 1
        
        logging.info(f"Estratti {symbol_count} simboli dalla pagina {page_num}")

    def analyze_symbols(self):
        logging.info("Analisi dei simboli estratti")
        
        # Raccolta dei descrittori
        descriptors_list = []
        symbol_indices = []
        for idx, symbol in enumerate(self.symbols):
            descriptors = symbol.get('descriptors')
            if descriptors is not None:
                descriptors_list.extend(descriptors)
                symbol_indices.extend([idx]*len(descriptors))

        if descriptors_list:
            # Riduzione della dimensionalità con PCA
            pca = PCA(n_components=10)
            descriptors_reduced = pca.fit_transform(descriptors_list)
            
            # Clustering dei descrittori
            kmeans = KMeans(n_clusters=10, random_state=42)
            labels = kmeans.fit_predict(descriptors_reduced)
            
            # Mappare le etichette ai simboli
            symbol_label_counts = {}
            for idx, label in zip(symbol_indices, labels):
                symbol_id = self.symbols[idx]['symbol_id']
                if symbol_id not in symbol_label_counts:
                    symbol_label_counts[symbol_id] = {}
                symbol_label_counts[symbol_id][label] = symbol_label_counts[symbol_id].get(label, 0) + 1
            
            # Assegnare l'etichetta più frequente a ciascun simbolo
            for symbol in self.symbols:
                symbol_id = symbol['symbol_id']
                if symbol_id in symbol_label_counts:
                    label_counts = symbol_label_counts[symbol_id]
                    most_common_label = max(label_counts, key=label_counts.get)
                    symbol['cluster_label'] = int(most_common_label)
                else:
                    symbol['cluster_label'] = None
            
            # Calcolare la frequenza di ciascun cluster
            cluster_freq = {}
            for symbol in self.symbols:
                label = symbol.get('cluster_label')
                if label is not None:
                    cluster_freq[label] = cluster_freq.get(label, 0) + 1
            
            logging.info("Frequenza dei cluster di simboli:")
            for label, freq in cluster_freq.items():
                logging.info(f"Cluster {label}: {freq} simboli")
        else:
            logging.info("Nessun descrittore estratto per l'analisi.")

        # Analisi delle dimensioni dei simboli
        symbol_sizes = [symbol['position']['width'] * symbol['position']['height'] for symbol in self.symbols]
        if symbol_sizes:
            avg_size = sum(symbol_sizes) / len(symbol_sizes)
            min_size = min(symbol_sizes)
            max_size = max(symbol_sizes)
            
            logging.info(f"Statistiche dei simboli:")
            logging.info(f"Numero totale di simboli: {len(self.symbols)}")
            logging.info(f"Dimensione media dei simboli: {avg_size:.2f} pixel")
            logging.info(f"Dimensione minima dei simboli: {min_size} pixel")
            logging.info(f"Dimensione massima dei simboli: {max_size} pixel")
        else:
            logging.info("Nessun simbolo estratto per l'analisi.")

    def update_json_db(self):
        logging.info("Aggiornamento del database JSON")
        if os.path.exists(self.json_db_path):
            with open(self.json_db_path, 'r') as f:
                db = json.load(f)
        else:
            db = {'symbols': []}
        
        # Preparare i simboli per il salvataggio (escludendo i descrittori)
        symbols_to_save = []
        for symbol in self.symbols:
            symbol_copy = symbol.copy()
            symbol_copy.pop('descriptors', None)
            symbols_to_save.append(symbol_copy)
        
        db['symbols'].extend(symbols_to_save)
        
        with open(self.json_db_path, 'w') as f:
            json.dump(db, f, indent=2)
        logging.info(f"Database JSON aggiornato: {self.json_db_path}")

    def run(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.process_pdf()
        self.analyze_symbols()
        self.update_json_db()
        logging.info("Elaborazione completata")

if __name__ == "__main__":
    # Specifica il percorso del PDF e la directory di output come parametri generali
    pdf_path = input("Inserisci il percorso del PDF da processare: ")
    output_dir = input("Inserisci la directory di output per i simboli estratti: ")
    json_db_path = input("Inserisci il percorso del file JSON per il database: ")
    
    processor = PDFProcessor(pdf_path, output_dir, json_db_path)
    processor.run()
