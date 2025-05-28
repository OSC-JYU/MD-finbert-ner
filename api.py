import os
import uuid
import json
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from typing import List
from transformers import pipeline
import syntok.segmenter as segmenter
import re

# This adds the MessyDeskAPI endpoint to Finbert-ner via transformers 

model_checkpoint = "./finbert-ner-model"
token_classifier = pipeline(
    "token-classification", model=model_checkpoint, aggregation_strategy="simple"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

OUTPUT_FOLDER = 'output'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.get("/")
def root():
    return 'finbert-ner API for MessyDesk'

@app.post("/process")
async def process_files(
    request: UploadFile = File(...),
    content: UploadFile = File(...)
):
    # Check if files are present in the request
    if not request or not content:
        raise HTTPException(status_code=400, detail='JSON file and text file are required')

    if request.filename == '' or content.filename == '':
        raise HTTPException(status_code=400, detail='Empty file submitted')

    try:
        output_id = str(uuid.uuid4())
        text = (await content.read()).decode('utf-8')
        sentences = split_text_into_chunks(text, 4000)
        predictions = token_classifier(sentences)
        # concat predictions to one array and adjust "start" and "end" values so that they match the original text
        output = []
        offset = 0
        for idx, p in enumerate(predictions):
            for w in p:
                # Convert numpy float32 values to native Python float
                for key, value in w.items():
                    if isinstance(value, np.float32):
                        w[key] = float(value)
                    elif isinstance(value, np.int32):
                        w[key] = int(value)
                # Adjust "start" and "end" values
                w['start'] = w['start'] + offset 
                w['end'] = w['end'] + offset
                output.append(w)
            offset += len(sentences[idx]) 
        with open(os.path.join(OUTPUT_FOLDER, output_id + '.ner.json'), "w") as file:
            json.dump(output, file, indent=4)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Predictions failed: {str(e)}')
    return JSONResponse(status_code=200, content={'response':{'type': 'stored', 'uri': ['/files/' + output_id + '.ner.json']}})

@app.get("/files/{filename:path}")
def serve_file(filename: str, background_tasks: BackgroundTasks):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail='File not found')

    def remove_file(path):
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error deleting file {path}: {e}")

    background_tasks.add_task(remove_file, file_path)
    return FileResponse(file_path, background=background_tasks)


def split_text_into_chunks(text, max_length=200):
    #split text to lines
    text = text.splitlines(True)
    chunks = []
    current_chunk = ""

    for line in text:
        # If adding this sentence to the current chunk would exceed the max_length,
        # then save the current chunk and start a new one.
        if len(current_chunk) + len(line) > max_length:  # +1 for space/newline between sentences
            chunks.append(current_chunk)
            current_chunk = line
        else:
            # Add the sentence to the current chunk
            current_chunk += line
    # Add the last chunk if there's any leftover content
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def split_text_into_chunks_old(text, max_length=200):
    # Split the text into sentences using a regex that matches sentence endings.
    sentence_endings = re.compile(r'(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=\\.|\\?)\\s')
    sentences = sentence_endings.split(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        # If adding this sentence to the current chunk would exceed the max_length,
        # then save the current chunk and start a new one.
        if len(current_chunk) + len(sentence) + 1 > max_length:  # +1 for space/newline between sentences
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            # Add the sentence to the current chunk
            current_chunk += " " + sentence
    # Add the last chunk if there's any leftover content
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def split_into_sentences(text):
    count = 0
    chuncks = []
    chunk = []
    sentences = segmenter.analyze(text)
    for sentence in sentences:
        for token in sentence:
            sentence_str = []
            for t in token:
                if(t.value != ',' and t.value != '.'):
                    count+=1
                sentence_str.append(t.value)            
            print(count)
            chunk.append(" ".join(sentence_str))
            if count > 120:
                chuncks.append(" ".join(chunk))
                count = 0
                chunk = []
    chuncks.append(" ".join(chunk))
    return chuncks


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8600) 
