import os
import subprocess
import re
import time

def getIP():
	reip = re.compile(r'ip (?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
	res = subprocess.Popen('adb shell ifconfig wlan0',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
	result = str(res.stdout.readlines())
	for ip in reip.findall(result):
		print ip
	ip=ip[3:]
	print ip
	if not ip.strip()=="":
		print "OK"
	return ip

def connectDevice(ip):
	res = subprocess.Popen('adb connect '+str(ip) ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
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
	res = subprocess.Popen('adb devices',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
	result = res.stdout.readlines()
	print len(result)
	return len(result)

def mkUSBcut():
	
	
	time.sleep(1)	
	if judgeConnect()==2:
		print "OK"
	else:
		print "you should cut down USB"
		mkUSBcut()		


if __name__ == '__main__':
	
	reSet()
	ips=getIP()
	print ips
	print "you should cut down USB"
	mkUSBcut()
	time.sleep(5)	
	print connectDevice(ips)

