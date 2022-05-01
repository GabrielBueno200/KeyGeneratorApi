import json
from time import perf_counter
import azure.functions as func
import KeyGeneratorApi.key_service as key_service


def validate_payload(initial_code: int, n: int) -> bool:
    return initial_code > 10000000 and 5000 < n < 15000


def generate_key(initial_code: int, n: int) -> int:
    lower_prime = key_service.calculate_lower_prime(initial_code, n)
    upper_prime = key_service.calculate_upper_prime(initial_code, n)

    return lower_prime * upper_prime


def main(req: func.HttpRequest) -> func.HttpResponse:
    request_start_time = perf_counter()

    if not req.get_body:
        return func.HttpResponse("Response body is empty", status_code=400)

    req_body: dict = req.get_json()

    try:
        payloads: list[dict] = req_body
        keys = []

        for payload in payloads:
            initial_code: int = payload['initialCode']
            n: int = payload['n']

            payload['isValid'] = validate_payload(initial_code, n)

            if payload['isValid']:
                key_generation_start_time = perf_counter()
                key = generate_key(initial_code, n)
                key_generation_total_time = perf_counter() - key_generation_start_time

            keys.append(
                {
                    "payload": payload,
                    "key": key if payload['isValid'] else None,
                    "time": key_generation_total_time if payload['isValid'] else 0
                })

        request_total_time = perf_counter() - request_start_time

        response = {
            "requestTime": request_total_time,
            "keys": keys,
        }

        return func.HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")

    except Exception as ex:
        return func.HttpResponse(str(ex), status_code=400)
