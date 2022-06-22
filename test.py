import copy

# test = ['[', '[', 'TEST', ']', ',', '[', 'TEST 2', ']', ']']   # -> [["TEST"], ["TEST 2"]]

test = "(156, 256, 356, 256, (255, 255, 255))"

lists = list()
openingBrackets = list()  # To keep track of used indices

for x in range(len(test)):
    if test[x] == "]":
        for y in range(x)[::-1]:
            if test[y] == "[" and y not in openingBrackets:
                openingBrackets.append(y)
                lists.append({'start': y, 'end': x})
                break
    elif test[x] == ")":
        for y in range(x)[::-1]:
            if test[y] == "(" and y not in openingBrackets:
                openingBrackets.append(y)
                lists.append({'start': y, 'end': x})
                break

print(f"Lists: {lists}")
print(test[0:37])

for part in lists:
    newList = list()
    print(test[part['start'] + 1:part['end']].split(","))
    for x in test[part['start'] + 1:part['end']]:
        if x != ",":
            newList.append(x)
    print(f"New List: {newList}")
