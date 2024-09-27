# Document-Symbol-Extractor
Technical Description
This script automates the processing and analysis of symbols present in PDF documents. It is designed to extract images from PDF files, detect and analyze graphical symbols on the pages, and then store the results in a JSON file for further analysis. The workflow is divided into several stages:

1. PDF Processing
The script starts by converting each page of the PDF into an image using the pdf2image library. Each image is saved in an output directory specified by the user. For each image, the script proceeds to extract symbols.

2. Symbol Extraction
After converting the PDF pages to images, the symbol extraction process involves:

Grayscale conversion: The image is converted to grayscale to reduce visual noise and facilitate processing.
Contrast enhancement: Contrast is enhanced using the CLAHE technique.
Noise reduction: Non-Local Means denoising is applied to remove noise from the images.
Adaptive thresholding: Binary adaptive thresholding is used to separate symbols from the background.
Morphological operations: Opening and closing operations are performed to clean the image and remove small artifacts.
Contour detection: Contours of the symbols are detected and classified based on area and aspect ratio.
Each extracted symbol is analyzed using the ORB (Oriented FAST and Rotated BRIEF) algorithm to calculate keypoint descriptors. The symbols' images and their descriptors are saved.

3. Symbol Analysis
The extracted symbols' descriptors are reduced dimensionally using Principal Component Analysis (PCA) and clustered using the K-Means algorithm. The script:

Labels each symbol with a cluster based on its descriptors.
Provides statistics on symbols such as average, minimum, and maximum size.
Analyzes the frequency of clusters to determine recurring patterns in symbols.
4. JSON Database Update
The symbols and their related data are saved in a JSON file, which can be updated every time the script runs.

5. Script Execution
The script prompts the user for the path of the PDF file, the output directory for symbol images, and the path for the JSON database, then runs the entire process of extraction, analysis, and database update.

---

Descrizione Tecnica
Questo script consente l'elaborazione e l'analisi automatizzata dei simboli presenti nei documenti PDF. È progettato per estrarre immagini da file PDF, individuare e analizzare simboli grafici nelle pagine, e successivamente salvare i risultati in un file JSON per ulteriori analisi. Il flusso di lavoro dello script è suddiviso in diverse fasi:

1. Processamento del PDF
Lo script inizia convertendo ogni pagina del PDF in un'immagine utilizzando la libreria pdf2image. Ogni immagine viene salvata in una directory di output specificata dall'utente. Successivamente, per ogni immagine, viene eseguita l'estrazione dei simboli.

2. Estrazione dei Simboli
Dopo la conversione in immagini, il processo di estrazione dei simboli coinvolge:

Conversione in scala di grigi: L'immagine viene convertita in scala di grigi per ridurre il rumore visivo e facilitare l'elaborazione.
Miglioramento del contrasto: Un miglioramento del contrasto viene eseguito utilizzando la tecnica CLAHE.
Riduzione del rumore: Viene applicato il denoising basato su "Non-Local Means" per rimuovere il rumore dalle immagini.
Soglia adattiva: La sogliatura binaria adattiva è utilizzata per separare i simboli dallo sfondo.
Operazioni morfologiche: Operazioni di apertura e chiusura vengono eseguite per pulire ulteriormente l'immagine ed eliminare piccoli artefatti.
Trovare i contorni: I contorni dei simboli vengono rilevati e classificati in base all'area e al rapporto d'aspetto.
Ogni simbolo estratto viene analizzato con l'algoritmo ORB (Oriented FAST and Rotated BRIEF) per calcolare i descrittori delle caratteristiche chiave. Le immagini dei simboli e i loro descrittori vengono salvati.

3. Analisi dei Simboli
I descrittori dei simboli estratti vengono ridotti dimensionalmente utilizzando l'analisi delle componenti principali (PCA) e raggruppati in cluster tramite l'algoritmo di K-Means. Lo script:

Etichetta ogni simbolo con un cluster basato sui descrittori.
Fornisce statistiche sui simboli come la dimensione media, minima e massima.
Analizza la frequenza dei cluster per determinare l'occorrere di certi pattern nei simboli.
4. Aggiornamento del Database JSON
I simboli e i dati relativi a essi vengono salvati in un file JSON, che può essere aggiornato ogni volta che lo script viene eseguito.

5. Esecuzione dello Script
Lo script chiede all'utente il percorso del file PDF, la directory di output per le immagini dei simboli e il percorso del database JSON, quindi esegue l'intero processo di estrazione, analisi e aggiornamento del database.
