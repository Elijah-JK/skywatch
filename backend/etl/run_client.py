from dotenv import load_dotenv
import os
from opensky_client import OpenSkyClient
import time

if __name__ == "__main__":
    load_dotenv()

    client = OpenSkyClient(os.environ["OPENSKY_CLIENT_ID"], os.environ["OPENSKY_CLIENT_SECRET"])
    print(len(client.get_states(31.0, -87.0, 36.0, -82.0)))
    time.sleep(10)
    print(len(client.get_states(31.0, -87.0, 36.0, -82.0)))
    client.close()