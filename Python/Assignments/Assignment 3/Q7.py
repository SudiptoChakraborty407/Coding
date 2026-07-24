s = input("Enter a string: ")
ch = input("Enter a character: ")
count = 0

for i in s:
    if (ch==i):
        count += 1

print ("The number of charecters in the string is ", count)