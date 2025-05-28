



# MessyDesk wrapper for Finbert-ner

https://huggingface.co/Kansallisarkisto/finbert-ner

Download pytorch_model.bin from  https://huggingface.co/Kansallisarkisto/finbert-ner/blob/main/pytorch_model.bin and place it to "finbert-ner-model" directory 


This requires Huggingface transformers, pytorch and syntok

## Python

	python -m venv .env
	source .env/bin/activate
	pip3 install -r requirements.txt
	pip3 install transformers syntok torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
	python api.py

Script uses syntok for splitting text to smaller chuncks. This means that start and end values does not match with the original text. Highlighting is therefore problematic.

## Container

	make build
	make start

## API call

curl -X POST -H "Content-Type: multipart/form-data" -F "request=@test/test.json;type=application/json"  -F "content=@test/sample.txt"  http://localhost:8600/process

