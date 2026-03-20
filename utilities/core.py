from rest_framework.response import Response

def api_response(status: bool, status_code: int, message: str = None, **kwargs):
    response_payload = {
        "status": status,
        "status_code": status_code,
        **({"message": message} if message else {}),
        **kwargs,
    }
    return Response(response_payload, status=status_code)