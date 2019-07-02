#!/bin/python
import telnetlib
import subprocess  
import time
import sys

class bcolors:
    MAGENTA = '\033[95m'
    NC = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'

M = bcolors.MAGENTA
NOC = bcolors.NC
R = bcolors.RED
GR = bcolors.GREEN

hostname = raw_input('[' + M + '+' + NOC + ']' ' Please enter the UUT IP Address: ' + GR + '10.1.1.' + NOC )
print ""
print ('[' + M + '+' + NOC + ']' ' 1  = ' + R + 'NETWORK ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 2  = ' + R + 'BASEBOARD ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 3  = ' + R + 'TEMPSENSOR ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 4  = ' + R + 'VOLTSENSOR ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 5  = ' + R + 'CURRENTSENSOR ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 6  = ' + R + 'POWERSENSOR ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 7  = ' + R + 'DEVICEINFO ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 8  = ' + R + 'SPROM ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 9  = ' + R + 'NCSI ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 10 = ' + R + 'FLASH ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 11 = ' + R + 'GPIO ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 12 = ' + R + 'PMBUS ' + NOC)
print ('[' + M + '+' + NOC + ']' ' 13 = ' + R + 'MODULE LEARN ALL ' + NOC)
print ""
testo = raw_input('[' + M + '+' + NOC + ']' ' Please Select your Test ID : ' )

#1
def network():
    #select_platform = raw_input('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Please Select the UUT Platform eg. [ ' + GR + 'S3X60M5' + NOC +' ] [ '+ GR  +'C480M5' + NOC +' ] [ '+ GR + 'C240M5' + NOC +' ] [ '+ GR +'C220M5'+ NOC +' ]: ')



    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run network\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Network test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

#2
def baseboard():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    #tn.set_debuglevel(5)
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run baseboard\n")
    time.sleep (6.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Baseboard test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\r")
    tn.write("exit\n")
    #tn.close()
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

#3
def tempsensor():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run tempsensor\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Tempsensor test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')


#4
def voltsensor():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run voltsensor\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Voltsensor test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

#5
def currentsensor():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run currentsensor\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Current Sensor test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("")

#6
def powersensor():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run powersensor\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Power Sensor test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

#7
def deviceinfo():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run deviceinfo\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Device Info test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

#8
def sprom():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run sprom\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Sprom test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')


#9
def ncsi():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run ncsi\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' NCSI test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

#10
def flash_flash_test():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run flash flash_test\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Flash test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

#11
def gpio():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run gpio\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' GPIO test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

#12
def pmbus():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("run pmbus\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Pmbus test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

def module_learn_all():

    bm = subprocess.Popen(["grep", 'Bmc_diag =' , "/usr/kcsdist/src/UCS/UCS_SEQUENCE/RACK/PLUMAS_1U/SYSFT/plumas_1u_sysft_software.cfg"], stdout=subprocess.PIPE)
    head = subprocess.Popen(["head" , "-n1"], stdin=bm.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", '{gsub(/,/, "");print $3}'], 
                           stdin=head.stdout, 
                           stdout=subprocess.PIPE,
                           )


    endOfPipe = awk.stdout
    for line in endOfPipe:  
        di = line.strip()


    user = ("root")
    tn = telnetlib.Telnet('10.1.1.' + hostname)

    tn.read_until("login: ")
    print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write(user + "\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

    tn.write("\n")
    tn.write("cat /proc/nuova/gpio/fm_bios_post_cmplt\n")
    tn.read_until("1")
    print ('[' + M + '+' + NOC + ']' ' Power On Self Test Completed.\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    print ('[' + M + '+' + NOC + ']' ' Checking UUT Power.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("blade-power status | grep Power-State")
    tn.read_until("Power-State:                 [ on ]", 3) 
    print ('[' + M + '+' + NOC + ']' ' UUT is in power on State. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("\n")
    tn.read_until("]$")
    tn.write("\n")
    print ('[' + M + '+' + NOC + ']' ' Changing location to binray directory \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Downloading the BMC DIAG Image to the UUT.  \t [ ' + GR + 'OK' + NOC +' ]')
    tn.write('cd /bin && tftp -gr ' + di  + ' 10.1.1.1' '\n')
    time.sleep (10.0)
    tn.read_until(']$')
    print ('[' + M + '+' + NOC + ']' ' Image Downloaded Complete. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("chmod 777 " + di + "\n")
    print ('[' + M + '+' + NOC + ']' ' Image Executed. \t\t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("./" + di +"\n")
    time.sleep (5.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' BMC DIAG Shell Received. \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (10.0)
    tn.read_until('%', 9)
    print ('[' + M + '+' + NOC + ']' ' Executed learn Modules all Command. \t\t [ ' + GR + 'OK' + NOC +' ]')
    #tn.read_until(' %')
    tn.write("verbosity enable verbose\n")
    tn.read_until('%', 4)
    print ('[' + M + '+' + NOC + ']' ' Verbose has been Enabled \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.write("module learn all\n")
    time.sleep (4.0)
    tn.read_until('%', 5)
    print ('[' + M + '+' + NOC + ']' ' Pmbus test executed succsessfully!  \t\t [ ' + GR + 'OK' + NOC +' ]')
    print ("----------------------------------------------------------------------------------------------------------")
    print ("")
    tn.write("exit\n")
    tn.write("exit\n")
    print tn.read_all()
    print ("")
    print ("----------------------------------------------------------------------------------------------------------")
    print ('[' + M + '+' + NOC + ']' ' Exited the UUT. \t \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
    print ('[' + M + '+' + NOC + ']' ' Done. \t \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

if testo == "1":
    network()
elif testo == "2":
    baseboard()
elif testo == "3":
    tempsensor()
elif testo == "4":
    voltsensor()
elif testo == "5":
    currentsensor()
elif testo == "6":
    powersensor()
elif testo == "7":
    deviceinfo()
elif testo == "8":
    sprom()
elif testo == "9":
    ncsi()
elif testo == "10":
    flash_flash_test()
elif testo == "11":
    gpio()
elif testo == "12":
    pmbus()
elif testo == "13":
    module_learn_all()
else:
    print "Wrong selection!"
    sys.exit()

