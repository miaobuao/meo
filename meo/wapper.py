import time

def timeit(func):
    def wapper(*args, **kwargs):
        st = time.time()
        res = func(*args, **kwargs)
        ed = time.time()
        return ed - st, res
    return wapper

if __name__ == '__main__':
    @timeit
    def test(k):
        time.sleep(5)
        print(k)
        return k ** 2
    print(test(3))