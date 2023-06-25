from itertools import permutations

PWD_SEED_NUMBER = b"0123456789"
PWD_SEED_LOWER_ALPHABET = b'qwertyuiopasdfghjklzxcvbnm'
PWD_SEED_UPPER_ALPHABET = b'QWERTYUIOPASDFGHJKLZXCVBNM'
PWD_SEED_SPECIAL_CHAR = b'!@#$%^&*()_+-=[{}]\|;:,<.>/?\'" '
PWD_SEED_ALPHABET = PWD_SEED_LOWER_ALPHABET + PWD_SEED_UPPER_ALPHABET
PWD_SEED_SIMPLE = PWD_SEED_LOWER_ALPHABET + PWD_SEED_NUMBER
PWD_SEED_COMPLEX = PWD_SEED_ALPHABET + PWD_SEED_SPECIAL_CHAR + PWD_SEED_NUMBER

           
def key_permution(seed, size):
    for k in permutations(seed, size):
        yield bytes(k)

def key_generator(seed=PWD_SEED_COMPLEX, start=None, end=None):
    n_size = 1 if start is None else max(int(start), 1)
    if end is None:
        while True:
            for k in key_permution(seed, n_size):
                yield k, n_size
            n_size += 1
    else:
        end = int(end)
        while True:
            if n_size <= end:
                for k in key_permution(seed, n_size):
                    yield k, n_size
            else:
                return StopIteration()
            n_size += 1
