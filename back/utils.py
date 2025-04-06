#utils.py
from supabase import create_client, Client
from config import Config
from io import BytesIO
import os

# Initialisation du client Supabase
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)


def upload_to_supabase(file_data, filename):
    """Uploads a file (passed as bytes) to Supabase Storage."""
    try:
        bucket_name = Config.SUPABASE_BUCKET_NAME if Config.SUPABASE_BUCKET_NAME else "default" # Assurez-vous que votre bucket existe dans Supabase
        res = supabase.storage.from_(bucket_name).upload(
            file=file_data,
            path=filename,
            file_options={"cacheControl": "3600", "contentType": "audio/wav"}  # Ajustez le contentType si nécessaire
        )
        if res.get('error') is not None:
            print(f"Erreur lors du téléversement vers Supabase: {res['error']}")
            return False
        else:
            return True
    except Exception as e:
        print(f"Erreur lors du téléversement vers Supabase: {e}")
        return False



def get_supabase_file_url(filename):
    """Returns the public URL of a file in Supabase Storage."""
    try:
        bucket_name = Config.SUPABASE_BUCKET_NAME if Config.SUPABASE_BUCKET_NAME else "default"
        # Utilisez get_public_url pour obtenir l'URL publique
        response = supabase.storage.from_(bucket_name).get_public_url(filename)
        return response
    except Exception as e:
        print(f"Erreur lors de la récupération de l'URL Supabase: {e}")
        return None


def transcribe_audio(audio_data):
    """Transcribe l'audio en utilisant SpeechRecognition (à adapter)."""
    # (Le code de transcription reste le même, vous pouvez le réutiliser)
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(BytesIO(audio_data)) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language="fr-FR")  # Adapter la langue
        return text
    except Exception as e:
        print(f"Erreur de transcription: {e}")
        return None