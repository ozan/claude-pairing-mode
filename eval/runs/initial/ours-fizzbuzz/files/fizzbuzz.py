for n in range(1, 101):
    s = ("Fizz" if n % 3 == 0 else "") + ("Buzz" if n % 5 == 0 else "")
    print(s or n)
