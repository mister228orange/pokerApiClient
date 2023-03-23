from config import cfg
import hashlib


def get_headers():
    enc_pass = hashlib.md5(cfg.PASSWORD.encode('utf-8')).hexdigest()
    key = enc_pass + cfg.API_KEY
    hash_api = hashlib.md5(key.encode('utf-8')).hexdigest()

    return {
        'Accept': 'application/json',
        'Username': cfg.EMAIL,
        'Password': hash_api,
        'User-Agent': 'Mozzila'
    }