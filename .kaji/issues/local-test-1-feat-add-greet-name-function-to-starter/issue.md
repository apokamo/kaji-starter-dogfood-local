---
id: local-test-1
title: 'feat: add greet(name) function to starter_app'
state: open
slug: feat-add-greet-name-function-to-starter
labels:
- type:feature
created_at: '2026-07-03T18:20:35Z'
---
> [!NOTE]
> **Worktree**: `../kaji-feat-local-test-1`
> **Branch**: `feat/local-test-1`

## 設計書

<details>
<summary>クリックして展開</summary>

# [設計] greet(name) 関数を starter_app に追加する

Issue: local-test-1

## 概要

`starter_app` package に、名前を受け取ってパーソナライズした挨拶文字列を返す
`greet(name: str) -> str` を追加する。starter を試す最初の TDD サンプル機能とする。

## 背景・目的

starter template の `src/starter_app/__init__.py` には固定文言を返す `hello()` のみがあり、
挨拶対象を指定できない。名前を引数で受け取る関数があると、正常系・異常系の両方をテスト →
実装で 1 周体験でき、starter の学習コストが下がる。

### ユースケース

- **starter 利用者**として、**TDD の 1 周（正常系 + 異常系）を最小コードで体験する**ために、
  **名前を渡すと挨拶文字列を得られる関数を import して呼び出したい**。

### 代替案と不採用理由

- `hello()` を引数付きに変更する案 → 既存の smoke テスト（`hello() == "Hello from starter_app!"`）と
  後方互換を壊す。Issue 要件でも「既存の `hello()` は変更しない」と明示されているため不採用。
  新規関数 `greet` を追加する方針とする。

## インターフェース

### 入力

| 引数 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `name` | `str` | 必須 | 挨拶対象の名前。前後空白は結果に含めない（トリムして埋め込む） |

### 出力

- 戻り値: `str`。`"Hello, {name}!"` 形式のパーソナライズ挨拶文字列。
- 副作用: なし（純粋関数。I/O・ログ・グローバル状態変更を持たない）。

### エラー

| 条件 | 挙動 |
|------|------|
| `name` が空文字 `""` | `ValueError` を送出 |
| `name` が空白のみ（例 `"   "`, `"\t"`） | 前後空白除去後に空になるため空扱いとし `ValueError` を送出 |

### 使用例

```python
from starter_app import greet

greet("Alice")        # -> "Hello, Alice!"
greet("  Bob  ")      # -> "Hello, Bob!"  (前後空白はトリム)
greet("")             # -> ValueError
greet("   ")          # -> ValueError
```

## 制約・前提条件

- 実装先は `src/starter_app/__init__.py`（既存 `hello()` と同じ module）。package から
  `from starter_app import greet` で import 可能にする。
- 既存の `hello()` / `__version__` は変更しない（後方互換維持）。
- 型注釈必須。mypy strict（`docs/reference/python-standards.md`）を通す。
- 外部依存を追加しない（標準ライブラリのみ）。

## 変更スコープ

- `src/starter_app/__init__.py` — `greet` 関数を追加
- `tests/test_smoke.py`（または新規 `tests/test_greet.py`）— `greet` の Small テストを追加

本プロジェクトは Python 単一スタック。backend / frontend の分岐はなし。

## 方針（Minimal How）

`str.strip()` で前後空白を除去した結果が空なら `ValueError` を送出し、そうでなければ
トリム済み名前を f-string で埋め込んで返す。疑似コード:

```python
def greet(name: str) -> str:
    trimmed = name.strip()
    if not trimmed:
        raise ValueError("name must not be empty")
    return f"Hello, {trimmed}!"
```

- エラーメッセージには対象（`name`）が空である旨を含め、呼び出し側が原因を判別できるようにする。
- `strip()` 済みの値を埋め込むことで、要件「前後の空白のみも空扱い」と、使用例
  `"  Bob  " -> "Hello, Bob!"` の双方を満たす。

## テスト戦略

### 変更タイプ
- 実行時コード変更（新規ドメインロジック + バリデーション分岐の追加）

#### Small テスト
- 正常系: `greet("Alice") == "Hello, Alice!"`（契約どおりの整形）
- 正常系（トリム）: `greet("  Bob  ") == "Hello, Bob!"`（前後空白除去の検証）
- 異常系: `greet("")` が `ValueError` を送出する（`pytest.raises`）
- 異常系（空白のみ）: `greet("   ")` が `ValueError` を送出する（空白のみ = 空扱いの分岐検証）

#### Medium テスト
- 不要。`greet` はファイル I/O・サブプロセス・外部サービス結合を持たない純粋関数であり、
  `docs/dev/testing-convention.md` の 4 条件のうち「外部依存を Small に持ち込まない」原則に沿って
  検証対象が存在しない。Small で全分岐を覆える。

#### Large テスト
- 不要。CLI エントリポイント・E2E フローは本 Issue のスコープ外（「CLI からの呼び出し」はスコープ外と
  Issue に明記）。実 API 疎通もなく、`docs/dev/testing-convention.md` の 4 条件（独自ロジックの
  E2E 経路がない / 既存 gate で捕捉 / 回帰検出情報が増えない）を満たすため恒久 Large テストは追加しない。

## 影響ドキュメント

| ドキュメント | 影響の有無 | 理由 |
|-------------|-----------|------|
| README.md | なし | starter の使用例レベルであり、公開利用者向け説明の追加は必須でない（`hello()` も README で個別説明していない） |
| docs/README.md | なし | docs 構成の変更なし |
| docs/dev/ | なし | ワークフロー・テスト規約の変更なし |
| docs/reference/ | なし | 既存の python-standards に従うのみで、規約・API 仕様の変更なし |
| docs/adr/ | なし | 新ライブラリ採用・技術選定なし |
| AGENTS.md / CLAUDE.md | なし | プロジェクト規約・必読ドキュメントの変更なし |

## 参照情報（Primary Sources）

| 情報源 | URL/パス | 根拠（引用/要約） |
|--------|----------|-------------------|
| Python 公式: `str.strip` | https://docs.python.org/3/library/stdtypes.html#str.strip | 「Return a copy of the string with the leading and trailing characters removed.」引数省略時は空白文字を除去する。空白のみ入力のトリム後空判定に用いる。 |
| Python 公式: `ValueError` | https://docs.python.org/3/library/exceptions.html#ValueError | 「Raised when an operation or function receives an argument that has the right type but an inappropriate value」。型は正しいが値が不適切（空名前）な入力の送出例外として適切。 |
| 既存実装 | `src/starter_app/__init__.py` | `hello() -> str` と `__version__`。`greet` は同 module に追加し、既存公開 API を変更しない。 |

</details>

## 背景

starter template の `src/starter_app/__init__.py` には動作確認用の `hello()` があるが、
挨拶対象を指定できない。starter を試す最初のサンプル機能として、名前を受け取って
挨拶を返す関数があると、テスト・実装の 1 周を体験しやすい。

## 目的

`src/starter_app/` に、名前を受け取ってパーソナライズした挨拶文字列を返す
`greet(name: str) -> str` を追加する。

## 要件

- `greet("Alice")` は `"Hello, Alice!"` を返す
- `name` が空文字 `""` の場合は `ValueError` を送出する（前後の空白のみも空扱い）
- 型注釈を付け、mypy strict を通す
- 既存の `hello()` は変更しない

## 完了条件

- `greet` が `src/starter_app/__init__.py`（または適切な module）に実装され、package から import できる
- `tests/` に `greet` の Small テストがあり、正常系（`"Alice"` → `"Hello, Alice!"`）と
  異常系（空文字 → `ValueError`）を覆っている
- `make check`（ruff / ruff format / mypy / pytest）がすべて通る

## スコープ外

- CLI からの呼び出し・エントリポイント追加
- 多言語対応・i18n

