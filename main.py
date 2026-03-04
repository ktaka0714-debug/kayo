import discord
from discord import option
from flask import Flask, request, jsonify
import threading
import os

# Discordボットのセットアップ
bot = discord.Bot()
app = Flask(__name__)

# データを保存する変数
map_data = {}

@bot.event
async def on_ready():
    print(f"✅ {bot.user} が起動しました！")

@bot.slash_command(name="vct_analytics", description="世界統合メタ統計を表示します")
@option("map_name", description="マップ名を選択", choices=[
    "ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss", 
    "fracture", "pearl", "split", "breeze", "corrode"
])
async def vct_analytics(ctx, map_name: str):
    # この下の2行が必ず「半角スペース4つ」で始まっている必要があります
    result = map_data.get(map_name, f"⚠️ {map_name} のデータはまだ届いていません。GASを実行してください。")
    await ctx.respond(result)

@app.route('/update_single_map', methods=['POST'])
def update_map():
    data = request.json
    m_name = data.get('map')
    m_content = data.get('data')
    if m_name and m_content:
        map_data[m_name] = m_content
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.run(os.getenv('DISCORD_TOKEN'))
