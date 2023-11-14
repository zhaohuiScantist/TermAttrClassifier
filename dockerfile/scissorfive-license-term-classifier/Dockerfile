FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /code

ADD requirements.txt .
RUN pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

ADD . .

EXPOSE 8555

ENTRYPOINT ["bash", "predict.sh"]
