FROM sptkl/cook:latest

COPY . /home/recipes/

WORKDIR /home/recipes/

RUN pip3 install -r requirements.txt

CMD ["./entrypoint.sh"]

EXPOSE 5000
