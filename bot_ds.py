# Bot discord - Mário

import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound

# Prefixo dos comandos no Discord
bot = commands.Bot("!")

# async - funções que funcionam separadamente e podem rodar ao mesmo tempo
# await - funções em que a proxima só é iniciada após o seu termino

# ---------------------------------------------------------------------------------------------
# Bot events:

# Sempre que o bot estiver pronto a funcionar envia uma mensagem no terminal
@bot.event
async def on_ready():
    print(f"Olá, Estou pronto! Estou conectado como {bot.user}")

# O bot lê as mensagens enviadas no servidor do discord e caso contenham a palavra "proibida", ele elimina a mensagem e exibe uma mensagem
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return # Se quem enviar a mensagem for o próprio bot, ignora

    if "palavrão" in message.content: # Neste caso "palavrão" é a palavra proibida
        await message.channel.send(f"Por favor, {message.author.name}, não ofenda os demais usuários!")

        await message.delete()
    
    await bot.process_commands(message)

# Função que atribui cargos no Discord atravéz de reações
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "👍":
        role = user.guild.get_role(994195995799863346) # ID do cargo
        await user.add_roles(role)
    elif reaction.emoji == "😠":
        role = user.guild.get_role(994196033083015271) # ID do cargo
        await user.add_roles(role)

# Caso o bot receba um comando inexistente, envia uma mensagem de erro
@bot.event 
async def on_command_error(ctx, error):
    if isinstance(error,CommandNotFound):
        await ctx.send("Esse comando não existe!")
    else:
        raise error


# ---------------------------------------------------------------------------------------------
# Bot comandos:

# O bot envia uma mensagem a saudar quem fez o comando
@bot.command(name = "ola", help = "Envia um \"Olá\"")
async def send_hello(ctx):
    name = ctx.author.name

    response = "Olá, " + name

    await ctx.send(response)

# O bot calcula o valor de uma expressão de 2 argumentos (tem que ser escrita junta, p.e.: 1+1)
@bot.command(name = "calcula", help = "Calcula a soma de 2 argumentos")                 
async def calculate_expression(ctx, expression): 
    response = eval(expression)

    await ctx.send("A resposta é: " + str(response))

# O bot envia uma DM a quem executou o comando
@bot.command(name = "segredo", help = "Envia te um segredo por DM")
async def secret(ctx):
    try:
        await ctx.author.send("Olá")
        await ctx.author.send("O Eduardo é lindo!")
    except Exception as error:
        await ctx.send("As tuas opções de privacidade não permitem que te conte o segredo!")

# O bot envia uma foto aleatória para o Discord
@bot.command(name = "foto", help = "Envia uma foto aleatória")
async def get_random_image(ctx):
    url_image = "https://picsum.photos/1920/1080"

    embed = discord.Embed(
        title = "Resultado da busca da imagem",
        description = "PS: A busca é totalmente aleatória",
        color = 0x0000FF,
    )

    embed.set_author(name = bot.user.name, icon_url = bot.user.avatar_url)

    embed.set_footer(text = bot.user.name, icon_url = bot.user.avatar_url)

    embed.add_field(name = "Ola", value = "Aprendi no youtube")
    embed.add_field(name = "Xau", value = "{largura}/{altura}")

    embed.add_field(name = "Eduardo", value = url_image, inline = False)

    embed.set_image(url = url_image)

    await ctx.send(embed = embed)



# ---------------------------------------------------------------------------------------------
# Token "secreto" que dá acesso ao manuseamento do bot
bot.run("token")

