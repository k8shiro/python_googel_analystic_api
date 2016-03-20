
## 概要

Google Analytics APIをPythonから呼びます。  
実行すろことで設定した期間内のpageviewによるRankingを 出力します。

## 使い方
https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py?hl=ja#enable
のステップ1とステップ2までの終了させます。

jsonファイルの準備をします

    cp config.json.sample config.json

config.jsonの中を以下のように編集します。

    {
        "email": "<your google developer email adress> ex) sample@sample.iam.gserviceaccount.com ",
        "key": "<*.p12 path> ex) ./sample-5a5a55a5a5a5.p12",
        "start_date": "ランキングの期間の開始日 ex) 2016-02-07",
        "end_date": "ランキングの期間の終了日 ex) 2016-03-07"
		"home": "あなたのpageのurl ex) http://qiita.com/"
    }

以下の二つをpipで入れます

    sudo pip install --upgrade google-api-python-client
    pip install pyopenssl


実行します

    python googel_analystic_api_ranking.py

