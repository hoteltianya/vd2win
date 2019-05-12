import time
import subprocess
import wmi
from win32com.client import GetObject

def ls_disk():
    ls = []
    disk_list = subprocess.getoutput('smartctl --scan').split('\n')
    for disk in disk_list:
        ls.append(disk.split()[0])
    return ls

def get_smartinfo():
    disklist = wmi.WMI().Win32_DiskDrive()
    disk_basic = []
    for phydisk in disklist:
        disk_basic.append([phydisk.Caption, phydisk.FirmwareRevision, phydisk.DeviceID, phydisk.SerialNumber,phydisk.PNPDeviceID])
    return disk_basic
    # diskinfo = wmi.WMI().Win32_MSStorageDrive()
    # for info in diskinfo:
    #     print(info)
def get_wmi_smartinfo():
    diskdict = {}
    wmi = GetObject('winmgmts:/root/wmi')
    processes = wmi.ExecQuery('SELECT * FROM MSStorageDriver_ATAPISmartData')
    time.sleep(5)
    # print(processes)
    for process in processes:
        diskdict[process.InstanceName] = process.VendorSpecific
    # print(diskdict)
    return diskdict

# get_smartinfo()
class smartformwin():
    def __init__(self):
        self.diskdict={}

    def get_wmi_disk_basic(self):
        self.wmi_name_vs = get_wmi_smartinfo()
        self.disk_basic = get_smartinfo()
        for disk in self.disk_basic:
            for key in self.wmi_name_vs.keys():
                if disk[4] in key.upper():
                    disk.append(self.wmi_name_vs[key])
            self.diskdict[disk[2]] = disk
        print(self.diskdict)
        # self.wmi_name_vs = get_wmi_smartinfo()




a=smartformwin()
a.get_wmi_disk_basic()
# get_wmi_smartinfo()