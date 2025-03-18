import jwt
from datetime import datetime, timedelta, timezone

class HobbyToken():
    def __init__(self, password):
        self.expiration = None
        try:
            payload = jwt.decode(password, options={"verify_signature": False})
        except jwt.exceptions.DecodeError:
            payload = None
        if payload:
            self.expiration = int(payload.get("exp"))

    def get_expiration_date(self):
        return datetime.fromtimestamp(self.expiration, timezone.utc)

    def will_expire_soon(self):
        if self.expiration is None:
            return False
        current_utc_timestamp = int(datetime.now(timezone.utc).timestamp())
        diff = self.expiration - current_utc_timestamp
        lifetime = timedelta(seconds=diff)
        two_week = timedelta(weeks=2)
        if lifetime < two_week:
            return True
        return False
    
    def is_a_token(self):
        return self.expiration is not None
