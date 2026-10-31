import time
import requests

TOKEN_URL = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
STATES_URL = "https://opensky-network.org/api/states/all"

class OpenSkyClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.token = None
        self.token_expires_at = None

    def close(self):
        self.session.close()
    
    def get_states(self, lamin, lomin, lamax, lomax) -> list[list]:
        params = {"lamin": lamin, "lomin": lomin, "lamax": lamax, "lomax": lomax}
        response = self.session.get(STATES_URL, params=params, headers={"Authorization": f"Bearer {self.get_token()}"}, timeout=30)
        response.raise_for_status()      

        states = response.json()["states"] or []
        return states             

    def get_token(self):
        '''Return a valid access token, refreshing automatically if needed'''
        if self.token and self.token_expires_at and time.monotonic() < self.token_expires_at:
            return self.token
        return self._refresh()

    def _refresh(self):
        '''Fetch a new access token from the OpenSky Authentication Server'''
        print("Fetching new token")
        response = self.session.post(TOKEN_URL, data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }, timeout=30)
        response.raise_for_status()

        data = response.json()
        self.token = data["access_token"]
        expires_in = data.get("expires_in", 1800)
        self.token_expires_at = time.monotonic() + expires_in - 30
        return self.token
