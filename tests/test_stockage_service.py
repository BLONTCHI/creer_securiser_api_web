import pytest
from src.model.user import User
from src.db.basic_db import BasicDb

@pytest.fixture
def fixture_basic_db() -> BasicDb:
    return BasicDb()

def test_create_new_user(fixture_basic_db: BasicDb):
    user = User(email="xyz@mail.com", password="azerty")
    fixture_basic_db.create(user)
    assert user.email in fixture_basic_db.users
    
def test_create_existing_user(fixture_basic_db: BasicDb):
    user = User(email="xyz@mail.com", password="azerty")
    fixture_basic_db.create(user)
    with pytest.raises(Exception) as e:
        fixture_basic_db.create(user)
        
def test_read_existing_user(fixture_basic_db: BasicDb):
    user = User(email="xyz@mail.com", raw_password="azerty")
    fixture_basic_db.create(user)
    read_user = fixture_basic_db.get_by_id(user.email)
    assert read_user != None
    
def test_read_non_existing_user(fixture_basic_db: BasicDb):
    user = User(email="xyz@mail.com", raw_password="azerty")
    with pytest.raises(Exception) as e:
        fixture_basic_db.get_by_id(user.email)