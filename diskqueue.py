#!/usr/bin/python3

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


# write to file
queuefilename = "/tmp/devqueue"
tempfile = open(queuefilename, 'a')
tempfile.write("%s,%s,%s\n" % (action,label, devpath))
tempfile.close()
