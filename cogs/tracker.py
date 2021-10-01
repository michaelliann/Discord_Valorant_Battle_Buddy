# Import libraries
import discord
from discord.ext import commands
from cogs.utils.tracker_engine import *


class tracker(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("tracker is online.")

    # Commands
    @commands.command(help="Displays a player's competitive stats.")
    async def track(self, ctx, username):
        try:
            # Get stats and images dictionaries
            stats_dictionary = get_stats_from_username(username)
            images_dictionary = get_images_from_username(username)

            # Create embed and set author
            embed_message = discord.Embed(title="Competitive Stats", color=0x0000ff)
            embed_message.set_author(name=username, icon_url=images_dictionary.get("profile_image"))

            # Add embed thumbnail
            embed_message.set_thumbnail(url=images_dictionary.get("rank_image"))

            # Add rank field to embed with False inline
            embed_message.add_field(name="Rank", value=stats_dictionary.get("Rank"), inline=False)
            stats_dictionary.pop("Rank")

            # Loop through stats and add them to embed
            for stat, value in stats_dictionary.items():
                embed_message.add_field(name=stat, value=value, inline=True)

            # Send the embed message
            await ctx.send(embed=embed_message)
        except PrivateProfileException:
            await ctx.send("Please sign in to https://tracker.gg/valorant with your Riot ID to view your stats!")
        except PlayerNotFoundException:
            await ctx.send(
                "Please make sure to include the # tag in the Riot ID to view your stats. If your riot ID contains any spaces, place it inside quotations.")
        except Exception:
            await ctx.send("An error has occurred while tracking stats. Please check if the player ID is a valid ID.")


    @commands.command(help="Shows a player's peak rank.")
    async def peak_rank(self, ctx, username):
        try:
            peak_rank_dictionary = get_peak_rank_from_username(username)
            images_dictionary = get_peak_rank_images_from_username(username)

            act = peak_rank_dictionary.get("Act")

            # Create embed and set author
            embed_message = discord.Embed(title=f"Peak Rank ({act})", color=0x0000ff)
            embed_message.set_author(name=username, icon_url=images_dictionary.get("profile_image"))

            # Add embed thumbnail
            embed_message.set_thumbnail(url=images_dictionary.get("peak_rank_image"))

            # Add rank field to embed with False inline
            embed_message.add_field(name="Rank", value=peak_rank_dictionary.get("Peak Rank"), inline=False)

            await ctx.send(embed=embed_message)
        except PrivateProfileException:
            await ctx.send("Please sign in to https://tracker.gg/valorant with your Riot ID to view your stats!")
        except PlayerNotFoundException:
            await ctx.send(
                "Please make sure to include the # tag in the Riot ID to view your stats. If your riot ID contains any spaces, place it inside quotations.")
        except Exception:
            await ctx.send("An error has occurred while tracking stats. Please check if the player ID is a valid ID.")


def setup(client):
    client.add_cog(tracker(client))
