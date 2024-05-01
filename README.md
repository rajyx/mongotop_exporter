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

Usage examples
---------------

- Using python files directly:
  ```
  python3 mongotop_exporter.py -mh <mongo_host> -mp <mongo_port> -u <user> -p <pwd>
  ``` 
  Also, you can use long cli keys
  ```
  python3 mongotop_exporter.py --mongo_host <mongo_host> --mongo_port <mongo_port> --username <user> --password <password>
  ```
- Run exporter in docker container:  
  Build docker image
  ```
  docker build ./ -t <image>:<tag>
  ```
  And then, run container with exporter
  ```
  docker run -d -p <host_port>:<container_port> --name <container_name> <image>:<tag> -mh <mongo_host> -mp <mongo_port> -u <user> -p <pwd>
  ```


Metrics url
---------------
Mongotop exporter publishes metrics by /metrics endpoint