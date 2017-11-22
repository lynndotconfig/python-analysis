import psutil

# cpu info
print "%s CPU Info: %s" %('-' * 10, '-' * 10)
print "cpu_time:", psutil.cpu_times()
print "cpu_count:", psutil.cpu_count()
print "cpu_count(logical):", psutil.cpu_count(logical=False)
print "cpu_stats:", psutil.cpu_stats()
print "cpu_freq:", psutil.cpu_freq()


print "cpu_percent:"
for x in range(3):
	print psutil.cpu_percent(interval=1)


print "cpu_percent(percpu):"
for x in range(3):
	print psutil.cpu_percent(interval=1, percpu=True)


print "cpu_times_percent(percpu):"
for x in range(3):
	print psutil.cpu_times_percent(interval=1, percpu=True)


# memory
print "%s Memory Info: %s" %('-' * 10, '-' * 10)
print "virtual_memory:", psutil.virtual_memory()
print "swap_memory:", psutil.swap_memory()


# disk
print "%s Disk Info: %s" %('-' * 10, '-' * 10)
print "disk_partitions:", psutil.disk_partitions()
print "disk_usage:", psutil.disk_usage('/')
print "disk_io_counters:", psutil.disk_io_counters(perdisk=False)

# network
print "%s Network Info: %s" %('-' * 10, '-' * 10)
print "net_io_counters:", psutil.net_io_counters(pernic=True)
print "net_connections:", psutil.net_connections()
print "net_if_addrs:", psutil.net_if_addrs()
print "net_if_stats:", psutil.net_if_stats()

# sensors
print "%s Sensors Info: %s" %('-' * 10, '-' * 10)
print "sensors_temperatures:", psutil.sensors_temperatures()
print "sensors_fans:", psutil.sensors_fans()
print "sensors_battery:", psutil.sensors_battery()

# other system info
print "%s Other System Info: %s" %('-' * 10, '-' * 10)
print "users:", psutil.users()
print "boot_time:", psutil.boot_time()

# process management
print "%s Process Management Info: %s" %('-' * 10, '-' * 10)
print "pids:", psutil.pids()
print "process(pid=304):"
pro = psutil.Process(304)
print "name: ", pro.name()
print "exe:", pro.exe()
print "cwd:", pro.cwd()
print "cmdline: ", pro.cmdline()
print "pid: ", pro.pid()
print "ppid: ", pro.ppid()
print "parent:", pro.parent()
print "children:", pro.children()
print "status: ", pro.status()
print "username: ", pro.username()
print "create_time: ", pro.create_time()
print "terminal: ", pro.terminal()
print "uids: ", pro.uids()
print "gids: ", pro.gids()
print "cpu_times: ", pro.cpu_times()
print "cpu_percent: ", pro.cpu_percent(interval=1)
print "cpu_affinity: ", pro.cpu_affinity()
print "cpu_num: ", pro.cpu_num()
print "memory_info: ", pro.memory_info()
print "memory_full_info: ", pro.memory_full_info()
print "memory_percent: ", pro.memory_percent()
print "memory_maps: ", pro.memory_maps()
print "io_counters: ", pro.io_counters()
print "open_files: ", pro.open_files()
print "connections: ", pro.connections()
print "num_threads: ", pro.num_threads()
print "num_fds: ", pro.num_fds()
print "threads: ", pro.threads()




