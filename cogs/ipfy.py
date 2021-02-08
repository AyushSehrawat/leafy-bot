import discord
import requests
from discord.ext import commands


class Ipfy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ipfy cog loaded successfully")

    @commands.command(
        aliases=["ip"], description="Shows the info about the given ip/webiste"
    )
    async def ipinfo(self, ctx, ip_address):
        if ip_address == None:
            await ctx.send("You forgot ip")
        else:
            # ip_address = int(ip_address)
            URL = f"http://ip-api.com/json/{ip_address}?fields=17000447"

            def check_valid_status_code(request):
                if request.status_code == 200:
                    return request.json()

                return False

            def get_info():
                request = requests.get(URL)
                data = check_valid_status_code(request)

                return data

            infoip = get_info()
            check = infoip["status"]
            if not infoip or check == "fail":
                await ctx.channel.send("Couldn't get info from API. Try again later.")

            else:
                embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    title="Ip Info",
                    description="Tells info about IP/Domain",
                    color=0xFF0000,
                )
                embed.add_field(name="Status", value=infoip["status"])
                embed.add_field(name="IP ADDRESS", value=infoip["query"])
                embed.add_field(name="Country Code", value=infoip["countryCode"])
                embed.add_field(name="Country Name", value=infoip["country"])
                embed.add_field(name="Region Code", value=infoip["region"])
                embed.add_field(name="Region Name", value=infoip["regionName"])
                embed.add_field(name="City", value=infoip["city"])
                embed.add_field(name="Zip Code", value=infoip["zip"])
                embed.add_field(name="Time Zone", value=infoip["timezone"])
                embed.add_field(name="Latitude", value=infoip["lat"])
                embed.add_field(name="Longitude", value=infoip["lon"])
                embed.add_field(name="ISP", value=infoip["isp"])
                embed.add_field(name="ORG", value=infoip["org"])
                embed.add_field(name="Mobile", value=infoip["mobile"])
                embed.add_field(name="Hosting", value=infoip["hosting"])
                embed.add_field(name="Proxy", value=infoip["proxy"])
                embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Ipfy(client))
