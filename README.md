# script.service.snapcast-client


Service that mute Snapcast client when Kodi is playing and a basic GUI to mute/unmute it.

Thanks to [frafall](https://github.com/frafall/service.snapcast) for is original work for LibreELEC.

Since release 0.2.0, this plugin doesn't stop systemd unit file, it will mute snapclient for better interoperability.

## Features

* Mute/Unmute from Kodi interface
* Optionally autostart snapcast on Kodi startup
* Optionally autostart snapcast when Kodi stop playing
* Optionally sync volume from Kodi to snapcast


* No dependencies on LibreELEC
* Python 3

## Install

### From repository

Add Rafaneto repository by installing this zip file [repository.rafaneto-0.0.2.zip](https://rimeno.github.io/repo/zips/repository.rafaneto/repository.rafaneto-0.0.2.zip)
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

**This addon will not install Snapcast server nor Snapcast client.**

You have to setup your snapclient installation, with the kodi user or by sharing a pulse daemon.
