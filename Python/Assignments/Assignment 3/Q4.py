s = input("Enter a string: ")
s = s+" "
count = 0
for ch in s:
    if (ch==" "):
        count += 1
print("Number of words =", count)