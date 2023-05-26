from time import sleep
from services import get_system_status


def main():
    while True:
        get_system_status()
        sleep(300)


if __name__ == "__main__":
    main()