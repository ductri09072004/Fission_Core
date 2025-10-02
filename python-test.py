# Python Test API for Fission
import json
from datetime import datetime

def main(context=None):
    """Main function for Fission"""
    print("Python Test API called!")
    print("Request URL:", context.request.url)
    print("Request Method:", context.request.method)
    
    # Parse URL to determine endpoint
    url = context.request.url
    method = context.request.method
    
    # Route handling
    if url.endswith('/') or url.endswith('/python-test'):
        # Root endpoint
        response_data = {
            "message": "Hello World!",
            "status": "success", 
            "data": "Xin chào từ Python API!",
            "timestamp": datetime.now().isoformat(),
            "endpoint": "/"
        }
        
    elif '/api/hello' in url:
        # API Hello endpoint
        response_data = {
            "message": "Hello from API!",
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "endpoint": "/api/hello"
        }
        
    elif '/health' in url:
        # Health check endpoint
        response_data = {
            "status": "healthy",
            "service": "Python Test API",
            "timestamp": datetime.now().isoformat(),
            "endpoint": "/health"
        }
        
    else:
        # Default response
        response_data = {
            "message": "Python Test API",
            "status": "success",
            "available_endpoints": [
                "/",
                "/api/hello", 
                "/health"
            ],
            "usage": "Add endpoint to URL to test specific API",
            "timestamp": datetime.now().isoformat()
        }
    
    return {
        "status": 200,
        "body": json.dumps(response_data, ensure_ascii=False, indent=2),
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*"
        }
    }
