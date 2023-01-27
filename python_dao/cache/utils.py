import hashlib
import pickle


def create_key(*args, **kwargs) -> str:
    key = hashlib.sha256(b'')
    for arg in args:
        key = key.update(pickle.dumps(arg))

    for name, value in kwargs.items():
        key = key.update(pickle.dumps(name))
        key = key.update(pickle.dumps(value))

    return key.hexdigest()

