# Simple Python API for Fission
import json
from datetime import datetime

def main():
    """Simple Python function for Fission"""
    print("Python Simple API called!")
    
    response_data = {
        "message": "Hello from Python API!",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "service": "Python Test API",
        "endpoints": [
            "GET / - Hello World",
            "GET /api/hello - Hello API", 
            "GET /health - Health Check"
        ]
    }
    
    return {
        "status": 200,
        "body": json.dumps(response_data, ensure_ascii=False, indent=2),
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*"
        }
    }
