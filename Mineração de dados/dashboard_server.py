from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "monitoramento_bgp.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    conn = get_db_connection()
    try:
        # Pega as últimas 50 coletas
        rows = conn.execute('''
            SELECT * FROM coletas_bgp 
            ORDER BY id DESC 
            LIMIT 50
        ''').fetchall()
        
        # Estatísticas básicas
        stats = conn.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status_mitigacao LIKE '%Mitigada%' THEN 1 ELSE 0 END) as mitigados
            FROM coletas_bgp
        ''').fetchone()

        data = [dict(row) for row in rows]
        return jsonify({
            "status": "success",
            "data": data,
            "stats": {
                "total": stats['total'],
                "mitigados": stats['mitigados'],
                "percent_mitigado": round((stats['mitigados'] / stats['total'] * 100), 2) if stats['total'] > 0 else 0
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    print("Servidor rodando em http://localhost:5000")
    app.run(debug=True, port=5000)
