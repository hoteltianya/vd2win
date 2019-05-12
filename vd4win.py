import subprocess
import sys
import os

def ls_disk():
    ls = []
    disk_list = subprocess.getoutput('smartctl --scan').split('\n')
    for disk in disk_list:
        ls.append(disk.split()[0])
    return ls

def get_disk_smartinfo(disk):
    smartlist = {}
    cmd = 'smartctl -a ' + disk
    smartinfo = subprocess.getoutput(cmd).split('\n')
    for i in smartinfo:
        if 'WDC' in i or 'TOSHIBA' in i or 'Virtual' in i:
            return None
        else:
            if 'Serial' in i:
                snlist = i.split()
                smartlist['SN'] = snlist[-1]
            if '172 Unknown_Attribute' in i:
                smartlist['172'] = int(i.split()[-1])
            if '5 Reallocated_Sector_Ct' in i:
                smartlist['05'] = int(i.split()[-1])
            if '171 Unknown_Attribute' in i:
                smartlist['171'] = int(i.split()[-1])
            if '160 Unknown_Attribute' in i:
                smartlist['160'] = int(i.split()[-1])
            if 'Firmware Version' in i:
                smartlist['FW'] = i.split()[-1]
    return smartlist


class Vdbench():
    def __init__(self):
        path = os.getcwd()
        self.vd_path = path + '\\vdbench50403\\vdbench.bat'
        self.lun_list = []

    def get_lun_list(self):
        cmd = 'wmic DISKDRIVE get deviceid,Caption,size'
        diskinfo = subprocess.getoutput(cmd)

        for disk in diskinfo.split('\n'):
            if 'SSDC' in disk or 'SSDE' in disk or 'GG0' in disk or 'SC36' in disk or 'JEYI' in disk or 'AMST' in disk:
                # print(disk.split())
                self.lun_list.append(disk.split()[-2])

    def creat_vd_config(self):
        sd = ''
        i = 1
        for lun in self.lun_list:
            sd = sd + 'sd=sd%d,lun=%s \n' % (i, lun)
            i = i+1
        config = '''data_errors=1
hd=localhost,jvms=8
sd=default,threads=16,openflags=directio
%swd=wd1,sd=sd*,xfersize=1M,rdpct=0,seekpct=0
rd=run1,wd=wd1,iorate=max,elapsed=600,interval=1
        ''' %sd
        with open('vdconfig', 'w') as f :
            f.write(config)

    def exec_vdbench(self):
        cmd = self.vd_path + ' -f vdconfig -o result'
        self.vdlog = subprocess.getoutput(cmd)

    def check_reult(self):
        with open('result/errorlog.html') as f:
            print(len(f.readlines()))
            if  len(f.readlines())>4:
                print('exec fail, please check disk')
                sys.exit()
        disk_list = ls_disk()
        print(disk_list)
        self.good_list = []
        self.bad_list = []
        for disk in disk_list:
            smartinfo = get_disk_smartinfo(disk)
            print(smartinfo)
            if smartinfo:
                if smartinfo['05'] == 0 and smartinfo['172'] == 0 and smartinfo['171'] == 0 and smartinfo['160'] == 0:
                    self.good_list.append(smartinfo['SN'])
                else:
                    self.bad_list.append(smartinfo['SN'])
        for good in self.good_list:
            print('good list :\n \033[5;37;40m %s \033[0m'% good)
        for bad in self.bad_list:
            print('bad list :\n \033[5;31;40m %s \033[0m'% bad)

    def run(self):
        self.get_lun_list()
        self.creat_vd_config()
        self.exec_vdbench()
        self.check_reult()

a = Vdbench()
a.run()









