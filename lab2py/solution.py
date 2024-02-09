import sys

data = []
sos = []
end = ''

method = sys.argv[1]

def removeTautology():
    global data
    removalSet = set()
    cnt = 0
    for clause in data:
        
        for i in range(len(clause) - 1):
            for j in range(i + 1, len(clause)):
                if clause[i].startswith('~') and not clause[j].startswith('~') and clause[i].replace('~', '') == clause[j]:
                    removalSet.add(cnt)
                if not clause[i].startswith('~') and clause[j].startswith('~') and clause[j].replace('~', '') == clause[i]:
                    removalSet.add(cnt)
        cnt += 1
    new_data = [clause for i, clause in enumerate(data) if i not in removalSet]
    
    sorted_data = [sorted(sublist, key=lambda x: x.lstrip('~')) for sublist in new_data] # stackOverflow
    data = sorted_data

def removeRedundant():
    global data
    #data = new_data

    remove_list = []
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            if set(data[i]).issubset(set(data[j])):
                if data[j] not in remove_list:
                    remove_list.append(data[j])
                break
            if set(data[j]).issubset(set(data[i])):
                if data[i] not in remove_list:
                    remove_list.append(data[i])
    for item in remove_list:
        data.remove(item)



def factorization():
    global data
    no_repeats = []
    for sublist in data:
        new_sublist = []
        for elem in sublist:
            if elem not in new_sublist:
                new_sublist.append(elem)
        if sorted(new_sublist) == sorted(set(sublist)):
            no_repeats.append(new_sublist)
    data = no_repeats


def negateLast():
    global data
    new_data = data
    
    if len(data[-1]) == 1:
        if data[-1][0].startswith('~'):
            last = new_data[-1][0].replace('~', '')
        if not data[-1][0].startswith('~'):
            last = new_data[-1][0].replace(new_data[-1][0], '~' + new_data[-1][0])
        new_data[-1][0] = last
        sos.append([last])
    else:
        last = new_data[-1]
        new_data.remove(new_data[-1])
        new_list = []
        for item in last:
            new_list.append([item])
            

        for item in new_list:
            if item[0].startswith('~'):
                new_item = item[0].replace('~', '')
            else:
                new_item = item[0].replace(item[0], '~' + item[0])
            item[0] = new_item
        for item in new_list:
            new_data.append(item)
            sos.append(item)

def checkTautology(list1):
    for i in range(0, len(list1)):
        for j in range(1, len(list1)):
            if list1[i] == list1[j].replace('~', '') and i != j:
                return False
            if list1[i].replace('~', '') == list1[j] and i != j:
                return False
            
    return True

def getData(file):
    global data
    global end
    curr_line = ""
    for line in file.readlines():
        if not line.startswith('#'):
            curr_line = line.strip()
            line = line.strip().split(" ")
            line = list(filter(lambda x: x != 'v' and x != 'V', line)) # uzeto sa stackOverflowa
            for i in range(len(line)):
                line[i] = line[i].lower()
                
            data.append(line)
    end = curr_line

def checkResolution():
    global data
    global end

    flag = True
    #print("data: ")
    #print(data)
    cntSos = 0
    while cntSos < len(sos) and flag:
        for sosClause in sos[cntSos]:
            cntData = 0
            item = ''
            if sosClause.startswith('~'):
                item = sosClause.replace('~', '')
            else:
                item = sosClause.replace(sosClause, '~' + sosClause)
            while cntData < len(data) and flag:
                if item in data[cntData] and item != data[cntData]:
                    newItem = [elem for elem in sos[cntSos] + data[cntData] if elem != sosClause and elem != item]
                    newItem = list(set(newItem))
                    if newItem not in data and checkTautology(newItem):
                        data.append(newItem)
                        sos.append(newItem)
                    if newItem == []:
                        flag = False
                cntData += 1
        cntSos += 1
        #print(f"data : {data}")

    #print(data)
    if flag:
        print(f"[CONCLUSION]: {end.lower()} is unknown")
    else:
        print(f"[CONCLUSION]: {end.lower()} is true")



def resolution():
    
    file = open(sys.argv[2], "r", encoding="utf-8")
    getData(file)
    print(data)
    factorization()
    removeTautology()
    negateLast()
    removeRedundant()
    checkResolution()
    

def cooking():
    global data
    global end
    global sos
    file = open(sys.argv[2], "r", encoding="utf-8")
    getData(file)
    print(data)
    factorization()
    removeTautology()
    removeRedundant()
    data1 = data.copy()
    sos1 = sos.copy()
    #print(data)
    file1 = open(sys.argv[3], "r", encoding="utf-8")
    for line in file1.readlines():
        line = line.strip()
        command = line[-1]
        clause = line[0:-2].lower()
        if command == '+':
            if ' ' in clause:
                clause = clause.split(" v ")
                if clause not in data:
                    clause.sort(key=lambda x: x[1:] if x.startswith('~') else x)
                    data.append(clause)
                    data1.append(clause)
            else:
                if clause not in data:
                    data.append([clause])
                    data1.append([clause])
        if command == '-':
            if ' ' in clause:
                clause = clause.split(" v ")
                clause.sort(key=lambda x: x[1:] if x.startswith('~') else x)
                data.remove(clause)
                data1.remove(clause)
            else:

                data.remove([clause])
                data1.remove([clause])
        if command == '?':
            end = clause
            if clause.startswith('~'):
                clause = clause.replace('~', '')
            else:
                clause = clause.replace(clause, '~' + clause)
            data.append([clause])
            sos.append([clause])
            checkResolution()
            data = data1.copy()
            sos = sos1.copy()
    
    
if method == 'resolution':
    resolution()

if method == 'cooking':
    cooking()
