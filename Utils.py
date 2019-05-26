def to_bytes(val):
    if isinstance(val, bytearray):
        return val
    elif isinstance(val, bytes):
        return bytearray(val)
    elif isinstance(val, str):
        return val.encode()
    elif isinstance(val, int) or isinstance(val, float):
        return str(val).encode()
    raise NameError("Unsupported type of input data")
