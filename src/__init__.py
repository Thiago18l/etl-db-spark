from src.logs.log import Logger

logging = Logger()

def main():
    logging.info("RUNNING PROJECT")
    if 1 == 1:
        logging.info(f"opa")

if __name__ == '__main__':
    main()