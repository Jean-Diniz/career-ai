-- Migration script for Career AI integration
-- Execute este script no banco de dados para criar as novas tabelas

-- Adicionar coluna user_id na tabela diagnostics (se não existir)
ALTER TABLE diagnostics 
ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id),
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();

-- Alterar tipo da coluna diagnostic para TEXT
ALTER TABLE diagnostics 
ALTER COLUMN diagnostic TYPE TEXT;

-- Criar tabela study_trails
CREATE TABLE IF NOT EXISTS study_trails (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_study_trails_user_id ON study_trails(user_id);
CREATE INDEX IF NOT EXISTS idx_study_trails_created_at ON study_trails(created_at);
CREATE INDEX IF NOT EXISTS idx_diagnostics_user_id ON diagnostics(user_id);
CREATE INDEX IF NOT EXISTS idx_diagnostics_created_at ON diagnostics(created_at);

-- Verificar se as tabelas foram criadas
SELECT 'study_trails' as table_name, count(*) as row_count FROM study_trails
UNION ALL
SELECT 'diagnostics' as table_name, count(*) as row_count FROM diagnostics
UNION ALL
SELECT 'users' as table_name, count(*) as row_count FROM users; 