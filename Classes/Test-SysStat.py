from SysStat import SysStat

pistat = SysStat()

statnow = pistat.get_systemstats()
print(statnow)
statnow = pistat.get_systemstats('no')
print(statnow)

timenow = pistat.get_uptime()
print(timenow)

#pistat.restart()
pistat.shut_down()