# MAS: Multi-Agent Document Processing System

MAS is a robust, LLM-powered, multi-agent document processor for PDFs, JSON, and Emails. It uses OpenAI LLMs for extraction and classification, with reliable fallback logic, and features a modern Streamlit UI (black/orange theme) for interactive use.

## Features

- **Multi-Agent Architecture:**
  - `PDFAgent`, `JSONAgent`, `EmailAgent`, and `ClassifierAgent` each handle their respective document types.
  - All agents use OpenAI LLMs for extraction/classification, with robust fallback to rule-based logic if LLMs are unavailable or fail.
- **PDF Extraction:**
  - Uses PyPDF2 for accurate text extraction before LLM processing.
- **Detailed Output:**
  - Agents return detailed, informative, and robust JSON outputs, including anomaly detection and structure warnings.
- **Modern UI:**
  - Streamlit app with a black/orange theme, tabbed interface for file upload, JSON, and email input.
  - Realistic sample data and easy-to-use interface.
- **FastAPI Backend:**
  - `/process` endpoint for unified document processing.
  - Streamlit UI and FastAPI backend can run together and connect seamlessly.
- **Sample Data:**
  - `data/sample_invoice.json`, `data/sample_invoice.pdf`, and `data/sample_email.eml` for testing and demonstration.

## Installation

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd MAS
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API key:**
   - Set the environment variable `OPENAI_API_KEY` before running the backend or UI.
   - Optionally, set `MAS_API_URL` to point the Streamlit UI to a remote backend.

## Usage

### 1. Start the FastAPI backend
```sh
uvicorn main:app --reload
```

### 2. Start the Streamlit UI (in a separate terminal)
```sh
streamlit run streamlit_app.py
```

- The UI will be available at [http://localhost:8501](http://localhost:8501)
- The backend runs at [http://localhost:8000/process](http://localhost:8000/process)

### 3. Process Documents
- **File Upload:** Upload PDF, JSON, or EML files via the UI.
- **Paste JSON:** Paste structured JSON data for extraction/classification.
- **Paste Email:** Paste raw email content (headers + body) for extraction.
- **Sample Data:** Use files in the `data/` folder for quick testing.

## Project Structure

- `main.py` — FastAPI backend
- `streamlit_app.py` — Streamlit UI
- `agents/` — Multi-agent logic (PDF, JSON, Email, Classifier)
- `data/` — Sample files
- `requirements.txt` — Python dependencies
- `README.md` — This documentation

## Requirements
See `requirements.txt` for all dependencies. Key packages:
- openai
- streamlit
- fastapi
- uvicorn
- requests
- PyPDF2

## Notes
- The system will fallback to rule-based extraction if LLMs are unavailable.
- For best results, ensure your OpenAI API key is valid and has sufficient quota.
- The UI and backend can be run on different machines; set `MAS_API_URL` as needed.

## License
MIT License