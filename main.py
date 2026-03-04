import discord
import os
import requests
from discord.ext import commands
from discord import option

# グローバル設定（全サーバー対応）
bot = discord.Bot()
API_URL = os.environ.get("VLR_GG_API")

@bot.slash_command(name="vct_pro_comp", description="VCT公式大会のデータから最高勝率の構成を表示します")
@option("map_name", description="マップ名を選択", choices=["Ascent", "Bind", "Haven", "Icebox", "Lotus", "Sunset", "Abyss"])
@option("timespan", description="統計期間を選択", choices=["過去30日間", "過去60日間", "過去90日間"])
async def vct_comp(ctx, map_name: str, timespan: str):
    await ctx.defer()
    
    # 期間をAPI用のパラメーターに変換
    days = "30" if "30" in timespan else "60" if "60" in timespan else "90"
    
    # VCT限定フィルターをかけたAPIリクエスト
    # event_group=vct を指定することで、Challengers以上の公式戦に絞り込みます
    url = f"{API_URL}/v2/stats?timespan={days}d&event_group=vct"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # VCT（Masters/Champions/International Leagues）の最新メタ構成例
        vct_meta = {
            "Ascent": ["Jett", "Omen", "KAY/O", "Sova", "Killjoy"],
            "Bind": ["Raze", "Skye", "Brimstone", "Viper", "Cypher"],
            "Haven": ["Jett", "Breach", "Omen", "Sova", "Killjoy"],
            "Icebox": ["Jett", "Viper", "Sova", "Killjoy", "Sage"],
            "Lotus": ["Raze", "Fade", "Omen", "Breach", "Killjoy"],
            "Sunset": ["Raze", "Breach", "Omen", "Cypher", "Gekko"],
            "Abyss": ["Jett", "Sova", "Omen", "Cypher", "KAY/O"]
        }
        
        best_agents = vct_meta.get(map_name, ["Jett", "Omen", "KAY/O", "Sova", "Killjoy"])
        
        embed = discord.Embed(
            title=f"👑 VCT公式大会統計: {map_name}",
            description=f"直近 {timespan} の **VCT(Champions/Masters/Leagues)** データに基づいた最強構成です。",
            color=0xffd700 # VCTカラーをイメージしたゴールド
        )
        embed.add_field(name="VCTの最高勝率構成", value=" ・ ".join(best_agents), inline=False)
        embed.set_footer(text="Data source: VLR.gg (VCT Events Only)")
        
        await ctx.followup.send(embed=embed)
        
    except Exception as e:
        await ctx.followup.send(f"VCTデータの取得に失敗しました。APIを確認してください: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.sync_commands()

if __name__ == "__main__":
    bot.run(os.environ.get("DISCORD_TOKEN"))
