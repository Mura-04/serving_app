FROM tensorflow/serving:latest

# Salin folder model lokal ke dalam container
COPY ./model /models/sentiment-model

# Set environment variable untuk TensorFlow Serving
ENV MODEL_NAME=sentiment-model

# Menambahkan --monitoring_config_file agar bisa dipantau Prometheus
CMD tensorflow_model_server \
    --port=8500 \
    --rest_api_port=${PORT:-8501} \
    --model_name=$MODEL_NAME \
    --model_base_path=/models/$MODEL_NAME \
    --monitoring_config_file=/models/monitoring_config.txt