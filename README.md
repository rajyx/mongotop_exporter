Mongotop exporter
===================================
Simple exporter of average metric times from mongodb top

Common usage ways
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
  docker run -d -p <host>:<host_port>:<container_port> <image>:<tag> -mh <mongo_host> -mp <mongo_port> -u <user> -p <pwd>
  ```
  Host in -p option may be empty or 0.0.0.0,  
  if you want exporter to listen any machine from current network