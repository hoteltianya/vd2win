#! /usr/bin/python3
# 用于在Linux获取多个盘的smart信息
import subprocess

def get_disk_smartinfo(disk):
    smartlist = {}
    cmd = 'smartctl -a ' + disk
    smartinfo = subprocess.getoutput(cmd).split('\n')
    for i in smartinfo:
        if 'WDC' in i or 'TOSHIBA' in i:
            break
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

def get_disklist():
    cmd = "lsscsi | grep SSD |awk -F ' ' '{print $NF}'"
    disklist = subprocess.getoutput(cmd).split('\n')
    return disklist
def check_smart(disklist):
    for disk in disklist:
        print(get_disk_smartinfo(disk))

check_smart(get_disklist())