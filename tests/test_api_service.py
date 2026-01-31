from unittest.mock import patch
from src.api_service import ApiService
import requests
from typing import Dict, Any


def test_validate_cable_design_success():
    """Test successful validation with dictionary input"""
    # Arrange
    service = ApiService(base_url="http://test-api.com")
    mock_response: Dict[str, Any] = {"confidence": 0.95, "is_out_of_scope": False, "validation": []}

    input_data: Dict[str, Any] = {
        "input_mode": "json",
        "data": {"standard": "IS 1554-1", "voltage": "0.6/1 kV"},
    }

    # Act
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        result = service.validate_cable_design(input_data)

    # Assert
    assert result == mock_response
    mock_post.assert_called_once()
    # Verify payload format
    call_kwargs = mock_post.call_args.kwargs
    assert call_kwargs["json"] == input_data


def test_validate_cable_design_free_text_payload():
    service = ApiService()

    payload: Dict[str, Any] = {
        "input_mode": "free_text",
        "data": {"description": "Cable design query"},
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}

        service.validate_cable_design(payload)

    call_kwargs = mock_post.call_args.kwargs
    assert call_kwargs["json"] == payload


def test_validate_cable_design_api_error():
    """Test handling of API errors"""
    service = ApiService()

    payload: Dict[str, Any] = {
        "input_mode": "json",
        "data": {"standard": "IS 1554-1"},
    }

    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("Connection refused")
        result = service.validate_cable_design(payload)

    assert "error" in result
    assert "Connection refused" in result["error"]
