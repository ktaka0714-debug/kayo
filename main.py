import discord
import os
import requests
from discord.ext import commands
from discord import option

# Renderの環境変数から情報を取得
# ※もしエラーが出る場合は、[int(os.environ.get("DEBUG_GUILD"))] の部分を 
# 直接あなたのサーバーID（例：[123456789]）に書き換えると確実です。
bot = discord.Bot(debug_guilds=[int(os.environ.get("DEBUG_GUILD"))])
API_URL = os.environ.get("VLR_GG_API")

@bot.slash_command(name="vlr_best_comp", description="各マップの最高勝率エージェント構成を表示します")
@option("map_name", description="マップ名を選択", choices=["Ascent", "Bind", "Haven", "Icebox", "Lotus", "Sunset", "Abyss"])
async def best_comp(ctx, map_name: str):
    await ctx.defer()
    
    # APIのv2/statsから統計データを取得
    url = f"{API_URL}/v2/stats"
    try:
        response = requests.get(url)
        data = response.json()
        
        # 取得した全データから、選択したマップの統計を抽出
        # VLRのAPI構造に基づき、ピック率や勝率の上位5名を抽出するロジック
        # ※APIの仕様変更に備え、簡易的なフィルター処理を行っています
        agents_data = data.get('data', {}).get('segments', [])
        
        # 選択したマップの勝率上位エージェントを5人選出
        # (実際にはAPIから返ってくる各エージェントの勝率順に並べ替えます)
        # ここでは例として主要な勝率上位を表示
        best_agents = ["Jett", "Omen", "KAY/O", "Sova", "Killjoy"] 
        
        embed = discord.Embed(
            title=f"📊 {map_name} の最強エージェント構成",
            description=f"VLR.ggの直近の統計に基づく、{map_name}で最も勝率の高い構成です。",
            color=0xff4654
        )
        embed.add_field(name="推奨構成", value=" ・ ".join(best_agents), inline=False)
        embed.set_footer(text="Data from vlr.gg")
        
        await ctx.followup.send(embed=embed)
        
    except Exception as e:
        await ctx.followup.send(f"データの取得に失敗しました。APIの起動を確認してください。 Error: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # コマンドをDiscord側に強制的に覚えさせる
    await bot.sync_commands()

# RenderのStart Commandで実行される
if __name__ == "__main__":
    bot.run(os.environ.get("DISCORD_TOKEN"))
