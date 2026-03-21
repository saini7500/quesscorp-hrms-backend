from rest_framework.response import Response

def get_error_message(errors):
    """
    Extracts a clean, human-readable error message from DRF serializers.
    Example: {"employee_id": ["employee with this employee id already exists."]} 
             -> "employee_id: employee with this employee id already exists."
    """
    if isinstance(errors, dict):
        for key, value in errors.items():
            if isinstance(value, list) and len(value) > 0:
                if key == "non_field_errors":
                    return str(value[0])
                # Format smartly for standard fields
                return f"{key.replace('_', ' ').capitalize()}: {value[0]}"
            return str(value)
    return str(errors)

def api_response(status: bool, status_code: int, message: str = None, **kwargs):
    response_payload = {
        "status": status,
        "status_code": status_code,
        **({"message": message} if message else {}),
        **kwargs,
    }
    return Response(response_payload, status=status_code)