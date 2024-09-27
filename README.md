# Document-Symbol-Extractor
Technical Description - English
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
