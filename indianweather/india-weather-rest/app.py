import warnings
from flask import Flask, jsonify
import bl
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Suppress specific warning about in-memory storage
warnings.filterwarnings("ignore", category=UserWarning, message="Using the in-memory storage for tracking rate limits as no storage was explicitly specified.")

# Load environment variable rate limits with defaults
RATE_LIMIT_DAILY = os.getenv('RATE_LIMIT_DAILY', '20')
RATE_LIMIT_HOURLY = os.getenv('RATE_LIMIT_HOURLY', '10')

app = Flask(__name__)

# Initialize Limiter with in-memory storage (for testing)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[f"{RATE_LIMIT_DAILY} per day", f"{RATE_LIMIT_HOURLY} per hour"]
)

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": "The requested resource could not be found"}), 404

@app.route('/station/<string:id>')
@limiter.limit(f"{RATE_LIMIT_HOURLY} per hour")
def get_station(id):
    try:
        if id == 'all':
            result = bl.get_all_stations()
        else:
            result = bl.get_station_by_id(int(id))
        return jsonify(result), result.get('code', 200)
    except ValueError:
        return jsonify({"error": "Invalid station ID format"}), 400
    except Exception as e:
        return jsonify({"error": "Error retrieving station data", "message": str(e)}), 500

@app.route('/weather/<int:id>')
@limiter.limit(f"{RATE_LIMIT_HOURLY} per hour")
def get_station_weather(id):
    try:
        result = bl.get_station_weather(id)
        return jsonify(result), result.get('code', 200)
    except Exception as e:
        return jsonify({"error": "Error retrieving weather data", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1875)
    # waitress.serve(app, host='0.0.0.0', port=1875)
