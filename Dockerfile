FROM python:3.9

##### Installing Chrome and Webdriver for Selenium

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmour -o /etc/apt/trusted.gpg.d/google-chrome.gpg


RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update

RUN apt-get install -y google-chrome-stable

RUN apt-get install -yqq unzip

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

##### Preparing the app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY ./test_scrapping.py /app/test_scrapping.py

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

RUN python3 -m unittest test_scrapping.py

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000