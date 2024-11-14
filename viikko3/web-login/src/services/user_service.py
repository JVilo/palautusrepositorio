import re
from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository
)


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password, password_confirmation):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)
        if username == user:
            raise UserInputError("Usename allredy exists")
    
        
        pattern = re.compile("^[a-zA-Z]+$")

        if pattern.match(username) == False:
            raise UserInputError("Username can only contain letters a-z")
        
        if len(username)< 3:
            raise UserInputError("Username must be minimum of 3 letters")
        
        if len(password) < 8:
            raise UserInputError("Password must be minimum of 8 characters")
        
        if any(map(str.isdigit,password)) == False or any(map(str.isdigit,password_confirmation))== False:
            raise UserInputError("Password must contain atleast one special charracter")
        
        if password != password_confirmation or len(password_confirmation)!= len(password):
            raise UserInputError("password confirmation does not match")




user_service = UserService()
