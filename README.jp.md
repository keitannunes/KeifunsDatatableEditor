# KeifunsDatatableEditor (KDE)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/keitannunes/KeifunsDatatableEditor/blob/main/README.md)
[![jp](https://img.shields.io/badge/lang-jp-red.svg)](https://github.com/keitannunes/KeifunsDatatableEditor/blob/main/README.jp.md)

KeifunsDatatableEditor(KDE)は、JPN08やCHN00用のTaikoSoundEditor(TSE)とは違い、JPN39の為に作られました。
KDEを使用する事でdatatableを簡単に変更・管理することが出来ます。

## 特徴
- **datatableの編集**: datatableを簡単に変更出来ます。
- **曲の追加/削除**: datatableに曲の追加や削除が出来ます。
- **曲の詳細情報を自動生成**: TJAファイルから曲の詳細情報を自動生成します。
- **fumenとsoundファイルの生成**: TJAファイルから直接fumenとsoundファイルを生成します。

## 追加予定の機能
- datatableからの曲の削除#???
- MusicAttributeのtag編集
- 曲名/サブタイトルで曲検索
- 称号/リワード編集機能
- 日本語訳

## 実行環境
- **FFmpeg**: このプロジェクトはaudioファイルの変換処理に[FFmpeg](https://ffmpeg.org/)を必要とします。システムのPATHにインストールされ、アクセス出来る事を確認してください。

## インストールガイド
1. 最新の実行ファイルを[GitHub Releases](https://github.com/keitannunes/KeifunsDatatableEditor/releases)からダウンロードします。
2. ダウンロードした`KeifunsDatatableEditor.exe`を実行します。
3. 起動後、`File > Set Keys`に進む。
4. プログラムを使用する為に必要なキーを設定してください。


## 使用ツール

- [TaikoPythonTools - TaikoNus3bankMake](https://github.com/cainan-c/TaikoPythonTools)： soundファイルの作成に使用します。
- [tja2fumen](https://github.com/vivaria/tja2fumen)： fumenファイルの作成に使用します。
- [tja-tools](https://github.com/WHMHammer/tja-tools)： TJAファイルの解析に使用します。

## ステータス
このプログラムは現在 **alpha** です。問題やバグがあれば、[GitHub Issues](https://github.com/keitannunes/KeifunsDatatableEditor/issues) ページから報告してください。

## 質問とサポート
質問やサポートが必要な場合は、**EGTS Discord** へ気軽に参加してください： [discord.egts.ca](https://discord.egts.ca)

## License
KeifunsDatatableEditor is licensed under the **GNU General Public License v3.0**.

For more details, refer to the [GPL 3.0 License](https://www.gnu.org/licenses/gpl-3.0.html).

---
Feel free to use, modify, and contribute, but remember to share your improvements under the same license.