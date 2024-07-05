



# MessyDesk wrapper for Finbert-ner


This requires Huggingface transformers, pytorch and syntok

	python -m venv .env
	source .env/bin/activate
	pip3 install transformers syntok torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
	python api.py



Note: no Dockerfile yet

## API call

curl -X POST -H "Content-Type: multipart/form-data" -F "request=@test/test.json;type=application/json"  -F "content=@test/sample.txt"  http://localhost:8600/process

