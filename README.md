# trpg-bot2

- [trpg-bot2](#trpg-bot2)
  - [Description](#description)
  - [Development](#development)
    - [Requirements](#requirements)
    - [Preparation](#preparation)

## Description

TRPG のオンラインセッションを行う際の補助として使うための discord の bot です。

## Development

### Requirements

- [Visual Studio Code](https://code.visualstudio.com/) (>= 1.74)
- [asdf](https://asdf-vm.com/) (>= v0.11.1-27c8a10)
- [poetry](https://python-poetry.org/) (>= 1.3.2)

### Preparation

1. VS Code で [推奨拡張機能](/.vscode/extensions.json) をインストールします。`Ctrl/Cmd + Shift + X` で拡張機能パネルを開き、`@recommended` で推奨拡張機能の一覧を表示し、インストールを行ってください。

2. `asdf install` で開発に必要なプログラミングのインストールを行ってください。

3. `poetry install` で Python のライブラリのインストールを行ってください。

4. `.envrc` がプロジェクトルートにない場合は作成し、そこに `.envrc.tmp` の内容を追記し、 `direnv allow .` で適用してください。
