from bisect import bisect
from sympy import isprime


def prime_sieve(n):
    sieve = [True] * (n//2)
    for i in range(3, int(n**0.5)+1, 2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [2] + [2*i+1 for i in range(1, n//2) if sieve[i]]


limit = 10**8
primes = prime_sieve(limit)

phi_cache = {}


def phi(x, a):
    # If value is cached, just return it
    if (x, a) in phi_cache:
        return phi_cache[(x, a)]

    # Base case: phi(x, a) is the number of odd integers <= x
    if a == 1:
        return (x + 1) // 2

    result = phi(x, a-1) - phi(x // primes[a-1], a-1)
    phi_cache[(x, a)] = result  # Memoize
    return result


pi_cache = {}


def pi(x):
    """
    Computes pi(x), the number of primes <= x, using
    the Meissel-Lehmer algorithm.
    """
    # If value is cached, return it
    if x in pi_cache:
        return pi_cache[x]

    # If x < limit, calculate pi(x) using a bisection
    # algorithm over the sieved primes.
    if x < limit:
        result = bisect(primes, x)
        pi_cache[x] = result
        return result

    a = pi(int(x ** (1./4)))
    b = pi(int(x ** (1./2)))
    c = pi(int(x ** (1./3)))

    # This quantity must be integral,
    # so we can just use integer division.
    result = phi(x, a) + (b+a-2) * (b-a+1) / 2

    for i in range(a+1, b+1):
        w = x / primes[i-1]
        b_i = pi(w ** (1./2))
        result = result - pi(w)
        if i <= c:
            for j in range(i, b_i+1):
                result = result - pi(w / primes[j-1]) + j - 1
    pi_cache[x] = result
    return result


def fill_phi_cache():
    for i in range(10_000_000, 1_000_000_000, 1_000_000):
        pi(i)


keys_dict = {}


def fill_keys_dict():
    #           5k      6k      7k       8k       9k       10k     11k        12k      13k      14k     15k
    values = [80_000, 95_000, 110_000, 127_000, 143_000,
              160_000,  176_000, 193_000, 209_000, 220_000, 225_000]

    count = 0
    for i in range(5000, 15000, 1000):
        keys_dict[i] = values[count]
        count += 1


fill_phi_cache()
fill_keys_dict()


def find_left_thprime(key, n):
    while n > 0:
        if isprime(key):
            n -= 1
        key -= 1

    return key+1


def find_right_thprime(key, n):
    while n > 0:
        if isprime(key):
            n -= 1
        key += 1

    return key-1


def find_thprime(key, n):
    pi_key = pi(key)

    n_int = (n//1000)*1000
    key_low = key-keys_dict[n_int]
    key_high = key+keys_dict[n_int]

    pi_key_low = pi(key_low)
    pi_key_high = pi(key_high)

    n_left = n-(pi_key - pi_key_low)
    n_right = n-(pi_key_high - pi_key)

    prime_left = find_left_thprime(key_low, int(n_left))
    prime_right = find_right_thprime(key_high, int(n_right))
    return prime_left*prime_right
