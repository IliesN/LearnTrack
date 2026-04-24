import sqlite3

DB_NAME = 'learntrack.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Permet d'accéder aux colonnes par leur nom
    conn.execute('PRAGMA foreign_keys = ON') # Active la suppression en cascade
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                mot_de_passe TEXT NOT NULL,
                role TEXT DEFAULT 'Utilisateur',
                date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS ressource (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                url TEXT NOT NULL,
                type TEXT NOT NULL,
                categorie TEXT,
                statut TEXT DEFAULT 'à_faire',
                date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
            );
            
            -- Index pour accélérer les requêtes fréquentes (Contrainte Green IT)
            CREATE INDEX IF NOT EXISTS idx_ressource_user_id ON ressource(user_id);
            CREATE INDEX IF NOT EXISTS idx_ressource_statut ON ressource(statut);
        ''')
    print("Base de données initialisée avec succès.")

if __name__ == '__main__':
    init_db()