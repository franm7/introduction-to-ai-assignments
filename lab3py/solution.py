import csv
import math
import sys



class Node:
    def __init__(self, attribute, label):
        self.attribute = attribute
        self.label = label
        self.children = {} 
        self.root = None
        self.predictions = []
        self.predictData = []
    
    def addChild(self, value, childNode):
        self.children[value] = childNode

class ID3:
    def __init__(self, path):
        self.path = path
        self.data = {}
        

    def findEntropy(self, attribute, data):
        
        entropy = 0
        visited = set()
        for item in data[attribute]:
            if item not in visited:
                visited.add(item)
                entropy += (data[attribute].count(item) / len(data[attribute])) * math.log2(data[attribute].count(item) / len(data[attribute]))

        entropy = abs(entropy)
        #print(entropy)

        return entropy
        
    def findInformationGain(self, target, attribute, data):
        totalEntropy = self.findEntropy(target, data)
        labelSet = set(data[attribute])
        
        for label in labelSet:
            subList = []
            for i in range(len(data[attribute])):
                if label == data[attribute][i]:
                    subList.append(data[target][i])
            visited = set()
            entropy = 0
            for item in subList:
                if item not in visited:
                    visited.add(item)
                    entropy += (subList.count(item) / len(subList)) * math.log2(subList.count(item) / len(subList))
            entropy = abs(entropy)
            
            totalEntropy -= entropy * data[attribute].count(label) / len(data[attribute])
        #print(totalEntropy)
       
        return totalEntropy
    
    def makeNewData(self, attribute, label, data):
        newData = {}
        for item in data:
            if item != attribute:
                newData[item] = []

        for i in range(len(data[attribute])):
            if data[attribute][i] == label:
                for item in newData:
                    newData[item].append(data[item][i])

        #print(newData)
        return newData
    
    def getMajority(self, labels):
        labelCounts = {}
        for label in labels:
            if label in labelCounts:
                labelCounts[label] += 1
            else:
                labelCounts[label] = 1
        majority = max(labelCounts, key=labelCounts.get)
        return majority
 
    

    def buildTree(self, data, attributes, depth=1000):
        target = list(data.keys())[-1]

        if len(set(data[target])) == 1:
            label = data[target][0]
            return Node(None, label)

        if depth == 0:
            label = self.getMajority(data[target])
            return Node(None, label)

        infGain = []
        for attribute in attributes:
            if target != attribute:
                gain = self.findInformationGain(target, attribute, data)
                infGain.append((gain, attribute))

        maxGain = max(infGain, key=lambda x: x[0])[0] # iskopirano od negdje
        maxAttributes = [attr for gain, attr in infGain if gain == maxGain]
        maxAttribute = maxAttributes[0] if len(maxAttributes) == 1 else min(maxAttributes)


        root = Node(maxAttribute, None)
        #print(infGain)
        labels = set(data[maxAttribute])

        for label in labels:
            newData = self.makeNewData(maxAttribute, label, data)
            newNode = self.buildTree(newData, list(newData.keys()), depth - 1)

            root.addChild(label, newNode)

        return root

    def fit(self):
        with open(self.path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                for i, label in enumerate(header):
                    if label in self.data:
                        self.data[label].append(row[i])
                    else:
                        self.data[label] = [row[i]]
        #print(self.data)
        if len(sys.argv) > 3:
            self.root = self.buildTree(self.data, list(self.data.keys()), int(sys.argv[3]))
        else:
            self.root = self.buildTree(self.data, list(self.data.keys()))
        
    def predict(self):
        predictData = []
        with open(sys.argv[2], "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                dict = {}
                for i in range(len(row)):
                    dict[header[i]]=row[i]
                predictData.append(dict)
        #print(predictData)
        self.predictData = predictData
        predictions = []
       
        for instance in predictData:
            prediction = self.predictRecursive(self.root, instance)
            predictions.append(prediction)

        self.predictions = predictions



        return predictions

    def predictRecursive(self, node, instance):
        if node.attribute is None:
            return node.label

        attributeValue = instance[node.attribute]
        if attributeValue in node.children:
            childNode = node.children[attributeValue]
            return self.predictRecursive(childNode, instance)
        else:
            return None
        

    def accuracy(self):
        target = list(self.data.keys())[-1]
        cnt = 0
        for i in range(len(self.predictions)):
            if self.predictData[i][target] == self.predictions[i]:
                cnt += 1
        return cnt/len(self.predictions)
        
    def confusionMatrix(self):
        target = list(self.data.keys())[-1]
        outcomes = list(set(self.predictions))
        outcomes = sorted(outcomes)
        matrix = [[0] * len(outcomes) for i in range(len(outcomes))]
        results = []
        for i in range(len(self.predictData)):
            results.append(self.predictData[i][target])

        for pred, true in zip(self.predictions, results):
            i = outcomes.index(pred)
            j = outcomes.index(true)
            matrix[j][i] += 1
        #print(matrix)
        return matrix
               
    

def printTree(node, level=1, text=""):
    if node.attribute is None:
        print(f"{text}{node.label}")
    else:
        for child, childNode in node.children.items():
            printTree(childNode, level + 1, f"{text}{level}:{node.attribute}={child} ")
              


model = ID3(sys.argv[1])
model.fit()
print("[BRANCHES]:")
printTree(model.root)
predictions = model.predict()
print("[PREDICTIONS]:", " ".join(predictions))
accuracy = model.accuracy()
print(f'[ACCURACY]: {accuracy:.5f}')
print("[CONFUSION_MATRIX]:")
matrix = model.confusionMatrix()
for i in range(len(matrix)):
    text = ""
    for j in range(len(matrix)):
        text = text + str(matrix[i][j]) + " "
    print(text)


