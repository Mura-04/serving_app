import os
import requests
from flask import Response, Flask

app = Flask(__name__)

RAILWAY_URL = "https://servingapp-production.up.railway.app/v1/models/sentiment-model"

@app.route('/')
def home():
    return "Exporter is running successfully!", 200

@app.route('/metrics')
def metrics():
    try:
        response = requests.get(RAILWAY_URL, timeout=5)
        data = response.json()
        
        model_status = 0
        if "model_version_status" in data:
            state = data["model_version_status"][0].get("state", "")
            if state == "AVAILABLE":
                model_status = 1

        metrics_output = f"""# HELP tensorflow_serving_model_available Status model sentiment (1 = Available, 0 = Down)
# TYPE tensorflow_serving_model_available gauge
tensorflow_serving_model_available{{model="sentiment-model",env="production"}} {model_status}
"""
        return Response(metrics_output, mimetype='text/plain')
    
    except Exception as e:
        error_metrics = """# HELP tensorflow_serving_model_available Status model sentiment
# TYPE tensorflow_serving_model_available gauge
tensorflow_serving_model_available{model="sentiment-model",env="production"} 0
"""
        return Response(error_metrics, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)