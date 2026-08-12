FROM tensorflow/serving:latest

# Salin folder model lokal ke dalam container
COPY ./model /models/sentiment-model

# Set environment variable untuk TensorFlow Serving
ENV MODEL_NAME=sentiment-model

# Expose port yang digunakan Heroku (Heroku menggunakan port dinamis dari $PORT)
CMD tensorflow_model_server --port=$PORT --model_name=$MODEL_NAME --model_base_path=/models/$MODEL_NAME