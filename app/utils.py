from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# for hashing passwords before storing in DB
def hash_password(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password_from_db):
    return pwd_context.verify(plain_password, hashed_password_from_db)