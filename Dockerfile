FROM python:3.7

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./data /data
COPY ./nero /nero
COPY ./run_nero.bash /run_nero.bash

CMD ["bash", "/run_nero.bash"]
