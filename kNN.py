import numpy as np
import math
import csv
import getopt
import sys


def dist(a, b):
    return math.sqrt((a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def w_i(k, i, case, nn):
    d_k = dist(case, nn[k - 1])
    d_1 = dist(case, nn[0])
    if d_k == d_1:
        return 1
    else:
        d_i = dist(case, nn[i])
        return (d_k - d_i) / (d_k - d_1)


def weights(k, case, nn):
    w = np.array([])
    for i in range(k):
        weight_i = w_i(k, i, case, nn)
        w = np.append(w, [weight_i])
    return w


def knn(k, case, casebase):
    nn = np.empty([0, 3])
    for i in range(len(casebase)):
        if len(nn) < k:
            nn = np.vstack((nn, casebase[i]))
            nn = sorted(
                nn,
                key=lambda x: math.sqrt((case[1] - x[1]) ** 2 + (case[2] - x[2]) ** 2),
            )
        else:
            if dist(case, casebase[i]) < dist(case, nn[k - 1]):
                nn = np.vstack((nn, casebase[i]))
                nn = sorted(
                    nn,
                    key=lambda x: math.sqrt(
                        (case[1] - x[1]) ** 2 + (case[2] - x[2]) ** 2
                    ),
                )
                nn = nn[:k]
    return nn


try:
    opts, _ = getopt.getopt(sys.argv[1:], "", ["data=", "k="])
except getopt.GetoptError:
    print("student.py --data <file> --eta <value> --k <value>")
    sys.exit(2)

for opt, arg in opts:
    if opt == "--data":
        data = arg
    elif opt == "--k":
        k = int(arg)

try:
    data
    k
except NameError:
    print("student.py --data <file> --eta <value> --k <value>")
    sys.exit(2)


# creating lists for the casebase and the cases we have to classify (ctc):
casebase = np.empty([0, 3], dtype=float)
ctc = np.empty([0, 3], dtype=float)
# loop over all rows in the csv:
with open(data) as f:
    reader = csv.reader(f)
    for row in reader:
        row[0] = 1 if row[0] == "A" else 2
        row[1] = float(row[1])
        row[2] = float(row[2])
        # row=the row/case we are working with in this iteration of the loop
        if len(casebase) == 0:
            casebase = np.vstack([casebase, row])

        nn = knn(1, row, casebase)
        if nn[0][0] != row[0]:
            casebase = np.vstack([casebase, row])
        else:
            ctc = np.vstack([ctc, row])

# iterated over all rows


errors = 0
# iterate over all cases c in ctc:
for c in ctc:
    c_class=0
    cweights = np.zeros(2)
    nn = knn(k, c, casebase)
    w = weights(k, c, nn)
    for i in range(k):
        if nn[i][0] == 1:
            cweights[0] += w[i]
        else:
            cweights[1] += w[i]

    if (cweights[0]>cweights[1]):  # what is supposed to happen if both weights are equal?
        c_class = 1
    else:
        c_class = 2

    if c_class != c[0]:
        errors += 1



# counted the false classifications

print(errors)
for case in casebase:
    if case[0] == 1:
        res = "A"
    else:
        res = "B"
    res += "," + str(case[1]) + "," + str(case[2])
    print(res)