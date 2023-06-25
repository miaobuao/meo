from .zip import ZipCracker

class Crack:
    @staticmethod
    def zip(path: str):
        return ZipCracker(path)

if __name__ == '__main__':
    zg = Crack.zip("./examples/flag.zip")
    k = zg.by_seed_mp()
    print(k)