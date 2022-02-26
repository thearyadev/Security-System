from utils import Server
from utils import Console


def main():
    server = Server()
    server.start("0.0.0.0", 80)


if __name__ == "__main__":
    main()
