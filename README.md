# Cat Weight Database CLI

`catdb.py` は、猫の体重記録を管理するためのコマンドラインインターフェース（CLI）です。このツールを使用すると、体重データベースを初期化したり、体重データを追加、更新、削除、表示することができます。

## 使用方法

以下のコマンドを使用して、体重データベースを管理します。

### 基本コマンド

```bash
./catdb.py [command] [options]
```

### コマンド一覧

#### データベース初期化

データベースと必要なテーブルを初期化します。

```
./catdb.py init --db-file <path/to/database>
```

- --db-file: データベースファイルのパス（オプション）。指定がない場合は、環境変数 CAT_DB の値を使用します。
環境変数 CAT_DB が設定されていない場合、エラーメッセージが出力されます。

#### 体重データの追加

新しい体重記録を追加します。

```
./catdb.py add <date> <weight> [--notes <notes>] [--db-file <path/to/database>]
```

-	date: 記録の日付（YYYY-MM-DD 形式）
-	weight: 猫の体重（kg 単位、浮動小数点数）
-	--notes: 任意のメモ（省略可）
-	--db-file: データベースファイルのパス（オプション）。指定がない場合は、環境変数 CAT_DB の値を使用します。

#### 体重データの更新

既存の体重記録を更新します。

```
./catdb.py update <date> <weight> [--notes <notes>] [--db-file <path/to/database>]
```

-	date: 更新する記録の日付（YYYY-MM-DD 形式）
-	weight: 新しい体重（kg 単位、浮動小数点数）
-	--notes: 更新するメモ（省略可）
-	--db-file: データベースファイルのパス（オプション）。指定がない場合は、環境変数 CAT_DB の値を使用します。


#### 体重データの削除

特定の日付の体重記録を削除します。

```
./catdb.py delete <date> [--db-file <path/to/database>]
```


- date: 削除する記録の日付（YYYY-MM-DD 形式）
-	--db-file: データベースファイルのパス（オプション）。指定がない場合は、環境変数 CAT_DB の値を使用します。


####	体重データの表示

特定の日付の体重記録またはすべての記録を表示します。

```
./catdb.py display [--date <date>] [--db-file <path/to/database>]
```

-	--date: 表示する特定の日付（YYYY-MM-DD 形式）。指定しない場合はすべての記録を表示します。
-	--db-file: データベースファイルのパス（オプション）。指定がない場合は、環境変数 CAT_DB の値を使用します。

### 使用例

#### 環境変数 CAT_DB の設定例

事前にデータベースファイルを指定する環境変数 CAT_DB を設定します。

```bash
export CAT_DB=/path/to/your/cat_data.db
```

#### データベースの初期化

```
./catdb.py init
```

#### 新しい記録の追加

```
./catdb.py add 2024-11-16 4.5 --notes "Healthy weight"
```

#### 既存の記録の更新

```
./catdb.py update 2024-11-16 4.6 --notes "Weight updated"
```

#### 記録の削除

```
./catdb.py delete 2024-11-16
```

#### すべての記録を表示

```
./catdb.py display
```

#### 特定の日付の記録を表示

```
./catdb.py display --date 2024-11-16
```

### 注意事項

-	--db-file オプションを指定しない場合、環境変数 CAT_DB に設定されたファイルが使用されます。
    CAT_DB が設定されていない場合、エラーメッセージが出力されます。
-	日付は柔軟なフォーマット（YYYY-MM-DD、YYYY/MM/DD、MM-DD-YYYY、MM/DD/YYYY）で入力可能です。

## 開発プラン

- 猫の体重を記録するコマンドラインアプリケーション
- 実装言語はpython
- データの保存はSQLite3を用いる
- SQLite3のデータファイル名はコマンドのオプションあるいは環境変数で与える
- データは日付と猫の体重の2つの要素で構成される
- コマンドはデータの追加､期間を指定した表示､日付を指定した削除､日付を指定した更新などを可能とする (他にもこの類のアプリケーションに必要な機能があれば提案すること)
- コマンドはヘルプも表示可能である
- ロジックの本体はライブラリとして再利用可能とする
- メイン処理はオプションとサブコマンドの解釈と上記のライブラリの呼び出しを行う｡ヘルプの表示もメイン処理である
- ライブラリはjupyterLabなどから利用することで､インタラクティブにデータ分析を行うことを想定する




