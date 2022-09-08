from flask_login import UserMixin
from .firestore_service import get_user

class UserData: # Con esta clase nos aseguramos que siempre vamos a tener la información que requerimos
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserModel(UserMixin):
    def __init__(self, user_data): # Cada que creemos un UserModel tenemos que pasarle un username y un password
        '''
        :param user_data: UserData
        '''
        self.id = user_data.username
        self.password = user_data.password

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.id,
            password=user_doc.to_dict()['password']
        )

        return UserModel(user_data)