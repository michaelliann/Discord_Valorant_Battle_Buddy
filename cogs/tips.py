# Import libraries
import discord
import os
import random
from discord.ext import commands

class tips(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("tips is online.")

    # Commands
    @commands.command(aliases=["Tip", "tips", "Tips"], help="Displays a random tip.")
    async def tip(self, ctx):
        tipsList = ["The spike takes 7 seconds to defuse.",
                    "Remember to keep your crosshair where enemies will be.",
                    "It takes 45 seconds for the spike to go off.",
                    "Try to hold angles from as far back as you can.",
                    "Don't forget to use your utilities!",
                    "Remember to ping the spike for your teammates during the post plant.",
                    "Try not to get greedy with kills!",
                    "Your crosshair should be placed at head level.",
                    "Remember that enemies can hear you reload. Be careful!",
                    "You can hear when enemies reload. Take advantage!",
                    "When playing Phoenix, you can use your blaze and hot hands abilities to heal.",
                    "Don't be toxic to your teammates.",
                    "When eating while playing, use chopsticks to keep your hands clean.",
                    "Remember to Sit with your back straight or recline at a comfortable angle.",
                    "If the spike is half defused, it will play a higher sound when tapped.",
                    "Don't forget to get up and stretch!",
                    "If the area is clear, plant the spike where it can be defended easily.",
                    "Astra's smokes last for 15 seconds before fading.",
                    "Brimstone's smokes last for 19.25 seconds before fading.",
                    "Brimstone's incendiary lasts for 7 seconds.",
                    "If an enemy Brimstone is using post plant lineups, you can use your character to block it.",
                    "Drink water to stay hydrated while playing.",
                    "Hey, sometimes your opponent is just having a good day.",
                    "Viper's snake bike lasts for 6.5 seconds.",
                    "Picking up a prime vandal will boost your aim by 15%.",
                    "Try to listen for Omen's teleport when he uses his from the shadows ultimate.",
                    "Omen's smokes last for 15 seconds.",
                    "When on a losing streak, take a break before playing again.",
                    "Play with your friends for more fun!"
                    ]

        tip = random.choice(tipsList)
        await ctx.send(tip)

def setup(client):
    client.add_cog(tips(client))