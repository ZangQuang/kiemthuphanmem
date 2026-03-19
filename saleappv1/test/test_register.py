from test.test_base import test_session, test_app
from eapp.models import User
from eapp.dao import add_user
import hashlib
import pytest


def test_success(test_session):
    add_user(username='a'*6, password='1a'*4, name='admin', avatar=None)

    u = User.query.filter(User.username.__eq__('a'*6)).first()

    assert u is not None
    assert u.name == 'admin'
    assert u.password == str(hashlib.md5(('1a'*4).encode('utf-8')).hexdigest())

@pytest.mark.parametrize('password', [
    '1a'*3 + '1', '12'*4 , 'a'*8
])
def test_invalid_password(password):
    with pytest.raises(ValueError):
        add_user(username='a'*6, password=password, name='admin', avatar=None)