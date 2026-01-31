import requests
from typing import Dict, Any


class ApiService:
    def __init__(self, base_url: str ="https://is-cable-design-validation-system.onrender.com"):
        self.base_url = base_url

    def validate_cable_design(self, input_data: Dict[str, Any]) -> Dict[str, Any]:

        if not isinstance(input_data, dict):
            return {"error": "Invalid payload: request_data must be a dict"}

        if "input_mode" not in input_data or "data" not in input_data:
            return {
                "error": "Invalid payload shape. Expected {input_mode, data}"
        }   
       
        payload = input_data

        try:
            response = requests.post(
                f"{self.base_url}/design/validate",
                json=payload,  # Use 'json=' instead of 'data=json.dumps()'
                timeout=30,
            )

            # If this fails, it will print the server's explanation of the 422 error
            if response.status_code == 422:
                return {
                    "error": "Validation error from backend",
                    "details": response.json()
                }

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            # Check if there is a detailed error message from FastAPI
            error_detail = ""
            if e.response is not None and hasattr(e.response, "json"):
                error_detail = e.response.json()
            return {"error": f"{str(e)} - Detail: {error_detail}"}
