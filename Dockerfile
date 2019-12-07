FROM python:3.7
LABEL maintainer zengzhengrong(bhg889@163.com)

WORKDIR /api
COPY . /api
ENV TZ='Asia/Shanghai'
RUN pip install -r requirements.txt

RUN python populate.py

ENTRYPOINT ["python","run.py"]