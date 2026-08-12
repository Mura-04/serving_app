FROM tensorflow/serving:latest

COPY ./model /models/sentiment-model
COPY monitoring_config.txt /models/monitoring_config.txt

ENV MODEL_NAME=sentiment-model

CMD tensorflow_model_server \
    --port=8500 \
    --rest_api_port=${PORT:-8501} \
    --model_name=$MODEL_NAME \
    --model_base_path=/models/$MODEL_NAME \
    --monitoring_config_file=/models/monitoring_config.txt