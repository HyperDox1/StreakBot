import datetime
from discord.ext import commands, tasks
import json

utc = datetime.timezone.utc

# If no tzinfo is given then UTC is assumed.
times = [datetime.time(hour=4, minute=0, tzinfo=utc)] #9:30 PDT
channel_id = 1113943554776125553 #general channel for HyperDox's Lab

class Streak(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.remind.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Streak.py is ready!")
    @tasks.loop(time=times)
    async def remind(self):
        with open("cogs/jsonfiles/days.json", "r") as f:
            num_days = json.load(f)
        #increase the streak by one each day
        num_days["Days"] += 1
        channel = self.client.get_channel(channel_id)
        await channel.send(f"@everyone Remember to continue your streak! We are on day {num_days['Days']}.") #keep count of days
        with open("cogs/jsonfiles/days.json", "w") as f:
            json.dump(num_days, f, indent=4)
        f.close()

async def setup(client):
    await client.add_cog(Streak(client))
