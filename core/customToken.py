from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, Token
from .settings import SIMPLE_JWT 
from datetime import timedelta


class CookieToken(Token):
    token_type = "cookie"
    lifetime = SIMPLE_JWT.get("COOKIE_TOKEN_LIFETIME",timedelta(days=3))

class CustomRefreshToken(RefreshToken):
    @property
    def cookie_token(self) -> CookieToken:
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        cookieToken = CookieToken()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        cookieToken.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            cookieToken[claim] = value

        return cookieToken