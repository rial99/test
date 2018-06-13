from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username, password): #to create the token
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload): #jwt authentication
    user_id = payload['identity']
    return User.find_by_id(user_id)
