#!/usr/bin/python3

import subprocess


def exec_cmd(cmd):
	env = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = env.communicate()
	return str(output, 'utf-8').strip()

label = exec_cmd('echo $ID_FS_LABEL')
devpath = exec_cmd('echo $DEVPATH')
mnt_cmd = str("mount " + devpath + " /media/" + label).strip()
print(label)
print(devpath)
print(mnt_cmd)

# write debug file
tempfile = open('/tmp/devices', 'w')
tempfile.write("device %s @ %s\n" % (label, devpath))
tempfile.write("exec %s\n" % (mnt_cmd))
tempfile.write(exec_cmd('env'))
tempfile.close()

if (len(label) > 0 and len(devpath) > 0):
	exec_cmd(mnt_cmd)