import discord
import os
from discord import option
from flask import Flask, request
from threading import Thread

bot = discord.Bot()

# 初期データ
MAP_CACHE = {m: "🌎 データを取得中です。数分お待ちください。" for m in ["ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss"]}

@bot.slash_command(name="vct_analytics", description="VCT最新統計を即座に表示します")
@option("map_name", description="マップ名を選択", choices=["ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss"])
async def vct_analytics(ctx, map_name: str):
    data = MAP_CACHE.get(map_name)
    
    embed = discord.Embed(
        title=f"📊 {map_name.upper()} 統計 (VCT 2026)",
        description=data,
        color=0xff4654
    )
    embed.set_footer(text="GASによる自動更新済み")
    await ctx.respond(embed=embed)

# --- GASからのデータ受け取り口 ---
app = Flask('')

@app.route('/')
def home():
    return "KAY/O Bot is Active"

@app.route('/update_single_map', methods=['POST'])
def update_single_map():
    global MAP_CACHE
    try:
        payload = request.json
        m_name = payload.get("map")
        m_data = payload.get("data")
        if m_name and m_data:
            MAP_CACHE[m_name] = m_data
            return "Update Success", 200
    except Exception:
        pass
    return "Update Failed", 400

def run():
    # Renderから指定されたポートでWebサーバーを起動
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.run(os.environ.get("DISCORD_TOKEN"))
