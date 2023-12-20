import bcrypt
import jwt
import inject
import datetime
from src.model.user import User
from src.config.api_configuration import ApiConfiguration


class CryptoService:
    
    config: ApiConfiguration = inject.attr(ApiConfiguration) # injection d'un objet ApiConfiguration dans CryptoService
    
    def hash_password(self, raw_password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        return hashed_password
    
    def check_password(self, raw_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password)
    
    
    def create_jwt(self, user: User) -> str:
        # JWT are encoded JSON objects that assert user identity and privileges. They contain 
        # a header (algorithm used to encode the token) and a payload (information about the user) and 
        # signature (to prevent tampering). The signature is generated using the secret key only known by the API
        return jwt.encode(
            payload={
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=6.0),
            "iss": "https://MY_APP",
            "aud": ["https://MY_APP/api"],
            "sub": user.email,
            "https://MY_APP/roles": user.roles,
            },
            key=self.config.token_secret_key,
            algorithm="HS256"
        ).encode("utf-8")
        
        
    def is_authenticated(self, encoded_jwt: str) -> bool:
        return jwt.decode(encoded_jwt, self.config.token_secret_key, 
                          audience="https://MY_APP/api", algorithms=["HS256"],
                          options={"require": ["exp", "iss", "aud", "https://MY_APP/roles"]})
        