
from modules.nexus_cli import NexusCli


if __name__ == '__main__':
    try:
        NexusCli().start()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        SystemExit, print("Stop service")

