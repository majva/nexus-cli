
from app_nexuscli_main.nexus_cli import NexusCli

from sys import path


if __name__ == '__main__':
    try:
        path.append("..")
        NexusCli().main()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        SystemExit, print("Stop service")

