# linkstat
<div align="center">
[![test-lint-format](https://github.com/DogFortune/linkstat/actions/workflows/lint-test-format.yml/badge.svg?branch=main)](https://github.com/DogFortune/linkstat/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
</div>

_linkstat_ はドキュメントに記載されているリンクの疎通確認を行うスクリプトです。リンク切れの早期発見を行う事でドキュメントの健全性を保ちます。  
現在対応しているのはMarkdownファイル（*.md）のみです。

## インストールと使い方
### インストール

```sh
pip install linkstat
```

### 使い方

```sh
linkstat {source_file_or_directory}
```

## コントリビュート
[ガイドライン](CONTRIBUTING_JP.md)
