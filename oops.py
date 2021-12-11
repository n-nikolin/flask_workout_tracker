file = open("wtf.txt", "r")
#read content of file to string
data = file.read()
#get number of occurrences of the substring in the string
occurrences = data.count("programme_name")
print('Number of occurrences of the word :', occurrences)
