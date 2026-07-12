import random
import string
import uuid

def get_random_string(len: int) -> str:

    allowed_characters = string.ascii_letters + string.digits
    random_str = ''.join(random.choice(allowed_characters) for _ in range(len))

    return random_str

def get_random_string_uuid4() -> str:
    return str(uuid.uuid4())