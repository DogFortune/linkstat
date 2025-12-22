# linkstat

[![test-lint-format](https://github.com/DogFortune/linkstat/actions/workflows/lint-test-format.yml/badge.svg)](https://github.com/DogFortune/linkstat/actions/workflows/lint-test-format.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

_linkstat_ はドキュメントに記載されているリンクの疎通確認を行うスクリプトです。リンク切れの早期発見を行う事でドキュメントの健全性を保ちます。  
現在対応しているのはMarkdownファイル（*.md）のみです。

## 注意
本ライブラリは実行時にサービスへアクセスするため、大量に実行すると相手サービスに負荷が発生します。動作確認及びCI/CDに取り込む場合は、リンク先のサービス負荷は限りなく少なくして下さい。

## インストール

```sh
pip install linkstat
```

## 使い方

```sh
linkstat {source_file_or_directory}
```

## 出力
オプションを使用することでJSON形式のレポートを出力できます。

```sh
linkstat --report-json {path} {source_file_or_directory}
```

## コントリビュート
[ガイドライン](CONTRIBUTING_JP.md)
