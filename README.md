# puppeteer

Simple puppetdb wrapper, written in python

## Examples
* Get the list of all nodes:
```
python puppeteer.py --list
```

* Get all the nodes running Centos 6.5 and Puppet 3.6.2
```
python puppeteer.py -f operatingsystem=CentOS,operatingsystemrelease=6.5,puppetversion=3.6.2
```

* Get the list of Out-Of-Sync nodes, which have not sent a report in the last 60 minutes:
```
python puppeteer.py -o 60
```

* Get the free swap of all hosts:
```
python puppeteer.py -f swapfree
```
