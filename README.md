# NerdyMonitorDaemon

## Installation
Installation of the NerdyGadgets monitor daemon application is very simple.
First, clone the Git repository using the following command:
```bash
$ git clone https://github.com/RafaelMuijsert/NerdyMonitorDaemon.git
```
Navigate into the project root directory
```bash
$ cd NerdyMonitorDaemon
```
Install the required dependencies and install the application
```bash
$ sudo make install
```

## Configuration
The configuration file is located in `/etc/nmd/config.ini`
Be sure to edit this configuration with your specific database configuration

## Enabling and running the daemon
After the daemon has been installed, the nmd service can now be configured using systemd.
To enable the daemon on startup, use the following command:
```bash
sudo systemctl enable nmd
```
To start the daemon once, use the following command:
```bash
sudo systemctl start nmd
```
To view the daemon status, use the following command:
```bash
sudo systemctl status nmd
```
