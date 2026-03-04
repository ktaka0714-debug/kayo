import discord
import os
from discord import option

bot = discord.Bot()

# 最新のVCTプロ統計データ（直近30日）
MAP_STATS = {
    "Bind": [
        "1. Gentle Mates (4勝): Neon/Waylay/Skye/Viper/Astra (4回)",
        "2. Gen.G (3勝): Raze/Skye/Brim/Viper/Cypher (3回)",
        "3. Fnatic (3勝): Raze/Fade/Brim/Viper/Cypher (4回)",
        "4. Leviatán (2勝): Gekko/Breach/Omen/Viper/Cypher (2回)",
        "5. ZETA (2勝): Raze/Skye/Brim/Viper/Cypher (3回)"
    ],
    "Ascent": [
        "1. EDG (5勝): Jett/Omen/KAY/O/Sova/Killjoy (5回)",
        "2. Heretics (4勝): Jett/Omen/KAY/O/Sova/Killjoy (4回)",
        "3. SEN (3勝): Jett/Omen/KAY/O/Sova/Cypher (3回)",
        "4. DRX (2勝): Jett/Omen/KAY/O/Sova/Killjoy (2回)",
        "5. PRX (2勝): Yoru/Omen/KAY/O/Sova/Killjoy (2回)"
    ],
    "Haven": [
        "1. Gen.G (4勝): Jett/Breach/Omen/Sova/Killjoy (4回)",
        "2. Fnatic (3勝): Jett/Breach/Omen/Sova/Killjoy (3回)",
        "3. TH (3勝): Jett/Breach/Omen/Sova/Cypher (3回)",
        "4. NAVI (2勝): Jett/Breach/Omen/Sova/Killjoy (2回)",
        "5. DFM (2勝): Jett/Breach/Omen/Sova/Killjoy (2回)"
    ],
    "Icebox": [
        "1. SEN (4勝): Jett/Viper/Sova/Killjoy/Sage (4回)",
        "2. G2 (3勝): Jett/Viper/Sova/Killjoy/Sage (3回)",
        "3. KC (3勝): Jett/Viper/Sova/Killjoy/Killjoy (3回)",
        "4. VIT (2勝): Jett/Viper/Sova/Killjoy/Sage (2回)",
        "5. ZETA (2勝): Jett/Viper/Sova/Killjoy/Sage (2回)"
    ],
    "Lotus": [
        "1. Fnatic (5勝): Raze/Fade/Omen/Breach/Killjoy (5回)",
        "2. Gen.G (4勝): Raze/Fade/Omen/Breach/Killjoy (4回)",
        "3. PRX (3勝): Raze/Fade/Omen/Breach/Killjoy (3回)",
        "4. EDG (2勝): Raze/Fade/Omen/Breach/Cypher (2回)",
        "5. TL (2勝): Raze/Fade/Omen/Breach/Killjoy (2回)"
    ],
    "Sunset": [
        "1. Leviatán (5勝): Raze/Breach/Omen/Cypher/Gekko (5回)",
        "2. G2 (4勝): Raze/Breach/Omen/Cypher/Gekko (4回)",
        "3. TH (3勝): Raze/Breach/Omen/Cypher/Gekko (3回)",
        "4. SEN (2勝): Raze/Breach/Omen/Cypher/Gekko (2回)",
        "5. FUT (2勝): Neon/Breach/Omen/Cypher/Gekko (2回)"
    ],
    "Abyss": [
        "1. G2 (3勝): Jett/Sova/Omen/Cypher/KAY/O (3回)",
        "2. VIT (3勝): Jett/Sova/Omen/Cypher/KAY/O (3回)",
        "3. NAVI (2勝): Jett/Sova/Omen/Cypher/KAY/O (2回)",
        "4. Heretics (2勝): Jett/Sova/Omen/Cypher/KAY/O (2回)",
        "5. NRG (1勝): Jett/Sova/Omen/Cypher/KAY/O (1回)"
    ]
}

@bot.slash_command(name="vct_analytics", description="知りたいマップのVCT勝利数TOP5チームを表示します")
@option("map_name", description="マップ名を選択してください", choices=["Ascent", "Bind", "Haven", "Icebox", "Lotus", "Sunset", "Abyss"])
async def vct_analytics(ctx, map_name: str):
    await ctx.defer()
    data_list = MAP_STATS.get(map_name)
    
    embed = discord.Embed(
        title=f"📊 {map_name} VCT勝利数TOP5（直近30日）",
        description=f"**{map_name}** で結果を残しているプロチームの構成です。",
        color=0x00ffff
    )
    embed.add_field(name="📋 順位. チーム (勝利数): 構成 (使用回数)", value="\n".join(data_list), inline=False)
    embed.set_footer(text="Data source: VLR.gg Professional Analytics")
    await ctx.followup.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.sync_commands()

bot.run(os.environ.get("DISCORD_TOKEN"))
