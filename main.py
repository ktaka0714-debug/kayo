import discord
import os
from discord import option
from flask import Flask, request
from threading import Thread
from waitress import serve  # 本番用サーバー

bot = discord.Bot()

# マップデータの保存先
MAP_CACHE = {m: "🌎 世界中の最新統計を統合中です。数分後にお試しください..." for m in ["ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss"]}

@bot.slash_command(name="vct_analytics", description="世界4大リーグを統合した最新統計を表示します")
@option("map_name", description="マップ名を選択", choices=["ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss"])
async def vct_analytics(ctx, map_name: str):
    data = MAP_CACHE.get(map_name)
    
    embed = discord.Embed(
        title=f"📊 {map_name.upper()} 世界統合メタ統計",
        description=data,
        color=0xff4654
    )
    embed.set_footer(text="📊 配信元: VCT Pacific / EMEA / Americas / CN (Past 30d)")
    await ctx.respond(embed=embed)

# --- Flaskの設定 (GASからの受取窓口) ---
app = Flask('')

@app.route('/')
def home():
    return "KAY/O Bot is Online"

@app.route('/update_single_map', methods=['POST'])
def update_single_map():
    global MAP_CACHE
    try:
        payload = request.json
        m_name = payload.get("map")
        m_data = payload.get("data")
        if m_name and m_data:
            MAP_CACHE[m_name] = m_data
            print(f"✅ Data updated: {m_name}")
            return "Update Success", 200
    except Exception as e:
        print(f"❌ Update Error: {e}")
    return "Update Failed", 400

def run_web_server():
    # Renderから指定されたポートを取得（デフォルト10000）
    port = int(os.environ.get("PORT", 10000))
    # Flaskの標準サーバーではなく、waitressで起動して警告を消す
    print(f"🚀 Starting Production WSGI Server on port {port}...")
    serve(app, host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    # スラッシュコマンドを強制的に同期
    await bot.sync_commands()

if __name__ == "__main__":
    # Webサーバーを別スレッドで起動
    t = Thread(target=run_web_server)
    t.start()
    # ボットを起動
    bot.run(os.environ.get("DISCORD_TOKEN"))
