import os
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from database_creation import get_db

app = Flask(__name__)
# Clé secrète (utiliser une variable d'environnement en production)
app.secret_key = os.environ.get('SECRET_KEY', 'cle_secrete_pour_le_dev')

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        # Récupération stricte des champs nécessaires (Green IT)
        g.user = db.execute('SELECT id, nom, email, role FROM user WHERE id = ?', (user_id,)).fetchone()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        password = request.form['mot_de_passe']
        
        if not email or not password or not nom:
            flash('Tous les champs sont requis.', 'error')
            return render_template('register.html')
            
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db = get_db()
        
        try:
            db.execute(
                'INSERT INTO user (nom, email, mot_de_passe) VALUES (?, ?, ?)',
                (nom, email, hashed_pw.decode('utf-8'))
            )
            db.commit()
            flash('Inscription réussie ! Vous pouvez vous connecter.', 'success')
            return redirect(url_for('login'))
        except db.IntegrityError:
            flash("L'email est déjà utilisé.", 'error')
            
    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['mot_de_passe']
        db = get_db()
        
        user = db.execute('SELECT id, mot_de_passe FROM user WHERE email = ?', (email,)).fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['mot_de_passe'].encode('utf-8')):
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
            
        flash('Email ou mot de passe incorrect.', 'error')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if g.user is None:
        return redirect(url_for('login'))
        
    db = get_db()
    page = request.args.get('page', 1, type=int)
    statut_filter = request.args.get('statut', 'tout')
    limit = 20
    offset = (page - 1) * limit
    
    query = 'SELECT id, titre, url, type, categorie, statut FROM ressource WHERE user_id = ?'
    params = [g.user['id']]
    
    if statut_filter != 'tout':
        query += ' AND statut = ?'
        params.append(statut_filter)
        
    query += ' ORDER BY date_ajout DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    
    ressources = db.execute(query, params).fetchall()
    
    return render_template('dashboard.html', ressources=ressources, page=page, current_filter=statut_filter)

@app.route('/resource/add', methods=('GET', 'POST'))
def add_resource():
    if g.user is None:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        titre = request.form['titre']
        url = request.form['url']
        type_res = request.form['type']
        categorie = request.form['categorie']
        
        if not titre or not url or not type_res:
            flash('Titre, URL et Type sont requis.', 'error')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO ressource (titre, url, type, categorie, statut, user_id) VALUES (?, ?, ?, ?, ?, ?)',
                (titre, url, type_res, categorie, 'à_faire', g.user['id'])
            )
            db.commit()
            flash('Ressource ajoutée avec succès.', 'success')
            return redirect(url_for('dashboard'))
            
    return render_template('add_resource.html')

@app.route('/resource/update_status/<int:id>', methods=('POST',))
def update_status(id):
    if g.user is None:
        return redirect(url_for('login'))
        
    nouveau_statut = request.form['statut']
    db = get_db()
    db.execute('UPDATE ressource SET statut = ? WHERE id = ? AND user_id = ?', (nouveau_statut, id, g.user['id']))
    db.commit()
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/resource/delete/<int:id>', methods=('POST',))
def delete_resource(id):
    if g.user is None:
        return redirect(url_for('login'))
        
    db = get_db()
    db.execute('DELETE FROM ressource WHERE id = ? AND user_id = ?', (id, g.user['id']))
    db.commit()
    flash('Ressource supprimée.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/profile', methods=('GET', 'POST'))
def profile():
    if g.user is None:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        nouveau_nom = request.form['nom']
        if nouveau_nom:
            db = get_db()
            db.execute('UPDATE user SET nom = ? WHERE id = ?', (nouveau_nom, g.user['id']))
            db.commit()
            flash('Profil mis à jour avec succès.', 'success')
            return redirect(url_for('profile'))
            
    return render_template('profile.html')

@app.route('/profile/delete', methods=('POST',))
def delete_profile():
    if g.user is None:
        return redirect(url_for('login'))
        
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (g.user['id'],))
    db.commit()
    session.clear()
    flash('Votre compte et toutes vos ressources ont été supprimés.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if g.user is None or g.user['role'] != 'Administrateur':
        flash('Accès refusé.', 'error')
        return redirect(url_for('index'))
        
    db = get_db()
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    
    utilisateurs = db.execute(
        'SELECT id, nom, email, role, date_inscription FROM user ORDER BY date_inscription DESC LIMIT ? OFFSET ?',
        (limit, offset)
    ).fetchall()
    
    return render_template('admin.html', utilisateurs=utilisateurs, page=page)

@app.route('/admin/delete_user/<int:id>', methods=('POST',))
def delete_user(id):
    if g.user is None or g.user['role'] != 'Administrateur':
        return redirect(url_for('index'))
        
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    flash('Utilisateur et ses ressources supprimés en cascade.', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)