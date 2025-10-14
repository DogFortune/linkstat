FROM gcr.io/distroless/python3-debian12:latest

WORKDIR /app
COPY src/ .

CMD [ "app.py" ]