import random
import discord
from discord.ext import commands

#TOKENの値を書き換えてください
TOKEN = "ここを書き換える"
intents = discord.Intents.default()
intents.message_content = True
#コマンドの接頭辞(!の場所)を好きなものに書き換えてください
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    #BOTが起動したときにterminalに出力されます
    print(f'Logged in as {client.user.name}')

@client.command()
async def lobby(ctx):
    #!lobbyとDiscord上で入力したときにチーム分け用のvcチャンネルの作成
    global default, Category, vc1, vc2
    LobbyName = "チーム分け"
    Guild = ctx.guild
    Category = await Guild.create_category(LobbyName)
    default = await Category.create_voice_channel("待機室")
    vc1 = await Category.create_voice_channel("チーム1")
    vc2 = await Category.create_voice_channel("チーム2")

@client.command()
async def group(ctx):
    #!groupとDiscord上で入力したときにチームvcに自動で振り分ける
    members = default.members.copy()
    random.shuffle(members)
    half = len(members)//2
    for i, member in enumerate(members):
        if i < half:
            await member.move_to(vc1)
        else:
            await member.move_to(vc2)
    await ctx.send("振り分け完了!!")

@client.command()
async def here(ctx):
    #!hereとDiscord上で入力したときに待機vcに全員を移動
    vc1_members = vc1.members.copy()
    vc2_members = vc2.members.copy()
    for member in vc2_members:
        await member.move_to(default)
    for member in vc1_members:
        await member.move_to(default)
    await ctx.send("集合!!")

@client.command()
async def dis(ctx):
    #!disとDiscord上で入力したときにチーム分け用のvcチャンネルの削除
    await vc1.delete()
    await vc2.delete()
    await default.delete()
    await Category.delete()
    await ctx.send("解散!!チーム分けチャンネルを削除します")

@client.event
async def on_voice_state_update(member, before, after):
    #チーム分け用vcに誰もいなくなったらチーム分け用のvcチャンネルの削除
    if before.channel != after.channel:
        if (len(vc1.members)==0) and (len(vc2.members)==0) and (len(default.members)==0):
            await vc1.delete()
            await vc2.delete()
            await default.delete()
            await Category.delete()
#bot起動するための関数
def client_run():
    client.run(TOKEN)

# bot起動用
client.run(TOKEN)