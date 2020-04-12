FROM python:3-slim
LABEL Renan Rosa
WORKDIR /golden_leaf

COPY requirements.txt ./
RUN apt update && apt install -y python3-dev build-essential && apt install libffi-dev
RUN pip install pip --upgrade
RUN python -m pip --no-cache-dir install -r requirements.txt

COPY . .

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD [ " wsgi.py runserver" ]