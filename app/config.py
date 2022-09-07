import uuid

HEX_SEC_KEY = uuid.uuid4().hex

class Config:
    SECRET_KEY = 'HEX_SEC_KEY'