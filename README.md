Mongotop exporter
===================================
Simple exporter of average metric times from mongodb top command

Permissions
---------------
Mongodb user should have the following rights:

```
  {
     "role":"clusterMonitor",
     "db":"admin"
  },
  {
     "role":"read",
     "db":"local"
  }
```

CLI Arguments
---------------

- -h, --help, show help message and exit
- --mongo_host MONGO_HOST, -mh MONGO_HOST mongo db host
- --mongo_port MONGO_PORT, -mp MONGO_PORT mongo db port
- --username USERNAME, -u USERNAME mongo user name
- --password PASSWORD, -p PASSWORD mongo user pwd
- --limit LIMIT, -l LIMIT limit output collections quantity

Usage examples
---------------

- Using python files directly:
  ```
  python3 mongotop_exporter.py -mh <mongo_host> -mp <mongo_port> -u <user> -p <pwd> -l <collections_in_top>
  ``` 
  Also, you can use long cli keys
  ```
  python3 mongotop_exporter.py --mongo_host <mongo_host> --mongo_port <mongo_port> --username <user> --password <password> --limit <collections_in_top>
  ```
- Run exporter in docker container:  
  Build docker image
  ```
  docker build ./ -t <image>:<tag>
  ```
  And then, run container with exporter
  ```
  docker run -d -p <host_port>:<container_port> --name <container_name> <image>:<tag> -mh <mongo_host> -mp <mongo_port> -u <user> -p <pwd> -l <collections_in_top>
  ```

Metrics url
---------------
Mongotop exporter publishes metrics by /metrics endpoint