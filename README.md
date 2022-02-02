# script.service.snapcast-client


Service that stop Snapcast client when Kodi is playing and a
basic GUI to start/stop it. It depends on a systemd unit file in
Kodi user space, `snapclient.service`.

Thanks to [frafall](https://github.com/frafall/service.snapcast) for is original work for LibreELEC.

## Features

* Start/Stop from Kodi interface
* Optionally autostart snapcast on Kodi startup
* Optionally autostart snapcast when Kodi stop playing
* Optionally sync volume from Kodi to snapcast



* No dependencies on LibreELEC
* Dependency on systemd
* Python 3

## Install

### From repository

Add Rafaneto repository by installing this zip file [repository.rafaneto-0.0.2.zip](https://rimeno.github.io/repository.rafaneto-0.0.2.zip)
and then search "snapcast client".

### Build

Install necessary dependencies for this addon.

* [script.module.snapcast](https://github.com/rimeno/script.module.snapcast),

To make the package (in your TMPDIR) :

```
git clone https://github.com/rimeno/script.service.snapcast-client
cd script.service.snapcast-client
./make.sh
```

## Notes

This addon will not install Snapcast server nor Snapcast client.
You have to setup your snapclient installation with systemd in userspace and it should
run with the Kodi user.

For instance, if the home directory of your Kodi user is `/home/kodi` and you have configured
snapclient in `/home/kodi/.config/snapclient`, you could use this service for your 
`/home/kodi/.config/systemd/user/snapclient.service`

```INI
[Unit]
Description=Snapcast client
Documentation=man:snapclient(1)
Wants=avahi-daemon.service
After=network.target time-sync.target sound.target avahi-daemon.service pulseaudio.service

[Service]
EnvironmentFile=-/home/kodi/.config/snapclient
ExecStart=/usr/bin/snapclient $SNAPCLIENT_OPTS
# very noisy on stdout
StandardOutput=null
Restart=on-failure

[Install]
WantedBy=default.target
```
