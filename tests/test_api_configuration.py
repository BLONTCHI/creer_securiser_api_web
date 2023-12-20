import pytest
import os
from src.config.api_configuration import ApiConfiguration

# Le décorateur @pytest.fixture fourni par la bibliothèque pytest,
# gère automatiquement l'injection des fixtures dans les méthodes de test
@pytest.fixture
def fixture_api_configuration() -> ApiConfiguration:
    return ApiConfiguration("tests/ressources/test_configuration.yaml")

@pytest.fixture
def fixture_api_configuration_with_env() -> ApiConfiguration:
    os.environ["MY_TOKEN"] = "this_is_a_token_in_env"
    return ApiConfiguration("tests/ressources/test_configuration_env.yaml")


def test_parameter_loading(fixture_api_configuration: ApiConfiguration):
    assert fixture_api_configuration.token_secret_key == "hello"

def test_parameter_loading_from_env(fixture_api_configuration_with_env: ApiConfiguration):
    assert fixture_api_configuration_with_env.token_secret_key == "this_is_a_token_in_env"