import asyncio
import datetime
import io
import json
import random

import discord
import requests
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands

from config import *

prefix = settings['PREFIX']

client = commands.Bot(
    command_prefix=settings['PREFIX'])

client.remove_command('help')


# на запуске скажет в консоль
@client.event
async def on_ready():
    print("ПОДКЛЮЧЁН И ГОТОВ МЯУ")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("&help"))


# если комманда введина не правильно
@client.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=discord.Embed(
            description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
        ))


# пинг бота к серверу
@client.command(
    aliases=['Ping', 'PING', 'pING', 'ping', 'Пинг', 'ПИНГ', 'пИНГ', 'пинг', 'Понг', 'ПОНГ', 'пОНГ', 'понг'])
async def __ping(ctx):
    ping = client.ws.latency
    ping_emoji = '🟩🔳🔳🔳🔳'
    if ping > 0.10000000000000000:
        ping_emoji = '🟧🟩🔳🔳🔳'
    if ping > 0.15000000000000000:
        ping_emoji = '🟥🟧🟩🔳🔳'
    if ping > 0.20000000000000000:
        ping_emoji = '🟥🟥🟧🟩🔳'
    if ping > 0.25000000000000000:
        ping_emoji = '🟥🟥🟥🟧🟩'
    if ping > 0.30000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟧'
    if ping > 0.35000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟥'

    message = await ctx.send('Пожалуйста, подождите. . .')
    await message.edit(
        content=f'Понг! {ping_emoji} `{ping * 1000:.0f}ms` :ping_pong:')
    print(
        f'[Logs:utils] Пинг сервера был выведен | {prefix}ping')
    print(f'[Logs:utils] На данный момент пинг == {ping * 1000:.0f}ms | {prefix}ping')


# помощь
@client.command(aliases=['Help', 'help', 'HELP', 'hELP', 'хелп', 'Хелп', 'ХЕЛП', 'хЕЛП'])
async def __help(ctx):
    emb = discord.Embed(title='ДОСТУПНЫЕ КОМАНДЫ:', colour=discord.Color.red())

    emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    emb.add_field(name='Информация',
                  value=f'`{prefix}хелп` `{prefix}инфо` `{prefix}server` `{prefix}профиль` `{prefix}авторы` ',
                  inline=False)
    emb.add_field(name='Модерирование', value=f'`{prefix}mute` `{prefix}ban` `{prefix}kick` `{prefix}clear`',
                  inline=False)
    emb.add_field(name='бот',
                  value=f'`{prefix}bot` `{prefix}cool` `{prefix}server` `{prefix}pic` `{prefix}ping`',
                  inline=False)
    emb.add_field(name='Что то..',
                  value=f'`{prefix}я/карта` `{prefix}time` `{prefix}phone_info` `{prefix}ip_info` `{prefix}game` `{prefix}roll`',
                  inline=False)
    emb.add_field(name='Крестики нолики',
                  value=f'`{prefix}tictactoe` `{prefix}place`', inline=False)
    emb.set_thumbnail(url=client.user.avatar_url)
    emb.set_footer(icon_url=client.user.avatar_url, text=f'{client.user.name} © Copyright 2022 | Все права защищены')

    await ctx.send(embed=emb)

    print(f'[Logs:info] Справка по командам была успешно выведена | {prefix}help ')


# рандомная картинка по поиску
@client.command('pic')
async def pic(ctx, naming):
    link = 'https://some-random-api.ml/img/' + naming
    response = requests.get(link)
    json_data = json.loads(response.text)
    embed = discord.Embed(color=0xff9900, title='Your pic')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)


# информация о сервере
@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Информация о сервере",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Владелец", value=owner, inline=True)
    embed.add_field(name="Айди сервера", value=id, inline=True)
    embed.add_field(name="Регион", value=region, inline=True)
    embed.add_field(name="Колличество участников", value=memberCount, inline=True)

    await ctx.send(embed=embed)


# рандомное число от N до N
@client.command()
async def roll(ctx, num1, num2):
    await ctx.send(random.randint(int(num1), int(num2)))


# Тот кто вызывает эту комманду не крутой(
@client.command()
async def cool(ctx, member: discord.Member):
    if ctx.invoked_subcommand is None:
        await ctx.send(f'Нет, {member.name} не крутой')


# Бот крутой!
@client.command(name='bot')
async def _bot(ctx):
    await ctx.send('Да бот крутой!')


# выдования роли
@client.event
async def on_member_join(member):
    channel = client.get_channel(935814911244767252)

    role = discord.utils.get(member.guild.roles, id=934744764908179476)

    await member.add_roles(role)
    await channel.send(
        embed=discord.Embed(description=f'Пользователь ``{member.name}``, присоеденился к нам!', color=0x3ec95d))


# цензура и приветствие
@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()
    if msg in greeting_words:
        await message.channel.send(f"{message.author.name}, ку!")

    for bad_content in msg.split(" "):
        if bad_content in bad_words:
            await message.channel.send(f"{message.author.mention}, нельзя такое писать")
            await message.delete()

# немного математики
@client.command()
async def math(ctx, a: int, arg, b: int):
    if arg == '+':
        await ctx.send(f'Result: {a + b}')

    elif arg == '-':
        await ctx.send(f'Result: {a - b}')

    elif arg == '/':
        await ctx.send(f'Result: {a / b}')


# информация о айпи
@client.command()
async def ip_info(ctx, arg):
    response = requests.get(f'http://ipinfo.io/{arg}/json')

    user_ip = response.json()['ip']
    user_city = response.json()['city']
    user_region = response.json()['region']
    user_country = response.json()['country']
    user_location = response.json()['loc']
    user_org = response.json()['org']
    user_timezone = response.json()['timezone']

    global all_info
    all_info = f'\n<INFO>\nIP : {user_ip}\nCity : {user_city}\nRegion : {user_region}\nCountry : {user_country}\nLocation : {user_location}\nOrganization : {user_org}\nTime zone : {user_timezone}'

    await ctx.author.send(all_info)


# uuid
@client.command()
async def key(ctx):
    import uuid
    await ctx.send(f'Key : {uuid.uuid4()}')


# информация о номере телефона
@client.command()
async def phone_info(ctx, arg):
    response = requests.get(f'https://htmlweb.ru/geo/api.php?json&telcod={arg}')

    user_country = response.json()['country']['english']
    user_id = response.json()['country']['id']
    user_location = response.json()['country']['location']
    user_city = response.json()['capital']['english']
    user_width = response.json()['capital']['latitude']
    user_lenth = response.json()['capital']['longitude']
    user_post = response.json()['capital']['post']
    user_oper = response.json()['0']['oper']

    global all_info
    all_info = f'<INFO>\nCountry : {user_country}\nID : {user_id}\nLocation : {user_location}\nCity : {user_city}\nLatitude : {user_width}\nLongitude : {user_lenth}\nIndex post : {user_post}\nOperator : {user_oper}'

    await ctx.author.send(all_info)


# очистка
@client.command(name="clear", brief="Очистить чат от сообщений, по умолчанию 10 сообщений", usage="clear <amount=10>")
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Was deleted {amount} messages...")


# кикнуть
@client.command(name="kick", brief="Выгнать пользователя с сервера", usage="kick <@user> <reason=None>")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete(delay=1)

    await member.send(f"Пока ботик")
    await ctx.send(f"Участник {member.mention} был выгнан с сервера!")
    await member.kick(reason=reason)


# забанить
@client.command(name="ban", brief="Забанить пользователя на сервере", usage="ban <@user> <reason=None>")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.send(f"Ты был забанен бот")
    await ctx.send(f"Участник {member.mention} был забанен на сервере")
    await member.ban(reason=reason)


# разбанить
@client.command(name="unban", brief="Разбанить пользователя на сервере", usage="unban <user_id>")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await client.fetch_user(user_id)
    await ctx.guild.unban(user)


# Узнать текущее время
@client.command()
async def time(ctx):
    emb = discord.Embed(title='ВРЕМЯ', description='Вы сможете узнать текущее время', colour=discord.Color.green(),
                        url='https://www.timeserver.ru')

    emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    emb.set_footer(text='Спасибо за использование нашего бота!')
    emb.set_thumbnail(url='https://sun9-35.userapi.com/c200724/v200724757/14f24/BL06miOGVd8.jpg')

    now_date = datetime.datetime.now()

    emb.add_field(name='Time', value='Time : {}'.format(now_date))

    await ctx.author.send(embed=emb)


@client.command()
async def quote(ctx):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=ru')
    r = response.json()

    await ctx.send(r["quoteText"])
    await ctx.send(r["quoteAuthor"])

# карточка участника
@client.command(aliases=['я', 'карта'])
async def card_user(ctx):
    await ctx.channel.purge(limit=1)

    img = Image.new('RGBA', (400, 200), '#232529')
    url = str(ctx.author.avatar_url)[:-10]

    response = requests.get(url, stream=True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)

    img.paste(response, (15, 15, 115, 115))

    idraw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator

    headline = ImageFont.truetype('arial.ttf', size=20)
    undertext = ImageFont.truetype('arial.ttf', size=12)

    idraw.text((145, 15), f'{name}#{tag}', font=headline)
    idraw.text((145, 50), f'ID: {ctx.author.id}', font=undertext)

    img.save('user_card.png')

    await ctx.send(file=discord.File(fp='user_card.png'))


# мут
@client.command(aliases=['mute'])
async def __mute(ctx, member: discord.Member = None, amount_time=None, *, reason=None):
    if member is None:
        await ctx.send(embed=discord.Embed(
            title=f'{ctx.author.mention}, **укажите пользователя**',
            description=f'Пример: .mute **@user** time reason'
        ))
    elif amount_time is None:
        await ctx.send(embed=discord.Embed(
            title=f'{ctx.author.mention}, **укажите кол-во времени**',
            description=f'Пример: .mute @user **time** reason'
        ))
    elif reason is None:
        await ctx.send(embed=discord.Embed(
            title=f'{ctx.author.mention}, **укажите причину**',
            description=f'Пример: .mute @user time **reason**'
        ))
    else:
        if 'm' in amount_time:
            await ctx.send(embed=discord.Embed(
                description=f'''**[<:_off:934743682626781184>]** Вы были замучены на **{amount_time}**.
                **Выдал мут:** {ctx.author}
                ```css
Причина: [{reason}]
                ```
                ''',
                color=0x36393E,
            ))

            mute_role = discord.utils.get(ctx.guild.roles, id=934743682626781184)
            await member.add_roles(mute_role)
            await asyncio.sleep(int(amount_time[:-1]) * 60)
            await member.remove_roles(mute_role)

            await ctx.send(embed=discord.Embed(
                description=f'''**[<:rage:934743682626781184>]** Время мута истекло, вы были размучены''',
                color=0x2F3136
            ))
        elif 'h' in amount_time:
            await ctx.send(embed=discord.Embed(
                description=f'''**[<::rage:934743682626781184>]** Вы были замучены на **{amount_time}**.
                **Выдал мут:** {ctx.author}
                ```css
Причина: [{reason}]
                ```
                ''',
                color=0x36393E,
            ))

            mute_role = discord.utils.get(ctx.guild.roles, id=934743682626781184)
            await member.add_roles(mute_role)
            await asyncio.sleep(int(amount_time[:-1]) * 60 * 60)
            await member.remove_roles(mute_role)

            await ctx.send(embed=discord.Embed(
                description=f'''**[<:rage:934743682626781184>]** Время мута истекло, вы были размучены''',
                color=0x2F3136
            ))
        elif 'd' in amount_time:
            await ctx.send(embed=discord.Embed(
                description=f'''**[<:rage:934743682626781184>]** Вы были замучены на **{amount_time}**.
                **Выдал мут:** {ctx.author}
                ```css
Причина: [{reason}]
                ```
                ''',
                color=0x36393E,
            ))

            mute_role = discord.utils.get(ctx.guild, id=934743682626781184)
            await member.add_roles(mute_role)
            await asyncio.sleep(int(amount_time[:-1]) * 60 * 60 * 24)
            await member.remove_roles(mute_role)

            await ctx.send(embed=discord.Embed(
                description=f'''**[<:rage:934743682626781184>]** Время мута истекло, вы были размучены''',
                color=0x2F3136
            ))
        else:
            await ctx.send(embed=discord.Embed(
                description=f'''**[<:rage:934743682626781184>]** Вы были замучены на **{amount_time}s**.
                **Выдал мут:** {ctx.author}
                ```css
Причина: [{reason}]
                ```
                ''',
                color=0x36393E,
            ))

            mute_role = discord.utils.get(ctx.guild.roles, id=934743682626781184)
            await member.add_roles(mute_role)
            await asyncio.sleep(int(amount_time))
            await member.remove_roles(mute_role)

            await ctx.send(embed=discord.Embed(
                description=f'''**[<:sunglasses:934743682626781184>]** Время мута истекло, вы были размучены''',
                color=0x2F3136
            ))


# Угадай число
@client.command()
async def game(self, ctx):
    number = random.randint(0, 100)
    for i in range(0, 5):
        await ctx.send('guess')
        response = await self.bot.wait_for('message')
        guess = int(response.content)
        if guess > number:
            await ctx.send('Больше')
        elif guess < number:
            await ctx.send('Меньше')
        else:
            await ctx.send('Угадали')


# создание поля и запуск игры
@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("Это ход <@" + str(player1.id) + ">")
        elif num == 2:
            turn = player2
            await ctx.send("Это ход <@" + str(player2.id) + ">")
    else:
        await ctx.send("Дождитесь окончания игры")


# Установка элемента
@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " победил!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Это ничья")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Вы точно ввели число в радиусе от 1 до 9")
        else:
            await ctx.send("Это не твой ход")
    else:
        await ctx.send("Пожалуйста начните новую игру коммандой !tictactoe")


# проверка на победу
def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


# ошибка запуска
@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Пожалуйста укажите двух игроков")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Пожалуйста пинганите того игрока с которым хочешь поиграть")


# ошибка в нарисовании крестика
@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Пожалуйста укажите в какую клеточку вы хотите поставить свою метку")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Пишите целыми числами")

if __name__ == '__main__':
    client.run(settings['TOKEN'])
