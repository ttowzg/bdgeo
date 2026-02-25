# SBDG - Monitoramento Global de Terremotos  
Para executar este projeto, instale o Python, o PostgreSQL e a extensão PostGIS. Acesse o PostgreSQL, crie um banco de dados chamado sbdg_terremotos e execute o comando SQL abaixo:  


CREATE EXTENSION IF NOT EXISTS postgis;  
CREATE TABLE terremotos (id VARCHAR(50) PRIMARY KEY, magnitude NUMERIC, local VARCHAR(255), data_hora TIMESTAMP, profundidade NUMERIC, geom GEOMETRY(Point, 4326));   
CREATE INDEX idx_terremotos_geom ON terremotos USING GIST (geom);  

No VS Code, abra coletor.py e app.py, altere DB_PASS para a senha do seu banco e instale as dependências no terminal:  

pip install requests psycopg2-binary flask flask-cors  

Popule o banco de dados com as informações da API:  

python coletor.py  
Inicie a API:  

python app.py  
Mantenha o terminal rodando e abra o arquivo index.html diretamente no seu navegador para visualizar o mapa.
