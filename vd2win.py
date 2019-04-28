import subprocess
import sys


def ls_disk():
    ls = []
    disk_list = subprocess.Popen('smartctl --scan', stdout=subprocess.PIPE).stdout.readlines()
    for disk in disk_list:
        ls.append(str(disk.split()[0], encoding="utf-8"))
    return ls

def get_disk_smartinfo(disk = '/dev/sdc'):
    smartlist = {}
    cmd = 'smartctl -a ' + disk
    smartinfo = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.readlines()
    model = smartinfo[5].split()
    if 'SSD' not in str(model[-1], encoding="utf-8"):
        return None
    sn = smartinfo[6].split()
    if sn[0] == b'Serial':
        smartlist['SN'] = sn[-1]
    ac = smartinfo[66].split()
    if ac[0] == b'172':
        smartlist['172'] = int(ac[-1])
    badblock = smartinfo[54].split()
    if badblock[0] == b'5':
        smartlist['05'] = int(badblock[-1])
    # 返回smart信息的字典
    print (smartlist)
    return smartlist


class Vdbench():
    def __init__(self, vd_path=''):
        self.vd_path = vd_path
        self.lun_list = ['\\.\PHYSICALDRIVE1', '\\.\PHYSICALDRIVE2']

    def get_lun_list(self):
        pass

    def creat_vd_config(self):
        sd=''
        i = 1
        for lun in self.lun_list:
            sd = sd + 'sd=sd%d,lun=%s \n' % (i, lun)
            i = i+1

        config = '''sd=default,threads=16,openflags=o_direct
%swd=wd1,sd=sd*,xfersize=1M,rdpct=0,seekpct=0
rd=run1,wd=wd1,iorate=max,elapsed=600,interval=1
        ''' %sd
        with open('vdconfig', 'w') as f :
            f.write(config)

    def exec_vdbench(self):
        cmd = self.vd_path + ' -f vdconfig -o result'
        subprocess.Popen(cmd)

    def check_reult(self):
        # with open('result/') as f :
        #     if 'error' in f.read():
        #         print('exec fail, please check disk')
        #         sys.exit()
        disk_list = ls_disk()
        good_list = []
        bad_list_05 = []
        bad_list_172 = []
        for disk in disk_list:
            smartinfo = get_disk_smartinfo(disk)
            if smartinfo:
                if '05' in smartinfo.keys() and smartinfo['05'] == 0:
                    if '172' in smartinfo.keys() and smartinfo['172'] == 0:
                        good_list.append(smartinfo['SN'])
                    else:
                        bad_list_172.append(smartinfo['SN'])
                else:
                    bad_list_05.append(smartinfo['SN'])
        for good in good_list:
            print('good list :\n \033[5;37;40m %s \033[0m'% good)
        for bad_05 in bad_list_05:
            print('bad list 05:\n \033[5;37;41m %s \033[0m'% bad_05)
        for bad_172 in bad_list_172:
            print('bad list 172:\n \033[5;34;43m %s \033[0m' % bad_172)




a =Vdbench()
a.check_reult()
# get_disk_smartinfo('/dev/sdc')







