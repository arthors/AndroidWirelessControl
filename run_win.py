import os
import subprocess
import re
import time
import ast

def getDeviceVersion():
	res = subprocess.Popen('adb shell getprop ro.build.version.release', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	res1 = str(res.stdout.readlines()[0])
	print res1 
	return res1


def getIP():
	if (ast.literal_eval(getDeviceVersion())<6.0):
		reip = re.compile(r'ip (?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
	else:	
		reip = re.compile(r'inet addr:(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
#	res = subprocess.Popen('adb shell ifconfig wlan0',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
	res = subprocess.Popen('adb shell ifconfig wlan0',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	result = str(res.stdout.readlines())
	print result
	for ip in reip.findall(result):
		print ip
	if (float(getDeviceVersion())<6.0):
		ip=ip[3:]
	else:
		ip=ip[10:]
	print ip
	if not ip.strip()=="":
		print "OK"
	return ip

def connectDevice(ip):
#	res = subprocess.Popen('adb connect '+str(ip) ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
	res = subprocess.Popen('adb connect '+str(ip) ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	result = str(res.stdout.readlines())
	return result

def reSet():
	os.system('adb kill-server')
	time.sleep(1)
	os.system('adb start-server')
	time.sleep(2)
#	os.system('adb shell setprop service.adb.tcp.port 5555')	
	time.sleep(2)
	os.system('adb tcpip 5555')	
	time.sleep(2)

def judgeConnect():
#	res = subprocess.Popen('adb devices',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
	res = subprocess.Popen('adb devices',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	result = res.stdout.readlines()
#	print len(result)
	return len(result)

def mkUSBcut():
	time.sleep(1)	
	if judgeConnect()==2:
		print "Successed to cut USB"
	else:
		print "you should cut down USB"
		mkUSBcut()		

def mkUSBCon():
	time.sleep(0.5)
	if judgeConnect()!=2:
		print "Successed Connection"
	else:
		print "you should connect USB cable"
		mkUSBCon()

def storeIP(ip):
	res = subprocess.Popen('adb shell getprop ro.serialno',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	result = res.stdout.readlines()[0]
	print str(result).strip()+"="+ip



def main():
#	mkUSBCon()
	reSet()
	mkUSBCon()
	ips=getIP()
	storeIP(ips)
	print "you should cut down USB"
	mkUSBcut()
	time.sleep(5)	
	print connectDevice(ips)


if __name__ == '__main__':
	main()	
