import os

#because there are 91 voxels on x, column 45 should be in both left and right images (overlapping)

for i in range (1,22):
	os.system('echo ' + str(i))
	j = str((2*i)-1)
	k = str(2*i)
	os.system('fslroi ' + str(i) + '_*.nii.gz ' + j + '.nii.gz 0 46 0 109 0 91')
	os.system('fslroi ' + str(i) + '_*.nii.gz ' + k + '.nii.gz 45 46 0 109 0 91')
	os.system('fslmaths ' + j + '.nii.gz -mul 0 empthy_right')
	os.system('fslmaths ' + k + '.nii.gz -mul 0 empthy_left')
	os.system('fslroi empthy_right empthy_right 0 45 0 109 0 91')
	os.system('fslroi empthy_left empthy_left 0 45 0 109 0 91')
	os.system('fslmerge -x ' + j + '.nii.gz ' + j + '.nii.gz empthy_left')
	os.system('fslmerge -x ' + k + '.nii.gz empthy_right ' + k + '.nii.gz')
	os.system('rm empthy* ')
