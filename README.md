# docker-svarog-ci
Docker container with SVAROG build tool and Jenkins CI

## Author and Credits
Roman Pavlyuk <roman.pavlyuk@gmail.com>

http://roman.pavlyuk.lviv.ua/

## Features
This container provides:
* CentOS 7.4+ based OS
* SystemD enabled on the container
* Jenkins CI as a service
* Docker daemon enabled the allows building docker images on the container
* SVAROG package maker (https://github.com/SoftServeInc/svarog)

## Building the Container
**NOTE:** You may skip this section if you just want to run the container
* Change directory to where the ```Dockerfile``` is:
```
cd docker-svarog-ci
```
* Run container build:
```
./build.sh
```
## Run the Container
### Run using systemdock (recommended)
SystemDock (https://github.com/rpavlyuk/systemdock) is the tool to run Docker containers as ```systemd``` service.
* Install systemdock by following the instructions from https://github.com/rpavlyuk/systemdock
* Within project root, change directory to where the systemdock profile is:
```
cd systemdock-svarog-ci/
```
* If you're using RedHat-based OS and installed ```systemdock``` using RPM installer then:
```
sudo make install-rpm clean
```
* Otherwise, use classic method:
```
sudo make install clean
```
* Check configuration file ```/etc/systemdock/containers.d/svarog-ci/config.yml```. Make sure that TCP ports (8080, 50000) are not in-use by any existing processes on the host system
* Enable the service on system boot:
```
sudo systemctl enable systemdock-svarog-ci
```
* Start the service:
```
sudo systemctl start systemdock-svarog-ci
```
* You can monitor service log by calling ```journalctl``` (hit CRTL+C to abort):
```
journalctl -u systemdock-svarog-ci -f
```

### Plain run of the container
You can run the container as any other Docker container:
```
docker run -it --name svarog-ci -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v /var/lib/jenkins:/var/lib/jenkins:rw -v /var/www/repo:/var/www/repo:rw -p 8080:8080 -p 50000:50000 --privileged docker.io/rpavlyuk/c7-svarog-ci
```

## Using the Container
Jenkins CI becomes available as http://<YOUR_HOST_OR_IP:8080/. Default ```admin``` password is auto-generated and can be found as:
```
docker exec svarog-ci cat /var/lib/jenkins/secrets/initialAdminPassword
```

You can use ```docker build ...``` instructions in your Jenkins jobs. It is already configured to run those. However, you should configure Docker Hub or any other registries that require access credentials.
The best way would be to log into registry on the host machine (example for Docker Hub):
```
docker login docker.io
```
And then to copy the config to Jenkins:
```
mkdir -p /var/lib/jenkins/.docker
cp ~/.docker/config.json /var/lib/jenkins/.docker
```
Fix the access permissions:
```
chown -R $(docker exec svarog-ci id -u jenkins | tr -d '\r'):$(docker exec svarog-ci id -g jenkins | tr -d '\r') /var/lib/jenkins/.docker
```

```svarog``` make tool is available either. You can either call it inside Jenkins job or in the container shell. More about **svarog** can be found here: https://github.com/SoftServeInc/svarog

