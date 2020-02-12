import platform

def get_sysinfo():
    info = {}
    
    #basic
    info["architecture"] = platform.architecture()[0]
    info["machine"] = platform.machine()
    info["node"] = platform.node()
    info["system"] = platform.system()
    
    #distro
    dist = platform.dist()
    info["dist"] = " ".join(x for x in dist)
    
    #cpuinfo
    with open("/proc/cpuinfo", "r") as f:
        cpuInfo = f.readlines()
    info["cpuinfo"] = [x.strip().split(":")[1] for x in cpuInfo if "model name" in x]

    #memory
    with open("/proc/meminfo", "r") as f:
        memInfo = f.readlines()
    info["memTotal"] = memInfo[0].strip()\
        .replace("MemTotal:        ", "").replace(" kB", "")
    info["memFree"] = memInfo[1].strip()\
        .replace("MemFree:          ", "").replace(" kB", "")

    #uptime
    with open("/proc/uptime") as f:
        uptime = f.read().split(" ")[0].strip()
    uptime = int(float(uptime))
    info["uptime"] = str(uptime)

    return info