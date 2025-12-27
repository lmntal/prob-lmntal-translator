def round_sig_6(num: float) -> str:
    from decimal import Decimal, ROUND_HALF_UP
    import math

    if num == 0:
        return "0"

    # Decimalに変換（精度を保つため文字列経由）
    dnum = Decimal(str(num))

    # 有効数字6桁に対応する指数を求めて丸める
    exponent = -int(math.floor(math.log10(abs(num)))) + 5
    rounded = dnum.quantize(Decimal("1e-" + str(exponent)), rounding=ROUND_HALF_UP)

    # 不要な0や小数点を除いて整形
    result = format(rounded.normalize(), "f").rstrip("0").rstrip(".")
    return result
