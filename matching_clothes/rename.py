import os
from os import listdir
from os.path import isfile, join
path = os.getcwd() + '/training_shirts'

origFileNames = []
for f in listdir(path):
    head = os.path.splitext(f)[0]
    origFileNames.append(head)
print (origFileNames)
print(len(origFileNames))

men_path = os.getcwd() + '/men_training'
i = 0
for file in listdir(men_path):
    print(os.path.join(path, file))
    os.rename(os.path.join(men_path, file), os.path.join(men_path, ''.join([origFileNames[i], '.jpg'])))
    i += 1

