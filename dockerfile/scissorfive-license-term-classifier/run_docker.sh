docker run \
--name scissorfive-license-term-classifier \
-p 8792:8555 \
-d --restart always \
-v $PWD/logs:/code/logs \
scissorfive-license-term-classifier:latest
