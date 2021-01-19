import discord, os, re, requests, asyncio, json, youtube_dl
from discord.utils import get
from discord.ext import commands

lastplayedname = "No past songs"
embed_colour = discord.Colour.red()


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        print("music.py: Ready")

    # Core music player code thanks to Kevin https://github.com/kevinlinxc/OmenBot, slightly modified to work with the cogs system

    # Takes a Youtube url or a youtube search query and then plays it
    @commands.command(
        aliases=["p"], brief="Plays a Youtube link or YT search query if its <10 m"
    )
    async def play(self, ctx, *url: str):
        await self.join(ctx)
        # takes multiple words as argument for longer search queries
        url = " ".join(url[:])
        text = False
        # checks for existing song.mp3 and deletes if so
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                # print("Removed old song file\n")
        except PermissionError:  # Can't play two songs at once
            # print("Trying to delete song file, but it's being played\n")
            alreadyplaying_e = discord.Embed(
                title="Song already playing, use ```sudo stop``` to stop",
                colour=embed_colour,
            )
            await ctx.send(embed=alreadyplaying_e)
            return
        # if trying to play a playlist, deny
        if "?list" in url:
            playlist_e = discord.Embed(
                title="No playlists",
                colour=embed_colour,
            )
            await ctx.send(embed=playlist_e)
            return
        # if it's a normal link, proceed
        elif "https" in url:
            pass
        # if it's a search query, make slight changes
        else:
            searching_e = discord.Embed(
                title=f"Searching for:",
                description=f"{url}",
                colour=embed_colour,
            )

            await ctx.send(embed=searching_e)
            text = True

        voice = get(self.bot.voice_clients, guild=ctx.guild)
        # use youtube_dl to get the video from url or query
        ydl_opts = {
            "default_search": "auto",
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # print("Downloading audio now\n")
            dict = ydl.extract_info(url, download=False)

            if (
                text
            ):  # if the request was a text search instead of a url, the extract_info dict will be different
                if len(dict["entries"]) == 0:

                    notfound_e = discord.Embed(
                        title="No idea what you're talking about",
                        colour=embed_colour,
                    )
                    await ctx.send(embed=notfound_e)
                    return
                if dict["entries"][0]["duration"] > 10 * 60:  # If the video is too long
                    toolong_e = discord.Embed(
                        title="Song too long (>10 min)",
                        colour=embed_colour,
                    )
                    await ctx.send(embed=toolong_e)
                    return
                else:
                    ydl.download([url])
            else:
                if (
                    dict["duration"] > 10 * 60
                ):  # if the video is too long, don't download
                    toolong_e = discord.Embed(
                        title="Song too long (>10 min)",
                        colour=embed_colour,
                    )
                    await ctx.send(embed=toolong_e)
                    return
                else:
                    ydl.download([url])
        # find the newly downloaded video and rename it. Save other sound effects in sounds so there's no conflicts
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                global lastplayedname
                lastplayedname = name
                # print("Renaming")
                os.rename(file, "song.mp3")
        # play the song
        voice.play(
            discord.FFmpegPCMAudio("song.mp3"),
            after=lambda e: print(f"{name} has finished playing"),
        )
        voice.source = discord.PCMVolumeTransformer(voice.source)
        # volume that seemed to work
        voice.source.volume = 0.50
        nname = name.rsplit("-", 2)

        playing_e = discord.Embed(
            title=f"Playing:",
            description=f"{nname[0]}",
            colour=embed_colour,
        )

        await ctx.send(embed=playing_e)
        # print("playing\n")

    # Repeats the last song played
    @commands.command(
        aliases=["replay", "restart"], brief="Repeats the last video from play"
    )
    async def repeat(self, ctx):
        name = lastplayedname
        if name == "No songs have been played yet":
            return

        voice.play(
            discord.FFmpegPCMAudio("song.mp3"),
            after=lambda e: print(f"{name} has finished playing"),
        )
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.50
        nname = lastplayedname.rsplit("-", 2)

        repeat_e = discord.Embed(
            title=f"Replaying:",
            description=f"{nname[0]}",
            colour=embed_colour,
        )

        await ctx.send(embed=repeat_e)
        # print("playing\n")

    # Pauses current song
    @commands.command(aliases=["pa"], brief="Pauses the music currently being played")
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            # print("Music paused")
            voice.pause()

            pause_e = discord.Embed(
                title="Pausing",
                colour=embed_colour,
            )

            await ctx.send(embed=pause_e)
        else:
            # print("Music not playing")
            pass

    @commands.command(aliases=["re"], brief="Resumes paused music")
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            # print("Resumed music")
            voice.resume()
            resume_e = discord.Embed(
                title=f"Resuming",
                colour=embed_colour,
            )
            await ctx.send(embed=resume_e)
        else:
            # print("Music is not paused")
            pass

    @commands.command(aliases=["st"], brief="Stops music")
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            # print("Music stopped")
            voice.stop()
            stop_e = discord.Embed(
                title=f"Stopping",
                colour=embed_colour,
            )
            await ctx.send(embed=stop_e)
        else:
            # print("Music not playing")
            pass

    # Joins the voice channel that you're in
    @commands.command(
        aliases=["j", "joi"], brief="Joins the voice channel that you're in"
    )
    async def join(self, ctx):
        global voice
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            join_e = discord.Embed(
                title=f"Joining:",
                description=f"{channel}",
                colour=embed_colour,
            )
            await ctx.send(embed=join_e)
            voice = await channel.connect()

    # Leaves the voice channel that you're in
    @commands.command(aliases=["l"], brief="Leaves the voice channel")
    async def leave(self, ctx):

        channel = ctx.guild.voice_client.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            leave_e = discord.Embed(
                title=f"Leaving:",
                description=f"{channel}",
                colour=embed_colour,
            )
            await ctx.send(embed=leave_e)
            await voice.disconnect()
        else:
            pass


def setup(bot):
    bot.add_cog(MusicCog(bot))
