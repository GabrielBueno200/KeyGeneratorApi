from sympy import primepi, isprime, prime


def calculate_upper_prime(initial_code: int, n: int) -> int:
    last_prime_index = primepi(initial_code)

    upper_prime_index = last_prime_index + n
    upper_prime = prime(upper_prime_index)

    return upper_prime


def calculate_lower_prime(initial_code: int, n: int) -> int:
    lower_prime = initial_code
    lower_primes_counter = 0

    while lower_primes_counter < n:
        lower_prime -= 1

        if isprime(lower_prime):
            lower_primes_counter += 1

    return lower_prime
