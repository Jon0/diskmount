#!/usr/bin/python3

import time
import subprocess

def exec_cmd(cmd):
	env = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = env.communicate()
	result = str(output, 'utf-8').strip()
	if (len(errors) > 0):
		result += " err: "
		result += str(errors, 'utf-8').strip()
	return result


def find_env(keys):
	for key in keys:
		result =  exec_cmd("echo $" + key)
		if (len(result) > 0):
			return result
	return ""


label = find_env(['ID_FS_LABEL', 'ID_FS_UUID'])
devpath = find_env(['DEVNAME', 'DEVPATH'])
mkdir_cmd = str("mkdir /media/" + label).strip()
mnt_cmd = str("mount " + devpath + " /media/" + label).strip()

# write debug file
logfilename = "/tmp/" + label
tempfile = open(logfilename, 'w')
tempfile.write("device %s @ %s\n" % (label, devpath))
tempfile.write("exec %s\n" % (mkdir_cmd))
tempfile.write("exec %s\n" % (mnt_cmd))
tempfile.write("%s\n" % (exec_cmd('env')))


if (len(label) > 0 and len(devpath) > 0):
	time.sleep(10)
	tempfile.write(exec_cmd(mkdir_cmd))
	tempfile.write(exec_cmd(mnt_cmd))

tempfile.close()