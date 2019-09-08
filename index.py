import aiohttp
import fortnitepy
import asyncio

class MyClient(fortnitepy.Client):
    BEN_BOT_BASE = 'http://benbotfn.tk:8080/api/cosmetics/search'

    def __init__(self):
        super().__init__(
            email='email',
            password='pass',
            net_cl='7681591'
        )
        self.session_event = asyncio.Event(loop=self.loop)

    async def event_ready(self):
        print('Client is ready as {0.user.display_name}.'.format(self))
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.session_event.set()
    async def event_friend_request(request):
        await request.accept()
    async def fetch_cosmetic_id(self, display_name):
        async with self.session.get(self.BEN_BOT_BASE, params={'displayName': display_name}) as r:
            print(r)
            data = await r.json()
            return data.get('id')
    async def event_party_invite(self, invite):
        await invite.accept()
    async def event_party_message(self, message):
        # wait until session is set
        await self.session_event.wait()

        split = message.content.split()
        command = split[0].lower()
        args = split[1:]

        # sets the current outfit
        if command == '!skin':
            cid = await self.fetch_cosmetic_id(' '.join(args))
            if cid is None:
                return await message.reply('Error: No Skin found by the name {0.args}')

            await self.user.party.me.set_outfit(
                asset=cid
            )

        # sets the current emote (since emotes are infinite)
        elif command == '!play':
            eid = await self.fetch_cosmetic_id(' '.join(args))
            if eid is None:
                return await message.reply('Error: no Dance found by the name {0.args}')

            await self.user.party.me.set_emote(
                asset=eid
            )

        # clears/stops the current emote
        elif command == '!stopemote':
            await self.user.party.me.clear_emote()
c = MyClient()
c.run()
