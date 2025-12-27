# LMNtal Prob Translator

確率付き LMNtal モデルのメタインタプリタの出力を，確率モデル検査器 PRISM の入力形式 (Explicit Model) に変換するツールです．

## 前提条件

- Python 3.x

## 準備

```
# スクリプトに実行権限を付与
$ chmod +x scripts/lmntal_prob_translator

# PATH を通す（必要に応じて ~/.bashrc 等に追加） 
$ echo 'export PATH="$PATH:/path/to/lmntal-prob-translator/scripts/"' >> ~/.bashrc
```

## 使い方

- 確率付き LMNtal のメタインタプリタの実行結果を標準入力から与えます．

```
$ lmntal_prob_translator --model-type <dtmc|ctmc|mdp> --output-for-prism --tra <output.tra> --lab <output.lab> (--trew <output.trew>) < input.txt
```

## 実行例

```
$ lmntal_prob_translator --model-type dtmc --output-for-prism --tra for-prism/example.tra --lab for-prism/example.lab --trew for-prism/example.trew < result.txt
```