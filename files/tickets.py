import discord 
from discord.ext import commands
import sqlite3
import asyncio 

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
    async def rename(self, ctx, *, name: str=None):
        server = ctx.message.guild.id
        db = sqlite3.connect('db/tickets.db')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM tickets WHERE server={server} and ticket={ctx.channel.id}')
        rows = cursor.fetchone()
        if rows == None:
            pass 
        else:
            if name == None:
                embed = discord.Embed(title='ZeeBot | Te hace falta un parametro - Nombre', color=0xffa348)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=f'ZeeBot | Nuevo nombre: {name}', color=0xffa348)
                await ctx.send(embed=embed)         
                await ctx.channel.edit(name=name)

    @commands.command()
    async def close(self, ctx):
        server = ctx.message.guild.id
        db = sqlite3.connect('db/tickets.db')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM tickets WHERE server={server} and ticket={ctx.channel.id}')
        rows = cursor.fetchone()
        if rows == None:
            pass 
        else:
            if ctx.channel.id == rows[1]:
                embed = discord.Embed(title='ZeeBot | Se cerrara el ticket en 5s', color=0xffa348)
                await ctx.send(embed=embed)
                await asyncio.sleep(5)
                await ctx.channel.delete()
                cursor.execute(f'DELETE FROM tickets WHERE server={server} and ticket={ctx.channel.id}')   
                db.commit()
                cursor.close()

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
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.name == self.client.user.name:
            pass 
        else:
            server = user.guild.id
            db = sqlite3.connect('db/tickets.db')
            cursor = db.cursor()
            cursor.execute(f'SELECT * FROM setup WHERE server={server}')
            rows = cursor.fetchone()
            if rows == None:
                pass
            else:
                if reaction.emoji == '📨':
                    if reaction.message.channel.id == rows[1]:
                        await reaction.remove(user)
                        ticket_channel = await user.guild.create_text_channel(f"ticket-{user.name}")
                        await ticket_channel.set_permissions(user.guild.get_role(user.guild.id), send_messages=False, read_messages=False)
                        role = user.guild.get_role(rows[2])
                        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)    
                        await ticket_channel.set_permissions(user, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                        msg = await ticket_channel.send(role.mention)
                        embed = discord.Embed(title='ZeeBot', description=f'¡Ticket creado con exito por {user.mention}! \n Sea paciente mientras un staff le responde.', color=0xffa348)
                        embed.set_footer(text='By Daldude1#9156')
                        await msg.edit(embed=embed)
                        await msg.add_reaction('🛠️')
                        cursor.execute(f'INSERT INTO tickets(server, ticket, message) VALUES(?, ?, ?)', (server, ticket_channel.id, msg.id))
                        db.commit()
                        cursor.close()
                elif reaction.emoji == '🛠️':
                    cursor.execute(f'SELECT * FROM tickets WHERE server={server} and ticket={reaction.message.channel.id}')
                    rows = cursor.fetchone()
                    if rows == None:
                        pass
                    else:
                        if reaction.message.channel.id == rows[1]:
                            await reaction.remove(user)
                            msg = await reaction.message.channel.fetch_message(rows[2])
                            await msg.add_reaction('✅')
                            await msg.add_reaction('❎')
                elif reaction.emoji == '✅':
                    cursor.execute(f'SELECT * FROM tickets WHERE server={server} and ticket={reaction.message.channel.id}')
                    rows = cursor.fetchone()
                    if rows == None:
                        pass
                    else:
                        if reaction.message.channel.id == rows[1]:
                            await reaction.remove(user)
                            embed = discord.Embed(title='ZeeBot | Se cerrara el ticket en 5s', color=0xffa348)
                            await reaction.message.channel.send(embed=embed)  
                            await asyncio.sleep(5)
                            await reaction.message.channel.delete()           
                            cursor.execute(f'DELETE FROM tickets WHERE server={server} and ticket={reaction.message.channel.id}')   
                            db.commit()
                            cursor.close()
                elif reaction.emoji == '❎':
                    cursor.execute(f'SELECT * FROM tickets WHERE server={server} and ticket={reaction.message.channel.id}')
                    rows = cursor.fetchone()
                    if rows == None:
                        pass
                    else:
                        if reaction.message.channel.id == rows[1]:
                            await reaction.message.clear_reaction('❎')
                            await reaction.message.clear_reaction('✅')
def setup(client):
    client.add_cog(ticketsSetup(client))
    client.add_cog(ticketsSystem(client))
