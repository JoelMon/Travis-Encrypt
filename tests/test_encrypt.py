"""Test the encrypt module of Travis Encrypt.

Fixtures:
repository -- a username/repository combination to test

Test functions:
test_public_key_retrieval -- test the Travis CI API for public key retrieval
test_invalid_credentials -- test the InvalidCredentialsError
test_encrypt_key -- test the encrypt_key function
"""
import pytest
import six

from travis.encrypt import (encrypt_key, InvalidCredentialsError,
                            retrieve_public_key)


@pytest.fixture
def repository():
    """Link to the Travis Encrypt repository."""
    return 'mandeep/Travis-Encrypt'


def test_public_key_retrieval(repository):
    """Test the encrypt module's retrieve_public_key function."""
    public_key = retrieve_public_key(repository)
    assert isinstance(public_key, six.text_type)
    assert 'BEGIN PUBLIC KEY' in public_key
    assert 'END PUBLIC KEY' in public_key


def test_invalid_credentials():
    """Test that an SystemExit is raised.

    click.BadParameter() exits with SystemExit when a bad parameter is passed in.
    """
    with pytest.raises(SystemExit):
        retrieve_public_key("INVALID_USER_NAME/INVALID_REPO")


def test_valid_credentials(repository):
    """Test that an SystemExit is not raised with valid credentials.

    click.BadParameter() exits with SystemExit when a bad parameter is passed in.
    """

    try:
        retrieve_public_key(repository)
    except SystemExit:
        pytest.fail("An unexpected credential error occurred.")


def test_encrypt_key(repository):
    """Test the encrypt module's encrypt_key function."""
    public_key = retrieve_public_key(repository)
    password = 'SUPER_SECURE_PASSWORD'
    encrypted_password = encrypt_key(public_key, password.encode())
    assert isinstance(encrypted_password, six.text_type)
