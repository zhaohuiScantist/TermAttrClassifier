# 许可证Term极性判断

描述：许可证Term文本，经过NLP方法判断极性。

# 接口文档
TODO

# 本地开发

## 依赖

```bash
conda create -n term_attr python=3.11
conda activate term_attr
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install -r requirements.txt
python app.py
```

# Docker部署

```bash
docker build -t term_attr .

docker rm -f term_attr

docker run \
--name term_attr \
-p 8791:8555 \
-d --restart always \
-v $PWD/model_dir:/code/model_dir \
term_attr:latest

docker logs -f -n 10 term_attr
```

## 验证APP是否正常启动

使用如下测试用例

```bash
bash -xe ./shells/test_example/test_demo1.sh 127.0.0.1 8792
```

应当看到类似如下JSON输出

```json

```