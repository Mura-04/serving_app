import os
import time
import requests
from flask import Response, Flask

app = Flask(__name__)

# URL Railway TensorFlow Serving kamu
RAILWAY_URL = "https://servingapp-production.up.railway.app/v1/models/sentiment-model"

@app.route('/metrics')
def metrics():
    try:
        # Ambil data JSON dari Railway
        response = requests.get(RAILWAY_URL, timeout=5)
        data = response.json()
        
        # Cek status model dari JSON response
        model_status = 0
        if "model_version_status" in data:
            state = data["model_version_status"][0].get("state", "")
            if state == "AVAILABLE":
                model_status = 1

        # Format ke teks standar Prometheus (OpenMetrics)
        metrics_output = f"""# HELP tensorflow_serving_model_available Status model sentiment (1 = Available, 0 = Down)
# TYPE tensorflow_serving_model_available gauge
tensorflow_serving_model_available{{model="sentiment-model",env="production"}} {model_status}
"""
        return Response(metrics_output, mimetype='text/plain')
    
    except Exception as e:
        # Jika gagal fetch ke Railway
        error_metrics = """# HELP tensorflow_serving_model_available Status model sentiment
# TYPE tensorflow_serving_model_available gauge
tensorflow_serving_model_available{model="sentiment-model",env="production"} 0
"""
        return Response(error_metrics, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)