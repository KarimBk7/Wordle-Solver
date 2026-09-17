

f = open("words_alpha.txt")

data = f.read()

words = ""

buf = ""
for i in data:
    if i == "\n":
        
        if len(buf) == 5:
            words += buf+"\n"
        buf = ""
    else:
        buf += i

        
with open("words_5.txt", "a") as f:
    
    f.write(words)

    

