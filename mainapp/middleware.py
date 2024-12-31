from channels.middleware.base import BaseMiddleware
import json
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

class TokenAuthMiddleware(BaseMiddleware):
    async def connect(self, message):
        # Extract token from the query parameters
        token = message.get('query_string', b'').decode()

        if not token:
            await self.close()
            return

        try:
            # Try to find the token in the database
            Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        await super().connect(message)
