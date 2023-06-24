from .zip import ZipCracker, PWD_SEED

class Crack:
    @staticmethod
    def zip(path: str, seed=PWD_SEED):
        return ZipCracker(path, seed)

if __name__ == '__main__':
    zg = Crack.zip("./examples/flag.zip")
    k = zg.by_seed_mp()
    print(k)