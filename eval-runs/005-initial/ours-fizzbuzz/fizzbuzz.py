rules = [(3, "Fizz"), (5, "Buzz"), (7, "Wazz")]
for n in range(1, 101):
    word = "".join(w for d, w in rules if n % d == 0)
    print(word or n)
