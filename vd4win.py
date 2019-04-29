import subprocess
import sys



def ls_disk():
    ls = []
    disk_list = subprocess.Popen('smartctl --scan', stdout=subprocess.PIPE).stdout.readlines()
    for disk in disk_list:
        ls.append(str(disk.split()[0], encoding="utf-8"))
    return ls

def get_disk_smartinfo(disk):
    smartlist = {}
    cmd = 'smartctl -a ' + disk
    smartinfo = subprocess.getoutput(cmd).split('\n')
    # model = smartinfo[5].split()
    for i in smartinfo:
        if 'WDC' in i or 'TOSHIBA' in i:
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
            if 'Firmware Version' in i:
                smartlist['FW'] = i.split()[-1]
    # print (smartlist)
    return smartlist


class Vdbench():
    def __init__(self, vd_path=''):
        self.vd_path = vd_path
        self.lun_list = ['\\.\PHYSICALDRIVE1', '\\.\PHYSICALDRIVE2']

    def get_lun_list(self):
        self.lun_list = []
        cmd = 'wmic diskdrive'
        diskinfo = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read()
        # print(diskinfo)
        # diskinfo = str(diskinfo,encoding="utf-8")
        disk = diskinfo.split(b'\n')
        for i in range(len(disk)):
            #根据容量检查，删除指定容量的盘符
            if '磁盘驱动器' in str(disk[i], encoding='ANSI') and disk[i].split()[-9] != b'1000202273280':
                self.lun_list.append(str(disk[i].split()[-19],encoding='ANSI'))


    def creat_vd_config(self):
        sd=''
        i = 1
        for lun in self.lun_list:
            sd = sd + 'sd=sd%d,lun=%s \n' % (i, lun)
            i = i+1

        config = '''sd=default,threads=16,openflags=directio
%swd=wd1,sd=sd*,xfersize=1M,rdpct=0,seekpct=0
rd=run1,wd=wd1,iorate=max,elapsed=6,interval=1
        ''' %sd

        with open('vdconfig', 'w') as f :
            f.write(config)

    def exec_vdbench(self):
        cmd = self.vd_path + ' -f vdconfig -o result'
        subprocess.run(cmd)
        # os.popen(cmd)
    def check_reult(self):
        with open('result/errorlog.html') as f:
            print(len(f.readlines()))
            if  len(f.readlines())>4:
                print('exec fail, please check disk')
                sys.exit()
        disk_list = ls_disk()
        print(disk_list)
        good_list = []
        bad_list = []
        for disk in disk_list:
            smartinfo = get_disk_smartinfo(disk)
            print(smartinfo)
            if smartinfo:
                if smartinfo['05'] == 0 and smartinfo['172'] == 0 and smartinfo['171'] == 0:
                    good_list.append(smartinfo['SN'])
                else:
                    bad_list.append(smartinfo['SN'])
        for good in good_list:
            print('good list :\n \033[5;37;40m %s \033[0m'% good)
        for bad in bad_list:
            print('bad list :\n \033[5;31;40m %s \033[0m'% bad)
    def run(self):
        self.get_lun_list()
        self.creat_vd_config()
        self.exec_vdbench()
        self.check_reult()

a = Vdbench(r'C:\Users\sumu\Desktop\vd\vdbench50403\vdbench.bat')
a.run()









