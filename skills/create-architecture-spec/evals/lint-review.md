# 同梱文書のlint審査

## SKILL.md

- `excess_list`: 手順、分類、検証項目を独立して参照できるようにするため、箇条書きを維持する。

## references/writing-quality.md

- `excess_list`: 意味保持と検査対象のチェックリストであり、各項目を独立して確認するため維持する。
- `slop_vocabulary`、`metaphor_verb`: 「解像度を上げる」「安全側に倒す」「静かに壊れる」は、使用を避ける表現の検出例として引用しているため維持する。

## references/inquiry-checkpoints.md

- `excess_list`: 質問要否を依存順に判定するチェックリストなので維持する。
- `negative_parallelism`: 「レイヤー名ではなく、実際に…」は調査対象を抽象名から実装箇所へ限定する規則であり、対比が必要なので維持する。

## references/quality-gates.md

- `excess_list`: 合否を項目ごとに判定するチェックリストなので維持する。

## references/stack-detection.md

- `excess_list`: 技術スタック別の検出規則を独立して参照する一覧なので維持する。
- `trailing_colon`: 英文の直後にコードブロックまたは判定一覧が続く導入記号なので維持する。

## references/yomiyasu-business.md

- `sentence_end_repetition`、`negative_parallelism`: 上流文書を改変せず同梱しているため維持する。生成文へ適用する規則そのものを示す資料であり、成果物テンプレートではない。

基本設計と詳細設計のテンプレートには指摘がなかった。
