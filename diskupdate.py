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


def apply(action, label, devpath):
	mntpath = "/media/test/" + label
	mkdir_cmd = "mkdir " + mntpath
	rmdir_cmd = "rm -rf " + mntpath
	mnt_cmd = "mount " + devpath + " " + mntpath
	umnt_cmd = "umount " + mntpath

	logfilename = "/tmp/" + label + "-" + action
	tempfile = open(logfilename, 'w')
	tempfile.write("%s device %s @ %s\n" % (action, label, devpath))

	if (action == "add" and len(label) > 0 and len(devpath) > 0):
		log_exec(tempfile, mkdir_cmd)
		log_exec(tempfile, mnt_cmd)

	if (action == "remove" and len(label) > 0 and len(devpath) > 0):
		log_exec(tempfile, umnt_cmd)
		log_exec(tempfile, rmdir_cmd)

	tempfile.close()


def read_queue(fname):
	queue = open(fname, 'rw')
	for line in queue.readlines():
		split = line.split(',')
		if len(split) == 3:
			apply(split[0].strip(), split[1].strip(), split[2].strip())

	queue.seek(0)
	queue.truncate()
	queue.close()


while True:
	time.sleep(10)
	read_queue("/tmp/devqueue")
