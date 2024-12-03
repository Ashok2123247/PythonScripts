### pyton basic commands ###
###################################################################

#check version
python --version 
# or
import sys
print(sys.version)

## if condition
if 5 > 2:
  print("Five is greater than two!")
  
## multiple line comment
"""
This is a comment
written in
more than just one line
"""
print("Hello, World!") 

## variable 
x = str(3)
y = int(3)
z = float(3)
print(x)
print(y)
print(z)

## data types
'''
Text Type       :	str
Numeric Types   :	int, float, complex

Sequence Types  :	list, tuple, range
#example
x = ["apple", "banana", "cherry"]	list	
x = ("apple", "banana", "cherry")	tuple	
x = range(6)

Mapping Type    :	dict
x = {"name" : "John", "age" : 36}

Set Types       :	set, frozenset
x = {"apple", "banana", "cherry"}
x = frozenset({"apple", "banana", "cherry"})

Boolean Type    :	bool
Binary Types    :	bytes, bytearray, memoryview
None Type       :	NoneType
'''


## casting
x = int(2.8) ## x will be 2
y = float(3) ## y will be 3.0
z = str(3.0) ## z will be '3.0'

## Slicing Strings
b = "hellow, world!"
print(b[0:5]) ## will be hellow
print(b.upper()) ## capitals
print(b.lower()) ## lower case
print(b.strip()) ## removes the whitespaces
print(b.replace("H", "J")) ## replace a string
print(b.split(",") ## splits the string into substring

## concate
a = "Hello"
b = "World"
c = a + b
print(c) ## helloWorld

## add space inbetween
a = "Hello"
b = "World"
c = a + " " + b
print(c)

## format string
age = 36
txt = f"My name is John, I am {age}"
print(txt)  ## My name is John, I am 36

price = 59
txt = f"The price is {price:.2f} dollars"
print(txt) ## The price is 59.00 dollars

txt = f"The price is {20 * 59} dollars"
print(txt) ## the price is 1180 dollars

## escape character allows you to use double quotes
txt = "We are the so-called \"Vikings\" from the north."
print(txt) ## We are the so-called "Vikings" from the north.
'''
\'	Single Quote    >> txt = 'It\'s alright.' >> It's alright
\\	Backslash	    >> txt = "This will insert one \\ (backslash)." >> This will insert one \ (backslash)
\n	New Line	    >> txt = "Hello\nWorld!" >> two lines 
\r	Carriage Return	>> txt = "Hello\rWorld!"
\t	Tab	            >> txt = "Hello\tWorld!" >> Hellow   world!
\b	Backspace	    >> txt = "Hello \bWorld!" >> HelloWorld!
\f	Form Feed	
\ooo	Octal value	>> txt = "\110\145\154\154\157" >> Hellow
\xhh	Hex value   >> txt = "\x48\x65\x6c\x6c\x6f" >> Hellow
'''
## Sting methods
capitalize()    Converts the first character to upper case

txt = "hello, and welcome to my world."
x = txt.capitalize()
print (x)

casefold()	    Converts string into lower case
center()	    Returns a centered string
count()	        Returns the number of times a specified value occurs in a string
endswith()	    Returns true if the string ends with the specified value

txt = "Hello, welcome to my world."
x = txt.endswith(".") >> TRUE

expandtabs()	Sets the tab size of the string

txt = "H\te\tl\tl\to"
x =  txt.expandtabs(3) >> H  e  l  l  o

find()	        Searches the string for a specified value and returns the position of where it was found

txt = "Hello, welcome to my world."
x = txt.find("welcome")  >> RETURN NUMBER

format()	    Formats specified values in a string

txt = "For only {price:.2f} dollars!"
print(txt.format(price = 49)) >> For only 49.00 dollars!

#named indexes:
txt1 = "My name is {fname}, I'm {age}".format(fname = "John", age = 36)
#numbered indexes:
txt2 = "My name is {0}, I'm {1}".format("John",36)
#empty placeholders:
txt3 = "My name is {}, I'm {}".format("John",36)

print(txt1)
print(txt2)
print(txt3)

output
My name is John, I'm 36
My name is John, I'm 36
My name is John, I'm 36

index()	        Searches the string for a specified value and returns the position of where it was found
isalnum()	    Returns True if all characters in the string are alphanumeric
isalpha()	    Returns True if all characters in the string are in the alphabet
isascii()	    Returns True if all characters in the string are ascii characters
isdecimal()	    Returns True if all characters in the string are decimals
isdigit()	    Returns True if all characters in the string are digits
isidentifier()	Returns True if the string is an identifier
islower()	    Returns True if all characters in the string are lower case
isnumeric()	    Returns True if all characters in the string are numeric
isprintable()	Returns True if all characters in the string are printable
isspace()	    Returns True if all characters in the string are whitespaces
istitle()	    Returns True if the string follows the rules of a title
isupper()	    Returns True if all characters in the string are upper case

join()	        Joins the elements of an iterable to the end of the string
#ex1
myTuple = ("John", "Peter", "Vicky")
x = "#".join(myTuple)  >> ## John#Peter#Vicky

#ex2
myDict = {"name": "John", "country": "Norway"}
mySeparator = "TEST"
x = mySeparator.join(myDict) >> ## nameTESTcountry

ljust()	        Returns a left justified version of the string
lower()	        Converts a string into lower case
lstrip()	    Returns a left trim version of the string
maketrans()	    Returns a translation table to be used in translations
partition()	    Returns a tuple where the string is parted into three parts
replace()	    Returns a string where a specified value is replaced with a specified value
rfind()	        Searches the string for a specified value and returns the last position of where it was found
rindex()	    Searches the string for a specified value and returns the last position of where it was found
rjust()	        Returns a right justified version of the string
rpartition()	Returns a tuple where the string is parted into three parts
rsplit()	    Splits the string at the specified separator, and returns a list
rstrip()	    Returns a right trim version of the string
split()	        Splits the string at the specified separator, and returns a list
splitlines()	Splits the string at line breaks and returns a list
startswith()	Returns true if the string starts with the specified value
strip()	        Returns a trimmed version of the string
swapcase()	    Swaps cases, lower case becomes upper case and vice versa
title()	        Converts the first character of each word to upper case
translate()	    Returns a translated string
upper()	        Converts a string into upper case
zfill()	        Fills the string with a specified number of 0 values at the beginning

