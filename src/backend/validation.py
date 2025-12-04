
def integer_or_default(v: str | int, default: int) -> int:
    if isinstance(v, int): return v
    if v.isdecimal():
        return int(v)
    else:
        return default