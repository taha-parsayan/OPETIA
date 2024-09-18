import os

for i in range (1,22):
    j = str(i)
    os.system('fslmaths ' + j + '_*  -thr 0.1 -bin ' + j + '_*')
