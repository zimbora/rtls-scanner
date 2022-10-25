
# How to run your docker program

x. Install docker
 [link](https://docs.docker.com/engine/install/)

 >> apt-get install docker.io

x. get image
  >> docker pull zimbora/rtls-scanner-xx

  xx can be:
    - armv7
    - amd64

  for other architectures contact support

x. create dir
  >> mkdir /opt/app
  >> mkdir /opt/app/rtls-scanner

x. move into it
  >> cd /opt/app/rtls-scanner

x. create file docker_run.sh
  >> touch docker_run.sh

x. make it runnable
  >> chmod u+x docker_run.sh

x. add the following commands
  >> nano docker_run.sh

    #!/bin/bash
    docker stop rtls-scanner
    docker rm rtls-scanner
    docker run --privileged \
      --volume /var/run/dbus:/var/run/dbus  \
      --restart unless-stopped \
      --name rtls-scanner \
      -td zimbora/rtls-scanner-armv7
    docker logs -f rtls-scanner

x. run container
>> ./docker_run.sh
