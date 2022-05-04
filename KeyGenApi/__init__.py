import json
from time import perf_counter
import azure.functions as func


def validate_payload(initial_code: int, n: int) -> bool:
    return initial_code > 10000000 and 5000 < n < 15000


def generate_key(initial_code: int, n: int, primes_hash: list[int]) -> int:
    threshold = 1_000_000
    int_code = (initial_code//threshold)*threshold

    indexes_hash = load_hash_list_from_file(f"indexHash/{int_code}.txt")

    lower_prime_hash = 0
    upper_prime_hash = 0

    indexHash = int(indexes_hash[initial_code-int_code])
    lower_prime_hash = int(primes_hash[indexHash-n+1])
    upper_prime_hash = int(primes_hash[indexHash+n]) if initial_code != int(
        primes_hash[indexHash+1]) else int(primes_hash[indexHash+n+1])

    return lower_prime_hash*upper_prime_hash


def load_hash_list_from_file(list_name: str) -> list[int]:
    with open(f"KeyGenApi/files/{list_name}", "r") as hash_file:
        hash_list = hash_file.readlines()

    return hash_list


def main(req: func.HttpRequest) -> func.HttpResponse:
    request_start_time = perf_counter()

    if not req.get_body:
        return func.HttpResponse("Response body is empty", status_code=400)

    req_body: dict = req.get_json()

    try:
        payloads: list[dict] = req_body
        primes_hash = load_hash_list_from_file("primeHash.txt")
        keys = []

        for payload in payloads:
            key_generation_start_time = perf_counter()
            
            initial_code = int(payload['initialCode'])
            n = int(payload['n'])

            payload['isValid'] = validate_payload(initial_code, n)

            if payload['isValid']:
                key = generate_key(initial_code, n, primes_hash)

            keys.append(
            {
                "payload": payload,
                "key": key if payload['isValid'] else None,
                "time": perf_counter() - key_generation_start_time if payload['isValid'] else 0
            })

        response = {
            "requestTime": perf_counter() - request_start_time,
            "keys": keys,
        }

        return func.HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")

    except Exception as ex:
        return func.HttpResponse(str(ex), status_code=400)
