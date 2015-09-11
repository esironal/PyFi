# Imports
import re
import subprocess
import time
import os.path
# Version
version = 1.0
# Starting message
print '\033[92m' + "Starting " + '\033[0m' + '\033[94m' + 'PyFi' + '\033[0m' + ' - Version: ' + str(version)
# Console commmand
command = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport', 'scan']
# Do the proccess
print('\033[94m' + 'Starting..' + '\033[0m')
print('\033[94m' + 'Checking files..' + '\033[0m')
if not os.path.isfile("pyfi_log.txt"):
	print('\033[91m' + 'Log file does not exist, creating..' + '\033[0m')
	open("pyfi_log.txt", "w+")
# Store the BSSID list here
bssid_list = []
# Store the JSON strings here
router_json_list = []
# Store the Regex pattern here
regex_pattern_info = '([a-zA-Z0-9-]+) ([a-z0-9][a-z0-9]:[a-z0-9][a-z0-9]:[a-z0-9][a-z0-9]:[a-z0-9][a-z0-9]:[a-z0-9][a-z0-9]:[a-z0-9][a-z0-9])'
print('\033[92m' + 'Scanning..' + '\033[0m')
while True:
	# Execute the airport scan
	proc = subprocess.Popen(command, stdout=subprocess.PIPE)
	tmp = proc.stdout.readlines()
	for line in tmp:
		# Get SSID & BSSID
		for m in re.finditer(regex_pattern_info, line):
			router_ssid = m.group(1)
			router_bssid = m.group(2)
			# If we've not already picked it up
			if router_bssid not in bssid_list:
				# Get security
				router_security = re.split('GB |-- |\*|\n', line)[1]
				# Build JSON string
				router_json_string = '{"ssid":"' + router_ssid + '","bssid":"' + router_bssid + '","encryption":"' + router_security + '"}'
				if router_json_string not in open('pyfi_log.txt', 'w+').read():
					# Add to router BSSID list
					bssid_list.append(router_bssid)
					# Add to list
					router_json_list.append(router_json_string)
					# Write line to file
					write_file = open('pyfi_log.txt','w+')
					write_file.write(router_json_string + "\n")
					write_file.close()
					# Tell user
					print('\033[92m' + router_ssid + ' - ' + router_bssid + '\033[0m')
	# Do this every 10 seconds, save resources
	time.sleep(10)