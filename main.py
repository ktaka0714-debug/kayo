import discord
from discord import option
from flask import Flask, request, jsonify
import threading
import os

# Discordボットのセットアップ
bot = discord.Bot()
app = Flask(__name__)

# 全マップのデータを個別に保存する辞書
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
    # 選択されたマップ名（小文字）でデータを検索
    m_name = map_name.lower()
    result = map_data.get(m_name, f"⚠️ {m_name} のデータはまだ届いていません。GASを実行してください。")
    await ctx.respond(result)

@app.route('/update_single_map', methods=['POST'])
def update_map():
    data = request.json
    m_name = data.get('map')
    m_content = data.get('data')
    
    if m_name and m_content:
        # マップ名をキーにして個別に保存（上書きされないように）
        map_data[m_name.lower()] = m_content
        print(f"✅ Data updated for: {m_name}")
        return jsonify({"status": "success", "map": m_name}), 200
    return jsonify({"status": "error"}), 400

def run_flask():
    # Renderのポート10000で待機
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    # Flaskを別スレッドで起動
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    # Discordボットを起動
    bot.run(os.getenv('DISCORD_TOKEN'))
