import os
import uuid
import json
from flask import Flask, request, jsonify, send_file
from argparse import ArgumentParser
from transformers import pipeline
import syntok.segmenter as segmenter

# This adds the MessyDeskAPI endpoint to Finbert-ner via transformers 


model_checkpoint = "Kansallisarkisto/finbert-ner"
token_classifier = pipeline(
    "token-classification", model=model_checkpoint, aggregation_strategy="simple"
)

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

OUTPUT_FOLDER = 'output'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


@app.route('/', methods=['GET'])
def root():
    return 'finbert-ner API for MessyDesk'

@app.route('/process', methods=['POST'])
def process_files():
    # Check if files are present in the request
    if 'request' not in request.files or 'content' not in request.files:
        return jsonify({'error': 'JSON file and image file are required'}), 400
    
    json_file = request.files['request']
    text_file = request.files['content']

    # Check if the file is empty
    if json_file.filename == '' or text_file.filename == '':
        return jsonify({'error': 'Empty file submitted'}), 400

    # Predict
    try:
        output_id = str(uuid.uuid4())
        text = text_file.read().decode('utf-8')
        sentences = split_into_sentences(text)
        predictions = token_classifier(sentences)
        print(predictions)
        # concat predictions to one array
        predictions = [item for sublist in predictions for item in sublist]
        with open(os.path.join(OUTPUT_FOLDER, output_id + '.ner.json'), "w") as file:
            json.dump(str(predictions), file, indent=4)



    except Exception as e:
        return jsonify({'error': 'Predictions failed: {}'.format(str(e))}), 500

    return jsonify({'response':{'type': 'stored', 'uri': ['/files/' + output_id + '.ner.json']}}), 200


# endpoint to serve files
@app.route('/files/<path:filename>', methods=['GET'])       
def serve_file(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return jsonify({'error': 'File not found'}), 404



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


if __name__ == '__main__':
    app.run(debug=True, port=8600)

