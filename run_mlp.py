from sklearn.neural_network import MLPClassifier
import sys
training_file = sys.argv[1]
testing_file = sys.argv[2]

def get_data(file_name):
  X = []
  y = []
  f = open(file_name, 'r')
  l = f.readline()
  l = l[:len(l)-1]
  while len(l)>0:
    X.append([int(x) for x in l[:len(l)-1]])
    y.append(int(l[len(l)-1]))
    l = f.readline()
    l = l[:len(l)-1]
  f.close()
  return X, y

X, y = get_data(training_file)
#print(X, y)
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(25, 2), random_state=1)
clf.fit(X, y)
X2, y2 = get_data(testing_file)
y3 = clf.predict(X2)
cnt = 0
for i in range(len(y2)):
  if y2[i]==y3[i]:
    cnt += 1
print("Accuracy: ", cnt/len(y2))

