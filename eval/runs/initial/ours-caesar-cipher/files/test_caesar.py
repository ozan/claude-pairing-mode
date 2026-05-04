from caesar import encode, decode

assert encode("hello", 3) == "khoor"
assert encode("HELLO", 3) == "KHOOR"
assert encode("Hello, World!", 3) == "Khoor, Zruog!"
assert encode("xyz", 3) == "abc"
assert decode(encode("Hello, World!", 13), 13) == "Hello, World!"

print("All tests passed!")
