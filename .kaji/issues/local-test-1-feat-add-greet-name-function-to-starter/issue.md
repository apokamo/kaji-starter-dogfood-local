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
