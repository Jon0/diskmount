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

def log_exec(logfile, cmd):
	logfile.write("exec %s\n" % (cmd))
	logfile.write("%s\n" % (exec_cmd(cmd)))

action = find_env(['ACTION'])
label = find_env(['ID_FS_LABEL', 'ID_FS_UUID'])
devpath = find_env(['DEVNAME', 'DEVPATH'])
mntpath = "/media/test/" + label
mkdir_cmd = str("mkdir " + mntpath).strip()
rmdir_cmd = str("rm -rf " + mntpath).strip()
mnt_cmd = str("mount " + devpath + " " + mntpath).strip()
umnt_cmd = str("umount " + mntpath).strip()

# write debug file
logfilename = "/tmp/" + label + "-" + action
tempfile = open(logfilename, 'w')
tempfile.write(action + " device %s @ %s\n" % (label, devpath))
if (action == "add" and len(label) > 0 and len(devpath) > 0):
	time.sleep(10)
	log_exec(tempfile, mkdir_cmd)
	log_exec(tempfile, mnt_cmd)
	subprocess.call(['mount', devpath, mntpath])

if (action == "remove" and len(label) > 0 and len(devpath) > 0):
	time.sleep(10)
	log_exec(tempfile, umnt_cmd)
	log_exec(tempfile, rmdir_cmd)

tempfile.write("%s\n" % (exec_cmd('env')))
tempfile.close()
