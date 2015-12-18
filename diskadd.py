#!/usr/bin/python3

import subprocess

def exec_cmd(cmd):
	env = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = env.communicate()
	return str(output, 'utf-8').strip()

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
tempfile = open('/tmp/devices', 'w')
tempfile.write("device %s @ %s\n" % (label, devpath))
tempfile.write("exec %s\n" % (mkdir_cmd))
tempfile.write("exec %s\n" % (mnt_cmd))
tempfile.write(exec_cmd('env'))
tempfile.close()

if (len(label) > 0 and len(devpath) > 0):
	exec_cmd(mkdir_cmd)
	exec_cmd(mnt_cmd)
