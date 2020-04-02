import discord
from discord.ext import commands
import logging
import temp_save_vc_id as ts
from read_VC_files import team_names


logging.basicConfig(level=logging.INFO)

with open('timmy_admin.txt', 'r') as f:
    TOKEN = f.read().rstrip()

bot = commands.Bot(command_prefix='.')
bot_admins = [278704257887240192, 228197649767989248]
# channel_user_limit = 4



@bot.event
async def on_ready():  # on starting bot
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name='CreatorOfVoices'))



# check decorator
def is_bot_admin():
    async def predicate(ctx):
        return ctx.author.id in bot_admins
    return commands.check(predicate)


@bot.command()
async def list_teams(ctx):
    await ctx.send(team_names)


@bot.command()
@is_bot_admin()
async def list_cool_kids(ctx):
    admins_names = []
    for admin_id in bot_admins:
        admin_obj = await bot.fetch_user(admin_id)
        admins_names.append(str(admin_obj))  # str outputs "name#1234" instead of just name
    await ctx.send(admins_names)


@bot.command()
@is_bot_admin()
async def test_cat_split(ctx, *categories):
    await ctx.send(categories)


@bot.command()
@is_bot_admin()
async def make_team_channels(ctx, channel_user_limit, *categories):
    # if temp_ids file exists: return
    if ts.temp_file.exists():
        await ctx.send(f'Error: Channels are already created. I have a temp file full of them.')
        return
    category_ids = []
    categories_temp = []
    for category_name in categories:
        category_obj = await ctx.guild.create_category(category_name)
        categories_temp.append(category_obj)
        category_ids.append(category_obj.id)

    voice_channel_ids = []
    for i_pos, t_name in enumerate(team_names):
        category_index = i_pos % len(categories)  # loop through categories for creation
        new_channel = await categories_temp[category_index].create_voice_channel(t_name, user_limit=channel_user_limit)
        # TODO: create invites for players
        voice_channel_ids.append(new_channel.id)

    # dump cat ids and vc ids so they can be deleted
    temp_data = {
        'cat_ids': category_ids,
        'vc_ids': voice_channel_ids
    }
    ts.dump_to_json(temp_data, ts.temp_file)


@bot.command()
@is_bot_admin()
async def delete_team_channels(ctx):
    if not ts.temp_file.exists():
        await ctx.send(f'I dont remember making channels. There is no temp file.')

    category_channels = []
    temp_ids = ts.read_json(ts.temp_file)
    # delete voice channels
    for vc_id in temp_ids.get('vc_ids'):
        chan = await bot.fetch_channel(vc_id)
        if chan.category not in category_channels:
            category_channels.append(chan.category)  # get categories from the channels
        await chan.delete()

    # delete categories
    for cat_chan in category_channels:
        await cat_chan.delete()

    # delete temp file
    ts.delete_file(ts.temp_file)


if __name__ == "__main__":
    bot.run(TOKEN)
