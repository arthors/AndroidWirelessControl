# -*- coding: UTF-8 -*- 
import os
import sys
import subprocess
import re
import time
import ast

def writeFile(files,line):
	f1 = open(files, 'a+')
	f1.write(line)
	f1.close()

def replaceline(files,oldline,newline):
	f = open(files,'r')
	f_new = open('tmp','w')
	for line in f:
#	judge file line
    		if oldline in line:
        		line = line.replace(oldline,newline.strip('\n'))
#	replace oldline into newline
		f_new.write(line)
	f.close()
	f_new.close()
	os.rename("tmp",files)



def readFile(files,SN,ip,MAC):
#	judge whether files name exists in workspace:
#	if not existe make new file
#	else write new configline into file
	flg=0;
#	if first connection make file and store it; 	
	if not os.path.exists(files):
		print "first connection and file record"
		writeFile(files,(SN+"="+ip+"="+MAC))
	else:
#	start find old record and renew it;
		f0 = open(files, 'r+')
		print "open file"
		for line in f0.readlines():
			linestr = line.strip()
#	find the Serial Numble if exist in file replace it;
			sn = linestr.split('=')[0]
			if (SN == sn):
				print "get old record and renew it"
				linestr2 = str(SN)+'='+str(ip)+'='+str(MAC)	
				replaceline(files,linestr,linestr2)
				flg=1;
			else:
#	if not go to end of file then continue;
				if line:
					continue;
#	make sure this is a new connection then break to store it;
				print "new connection and record it"
				break;
		f0.close()			
#	finish find old record and renew it;
#	start add new record;
		if flg == 0:
			f1 = open(files, 'a+')
			f1.write(SN+"="+ip+"="+MAC)
			f1.close()
#	finish add new record;

def getDeviceVersion():
	res = subprocess.Popen('adb shell getprop ro.build.version.release', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	res1 = str(res.stdout.readlines()[0])
#	print res1 
	return res1

def getMAC():
	res = subprocess.Popen('adb shell cat /sys/class/net/wlan0/address', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	result = str(res.stdout.readlines()[0])
	return result

def getIP():
	if (ast.literal_eval(getDeviceVersion())<6.0):
		reip = re.compile(r'ip (?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
	else:	
		reip = re.compile(r'inet addr:(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
#	res = subprocess.Popen('adb shell ifconfig wlan0',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
	res = subprocess.Popen('adb shell ifconfig wlan0',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	result = str(res.stdout.readlines())
#	print result
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
	print result;
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
	time.sleep(1)
	if judgeConnect()!=2:
		print "Successed Connection"
	else:
		print "you should connect USB cable"
		mkUSBCon()

def storeIP(ip):
	res = subprocess.Popen('adb shell getprop ro.serialno',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	result = res.stdout.readlines()[0]
	return result



def newDevices():
#	mkUSBCon()
	reSet()
	mkUSBCon()
	ips=getIP()
	SN=storeIP(ips)
	MAC=getMAC()
	line=str(SN).strip()+"="+ips+"="+str(MAC)
#	readFile('list',str(SN).strip(),ips,str(MAC))
	print "you should cut down USB"
	mkUSBcut()
	time.sleep(5)	
	print connectDevice(ips)
	readFile('list',str(SN).strip(),ips,str(MAC))




def getRecord(files):
	SN=''
	f = open(files,'r');
	count = 1;
	for line in f:
#		print each line;
		print str(count)+ '---' +line.strip() + "   \t" + str(count);
		count = count + 1;
		if not line:
			break;
	Number = input("Please intput your choose:\n eg. 1\n")
	f.close();
	try:
		f = open(files,'r');
		if int(Number) == 0:
			getRecord(files)
		SN=f.readlines()[int(Number)-1].strip().split('=')[0];	
		f.close();
	except:
		print "	error!!	please type "
		SN=''
		getRecord(files)
#	print SN;
	return SN;


def SNgetIP(files,SN):
	f = open(files,'r')
	for line in f:
		if not line:
			break;
		if SN == line.split('=')[0].strip():
			return line.split('=')[1];

def ConnectFfile():
        SN=getRecord('list');
	ip=SNgetIP('list',SN);
	print ip
	connectDevice(ip)

def usage():
	print "\t\t\t========================================================="
	print "\t\t\t|使用方式：python run_win.py list 使用为读取已连接的设备|"
	print "\t\t\t|          python run_win.py new  使用为建立新连接	|"
	print "\t\t\t========================================================="

def optChoose():
	for opt_name in sys.argv:
		if opt_name == 'list':
			ConnectFfile();
			exit()
		elif opt_name == 'new':
			newDevices()
			exit()
		elif opt_name == 'help':
			usage()
		else:
			usage()

def main():
	optChoose()


if __name__ == '__main__':
	main()
