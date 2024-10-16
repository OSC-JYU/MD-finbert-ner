FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Ensure the virtual environment is activated by default
ENV PATH="/opt/venv/bin:$PATH"
#RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./api.py" ]
