import discord
import os
from discord import option
from flask import Flask, request
from threading import Thread

bot = discord.Bot()

# 初期データ
MAP_CACHE = {m: "データ更新待ち..." for m in ["ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss"]}

@bot.slash_command(name="vct_analytics", description="VCT最新統計を即座に表示します")
@option("map_name", description="マップ名を選択", choices=["ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss"])
async def vct_analytics(ctx, map_name: str):
    data = MAP_CACHE.get(map_name)
    
    embed = discord.Embed(
        title=f"📊 {map_name.upper()} リアルタイム統計",
        description=data,
        color=0x00ff00
    )
    embed.set_footer(text="🕒 マップ別に順次ローテーション更新中")
    await ctx.respond(embed=embed)

app = Flask('')

@app.route('/')
def home():
    return "KAY/O Bot is Active"

# 1つのマップを更新する専用の窓口
@app.route('/update_single_map', methods=['POST'])
def update_single_map():
    global MAP_CACHE
    payload = request.json
    m_name = payload.get("map")
    m_data = payload.get("data")
    
    if m_name and m_data:
        MAP_CACHE[m_name] = m_data
        print(f"Updated cache for: {m_name}")
        return "Update Success", 200
    return "Update Failed", 400

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.sync_commands()

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.run(os.environ.get("DISCORD_TOKEN"))
