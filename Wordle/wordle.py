import consts as cn
import time

def filter_dupes():
   
    green_zip = zip(cn.green, cn.green_mul)
    
    cn.letters = list(cn.letters) + cn.green + ["".join(i) for i in cn.yellow_list]
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
            if j in cn.yellow_dic and cn.yellow_dic[j] == 1 and j in i:
                continue

            for k in cn.k_list:     
                if k in cn.yellow_dic and cn.yellow_dic[k] == 1 and k in i+j:
                    continue

                for l in cn.l_list:   
                    if l in cn.yellow_dic and cn.yellow_dic[l] == 1 and l in i+j+k:
                        continue

                    for m in cn.m_list:   
                        if m in cn.yellow_dic and cn.yellow_dic[m] == 1 and m in i+j+k+l:
                            continue   

                        # create word   
                        buff = i + j + k + l + m

                        # check if word exists
                        if check_yellows_included(buff) and check_yellow_amount(buff) and buff in cn.data:
                            cn.words.append(buff)

def adjust_list(x):
    cn.words.remove(x)


def check_yellows_included(word):
   
    yel = []
    for i in cn.yellow_list:
        for j in i:
            yel.append(j)
            
    yel = set(yel)
    
    for i in yel:
        if not i in word:
            return False
    
    return True

def check_yellow_amount(word):
    
    for i in cn.yellow_dic:
        n = cn.yellow_dic[i]
        if n == 0:
            continue
        elif n == 1 and (not 1 == word.count(i)):
            return False
        elif n == 2 and (not 1 < word.count(i)):
            return False
        elif n == 3 and (not 2 == word.count(i)):
            return False
        elif n == 4 and (not 2 < word.count(i)):
            return False
    return True


    
def extract(gui_data): 
    
    cn.green = gui_data["green"]
    cn.green_mul = gui_data["green_more_than_once"]
    cn.yellow_list = gui_data["yellow"]
    cn.letters = list(set(gui_data["available_letters"]))
    cn.yellow_zip = zip(cn.yellow_list, gui_data["yellow_more_than_once"])
    
    cn.create_yellow_dict()
    
    filter_dupes()
    cn.Print()
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