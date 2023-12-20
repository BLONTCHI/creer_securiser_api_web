import pytest
import jwt
import inject
import datetime
from src.services.crypto_services import CryptoService
from src.config.api_configuration import ApiConfiguration
from src.model.user import User


@pytest.fixture
def fixture_api_configuration() -> ApiConfiguration:
    return ApiConfiguration("tests/ressources/test_configuration.yaml")


@pytest.fixture
def fixture_crypto_service(fixture_api_configuration):
    inject.clear_and_configure(lambda binder: binder.bind(ApiConfiguration, fixture_api_configuration))
    return CryptoService()


def test_hash_password(fixture_crypto_service):
    password = "XXXXXXXX"
    hashed_password = fixture_crypto_service.hash_password(password)
    assert hashed_password != password
    assert fixture_crypto_service.check_password(password, hashed_password) == True
    

# def test_check_password(fixture_crypto_service):
#     """Écrivez un test prouvant que la méthode check_password renvoie False 
#     si deux mots de passe différents sont utilisés."""
#     password = "XXXXXXXX"
#     hashed_password = fixture_crypto_service.hash_password(password)
#     assert fixture_crypto_service.check_password(password*2, hashed_password) == False
    
# Test pour vérifier que nous sommes capables de produire un JWT     
def test_create_jwt(fixture_crypto_service: CryptoService):
    user = User(email="xyz@mail.com", raw_password="azerty")
    jwt = fixture_crypto_service.create_jwt(user)
    assert jwt is not None
    
# Test pour vérifier que nous sommes capables de décoder un JWT valide
def test_validate_jwt(fixture_crypto_service: CryptoService):
    user = User(email="xyz@mail.com", raw_password="azerty", roles=["admin"])
    jwt = fixture_crypto_service.create_jwt(user)
    decoded_jwt = fixture_crypto_service.is_authenticated(jwt)
    assert decoded_jwt["iss"] == "https://MY_APP"
    assert decoded_jwt["sub"] == user.email
    
# Tester le décodage d'un JWT invalide
def test_refuse_expired_jwt(fixture_api_configuration: ApiConfiguration, fixture_crypto_service: CryptoService):
    user = User(email="xyz@mail.com", raw_password="azerty")
    encoded_jwt = jwt.encode(
        {
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(hours=6.0),
            "iss": "https://MY_APP",
            "aud": ["https://MY_APP/api"],
            "sub": user.email,
            "https://MY_APP/roles": ["admin"]
        },
        key=fixture_api_configuration.token_secret_key,
        algorithm="HS256").encode("utf-8")
    with pytest.raises(jwt.exceptions.ExpiredSignatureError):
        fixture_crypto_service.is_authenticated(encoded_jwt)
        
# Test de rejet d'un JWT avec tous les paramètres corrects mais encodé avec une clé incorrecte
def test_refuse_jwt_with_wrong_secret(fixture_crypto_service: CryptoService):
    user = User(email="xyz@mail.com", raw_password="azerty")
    encoded_jwt = jwt.encode(
        {
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=6.0),
            "iss": "MY_COMPANY",
            "aud": ["api.MY_COMPANY"],
            "sub": user.email,
            "MY_APP/roles": user.roles
        },
        key="bad_token",
        algorithm="HS256").encode("utf-8")

    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        fixture_crypto_service.is_authenticated(encoded_jwt)