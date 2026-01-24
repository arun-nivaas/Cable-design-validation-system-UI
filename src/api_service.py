import requests


class ApiService:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def validate_cable_design(self, input_data: int | str | dict) -> dict:
        """
        input_data: Either a raw string (free text) or a dictionary (structured data).
        """
        if isinstance(input_data, dict):
            payload = input_data
        else:
            # If it's a string, wrap it in the expected 'input' key for the AI service
            payload = {"input": str(input_data)}

        try:
            response = requests.post(
                f"{self.base_url}/design/validate",
                json=payload,  # Use 'json=' instead of 'data=json.dumps()'
                timeout=30,
            )

            # If this fails, it will print the server's explanation of the 422 error
            if response.status_code == 422:
                print(f"Detail of 422 error: {response.json()}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            # Check if there is a detailed error message from FastAPI
            error_detail = ""
            if hasattr(e.response, "json"):
                error_detail = e.response.json()
            return {"error": f"{str(e)} - Detail: {error_detail}"}
