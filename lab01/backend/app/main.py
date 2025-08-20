from flask import Flask, jsonify
import os
import psycopg2
import time

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')

def get_db_connection():
    conn = None
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Conexão com o banco de dados estabelecida com sucesso!")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Erro ao conectar ao banco de dados: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)
            retries -= 1
    raise Exception("Não foi possível conectar ao banco de dados após várias tentativas.")


@app.route('/')
def home():
    return "Backend está funcionando!"

@app.route('/data')
def get_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                text VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

        new_message = f"Olá do backend! Hora: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}"
        cur.execute("INSERT INTO messages (text) VALUES (%s) RETURNING id;", (new_message,))
        message_id = cur.fetchone()[0]
        conn.commit()

        cur.execute("SELECT text, created_at FROM messages ORDER BY id DESC LIMIT 1;")
        latest_message, created_at = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({
            "message": latest_message,
            "inserted_id": message_id,
            "timestamp": created_at.isoformat()
        })
    except Exception as e:
        print(f"Erro na rota /data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)