FROM tensorflow/serving:latest

# Salin folder model lokal ke dalam container
COPY ./model /models/sentiment-model

# Set environment variable untuk TensorFlow Serving
ENV MODEL_NAME=sentiment-model

# TensorFlow Serving menggunakan --rest_api_port untuk HTTP/REST API.
# Di Railway, kita bisa menggunakan port default 8501 atau membaca dari variabel PORT jika disediakan.
EXPOSE 8501

# Jalankan TensorFlow Serving dengan port REST API 8501 (standar Railway / Docker container)
CMD tensorflow_model_server \
    --port=8500 \
    --rest_api_port=8501 \
    --model_name=$MODEL_NAME \
    --model_base_path=/models/$MODEL_NAME