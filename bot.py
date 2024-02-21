import asyncio
import discord
from discord import member
from discord import client
from discord import message
from discord import channel
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from async_timeout import asyncio
import datetime
import random
import os
from urllib import parse, request
import re
import DiscordUtils
import aiohttp
from discord.ext.commands.core import check_any, command
from discord.utils import sleep_until

bot = commands.Bot(command_prefix='&', description="This is a Helper Bot")
bot.remove_command("help")
# bot command ussles 

@bot.command(aliases=['Ping','Pong'])
async def ping(ctx):
    await ctx.send(f'Pong! {round (bot.latency * 1000)} ms')

@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)

@bot.command()
async def mul(ctx, num0ne: int, numTwo: int):
    await ctx.send(num0ne * numTwo)  

 
#help command (comando para ver la ayuda del bot faltarian cosas por poner )
@bot.command(aliases=['Help','hp','Hp'])
async def help(ctx):
    helpEmbed = discord.Embed(title="Help commands", color= discord.Color.dark_blue())
    helpEmbed.add_field(name='Moderación',value="```Ban``````kick``````muted``````purge``````clear```")
    helpEmbed.add_field(name="Información",value="```serverinfo``````info [user]``````avatar```")
    helpEmbed.add_field(name='Otros', value="```HUG``````8ball``````ping``````salsa``````gafo``````Slap```")
    await ctx.send(embed = helpEmbed)

#kick command (comando para kickear usuarios (le falta acomodar los permisos)
@bot.command(aliases=['kick'])
@commands.has_permissions(manage_messages=True)
async def Kick(ctx, member:discord.Member, *,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} a sido kikeado Razón: {reason}")

#BAN command (comando para banear usuarios (le falta acomodar los permisos)
@bot.command(aliases=['ban'])
@commands.has_permissions(manage_messages=True)
async def Ban(ctx, member:discord.Member, *,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} a sido baneado Razón: {reason}")

    #Severinfo command (Para ver la infomacion general de un servidor)
@bot.command(aliases=['SvInfo','ServerInfo','svinfo'])
async def serverinfo(ctx):
    icon = str(ctx.guild.icon_url)
    role_count= len(ctx.guild.roles)
    list_of_bots= [bot.mention for bot in ctx.guild.members if bot.bot]

    serverinfoEmbed= discord.Embed(title=f"{ctx.guild.name}", description="**Información del Server:**", timestamp=datetime.datetime.utcnow(), color=discord.Color.blurple())
    serverinfoEmbed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    serverinfoEmbed.add_field(name = "Numero de Miembros",value=ctx.guild.member_count, inline=False)
    serverinfoEmbed.add_field(name = "Verificacion level",value=str(ctx.guild.verification_level), inline=False)
    serverinfoEmbed.add_field(name = "Rol más alto",value=ctx.guild.roles[-2], inline=False)
    serverinfoEmbed.add_field(name = "Numero de Roles",value=str(role_count), inline=False)
    serverinfoEmbed.add_field(name = "Bots",value=','.join(list_of_bots), inline=False)
    serverinfoEmbed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    serverinfoEmbed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    serverinfoEmbed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    serverinfoEmbed.set_thumbnail(url=icon)
    serverinfoEmbed.set_footer(icon_url= ctx.author.avatar_url, text=f"Pedido por: {ctx.author.name} ")
   #serverinfoEmbed.add_field(name = "server name",value=f"{ctx.guild.name}", inline=False)
    await ctx.send(embed= serverinfoEmbed)

#avatar command (Comando para ver el avatar de un usuario, sin embed)
@bot.command(aliases=['av','Avatar'])
async def avatar(ctx, member:discord.Member=None):
    if member==None:
        member= ctx.author
 
        memberAvatar =member.avatar_url
        await ctx.send(memberAvatar)

  #info command (Informacion de un usuario)      
@bot.command(aliases=['Info','in','In'])
async def info(ctx,member: discord.Member):
    embed= discord.Embed(title="usuario", description= member.mention, color= discord.Color.dark_green())
    embed.add_field(name="**La cuenta fue creada:**", value=f"{member.created_at.date()}".replace("-", "/"), inline=True)
    embed.add_field(name="**Tiempo en el servidor**", value=f"{member.joined_at.date()}".replace("-", "/"), inline = True)
    embed.add_field(name="**•Status•**", value=str(member.status).replace("dnd", "Do Not Disturb"), inline=True)
    embed.add_field(name= "ID",value= member.id, inline=True)
    embed.set_thumbnail(url= member.avatar_url)
    embed.set_footer(icon_url= ctx.author.avatar_url, text=f"Pedido por: {ctx.author.name} ")
    await ctx.send(embed= embed)

#clear command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.message.delete()
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=limit)
    purge_embed = discord.Embed(title='Purge', description=f'Purga hecha {limit} mensajes.', color=discord.Colour.dark_red())
    purge_embed.set_footer(icon_url= ctx.author.avatar_url, text=f"Pedido por: {ctx.author.name} ")
    await ctx.channel.send(embed=purge_embed, delete_after=True)

#comando de youtube    
@bot.command(aliases=['youtube','Yt'])
async def yt(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
    print(search_results)
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

@bot.command(aliases=['Join','J','j'])
async def join(ctx):
     await ctx.author.voice.channel.connect()
     await ctx.send('Entré al canal de voz')

@bot.command(aliases=['Salsa','sasa'])
async def salsa(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/813613121474002974/884183463886999582/92785570_521251308779651_1359881195323654144_n.mp4")
@bot.command(aliases=['gafo'])
async def Gafo(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/903334910184521823/908754231782154280/GAFO.mp4')

@bot.command(aliases=['glowup'])
async def Glowup(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/803649323010359314/908754461420294144/meme_2.mp4')

@bot.command(aliases=['Justinpleaños','Justpleaños'])
async def justpleaños(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/671138987259199522/817957235685982218/Kenosuba_1367306622972887042270P.mp4\n **Feliz cumple Justin** :tada: :heart:  @everyone')
    

@bot.command(aliases=['8ball','8b'])
async def eightball(ctx, *, question):
 responses=[' Es cierto.', 'Es decididamente así.','Sin lugar a dudas.'
   ,'Sí, definitivamente.',' Puedes confiar en eso.','Lo más probable.',' Las señales apuntan a que sí.'
   ,' Pregunta confusa, vuelve a intentarlo.',' Mejor no decirte ahora.','La respuesta es no.','Mis fuentes dicen que no.'
   ,'cry about it.','el pepe']
 await ctx.send(f':8ball: Pregunta: {question}\n :green_circle: Respuesta: {random.choice(responses)} ')

@bot.command(aliases=['pl'])
async def poll(ctx,*,msg):
    channel=ctx.channel
    try:
        op1, op2= msg.split("or")
        txt=f"Reacciona a :white_check_mark: si {op1} o a :negative_squared_cross_mark: si {op2} "
    except:
        await channel.send("Mala formulacion del poll")
        return
    embed= discord.Embed(title="Poll", description="votación", color= discord.Color.dark_green())
    embed.add_field(name="", value=txt)
    message_= await channel.send(embed=embed)
    await message_.add_reaction("✅")
    await message_.add_reaction("❎")
    await ctx.message.delete() 


@bot.event
async def on_member_join(member):
    try:
        channel = bot.get_channel(803649323010359314)
        try:
            embed = discord.Embed(colour=discord.Colour.green())
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.add_field(name= "Bievenido" ,value=f"**Hola,{member.mention}! Bienvenido a {member.guild.name}\n Gracias por entrar al Servidor :taba: ", inline=False)
            embed.set_thumbnail(url=member.guild.icon_url)
            await channel.send(embed=embed)
        except Exception as e:
            raise e
    except Exception as e:
        raise e
#comando para dar cachetadas
@bot.command(aliases=['Slap','Sp','sape','Sape'],pass_context=True)
async def slap(ctx, member: discord.Member):
    embed = discord.Embed(title="", description="**{1}** Le dio una Cachetada a **{0}**!".format(member.name, ctx.message.author.name), color=0x176cd5)
    responses=['https://c.tenor.com/iDdGxlZZfGoAAAAM/powerful-head-slap.gif', 'https://c.tenor.com/EfhPfbG0hnMAAAAM/slap-handa-seishuu.gif',
    'https://c.tenor.com/BYu41fLSstAAAAAM/when-you-cant-accept-reality-slap.gif',
    'https://c.tenor.com/noSQI-GitQMAAAAM/mm-emu-emu.gif',
    'https://c.tenor.com/rVXByOZKidMAAAAM/anime-slap.gif',
    'https://c.tenor.com/OuYAPinRFYgAAAAM/anime-slap.gif',
    'https://c.tenor.com/2R9-4O6jqEsAAAAM/slap-slapping.gif',
    'https://c.tenor.com/ydg0wBHVDYYAAAAM/deku-x-uraraka-izuku-midoriya.gif',
    'https://c.tenor.com/Sp7yE5UzqFMAAAAM/spank-slap.gif',
    'https://c.tenor.com/gXUhWuB6QDkAAAAS/family-guy-smack.gif',
    'https://c.tenor.com/PTONt_7DUTgAAAAM/batman-slap-robin.gif'
    ]
    embed.set_image(url=random.choice(responses))
    await ctx.send(embed=embed)
#comando de abrazo, puedo agregar mas.
@bot.command(aliases=['Hug','hg','Abrazo','abrazo'],pass_context=True)
async def hug(ctx,member:discord.Member):
    embed= discord.Embed(title="", description="**{1}** Abrazó a **{0}**!".format(member.name, ctx.message.author.name), color=0x176cd5)
    responses=[
    'https://c.tenor.com/Ct4bdr2ZGeAAAAAS/teria-wang-kishuku-gakkou-no-juliet.gif',
    'https://c.tenor.com/xgVPw2QK5n8AAAAM/sakura-quest-anime.gif',
    'https://c.tenor.com/c8M8yU1q6c4AAAAM/hug-anime.gif',
    'https://c.tenor.com/UhcyGsGpLNIAAAAM/hug-anime.gif',
    'https://c.tenor.com/xIuXbMtA38sAAAAM/toilet-bound-hanakokun.gif',
    'https://c.tenor.com/mmQyXP3JvKwAAAAM/anime-cute.gif',
    'https://c.tenor.com/vkiqyZJWJ4wAAAAS/hug-cat.gif'
    ]
    embed.set_image(url=random.choice(responses))
    await ctx.send(embed=embed)

@bot.command(aliases=['Punch','Golpe','Pch'])
async def punch(ctx,member:discord.Member):
    embed= discord.Embed(title="",description="**{1}** Golpeo a **{0}**!".format(member.name, ctx.message.author.name),color=0x176cd5)
    responses=[
        'https://c.tenor.com/SwMgGqBirvcAAAAM/saki-saki-kanojo-mo-kanojo.gif'
        'https://c.tenor.com/rjR2Z67erfkAAAAM/death-saitama.gif'
        'https://c.tenor.com/6a42QlkVsCEAAAAM/anime-punch.gif'
        'https://c.tenor.com/s0bU-NO1QIQAAAAM/anime-punch.gif'
        'https://c.tenor.com/b8XaMD-FD-MAAAAS/anime-punch.gif'
        'https://c.tenor.com/iJhyeogN3icAAAAS/rimuru-rimuru-punch.gif'
        'https://c.tenor.com/EdV_frZ4e_QAAAAS/anime-naruto.gif'
        'https://c.tenor.com/w8gsT2Es2AMAAAAM/anime-punch.gif'
    ]
    embed.set_image(url=random.choice(responses))
    await ctx.send(embed=embed)

@bot.command(aliases=['Kiss','beso','Beso','Ks'])
async def kiss(ctx,member:discord.Member):
 embed= discord.Embed(title="",description="**{1}** Beso a **{0}**!".format(member.name, ctx.message.author.name),color=0x176cd5)
 respones=[
'https://c.tenor.com/wDYWzpOTKgQAAAAM/anime-kiss.gif'
'https://c.tenor.com/3wE3JNW0fswAAAAM/anime-kiss-love.gif'
'https://c.tenor.com/hK8IUmweJWAAAAAM/kiss-me-%D0%BB%D1%8E%D0%B1%D0%BB%D1%8E.gif'
'https://c.tenor.com/9rN8nw7pVcEAAAAM/anime-kiss.gif'
'https://c.tenor.com/F02Ep3b2jJgAAAAM/cute-kawai.gif'
'https://c.tenor.com/Ct9yIxN5nE0AAAAM/kiss-anime.gif'
'https://c.tenor.com/9vycr5sUYBMAAAAM/eden-of-the-east-anime.gif'
'https://c.tenor.com/Ze6FyEgy4WAAAAAM/kiss-anime.gif'
'https://c.tenor.com/W571AcafidcAAAAM/anime-kissing.gif'
'https://c.tenor.com/YTsHLAJdOT4AAAAM/anime-kiss.gif'
 ]
 embed.set_image(url=random.choice(respones))
 await ctx.send(embed=embed)
     
# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='&help'))
    print('El bot esta listo para iniciar')
bot.run('#')