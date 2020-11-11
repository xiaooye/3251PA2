import sys

for line in sys.stdin:
    if 'q' == line.rstrip():
        break
    input = line.split('\"')
    for word in input:
        if len(word) <= 0:
            print("o shit")
        else:
            print(word)
    print(f'Input : {line}')

print("Exit")