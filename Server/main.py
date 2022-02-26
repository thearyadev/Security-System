from utils import Server
from utils import Console


def main():
    server = Server()
    server.run(host="0.0.0.0", port=80, debug=True)
    # server.start(host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()
