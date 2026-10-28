import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
STATES_URL = "https://opensky-network.org/api/states/all"

# 1. Exchange client credentials for an access token
token_resp = httpx.post(TOKEN_URL, data={
    "grant_type": "client_credentials",
    "client_id": os.environ["OPENSKY_CLIENT_ID"],
    "client_secret": os.environ["OPENSKY_CLIENT_SECRET"],
})
token_resp.raise_for_status()
token = token_resp.json()["access_token"]

# 2. Request aircraft in a 5x5 degree box (25 sq deg = 1 credit)
params = {"lamin": 31.0, "lomin": -87.0, "lamax": 36.0, "lomax": -82.0}
r = httpx.get(STATES_URL, params=params,
              headers={"Authorization": f"Bearer {token}"}, timeout=30)
r.raise_for_status()

print("Credits left:", r.headers.get("X-Rate-Limit-Remaining"))
states = r.json()["states"] or []
print(f"{len(states)} aircraft in the box\n")

for s in states[:10]:
    icao24, callsign = s[0], (s[1] or "").strip()
    lon, lat, alt_m = s[5], s[6], s[7]
    print(f"{icao24}  {callsign:<8}  lat={lat}  lon={lon}  alt_m={alt_m}")