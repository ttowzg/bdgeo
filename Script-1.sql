-- Habilita a extensão geográfica no banco de dados
CREATE EXTENSION IF NOT EXISTS postgis;

-- Cria a tabela para armazenar os dados dos terremotos
CREATE TABLE terremotos (
    id VARCHAR(50) PRIMARY KEY,       
    magnitude NUMERIC,                
    local VARCHAR(255),               
    data_hora TIMESTAMP,              
    profundidade NUMERIC,             
    geom GEOMETRY(Point, 4326)        
);

-- Cria um índice espacial para deixar as buscas mais rápidas
CREATE INDEX idx_terremotos_geom ON terremotos USING GIST (geom);