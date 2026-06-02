from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# Service map config from environment variables
SERVICES = {
    'process': os.getenv('PROCESS_SERVICE_URL', 'http://localhost:5001'),
    'git': os.getenv('GIT_SERVICE_URL', 'http://localhost:5002'),
    'inspection': os.getenv('INSPECTION_SERVICE_URL', 'http://localhost:5003'),
    'testing': os.getenv('TESTING_SERVICE_URL', 'http://localhost:5004'),
}

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok", "service": "api-gateway"}

@app.route('/api/<service_name>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service_name, path):
    if service_name not in SERVICES:
        return {"error": "Service not found"}, 404

    url = f"{SERVICES[service_name]}/api/{service_name}/{path}"
    
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, headers)
    except requests.exceptions.RequestException as e:
        return {"error": "Service unavailable", "details": str(e)}, 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
