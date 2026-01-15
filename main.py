from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config.database import db
from models.user import User
from models.shipment import Shipment
from models.post import Post
from models.offer import Offer
import os
from dotenv import load_dotenv
import requests
from services.transport_service import get_transport_options

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    if not current_user.is_authenticated:
        # Usuario dummy para desarrollo
        dummy_user = User.query.filter_by(email='dev@example.com').first()
        if not dummy_user:
            dummy_user = User(
                name='Desarrollador',
                email='dev@example.com',
                company='TransportCo',
                country='Argentina',
                has_air=True,
                has_ship=False,
                has_truck=True,
                profile_pic='https://via.placeholder.com/40x40?text=Dev'
            )
            db.session.add(dummy_user)
            db.session.commit()
        login_user(dummy_user)
    
    posts = Post.query.order_by(Post.created_at.desc()).all()
    shipments = Shipment.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', posts=posts, shipments=shipments)

@app.route('/login')
def login():
    # Aquí irá la lógica de Google OAuth
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/auth/google')
def auth_google():
    google_client_id = os.getenv('GOOGLE_CLIENT_ID')
    redirect_uri = url_for('auth_google_callback', _external=True)
    scope = 'openid email profile'
    auth_url = f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={google_client_id}&redirect_uri={redirect_uri}&scope={scope}'
    return redirect(auth_url)

@app.route('/auth/google/callback')
def auth_google_callback():
    code = request.args.get('code')
    if not code:
        return redirect(url_for('login'))
    
    google_client_id = os.getenv('GOOGLE_CLIENT_ID')
    google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    redirect_uri = url_for('auth_google_callback', _external=True)
    
    # Exchange code for token
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': google_client_id,
        'client_secret': google_client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    
    if 'access_token' not in token_json:
        return redirect(url_for('login'))
    
    # Get user info
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {'Authorization': f'Bearer {token_json["access_token"]}'}
    user_response = requests.get(user_info_url, headers=headers)
    user_info = user_response.json()
    
    # Create or get user
    user = User.query.filter_by(google_id=user_info['id']).first()
    if not user:
        user = User(
            google_id=user_info['id'],
            name=user_info['name'],
            email=user_info['email'],
            profile_pic=user_info.get('picture', ''),
            company='Usuario Google',
            country='Desconocido'
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return redirect(url_for('index'))

@app.route('/login_as/<user_email>')
def login_as(user_email):
    user = User.query.filter_by(email=user_email).first()
    if user:
        login_user(user)
    return redirect(url_for('index'))

@app.route('/add_shipment', methods=['GET', 'POST'])
def add_shipment():
    if not current_user.is_authenticated:
        # Auto-login con user2 para desarrollo
        user2 = User.query.filter_by(email='user2@example.com').first()
        if not user2:
            user2 = User(
                name='María García',
                email='user2@example.com',
                company='Transportes XYZ',
                country='México',
                has_air=False,
                has_ship=True,
                has_truck=True,
                profile_pic='https://via.placeholder.com/40x40?text=MG'
            )
            db.session.add(user2)
            db.session.commit()
        login_user(user2)
    
    if request.method == 'POST':
        volume = request.form['volume']
        transport_mode = request.form['transport_mode']
        origin_country = request.form['origin_country']
        destination_country = request.form['destination_country']
        origin_port = request.form.get('origin_port')
        destination_port = request.form.get('destination_port')
        min_budget = request.form['min_budget']
        max_budget = request.form['max_budget']
        
        shipment = Shipment(
            user_id=current_user.id,
            volume=volume,
            transport_mode=transport_mode,
            origin_country=origin_country,
            destination_country=destination_country,
            origin_port=origin_port,
            destination_port=destination_port,
            min_budget=min_budget,
            max_budget=max_budget
        )
        db.session.add(shipment)
        db.session.commit()
        
        # Crear post automático con info del envío
        post_content = f"🚛 Nuevo envío: {volume}L de {origin_country} a {destination_country} por {transport_mode}"
        if origin_port:
            post_content += f" desde {origin_port}"
        if destination_port:
            post_content += f" hasta {destination_port}"
        post_content += f". Presupuesto: ${min_budget} - ${max_budget}"
        post = Post(content=post_content, user_id=current_user.id, shipment_id=shipment.id)
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('add_shipment.html')

@app.route('/get_transport_options')
def get_transport_options_route():
    mode = request.args.get('mode')
    country = request.args.get('country')
    options = get_transport_options(mode, country)
    return jsonify(options)

@app.route('/add_post', methods=['POST'])
def add_post():
    if not current_user.is_authenticated:
        # Auto-login con user2
        user2 = User.query.filter_by(email='user2@example.com').first()
        if not user2:
            user2 = User(
                name='María García',
                email='user2@example.com',
                company='Transportes XYZ',
                country='México',
                has_air=False,
                has_ship=True,
                has_truck=True,
                profile_pic='https://via.placeholder.com/40x40?text=MG'
            )
            db.session.add(user2)
            db.session.commit()
        login_user(user2)
    
    content = request.form['content']
    if content:
        post = Post(content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/search_users')
def search_users():
    query = request.args.get('q', '')
    if query:
        users = User.query.filter(
            (User.name.contains(query)) | 
            (User.company.contains(query)) |
            (User.email.contains(query))
        ).all()
    else:
        users = []
    return render_template('search_users.html', users=users, query=query)

@app.route('/shipment/<int:shipment_id>')
def shipment_detail(shipment_id):
    shipment = Shipment.query.get_or_404(shipment_id)
    offers = Offer.query.filter_by(shipment_id=shipment_id).order_by(Offer.created_at.desc()).all()
    last_offer = offers[0] if offers else None
    return render_template('shipment_detail.html', shipment=shipment, offers=offers, last_offer=last_offer)

@app.route('/make_offer/<int:shipment_id>', methods=['POST'])
def make_offer(shipment_id):
    if not current_user.is_authenticated:
        # Auto-login con user2
        user2 = User.query.filter_by(email='user2@example.com').first()
        if not user2:
            user2 = User(
                name='María García',
                email='user2@example.com',
                company='Transportes XYZ',
                country='México',
                has_air=False,
                has_ship=True,
                has_truck=True,
                profile_pic='https://via.placeholder.com/40x40?text=MG'
            )
            db.session.add(user2)
            db.session.commit()
        login_user(user2)
    
    shipment = Shipment.query.get_or_404(shipment_id)
    if shipment.user_id == current_user.id:
        # No permitir ofertar en tu propio envío
        return redirect(url_for('shipment_detail', shipment_id=shipment_id))
    
    amount = float(request.form['amount'])
    if amount < shipment.min_budget or amount > shipment.max_budget:
        # Oferta fuera de rango, redirigir sin crear
        return redirect(url_for('shipment_detail', shipment_id=shipment_id))
    
    offer = Offer(shipment_id=shipment_id, user_id=current_user.id, amount=amount)
    db.session.add(offer)
    db.session.commit()
    return redirect(url_for('shipment_detail', shipment_id=shipment_id))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Crear usuarios de ejemplo si no existen
        if not User.query.filter_by(email='user1@example.com').first():
            user1 = User(name='Juan Pérez', email='user1@example.com', company='Logistics SA', country='Chile', has_air=True, has_ship=True, has_truck=False, profile_pic='https://via.placeholder.com/40x40?text=JP')
            db.session.add(user1)
        if not User.query.filter_by(email='user2@example.com').first():
            user2 = User(name='María García', email='user2@example.com', company='Transportes XYZ', country='México', has_air=False, has_ship=True, has_truck=True, profile_pic='https://via.placeholder.com/40x40?text=MG')
            db.session.add(user2)
        if not User.query.filter_by(email='user3@example.com').first():
            user3 = User(name='Carlos López', email='user3@example.com', company='Global Shipping', country='Colombia', has_air=True, has_ship=True, has_truck=True, profile_pic='https://via.placeholder.com/40x40?text=CL')
            db.session.add(user3)
        db.session.commit()
        
        # Crear shipment de ejemplo si no existe
        if not Shipment.query.first():
            user1 = User.query.filter_by(email='user1@example.com').first()
            shipment = Shipment(
                user_id=user1.id,
                volume=1000,
                transport_mode='sea',
                origin_country='Chile',
                destination_country='Argentina',
                origin_port='Port of Valparaiso',
                destination_port='Port of Buenos Aires',
                min_budget=500,
                max_budget=1000
            )
            db.session.add(shipment)
            db.session.commit()
            
            post = Post(
                content="🚛 Nuevo envío: 1000L de Chile a Argentina por Mar desde Port of Valparaiso hasta Port of Buenos Aires. Presupuesto: $500 - $1000",
                user_id=user1.id,
                shipment_id=shipment.id
            )
            db.session.add(post)
            db.session.commit()
    app.run(debug=True)
