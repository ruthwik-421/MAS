import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
import os
from dotenv import load_dotenv

# Import our agents and memory module
from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from agents.pdf_agent import PDFAgent
from memory.shared_memory import SharedMemory

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Multi-Agent System for Document Processing")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize shared memory
shared_memory = SharedMemory()

# Initialize agents
classifier_agent = ClassifierAgent(shared_memory)
json_agent = JSONAgent(shared_memory)
email_agent = EmailAgent(shared_memory)
pdf_agent = PDFAgent(shared_memory)

@app.get("/")
async def root():
    # Redirect to the static HTML page
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

@app.post("/process")
async def process_document(file: UploadFile = File(None), 
                          json_data: str = Form(None),
                          email_content: str = Form(None)):
    
    # Ensure at least one input is provided
    if not any([file, json_data, email_content]):
        raise HTTPException(status_code=400, detail="No input provided. Please provide a file, JSON data, or email content.")
    
    try:
        # If file is provided, read its content
        if file:
            content = await file.read()
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            # Process with classifier agent
            classification = classifier_agent.classify(content, file_extension)
            
            # Route to appropriate agent based on classification
            if classification['format'] == 'json':
                result = json_agent.process(content)
            elif classification['format'] == 'email':
                result = email_agent.process(content)
            elif classification['format'] == 'pdf':
                result = pdf_agent.process(content)
            else:  # Other formats would be handled here
                result = {"message": f"Processing {classification['format']} documents is not implemented yet."}
                
        # If JSON data is provided
        elif json_data:
            classification = classifier_agent.classify(json_data, '.json')
            result = json_agent.process(json_data)
            
        # If email content is provided
        elif email_content:
            classification = classifier_agent.classify(email_content, '.eml')
            result = email_agent.process(email_content)
        
        # Return the result along with classification
        return JSONResponse(content={
            "classification": classification,
            "result": result,
            "memory_id": shared_memory.get_last_entry_id()
        })
        
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.get("/memory/{entry_id}")
async def get_memory(entry_id: str):
    try:
        memory_entry = shared_memory.get_entry(entry_id)
        if not memory_entry:
            raise HTTPException(status_code=404, detail=f"Memory entry with ID {entry_id} not found")
        return memory_entry
    except Exception as e:
        logger.error(f"Error retrieving memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving memory: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting Multi-Agent System for Document Processing")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)