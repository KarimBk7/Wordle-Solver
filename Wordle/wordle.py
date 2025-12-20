import time
import sys
import consts as c

start_time = time.process_time()

# Fetch words with 5 letters
f = open("words_5.txt")
data = f.read()


alpha ="abcdefghijklmnopqrstuvwxyz"
green =  ["","","","",""]
green_mul = [1,1,1,1,1]
yellow_list =[[""],[""],[""],[""],[""]]
yellow_dic = {}

letters = ""

def filter_dupes():
    global green # liste aus str
    global green_mul # liste aus 0 und 1
    global yellow_list
    global letters
     
    
    green_zip = zip(green, green_mul)
    
    letters = list(letters) + green + yellow_list
    letters = list("".join(set(letters)))
    
    for c, i in green_zip:
        if not i:
            letters.remove(c)
    letters = "".join(letters)
        
def start():
    global green
    global green_mul
    global yellow_list
    global yellow_dic
    global letters
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "-c":
            for i in range(5):
                buff = input(f"\n\n\n{i+1}. Letter green?:")
                if buff in alpha and len(buff) == 1:
                    green[i] = buff
                
                buff = input(f"\n{i+1}. Letter yellow?:")
                while buff in alpha and len(buff) == 1:
                    
                    if not buff in yellow_dic:
                        yellow_dic[buff] = 0
                        
                    yellow_list[i][0] += buff
                    buff = input(f"\n{i+1}. Letter yellow?:") 
                    
            filter_dupes()
        else:
            print("No arg with:", sys.argv[1])
            exit(1)
        
        print("\t",green)
        print("\t",yellow_list)
        print("\t",yellow_dic)
        print("\t",letters)
        #exit(0)
        
    else: 
        green = ["","","i","t","e"]
        yellow_list =[["h"],["e"],["e"],[""],["t"]]
        yellow_dic = {"h": 0, "e": 0, "t":0}
        letters = "qwertyihjzxcvbm"





i_list = []
j_list = []
k_list = []
l_list = []
m_list = []
def create_lists():
    # List for each position
    global i_list
    global j_list
    global k_list
    global l_list
    global m_list
    global letters
    
    if green[0] != "":
        i_list = [green[0]]
    else:
        print(yellow_list) 

        i_list = [i for i in letters if i not in yellow_list[0]]

    if green[1] != "":
        j_list = [green[1]]
    else:
        j_list = [i for i in letters if i not in yellow_list[1]]
        
    if green[2] != "":
        k_list = [green[2]]
    else:
        k_list = [i for i in letters if i not in yellow_list[2]]
        
    if green[3] != "":
        l_list = [green[3]]
    else:
        l_list = [i for i in letters if i not in yellow_list[3]]
        
    if green[4] != "":
        m_list = [green[4]]
    else:
        m_list = [i for i in letters if i not in yellow_list[4]]



words = []
def calculate():
    global words
    global i_list
    global j_list
    global k_list
    global l_list
    global m_list
    words = []
    for i in i_list:
        for j in j_list:
            if j in yellow_dic and (not yellow_dic[j]) and j in i:
                continue
            
            for k in k_list:     
                if k in yellow_dic and (not yellow_dic[k]) and k in i+j:
                    continue
            
                for l in l_list:   
                    if l in yellow_dic and (not yellow_dic[l]) and l in i+j+k:
                        continue
                            
                    for m in m_list:   
                        if m in yellow_dic and (not yellow_dic[m]) and m in i+j+k+l:
                            continue   
                        
                        # create word   
                        buff = i + j + k + l + m
                        print(buff)
                        # check if word exists
                        if buff in data and check_word(buff):
                            words.append(buff)
    return words

y_list = []
def check_word(word):
    global yellow_list
    yel = []
    for i in yellow_list:
        for j in i:
            yel.append(j)
            
    yel = set(yel)
    
    for i in yel:
        if not i in word:
            return False
    
    return True

def extract(gui_data): 
    global green
    global green_mul
    global yellow_list
    global yellow_dic
    global letters
        
    green = gui_data["green"]
    green_mul = gui_data["green_more_than_once"]
    
    yellow_list = gui_data["yellow"]
    
    letters = gui_data["available_letters"]
    
    filter_dupes()
    create_lists()
    
    return calculate()
    
    
'''
# Sort distinct letters
def sort(x):
    return len(set(x))

sorted(words, key=sort, reverse=True)



print(f"\n\n\nAll possible Words:\n\n{words}")


end_time = time.process_time()
print(f"\n\n\nLaufzeit: {round(end_time - start_time, 2)} Sekunden\n")

             
    
    
    
    
    
    
    
    
exit(0)  
# Writer    
#time.sleep(2)        
for i in words:
    pyautogui.write(i)
    
    pyautogui.press("enter")
    
    pyautogui.press("backspace", presses=6)'''