



# MessyDesk wrapper for Finbert-ner


This requires Huggingface transformers, pytorch and syntok

	python -m venv .env
	source .env/bin/activate
	pip3 install transformers syntok torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
	python api.py

Script uses syntok for splitting text to smaller chuncks. This means that start and end values does not match with the original text. Highlighting is therefore problematic.

Note: no Dockerfile yet

## API call

curl -X POST -H "Content-Type: multipart/form-data" -F "request=@test/test.json;type=application/json"  -F "content=@test/sample.txt"  http://localhost:8600/process

