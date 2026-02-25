from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

DB_HOST = "localhost"
DB_NAME = "sbdg_terremotos"
DB_USER = "postgres"
DB_PASS = "8624"

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route('/api/terremotos', methods=['GET'])
def get_terremotos():
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """
        SELECT id, magnitude, local, data_hora, profundidade, ST_AsGeoJSON(geom)::json AS geometria
        FROM terremotos;
    """
    cur.execute(sql)
    linhas = cur.fetchall()
    
    features = []
    for linha in linhas:
        feature = {
            "type": "Feature",
            "properties": {"id": linha[0], "magnitude": float(linha[1]) if linha[1] else 0, "local": linha[2], "data_hora": str(linha[3]), "profundidade": float(linha[4]) if linha[4] else 0},
            "geometry": linha[5] 
        }
        features.append(feature)
        
    cur.close()
    conn.close()
    return jsonify({"type": "FeatureCollection", "features": features})

@app.route('/api/terremotos/raio', methods=['GET'])
def get_terremotos_raio():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    raio_km = request.args.get('raio', default=1000, type=float)
    raio_metros = raio_km * 1000

    conn = get_db_connection()
    cur = conn.cursor()
    
    sql = """
        SELECT id, magnitude, local, data_hora, profundidade, ST_AsGeoJSON(geom)::json AS geometria
        FROM terremotos
        WHERE ST_DWithin(
            geom::geography, 
            ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, 
            %s
        );
    """
    cur.execute(sql, (lon, lat, raio_metros))
    linhas = cur.fetchall()
    
    features = []
    for linha in linhas:
        feature = {
            "type": "Feature",
            "properties": {"id": linha[0], "magnitude": float(linha[1]) if linha[1] else 0, "local": linha[2], "data_hora": str(linha[3]), "profundidade": float(linha[4]) if linha[4] else 0},
            "geometry": linha[5] 
        }
        features.append(feature)
        
    cur.close()
    conn.close()
    return jsonify({"type": "FeatureCollection", "features": features})

if __name__ == '__main__':
    app.run(debug=True, port=5000)