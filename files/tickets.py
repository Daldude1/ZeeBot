import discord 
from discord.ext import commands
import sqlite3

class ticketsSetup(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def configT(self, ctx, channel:discord.TextChannel=None, support: discord.Role=None):
        if channel == None:
            embed = discord.Embed(title='ZeeBot', description=f'Haz solicitado ayuda :eyes: \n Los parametros de este comando son channel, support \n Intente ejecutarlo de esta forma: .configT parametro1 parametro2 \n Donde parametro1 es el canal de tickets y parametro2 es el rol de soporte.', color=0xffa348)
            embed.set_footer(text='By Daldude1#9156')
            await ctx.send(embed=embed)
        elif support == None:
            embed = discord.Embed(title='ZeeBot', description=f'¡No haz puesto el parametro support!', color=0xffa348)
            embed.set_footer(text='By Daldude1#9156')
            await ctx.send(embed=embed)
        else:
            db = sqlite3.connect('db/tickets.db')
            cursor = db.cursor()
            server = ctx.message.guild.id
            cursor.execute(f'SELECT * FROM setup WHERE server={server}')
            rows = cursor.fetchone()
            if rows == None:
                cursor.execute('INSERT INTO setup(server, channel, support) VALUES(?, ?, ?)', (server, channel.id, support.id))
                db.commit()
                cursor.close()
                embed = discord.Embed(title='ZeeBot', description=f'Hola {ctx.author.mention} \n He guardado la configuración con exito', color=0xffa348)
                embed.set_footer(text='By Daldude1#9156')
                await ctx.send(embed=embed)           
            else:
                cursor.execute(f'UPDATE setup SET channel={channel.id}')
                cursor.execute(f'UPDATE setup SET support={support.id}')
                db.commit()
                cursor.close()
                embed = discord.Embed(title='ZeeBot', description=f'Hola {ctx.author.mention} \n He actualizado la configuración con exito', color=0xffa348)
                embed.set_footer(text='By Daldude1#9156')
                await ctx.send(embed=embed)                         

class ticketsSystem(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command()
    async def ticket(self, ctx):
        server = ctx.message.guild.id
        db = sqlite3.connect('db/tickets.db')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM setup WHERE server={server}')
        rows = cursor.fetchone()
        if rows == None:
            await ctx.send('**¡No se han configurado los tickets!**')
        else:
            if server == rows[0]:
                embed = discord.Embed(title='ZeeBot', description=f'Hola de seguro vienes a pedir ayuda \n Reacciona a 📨 para abrir un ticket', color=0xffa348)
                embed.set_footer(text='By Daldude1#9156')
                msg = await ctx.send(embed=embed)    
                await msg.add_reaction('📨')
        
def setup(client):
    client.add_cog(ticketsSetup(client))
    client.add_cog(ticketsSystem(client))
