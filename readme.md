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
bash ./dockerfile/scissorfive-license-term-classifier/build_docker.sh

docker rm -f license-term-attr-classifier

docker run \
--name license-term-attr-classifier \
-p 8792:8555 \
-d --restart always \
license-term-attr-classifier:latest

docker logs -f -n 10 license-term-attr-classifier
```

## 验证APP是否正常启动

使用如下测试用例

```bash
bash -xe ./shells/test_example/test_demo1.sh
```

应当看到类似如下JSON输出

```json
{
    "code": 0,
    "data": [
        {
            "label": "CAN",
            "score": 0.9999476671218872,
            "name": "Use Patent Claims",
            "text": "The Licensor grants to the Licensee royalty-free, non-exclusive usage rights to any patents held by the Licensor, to the extent necessary to make use of the rights granted on the Work under this Licence."
        },
        {
            "label": "CAN NOT",
            "score": 0.9999679327011108,
            "name": "Use Trademark",
            "text": "under intellectual property rights (other than patent or trademark) Licensable by Initial Developer"
        }
    ],
    "msg": null,
    "runtime": 0.04
}
```