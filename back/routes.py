# routes.py
from flask import Flask, request, jsonify
from models import User, Audio, db
from utils import upload_to_supabase, transcribe_audio, get_supabase_file_url #Importation de la nouvelle fonction
from functools import wraps
import jwt
import datetime
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>

        if not token:
            return jsonify({'message': 'Token manquant!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token invalide!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Nouvel utilisateur créé!'})


@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth['email'] or not auth['password']:
        return jsonify({'message': 'Authentification requise'}), 401

    user = User.query.filter_by(email=auth['email']).first()

    if not user:
        return jsonify({'message': 'Utilisateur non trouvé'}), 401

    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({'user_id': user.id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({'message': 'Mot de passe incorrect'}), 401


@app.route('/audios', methods=['GET'])
@token_required
def get_audios(current_user):
    audios = Audio.query.filter_by(user_id=current_user.id).all()
    output = []
    for audio in audios:
        audio_data = {}
        audio_data['id'] = audio.id
        audio_data['filename'] = audio.filename
        audio_data['transcription'] = audio.transcription
        output.append(audio_data)

    return jsonify({'audios': output})


@app.route('/audio', methods=['POST'])
@token_required
def upload_audio(current_user):
    if 'audio' not in request.files:
        return jsonify({'message': 'Pas de fichier audio'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'message': 'Nom de fichier vide'}), 400

    audio_data = audio_file.read()
    filename = f"{current_user.id}_{datetime.datetime.now().isoformat()}.wav"  # Nom unique

    if upload_to_supabase(audio_data, filename):
        # Transcription (à mettre en tâche asynchrone !)
        transcription = transcribe_audio(audio_data) # peut prendre du temps!

        #Récupération de l'URL publique
        file_url = get_supabase_file_url(filename)

        # Enregistrement en base de données
        new_audio = Audio(filename=filename, transcription=transcription, user_id=current_user.id) #stocker le nom du fichier. L'url peut être reconstruite à partir de ça.
        db.session.add(new_audio)
        db.session.commit()

        return jsonify({'message': 'Audio téléversé et transcrit!', 'filename': filename, 'transcription': transcription, 'file_url': file_url}), 201
    else:
        return jsonify({'message': 'Erreur lors du téléversement vers Supabase'}), 500