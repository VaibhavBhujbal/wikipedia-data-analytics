FROM python:3.9.1
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

#ENTRYPOINT ["python"]
#CMD python app.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
