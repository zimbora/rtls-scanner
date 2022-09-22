
# Network Scanner

  Scan network devices and send info to inloc server

## run
  >> sudo python3 index.py

## Operation mode

  Service uses ssid and bssid to get map id, with inloc cloud help

  If map id is found, it will listen for arp requests associating ip address to mac address.
  If a new association is detected it will send the new info to the inloc cloud

  This association is important on situations that mobile apps cannot get mac address from the device, mainly on iphone devices

## docker

  check DockerInstructions file
