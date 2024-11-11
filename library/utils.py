import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()

def get_fernet():
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        raise ValueError("ENCRYPTION_KEY is not set in environment")
    return Fernet(key.encode()) 


def encrypt_text(text):
    print(text,"shariq khan")
    fernet = get_fernet()
    return fernet.encrypt(text.encode()).decode()


def decrypt_text(encrypted_text):
    try:
        fernet = get_fernet()
        return fernet.decrypt(encrypted_text.encode()).decode()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None