import aiohttp

twitch_token = None
was_live = False

class TwitchService:


    def __init__(self, TWITCH_CLIENT_ID,TWITCH_CLIENT_SECRET,STREAMER,CHANNEL_ID,BOT):
        self.TWITCH_CLIENT_ID = TWITCH_CLIENT_ID
        self.TWITCH_CLIENT_SECRET = TWITCH_CLIENT_SECRET
        self.STREAMER = STREAMER
        self.CHANNEL_ID = CHANNEL_ID
        self.BOT = BOT

    async def get_twitch_token(self,session):
        async with session.post(
                "https://id.twitch.tv/oauth2/token",
                params={
                    "client_id": self.TWITCH_CLIENT_ID,
                    "client_secret": self.TWITCH_CLIENT_SECRET,
                    "grant_type": "client_credentials",
                },
            ) as resp:
                data = await resp.json()
                return data["access_token"]

    async def check_stream(self):
        global was_live
        async with aiohttp.ClientSession() as session:
            stream = await self.fetch_stream(session)
        
        is_live = stream is not None
        if is_live and not was_live:
            channel = self.BOT.get_channel(self.CHANNEL_ID)
            if channel:
                await channel.send(
                    f"🔴 **{stream['user_name']}** ist jetzt live!\n"
                    f"**{stream['title']}** – Spiel: {stream['game_name']}\n"
                    f"https://twitch.tv/{self.STREAMER}\n"
                    f"@everyone"
                )
        was_live = is_live

    async def fetch_stream(self,session):
        global twitch_token
        if twitch_token is None:
            twitch_token = await self.get_twitch_token(session)
        
        headers = {
            "Client-ID": self.TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {twitch_token}",
        }
        async with session.get(
            "https://api.twitch.tv/helix/streams",
            params={"user_login": self.STREAMER},
            headers=headers,
        ) as resp:
            if resp.status == 401:  # Token abgelaufen -> beim nächsten Durchlauf neu holen
                twitch_token = None
                return None
            data = await resp.json()
            return data["data"][0] if data.get("data") else None