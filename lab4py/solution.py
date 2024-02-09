import numpy as np
import sys
import random



trainFile = sys.argv[2]
testFile = sys.argv[4]
architecture = sys.argv[6]
popsize = int(sys.argv[8])
elitism = int(sys.argv[10])
p = float(sys.argv[12])
K = float(sys.argv[14])
iter = int(sys.argv[16])


class NN:
    def __init__(self):
        self.weights = []
        self.biases = []
        self.architecture = []
        self.features = []
        self.target = []
        self.outputs = []
        

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def getData(self, trainFile, testFile, architecture):
        with open(trainFile, 'r') as file:
            lines = file.readlines()

        data = [line.strip().split(',') for line in lines[1:]]
        dataArray = np.array(data, dtype=np.float32)
        features = dataArray[:, :-1]
        target = dataArray[:, -1]
        #print(features)
        #print(target)
        inputNum = len(features[0])
        architecture = architecture.strip().split("s")
        architecture = architecture[:-1]
        architecture = [eval(i) for i in architecture]
        architecture.insert(0, inputNum)
        architecture.append(1)
        #print(architecture)
        self.features = features
        self.target = target
        self.architecture = architecture
        #(type(architecture[1]))

    def build(self):
        weights = []
        biases = []

        for i in range(1, len(self.architecture)):
            last = self.architecture[i-1]
            curr = self.architecture[i]

            weightMatrix = np.random.normal(0, 0.01, size=(curr, last))
            weights.append(weightMatrix)

            biasVector = np.random.normal(0, 0.01, size=(curr, 1))

            biases.append(biasVector)

        self.weights = weights
        self.biases = biases
        #print(weights)
        #print(biases)

    def forward(self, data):
        outputs = []
        for item in data:
            x = np.array(item).reshape((-1, 1))
            for i in range(len(self.weights)):
                weights = self.weights[i]
                biases = self.biases[i]
                if i == 0:
                    result = np.dot(weights, x) + biases
                    result = self.sigmoid(result)
                else:
                    result = np.dot(weights, result) + biases
                    if i < len(self.weights) - 1:
                        result = self.sigmoid(result)  
                
            outputs.append(result)
        self.outputs = outputs

    def MSE(self, target):
        #print(target)
        sum = 0
        for i in range(len(target)):
            sd = np.square(target[i] - np.squeeze(self.outputs[i]))
            sum += sd

        mse = sum / len(target)

        return mse

    def fit(self):
        self.getData(trainFile, testFile, architecture)
        self.build()
        self.forward(self.features)

def getFitness(MSE, maxErr):
    fitness = []
    for i in range(len(MSE)):
        fit = 1 - (MSE[i]/maxErr)
        fitness.append(fit)

    return fitness

def crossOver(model1, model2):
    newModel = NN()
    newModel.fit()
    for i in range(len(model1.weights)):
        weightMatrix1 = model1.weights[i]
        weightMatrix2 = model2.weights[i]
        
        for j in range(len(weightMatrix1)):
            for k in range(len(weightMatrix1[j])):
                newModel.weights[i][j][k] = (weightMatrix1[j][k] + weightMatrix2[j][k]) / 2
        


    for i in range(len(model1.biases)):
        for j in range(len(model1.biases[i])):
            newModel.biases[i][j] = (model1.biases[i][j] + model2.biases[i][j]) / 2
            

    newModel.forward(newModel.features)

    return newModel

    
def mutate(model):
    for weightMatrix in model.weights:
        for vector in weightMatrix:
            for j in range(len(vector)):
                rand = random.uniform(0, 1)
                if rand < p:
                    vector[j] += np.random.normal(0, K)

    #print(f'old biases:{model.biases}')
    for i in range(len(model.biases)):
        for bias in model.biases[i]:
            rand = random.uniform(0, 1)
            if rand < p:
                bias[0] += np.random.normal(0, K)
    #print(f'new biases:{model.biases}')


models = []
for i in range(popsize):
    model = NN()
    model.fit()
    #print(model.weights)
    #error = model.MSE()
    models.append(model)
    #MSE.append(error)
    #print(MSE[i])

#print(models[0].biases)
#print(models[0].weights)
#print(models[1].target)

for i in range(1, iter + 1):
    best = []
    newPop = []
    MSE = []
    maxErr = 0
    for j in range(popsize):
        error = models[j].MSE(models[j].target)
        if error > maxErr:
            maxErr = error
        MSE.append(error)


    for j in range(elitism):
        a=MSE.index(min(MSE))
        best.append(a)
        newPop.append(models[a])

    
    fitness = getFitness(MSE, maxErr)
    #print(fitness)
    fitnessSum = sum(fitness)
    for j in range(elitism, popsize):
        cross = []
        for l in range(2):
            randomNum = random.uniform(0, fitnessSum)
            sumNum = 0
            index = -1
            for k in range(popsize):
                sumNum += fitness[k]
                if randomNum < sumNum:
                    index = k
                    break
            cross.append(index)
        newModel = crossOver(models[cross[0]], models[cross[1]])
        mutate(newModel)
        newPop.append(newModel)
        
    if i % 2000 == 0:
        #print(models[0].biases)
        print(f'[Train error @{i}]: {MSE[0]}')

    models = newPop



    

with open(testFile, 'r') as file:
    lines = file.readlines()
data = [line.strip().split(',') for line in lines[1:]]
dataArray = np.array(data, dtype=np.float32)
features = dataArray[:, :-1]
target = dataArray[:, -1]
models[0].forward(features)
testMSE = models[0].MSE(target)
print(f'[Test error]: {testMSE}')
