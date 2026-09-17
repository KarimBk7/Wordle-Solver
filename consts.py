f = open("words_5.txt")
data = f.read()

alpha ="abcdefghijklmnopqrstuvwxyz"
green =  ["","","","",""]
green_mul = [1,1,1,1,1]
yellow_list =[[""],[""],[""],[""],[""]]
yellow_dic = {}
yellow_zip = None
letters = ""


i_list = []
j_list = []
k_list = []
l_list = []
m_list = []

y_list = []


def reset():
    green =  ["","","","",""]
    green_mul = [1,1,1,1,1]
    yellow_list =[[""],[""],[""],[""],[""]]
    yellow_dic = {}
    yellow_zip = None
    letters = ""


    i_list = []
    j_list = []
    k_list = []
    l_list = []
    m_list = []

    y_list = []

    words = []



def create_yellow_dict():
    count = 0
    for char, amount  in yellow_zip:
        print(f"Count: {count} --- {char} --- {amount}")
        for i in range(5):
            if char[i] != "" and char[i] in alpha :
                
                m = amount[i]
                s = 0
                if m == ">0":
                    s = 0           # 0: at least once
                elif m == "=1":
                    s = 1           # 1: exactly one
                elif m == ">1":
                    s = 2           # 2: more than one
                elif m == "=2":
                    s = 3           # 3: exactly twice
                elif m == ">2":
                    s = 4           # 4: more than zwice
                elif m == "=3":
                    s = 4
                
                yellow_dic[char[i]] = s
        
        
        count += 1
        
        

def Print():
    print("Green:", green)
    print("Yellow-List:", yellow_list)
    print("Yellow-Dict:", yellow_dic)
    print("Letters:", letters)