FROM sptkl/cook:latest

ARG PORT=5000

COPY . /home/recipes/

WORKDIR /home/recipes/

RUN pip3 install -r requirements.txt

CMD ["./entrypoint.sh"]

EXPOSE ${PORT}
