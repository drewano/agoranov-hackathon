# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clé_secrète_par_défaut'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    SUPABASE_BUCKET_NAME = os.environ.get('SUPABASE_BUCKET_NAME') # (optionnel, si vous voulez que ça soit paramétrable)
    
    GLADIA_API_KEY = os.environ.get('GLADIA_API_KEY') # Ajout de la clé API Gladia
