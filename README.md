#  Bajaj Finserv Qualifier 2  
#  Lab Report Extractor API

This FastAPI-based web service processes lab report images and extracts lab test names, values, and reference ranges using OCR (Tesseract).

##  Features

- Accepts lab report images via POST request
- Uses Tesseract OCR to extract text from the image
- Parses and returns structured lab test data
- Returns response in JSON format

##  Requirements

- Python 3.8+
- Tesseract OCR installed and available in system PATH

##  Setup Instructions

### 1. Clone the Repository

bash
git clone https://github.com/YOUR_USERNAME/lab-api.git
cd lab-api


### 2. Create Virtual Environment

bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate


### 3. Install Dependencies

bash
pip install -r requirements.txt


### 4. Install Tesseract OCR

#### Windows:
- Download and install Tesseract from:
  [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- Add Tesseract installation path (e.g., C:\Program Files\Tesseract-OCR) to your system PATH
- Or specify path manually in your code:
  python
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  

#### macOS:
bash
brew install tesseract


#### Ubuntu/Linux:
bash
sudo apt update
sudo apt install tesseract-ocr


---

## Run the Application

bash
uvicorn main:app --reload


Then open your browser and go to:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoint

### POST /get-lab-tests

#### Form Data:
- file: Image file (e.g., PNG or JPG of lab report)

#### Response Format:
json
{
  "is_success": true,
  "data": [
    {
      "test_name": "Hemoglobin",
      "value": "13.4",
      "unit": "g/dL",
      "reference_range": "13.0 - 17.0"
    },
    ...
  ]
}


#### Error Response Example:
json
{
  "is_success": false,
  "error": "Tesseract is not installed or it's not in your PATH"
}
