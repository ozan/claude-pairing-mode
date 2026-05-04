for n in range(1, 101):
    word = ("Fizz" if n % 3 == 0 else "") + ("Buzz" if n % 5 == 0 else "")
    print(word or n)
