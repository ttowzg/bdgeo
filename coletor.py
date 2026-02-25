import requests
import psycopg2
from datetime import datetime

DB_HOST = "localhost"
DB_NAME = "sbdg_terremotos"
DB_USER = "postgres"
DB_PASS = "8624"

def fetch_and_insert_earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    response = requests.get(url)
    data = response.json()

    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()

    for feature in data['features']:
        eq_id = feature['id']
        mag = feature['properties']['mag']
        place = feature['properties']['place']
        time_ms = feature['properties']['time']
        
        if time_ms is not None:
            dt_object = datetime.fromtimestamp(time_ms / 1000.0)
        else:
            dt_object = datetime.now()
        
        coords = feature['geometry']['coordinates']
        lon = coords[0]
        lat = coords[1]
        depth = coords[2]

        sql = """
            INSERT INTO terremotos (id, magnitude, local, data_hora, profundidade, geom)
            VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
            ON CONFLICT (id) DO NOTHING;
        """
        cur.execute(sql, (eq_id, mag, place, dt_object, depth, lon, lat))

    conn.commit()
    cur.close()
    conn.close()
    print("Dados inseridos com sucesso!")

if __name__ == "__main__":
    fetch_and_insert_earthquakes()