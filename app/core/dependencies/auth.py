from app.core.security import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")
