### 2023 年 10 月 6 日更新

リアルタイム声変換のためのインターフェース go-realtime-gui.bat/gui_v1.py を作成しました（実際には既に存在していました）。今回のアップデートでは、リアルタイム声変換のパフォーマンスを重点的に最適化しました。0813 版との比較：

- 1.  インターフェース操作の最適化：パラメータのホット更新（パラメータ調整時に中断して再起動する必要がない）、レイジーロードモデル（既にロードされたモデルは再ロードする必要がない）、音量因子パラメータ追加（音量を入力オーディオに近づける）
- 2.  内蔵ノイズリダクション効果と速度の最適化
- 3.  推論速度の大幅な最適化

入出力デバイスは同じタイプを選択する必要があります。例えば、両方とも MME タイプを選択します。

1006 バージョンの全体的な更新は：

- 1.  rmvpe 音声ピッチ抽出アルゴリズムの効果をさらに向上、特に男性の低音部分で大きな改善
- 2.  推論インターフェースレイアウトの最適化

### 2023 年 8 月 13 日更新

1-通常のバグ修正

- 保存頻度と総ラウンド数の最小値を 1 に変更。総ラウンド数の最小値を 2 に変更
- pretrain モデルなしでのトレーニングエラーを修正
- 伴奏とボーカルの分離完了後の VRAM クリア
- faiss 保存パスを絶対パスから相対パスに変更
- パスに空白が含まれる場合のサポート（トレーニングセットのパス+実験名がサポートされ、エラーにならない）
- filelist の強制的な utf8 エンコーディングをキャンセル
- リアルタイム声変換中にインデックスを有効にすることによる CPU の大幅な使用問題を解決

2-重要なアップデート

- 現在最も強力なオープンソースの人間の声のピッチ抽出モデル RMVPE をトレーニングし、RVC のトレーニング、オフライン/リアルタイム推論に使用。pytorch/onnx/DirectML をサポート
- pytorch-dml を通じて A カードと I カードのサポート
  （1）リアルタイム声変換（2）推論（3）ボーカルと伴奏の分離（4）トレーニングはまだサポートされておらず、CPU でのトレーニングに切り替わります。onnx_dml を通じて rmvpe_gpu の推論をサポート

### 2023 年 6 月 18 日更新

- v2 に 32k と 48k の 2 つの新しい事前トレーニングモデルを追加
- 非 f0 モデルの推論エラーを修正
- 1 時間を超えるトレーニングセットのインデックス構築フェーズでは、自動的に kmeans で特徴を縮小し、インデックスのトレーニングを加速し、検索に追加
- 人間の声をギターに変換するおもちゃのリポジトリを添付
- データ処理で異常値スライスを除外
- onnx エクスポートオプションタブ

失敗した実験：

- ~~特徴検索に時間次元を追加：ダメ、効果がない~~
- ~~特徴検索に PCAR 次元削減オプションを追加：ダメ、大きなデータは kmeans でデータ量を減らし、小さいデータは次元削減の時間が節約するマッチングの時間よりも長い~~
- ~~onnx 推論のサポート（推論のみの小さな圧縮パッケージ付き）：ダメ、nsf の生成には pytorch が必要~~
- ~~トレーニング中に音声、ジェンダー、eq、ノイズなどで入力をランダムに増強：ダメ、効果がない~~
- ~~小型声码器の接続調査：ダメ、効果が悪化~~

todolist：

- ~~トレーニングセットの音声ピッチ認識に crepe をサポート：既に RMVPE に置き換えられているため不要~~
- ~~多プロセス harvest 推論：既に RMVPE に置き換えられているため不要~~
- ~~crepe の精度サポートと RVC-config の同期：既に RMVPE に置き換えられているため不要。これをサポートするには torchcrepe ライブラリも同期する必要があり、面倒~~
- F0 エディタとの連携

### 2023 年 5 月 28 日更新

- v2 の jupyter notebook を追加、韓国語の changelog を追加、いくつかの環境依存関係を追加
- 呼吸、清辅音、歯音の保護モードを追加
- crepe-full 推論をサポート
- UVR5 人間の声と伴奏の分離に 3 つの遅延除去モデルと MDX-Net の混响除去モデルを追加、HP3 人声抽出モデルを追加
- インデックス名にバージョンと実験名を追加
- 人間の声と伴奏の分離、推論のバッチエクスポートにオーディオエクスポートフォーマットオプションを追加
- 32k モデルのトレーニングを廃止

### 2023 年 5 月 13 日更新

- ワンクリックパッケージ内の古いバージョンの runtime 内の lib.infer_pack と uvr5_pack の残骸をクリア
- トレーニングセットの事前処理の擬似マルチプロセスバグを修正
- harvest による音声ピッチ認識で無声音現象を弱めるために中間値フィルターを追加、中間値フィルターの半径を調整可能
- 音声エクスポートにポストプロセスリサンプリングを追加
- トレーニング時の n_cpu プロセス数を「F0 抽出のみ調整」から「データ事前処理と F0 抽出の調整」に変更
- logs フォルダ下の index パスを自動検出し、ドロップダウンリスト機能を提供
- タブページに「よくある質問」を追加（または github-rvc-wiki を参照）
- 同じパスの入力音声推論に音声ピッチキャッシュを追加（用途：harvest 音声ピッチ抽出を使用すると、全体のパイプラインが長く繰り返される音声ピッチ抽出プロセスを経験し、キャッシュを使用しない場合、異なる音色、インデックス、音声ピッチ中間値フィルター半径パラメーターをテストするユーザーは、最初のテスト後の待機結果が非常に苦痛になります）

### 2023 年 5 月 14 日更新

- 音量エンベロープのアライメント入力ミックス（「入力が無音で出力がわずかなノイズ」の問題を緩和することができます。入力音声の背景ノイズが大きい場合は、オンにしないことをお勧めします。デフォルトではオフ（1 として扱われる））
- 指定された頻度で抽出された小型モデルを保存する機能をサポート（異なるエポックでの推論効果を試したいが、すべての大きなチェックポイントを保存して手動で小型モデルを抽出するのが面倒な場合、この機能は非常に便利です）
- システム全体のプロキシが開かれている場合にブラウザの接続エラーが発生する問題を環境変数の設定で解決
- v2 事前訓練モデルをサポート（現在、テストのために 40k バージョンのみが公開されており、他の 2 つのサンプリングレートはまだ完全に訓練されていません）
- 推論前に 1 を超える過大な音量を制限
- データ事前処理パラメーターを微調整

### 2023 年 4 月 9 日更新

- トレーニングパラメーターを修正し、GPU の平均利用率を向上させる。A100 は最高 25％から約 90％に、V100 は 50％から約 90％に、2060S は 60％から約 85％に、P40 は 25％から約 95％に向上し、トレーニング速度が大幅に向上
- パラメーターを修正：全体の batch_size を各カードの batch_size に変更
- total_epoch を修正：最大制限 100 から 1000 に解除; デフォルト 10 からデフォルト 20 に引き上げ
- ckpt 抽出時に音声ピッチの有無を誤って認識し、推論が異常になる問題を修正
- 分散トレーニングで各ランクが ckpt を 1 回ずつ保存する問題を修正
- 特徴抽出で nan 特徴をフィルタリング
- 入力が無音で出力がランダムな子音またはノイズになる問題を修正（旧バージョンのモデルはトレーニングセットを作り直して再トレーニングする必要があります）

### 2023 年 4 月 16 日更新

- ローカルリアルタイム音声変換ミニ GUI を新設、go-realtime-gui.bat をダブルクリックで起動
- トレーニングと推論で 50Hz 以下の周波数帯をフィルタリング
- トレーニングと推論の音声ピッチ抽出 pyworld の最低音声ピッチをデフォルトの 80 から 50 に下げ、50-80hz の男性低音声が無声にならないように
- WebUI がシステムの地域に基づいて言語を変更する機能をサポート（現在サポートされているのは en_US、ja_JP、zh_CN、zh_HK、zh_SG、zh_TW、サポートされていない場合はデフォルトで en_US になります）
- 一部のグラフィックカードの認識を修正（例えば V100-16G の認識失敗、P4 の認識失敗）

### 2023 年 4 月 28 日更新

- faiss インデックス設定をアップグレードし、速度が速く、品質が高くなりました
- total_npy 依存をキャンセルし、今後のモデル共有では total_npy の記入は不要
- 16 シリーズの制限を解除。4G メモリ GPU に 4G の推論設定を提供
- 一部のオーディオ形式で UVR5 の人声伴奏分離のバグを修正
- リアルタイム音声変換ミニ gui に 40k 以外のモデルと妥協のない音声ピッチモデルのサポートを追加

### 今後の計画：

機能：

- 複数人のトレーニングタブのサポート（最大 4 人）

底層モデル：

- 呼吸 wav をトレーニングセットに追加し、呼吸が音声変換の電子音の問題を修正
- 歌声トレーニングセットを追加した底層モデルをトレーニングしており、将来的には公開する予定です
