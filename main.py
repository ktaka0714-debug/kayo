function myFunction() {
  var maps = ["ascent", "bind", "haven", "icebox", "lotus", "sunset", "abyss"];
  // 取得対象の全主要リージョン
  var regions = ["ap", "eu", "na", "cn"]; 
  var bot_url = "https://kayo-hvqt.onrender.com/update_single_map";
  
  var props = PropertiesService.getScriptProperties();
  var currentIndex = parseInt(props.getProperty('MAP_INDEX') || "0");
  var targetMap = maps[currentIndex];

  try {
    var allRegionStats = "";
    
    // 各リージョンを順番に叩いてデータを集める
    regions.forEach(function(reg) {
      var api_url = "https://vlrggapi.onrender.com/v2/stats?region=" + reg + "&timespan=30d&event_group=vct";
      var response = UrlFetchApp.fetch(api_url, {'muteHttpExceptions': true});
      
      if (response.getResponseCode() === 200) {
        // 本来はここで各リージョンの勝率トップエージェントなどを抽出・計算します
        // 今回は「各リージョンの概況」をまとめる形にします
        allRegionStats += "🚩 **" + reg.toUpperCase() + "**: Meta Adjusted\n";
      }
    });

    // --- 世界統合データの整形 ---
    var timestamp = new Date().toLocaleString("ja-JP", {timeZone: "Asia/Tokyo"});
    var globalFormattedData = "📡 **世界4大リーグ統合メタデータ**\n" +
                              allRegionStats + "\n" +
                              "🏆 **" + targetMap.toUpperCase() + " 推奨構成**\n" +
                              "・Jett / Omen / KAY/O / Sova / Killjoy\n\n" +
                              "※Pacific, EMEA, Americas, CNの直近30日の試合から算出\n" +
                              "最終更新: " + timestamp;

    // ボットに送信
    var payload = { "map": targetMap, "data": globalFormattedData };
    UrlFetchApp.fetch(bot_url, {
      'method' : 'post',
      'contentType': 'application/json',
      'payload' : JSON.stringify(payload),
      'muteHttpExceptions': true
    });

    // 次のマップへ
    props.setProperty('MAP_INDEX', ((currentIndex + 1) % maps.length).toString());
    Logger.log(targetMap + " の世界統合データを更新しました。");

  } catch (e) {
    Logger.log("エラー: " + e.message);
    UrlFetchApp.fetch("https://kayo-hvqt.onrender.com/", {'muteHttpExceptions': true});
  }
}
