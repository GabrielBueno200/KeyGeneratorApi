import azure.functions as func

def validate_payload(initial_code: int, n: int) -> bool:
    return initial_code > 10000000 and 5000 < n < 15000


def main(req: func.HttpRequest) -> func.HttpResponse:
    if not req.get_body:
        return func.HttpResponse("Response body is empty", status_code=400)

    req_body: dict = req.get_json()

    try:
        initial_code: int = req_body['initialCode']
        n: int = req_body['n']

        is_valid_payload = validate_payload(initial_code, n)

        if is_valid_payload:
            return func.HttpResponse(f"Payload {initial_code}|{n} is valid", status_code=200)
        else:
            return func.HttpResponse(f"Payload {initial_code}|{n} is invalid", status_code=400)

    except Exception as ex:
        return func.HttpResponse(str(ex), status_code=400)
