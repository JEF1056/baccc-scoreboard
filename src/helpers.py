#ensure that config is passed
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config["allowed_extensions"] #rewrite this. this is embarassingly bad

def create_dir(path):
    try: os.makedirs(path)
    except: pass

def normalize_scores():
    pass