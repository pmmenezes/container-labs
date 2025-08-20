from flask import Flask, send_from_directory, jsonify, request
import os
import requests

app = Flask(__name__, static_folder='static', static_url_path='/static')

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend:5000')

@app.route('/')
def serve_index():
    # Mudança: usar '.' em vez de 'app' (já estamos no diretório /app)
    return send_from_directory('.', 'index.html')

@app.route('/api/data')
def proxy_data():
    try:
        print(f"Encaminhando requisição para: {BACKEND_URL}/data")
        response = requests.get(f"{BACKEND_URL}/data")
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão com o backend: {e}")
        return jsonify({"error": f"Não foi possível conectar ao backend: {str(e)}"}), 503
    except requests.exceptions.HTTPError as e:
        print(f"Backend retornou um erro HTTP: {e.response.status_code} - {e.response.text}")
        return jsonify({"error": f"Backend retornou um erro: {e.response.status_code} - {e.response.text}"}), e.response.status_code
    except Exception as e:
        print(f"Erro inesperado no proxy: {e}")
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500

@app.route('/<path:path>')
def serve_other_files(path):
    if path.startswith('static/'):
        return send_from_directory('.', path)
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)