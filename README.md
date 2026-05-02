# LearnTrack

**LearnTrack** est un service web de gestion de ressources pédagogiques personnelles (articles, vidéos, cours, livres). Conçu pour les étudiants et les autodidactes, il permet d'ajouter, d'organiser et de suivre l'état de ses apprentissages de manière centralisée. Pensé selon les principes stricts du Green IT, l'outil se veut sobre, rapide, sans distraction, et respectueux des données (zéro cookie, zéro traceur).

**URL du site déployé :** [https://learntrack-zw6c.onrender.com/](https://learntrack-zw6c.onrender.com/)
**Lien du repository GitHub :** [https://github.com/IliesN/LearnTrack](https://github.com/IliesN/LearnTrack)

---

## Équipe et Rôles

Ce projet a été réalisé dans le cadre du module "Numérique Durable (TI616)" par :

* **Ismaël RADOUANE :** Base de données & Authentification (Back-end)
* **Ilies NASR :** Back-end, routes et CRUD des Ressources
* **Tim NGUYEN--MENU :** Front-end & Intégration
* **Yanis OUAHAB :** Administration (Back-end/Front-end)
* **Kêmi PADONOU :** Qualité, tests, documentation et déploiement

---

## Stack Technique & Justification Green IT

| Technologie | Composant | Justification Éco-responsable |
| :--- | :--- | :--- |
| **HTML5 / CSS3** | Front-end | Zéro framework (pas de Bootstrap/Tailwind). Aucune dépendance npm. Poids de la page réduit à l'essentiel (< 50 Ko). |
| **JS Vanilla** | Front-end | Utilisation native, sans bibliothèque lourde type React ou Vue. |
| **Python 3 / Flask** | Back-end | Micro-framework léger et rapide, sans surcharge inutile de dépendances. |
| **SQLite** | Base de données | Base de données embarquée dans un fichier unique, ne nécessitant aucun serveur tiers lourd pour cette volumétrie. |
| **Polices système** | Interface | Évite les requêtes HTTP externes coûteuses en bande passante vers Google Fonts. |
| **Render** | Déploiement | Hébergement cloud optimisé (Bilan carbone réduit). |

---

## Installation et Lancement Local

Pour tester le projet sur votre machine, suivez ces étapes :

**1. Cloner le dépôt :**
```bash
git clone [https://github.com/IliesN/LearnTrack](https://github.com/IliesN/LearnTrack)
cd LearnTrack
```

**2. Créer et activer un environnement virtuel (recommandé) :**
```bash
# Sur Windows :
python -m venv venv
venv\Scripts\activate

# Sur macOS / Linux :
python3 -m venv venv
source venv/bin/activate
```

**3. Installer les dépendances :**
```bash
pip install -r requirements.txt
```

**4. Initialiser la base de données :**
Cette commande va créer le fichier `learntrack.db` et construire les tables nécessaires.
```bash
python database_creation.py
```

**5. Lancer l'application :**
```bash
python app.py
```
Le site sera accessible localement à l'adresse : `http://127.0.0.1:5000`

---

## Structure du dépôt

```text
LearnTrack/
├── app.py                   # Point d'entrée de l'application et logique serveur (routes)
├── database_creation.py     # Script d'initialisation de la base SQLite et création des tables
├── learntrack.db            # Fichier de la base de données locale (généré localement)
├── requirements.txt         # Liste des dépendances Python (Flask, bcrypt, gunicorn)
├── .gitignore               # Fichiers ignorés par Git (venv, .db, .env, etc.)
├── README.md                # Documentation principale
├── docs/
│   ├── Rapport_LearnTrack.pdf # Rapport de projet final (Conception, Tests, Empreinte Carbone)
│   └── Diagrammes/          # Diagrammes UML et maquettes (Livrable 1)
├── static/
│   └── css/
│       └── style.css        # Feuille de style unique et minimaliste
└── templates/               # Vues HTML (Jinja2)
    ├── base.html            # Layout principal (Header, Footer, Navigation)
    ├── index.html           # Page d'accueil
    ├── login.html           # Page de connexion
    ├── register.html        # Page d'inscription
    ├── dashboard.html       # Tableau de bord des ressources
    ├── add_resource.html    # Formulaire d'ajout
    ├── profile.html         # Gestion du compte
    └── admin.html           # Interface d'administration
```

---

## Documentation

L'ensemble de la conception (UML, architecture), des choix techniques, ainsi que l'analyse des tests de performance (EcoIndex, Website Carbon) sont disponibles dans notre rapport final

[Lien du rapport](https://github.com/IliesN/LearnTrack/blob/main/docs/Green_IT_Livrable_2.pdf)
