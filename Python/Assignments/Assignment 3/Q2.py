s = input("Enter a String: ")
n = len(s)
is_palindrome = True
for i in range(int(n/2)):
    if(s[i]!=s[n-i-1]):
        is_palindrome = False
        break
print (is_palindrome)