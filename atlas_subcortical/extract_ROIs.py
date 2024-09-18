import os

for i in range (1,49):
    j = str(i)
    os.system('fslmaths atlas_harvardoxford-cortical.nii.gz -uthr ' + j + ' -thr ' + j + ' -bin ' + j)
