# supergelf
GELF logger for supervisor that actually works

## Usage
Until I do something more advanced just clone the repo somewhere and set up a logger to use it

```sh
cd /opt
git clone git@github.com:ev0rtex/supergelf.git
vim /etc/supervisor/conf.d/logging.conf
```

```
[eventlistener:supergelf]
command = /opt/supergelf/log.py
environment = GRAYLOG_HOST=graylog.mysite.com,GRAYLOG_PORT=12201
events = PROCESS_STATE
buffer_size = 1024
```
