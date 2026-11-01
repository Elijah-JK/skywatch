from dotenv import load_dotenv
import logging
import os
from opensky_client import OpenSkyClient
import time

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    client = OpenSkyClient(os.environ["OPENSKY_CLIENT_ID"], os.environ["OPENSKY_CLIENT_SECRET"])

    try:
        while True:
            client.get_states(31.0, -87.0, 36.0, -82.0)
            time.sleep(30) 
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    finally:
        client.close()