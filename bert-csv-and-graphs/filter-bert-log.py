def isOdd(counter):
    r = counter % 2
    return (r == 1)

def getF1(line):
    toks = line.split(',')
    rawF1 = toks[0]
    toks2 = rawF1.split(':')
    f1 = toks2[1]
    return f1[1:]
def getRocAuc(line):
    toks = line.split(',')
    rawF1 = toks[1]
    toks2 = rawF1.split(':')
    rocAuc = toks2[1]
    return rocAuc[12:-1]
def getAccuracy(line):
    toks = line.split(',')
    rawF1 = toks[2]
    toks2 = rawF1.split(':')
    accuracy = toks2[1]
    return accuracy[1:-1]

csvRows = []

if __name__ == '__main__':
    fw1 = open('csv/bert-50-labels-metrics-test-set.csv', 'w')
    fw1.write('"epoch","f1","roc_auc","accuracy"\n')

    with open('raw-logs/log-BERT.txt', 'r') as fd:
        counter = 0
        epoch = 0
        for line in fd.readlines():
            if line.startswith("{'f1': "):
                line = line[:-1]
                counter += 1
                if (counter == 0) or isOdd(counter):
                    fw1.write(str(epoch) + ',' + getF1(line) + ',' + getRocAuc(line) + ',' + getAccuracy(line) + '\n')
                    epoch += 1

    fw1.close()

    fw2 = open('csv/bert-50-labels-losses-metrics-validation-set.csv', 'w')
    fw2.write('"Epoch","Training Loss","Validation Loss","Model Preparation Time","F1","Roc Auc","Accuracy"\n')

    with open('raw-logs/log-BERT.txt', 'r') as fd:
        lines = fd.readlines()

    i = 0
    epoch = 0
    while (i  < len(lines)):
        line = lines[i]
        counter = 0
        if line.startswith("Epoch	Training Loss"):
            i += 1
            line = lines[i]
            line = line[:-1]
            toks = line.split('\t')
            fw2.write(str(epoch) + ',' + toks[1] + ',' + toks[2]  + ',' + toks[3]
                      + ',' + toks[4] + ',' + toks[5] + ',' + toks[6] + '\n')
            epoch += 1

        i += 1

    fw2.close()

    print('Done!')
