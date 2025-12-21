import consts as cn


def filter_dupes():
   
    green_zip = zip(cn.green, cn.green_mul)
    
    cn.letters = list(cn.letters) + cn.green + cn.yellow_list
    cn.letters = list("".join(set(cn.letters)))
    
    for c, i in green_zip:
        if not i:
            cn.letters.remove(c)
    cn.letters = "".join(set(cn.letters))
        

        
'''
cn.green = ["","","i","t","e"]
cn.yellow_list =[["h"],["e"],["e"],[""],["t"]]
cn.yellow_dic = {"h": 0, "e": 0, "t":0}
cn.letters = "qwertyihjzxcvbm"
'''

def create_lists():
    
    if cn.green[0] != "":
        cn.i_list = [cn.green[0]]
    else:
        cn.i_list = [i for i in cn.letters if i not in cn.yellow_list[0]]

    if cn.green[1] != "":
        cn.j_list = [cn.green[1]]
    else:
        cn.j_list = [i for i in cn.letters if i not in cn.yellow_list[1]]
        
    if cn.green[2] != "":
        cn.k_list = [cn.green[2]]
    else:
        cn.k_list = [i for i in cn.letters if i not in cn.yellow_list[2]]
        
    if cn.green[3] != "":
        cn.l_list = [cn.green[3]]
    else:
        cn.l_list = [i for i in cn.letters if i not in cn.yellow_list[3]]
        
    if cn.green[4] != "":
        cn.m_list = [cn.green[4]]
    else:
        cn.m_list = [i for i in cn.letters if i not in cn.yellow_list[4]]


def calculate():
    cn.words = []
    for i in cn.i_list:
        for j in cn.j_list:
            if j in cn.yellow_dic and (not cn.yellow_dic[j]) and j in i:
                continue

            for k in cn.k_list:     
                if k in cn.yellow_dic and (not cn.yellow_dic[k]) and k in i+j:
                    continue

                for l in cn.l_list:   
                    if l in cn.yellow_dic and (not cn.yellow_dic[l]) and l in i+j+k:
                        continue

                    for m in cn.m_list:   
                        if m in cn.yellow_dic and (not cn.yellow_dic[m]) and m in i+j+k+l:
                            continue   

                        # create word   
                        buff = i + j + k + l + m

                        # check if word exists
                        if buff in cn.data and check_word(buff):
                            cn.words.append(buff)


def check_word(word):
   
    yel = []
    for i in cn.yellow_list:
        for j in i:
            yel.append(j)
            
    yel = set(yel)
    
    for i in yel:
        if not i in word:
            return False
    
    return True


def cn_Print():
    print("Green:", cn.green)
    print("Yellow-List:", cn.yellow_list)
    print("Yellow-Dict:", cn.yellow_dic)
    print("Letters:", cn.letters)

def extract(gui_data): 
    
    cn.green = gui_data["green"]
    cn.green_mul = gui_data["green_more_than_once"]
    cn.yellow_list = gui_data["yellow"]
    cn.letters = list(set(gui_data["available_letters"]))
    yellow_zip = zip(cn.yellow_list, gui_data["yellow_more_than_once"])
    
    for i, j in yellow_zip:
        n = len(i)
        m = len(j)
        if n != m:
            continue
        for k in range(n):
            cn.yellow_dic[i[k]] = int(j[k])
            
    
    filter_dupes()
    cn_Print()
    create_lists()
    calculate()
    
    def sort(x):
        return len(set(x))
    sorted(cn.words, key=sort, reverse=True)
    
    return cn.words


'''
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