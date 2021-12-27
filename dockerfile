FROM python
COPY . /app/
WORKDIR /app
RUN python -m pip install -r requirements.txt

EXPOSE 8090

CMD [ "python" , '/app/ground_station/picWeb/main.py' ]
