import json
from time import perf_counter
import azure.functions as func
from KeyGeneratorApi.utils import get_numbers_file


primeHash = get_numbers_file('primeHash.txt')
indexHash = get_numbers_file('indexHash.txt')


def validate_payload(initial_code: int, n: int) -> bool:
    return initial_code > 10000000 and 5000 < n < 15000


def generate_key(initial_code: int, n: int) -> int:
    indexHash = int(indexHash[initial_code])
    lprimeHash = int(primeHash[indexHash-n+1])
    rprimeHash = int(primeHash[indexHash+n]) if initial_code != int(
        primeHash[indexHash+1]) else int(primeHash[indexHash+n+1])

    return lprimeHash*rprimeHash


def main(req: func.HttpRequest) -> func.HttpResponse:
    if not req.get_body:
        return func.HttpResponse("Response body is empty", status_code=400)

    req_body: dict = req.get_json()

    try:
        payloads: list[dict] = req_body
        response = []

        for payload in payloads:
            initial_code: int = payload['initialCode']
            n: int = payload['n']

            is_valid_payload = validate_payload(initial_code, n)

            if is_valid_payload:
                start_time = perf_counter()
                key = generate_key(initial_code, n)
                finish_time = perf_counter()
                total_time = finish_time - start_time

                response.append(
                    {
                        "isValid": True,
                        "key": key,
                        "time": total_time
                    })
            else:
                response.append({"isValid": False})

        return func.HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")

    except Exception as ex:
        return func.HttpResponse(str(ex), status_code=400)
