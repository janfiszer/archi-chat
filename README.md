# Archi-chat

## Context
GPT sometimes messes up with answering the question about construction law but this tool allows the user to prompt a model and get the answer with the context from 
[Polish construction law](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19940890414/U/D19940414Lj.pdf).

## Installation
# PDF Vector Database - Installation Guide

This project creates a vector database from PDF files using Google's Gemini embedding API and ChromaDB for semantic search.

## Prerequisites

- Python 3.12 or higher
- Git
- Google AI API key ([Get one here](https://docs.cloud.google.com/docs/authentication/api-keys))

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/janfiszer/archi-chat.git
cd your-repo-name
```

### 2. Create a Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure 

Configure files in `./config`. 
Most importantly: 
1. Google api key: `API_KEY` in `.config/local.py`
2. Input context file: `CONTEXT_FILEPATH` in `.config/paths.py` 

The other parameters are tuned for current application.   
Create a `.env` file in the project root directory or set your Google AI API key directly in the code:

```bash
# Option 1: Using .env file (recommended)
echo "GOOGLE_AI_API_KEY=your-api-key-here" > .env
```

Or edit `app.py` and replace:
```python
API_KEY = "your-google-ai-api-key-here"
```

### 5. Add Your PDF File

Place your PDF file in the project directory and update the path in `app.py`:

```python
PDF_PATH = "your-document.pdf"
```

### 6. Run the Application

```bash
python app.py
```


## Example usage

Input: 
```text
Czy na tablicy informacyjnej określa się adres inwestora?
```

Found context (the most similar chunk):
```text
1. Art. 45b. 1. Na tablicy informacyjnej określa się: 
1) 
rodzaj robót budowlanych i adres prowadzenia tych robót; 
2) 
datę i numer decyzji o pozwoleniu na budowę lub dokonanego zgłoszenia; 
3) 
organ wydający decyzję o pozwoleniu na budowę lub rozpatrujący zgłoszenie; 
4) 
nazwę i numer telefonu właściwego organu nadzoru budowlanego; 
5) 
imię i nazwisko lub nazwę i numer telefonu inwestora; 
6) 
imię i nazwisko oraz numer telefonu kierownika budowy. 
...
```
Answer:
```text
Na tablicy informacyjnej określa się imię i nazwisko lub nazwę oraz numer telefonu inwestora, ale nie adres inwestora.
```
