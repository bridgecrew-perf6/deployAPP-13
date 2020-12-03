FROM python:3.7.5
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt install libgomp1
EXPOSE 9099
COPY . /.
CMD ["python","app.py"]