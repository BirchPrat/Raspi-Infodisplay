import subprocess

class SysStat:
    """Class for Systemstats"""
    def get_systemstats(self, light = 'yes'):
        """Shell scripts for system monitoring"""
        if light == 'yes':
            cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"%.1f\", $(NF-0) / 1000}'" 
            temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

            return temp
        else:
            cmd = "hostname -I | cut -d' ' -f1"
            ip_adress = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            cpu_util = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s \", $3,$2,$3*100/$2 }'"
            mem_usage = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
            disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
            cpu_temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

            return [ip_adress, cpu_util, cpu_temp, mem_usage, disk]

    def get_uptime(self):
        """Reading the uptime of the pi from a file""" 
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_days = uptime_seconds/60/60/24

        return round(uptime_days, 2)
    
    def shut_down(self):
        """Shutting down pi"""
        print('Shutdown')
        subprocess.call("sudo shutdown -h now", shell=True)
        
    def reboot(self):
        """Resatrting pi"""
        print('Restart')
        subprocess.call("sudo reboot", shell=True)
        
        
