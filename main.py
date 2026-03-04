import discord
import os
from discord import option
from flask import Flask, request
from threading import Thread

bot = discord.Bot()

# 全マップのデータを保存する脳内メモリ
MAP_CACHE = {m: "🌎 世界中の最新統計を統合中です。数分後にお試しください..." for m in ["ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss"]}

@bot.slash_command(name="vct_analytics", description="世界4大リーグ（Pacific/EMEA/Americas/CN）を統合した最新統計を表示します")
@option("map_name", description="マップ名を選択", choices=["ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss"])
async def vct_analytics(ctx, map_name: str):
    # 通信を待たずに即答！
    data = MAP_CACHE.get(map_name)
    
    embed = discord.Embed(
        title=f"📊 {map_name.upper()} 世界統合メタ統計",
        description=data,
        color=0xff4654
    )
    embed.set_footer(text="📊 配信元: VCT Pacific / EMEA / Americas / CN (Past 30d)")
    await ctx.respond(embed=embed)

# --- GASからデータを受け取る窓口 ---
app = Flask('')

@app.route('/')
def home():
    return "KAY/O Global Analytics Active"

@app.route('/update_single_map', methods=['POST'])
def update_single_map():
    global MAP_CACHE
    try:
        payload = request.json
        m_name = payload.get("map")
        m_data = payload.get("data")
        if m_name and m_data:
            MAP_CACHE[m_name] = m_data
            print(f"Update successful for {m_name}")
            return "Update Success", 200
    except Exception as e:
        print(f"Update Error: {e}")
    return "Update Failed", 400

def run():
    # Renderのポートに合わせてWebサーバーを起動
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.sync_commands()

if __name__ == "__main__":
    # Webサーバーを別スレッドで起動
    t = Thread(target=run)
    t.start()
    # Discordボットを起動
    bot.run(os.environ.get("DISCORD_TOKEN"))
