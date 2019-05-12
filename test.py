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
    print(processes)
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
    def parise_smart(self):
        self.smartinfolist=[]
        for key in self.diskdict:
            if len(self.diskdict[key]) > 5:
                info = {}
                info['ID'] = key
                info['Model'] = self.diskdict[key][0]
                info['SN'] = self.diskdict[key][3]
                info['FW'] = self.diskdict[key][1]
                A_smart = list(self.diskdict[key][-1])
                del A_smart[0]
                del A_smart[0]
                l = A_smart
                n=12
                A_smarlist = [l[i:i + n] for i in range(0, len(l), n)]
                for A in A_smarlist:
                    print(A)
                    if A[0] == 5:
                        info['05'] = A[5] + 256*A[6]
                    if A[0] ==160:
                        info['160'] = A[5] + 256 * A[6]
                    if A[0] ==171:
                        info['171'] = A[5] + 256 * A[6]
                    if A[0] ==172:
                        info['172'] = A[5] + 256 * A[6]
                self.smartinfolist.append(info)
        print(self.smartinfolist)




a=smartformwin()
a.get_wmi_disk_basic()
a.parise_smart()
# get_wmi_smartinfo()