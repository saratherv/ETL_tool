FROM python:latest
WORKDIR /flow


ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt



RUN apt-get update && apt-get install -y firefox-esr

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -x geckodriver -zf geckodriver-v0.24.0-linux64.tar.gz -O > /usr/bin/geckodriver
RUN chmod +x /usr/bin/geckodriver
RUN rm geckodriver-v0.24.0-linux64.tar.gz


COPY prefectFlow.py prefectFlow.py
COPY scrape.py scrape.py
COPY db_querries.py db_querries.py

CMD ["python3", "-u", "prefectFlow.py"]