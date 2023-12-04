from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create(plain_string: str):
    return pwd_context.hash(plain_string)


def verify(plain_string, hashed_string):
    return pwd_context.verify(plain_string, hashed_string)
