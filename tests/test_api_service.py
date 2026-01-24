from unittest.mock import patch
from src.api_service import ApiService
import requests

def test_validate_cable_design_success():
    """Test successful validation with dictionary input"""
    # Arrange
    service = ApiService(base_url="http://test-api.com")
    mock_response = {
        "confidence": 0.95,
        "is_out_of_scope": False,
        "validation": []
    }
    
    input_data = {"standard": "IS 1554-1", "voltage": "0.6/1 kV"}
    
    # Act
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
        
        result = service.validate_cable_design(input_data)
        
    # Assert
    assert result == mock_response
    mock_post.assert_called_once()
    # Verify payload format
    call_kwargs = mock_post.call_args.kwargs
    assert call_kwargs['json'] == input_data

def test_validate_cable_design_string_input():
    """Test validation with string input (e.g. from AI input mode)"""
    service = ApiService()
    text_input = "Cable design query"
    
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}
        
        service.validate_cable_design(text_input)
        
    # Verify string was wrapped in dict
    call_kwargs = mock_post.call_args.kwargs
    assert call_kwargs['json'] == {"input": text_input}

def test_validate_cable_design_api_error():
    """Test handling of API errors"""
    service = ApiService()
    
    with patch('requests.post') as mock_post:
        
        mock_post.side_effect = requests.exceptions.RequestException("Connection refused")
        result = service.validate_cable_design({})
        
    assert "error" in result
    assert "Connection refused" in result["error"]
