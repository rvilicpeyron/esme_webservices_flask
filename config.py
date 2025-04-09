import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://myuser:mot_de_passe@localhost:5432/esme_inge')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
