import pytest
from unittest.mock import patch
from dashboard.services.ingestion import fetch_token_balance
from django.conf import settings

@pytest.fixture
def mock_alchemy_response():
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "address": "0x123",
            "tokenBalances": [
                {"contractAddress": "0xabc", "tokenBalance": "1000"},
                {"contractAddress": "0xdef", "tokenBalance": "5000"},
            ]
        }
    }

@patch("dashboard.services.ingestion.requests.post")
def test_fetch_token_balance_success(mock_post, mock_alchemy_response):
    # Mock the HTTP response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_alchemy_response

    address = "0x123"
    response = fetch_token_balance(address)

    # Validate returned data
    assert response == mock_alchemy_response

    # Validate request was made correctly
    mock_post.assert_called_once()
    called_args, called_kwargs = mock_post.call_args

    # URL should come from Django settings
    assert called_args[0] == settings.ALCHEMY_URL

    # Address should be passed correctly
    assert called_kwargs["json"]["params"][0] == address
