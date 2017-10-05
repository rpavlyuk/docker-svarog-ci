FROM centos:7
MAINTAINER "Roman Pavlyuk" <roman.pavlyuk@gmail.com>

ENV container docker

RUN yum install -y epel-release

RUN yum update -y

RUN yum install -y less file wget mc

RUN yum install -y java-1.8.0-openjdk.x86_64 java-1.8.0-openjdk-devel.x86_64

RUN yum install -y initscripts net-tools 

### Let's enable systemd on the container
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]

# Prepare for Jenkins
RUN wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat/jenkins.repo
RUN rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key

# Install  svarog repo deinition
COPY svarog-master.repo /etc/yum.repos.d/

# Install SVAROG
RUN yum install -y svarog svarog-ci svarog-repo
VOLUME ["/var/lib/jenkins", "/var/www/repo"]

COPY bash-4.3.42-1.fc21.src.rpm /root
RUN yum install -y texinfo bison ncurses-devel autoconf gettext gcc make automake autoconf sed
RUN rpm -Uvh /root/bash-4.3.42-1.fc21.src.rpm
RUN sed -i '1i%define _unpackaged_files_terminate_build 0' /root/rpmbuild/SPECS/bash.spec
RUN rpmbuild -bb /root/rpmbuild/SPECS/bash.spec
RUN yum localinstall -y /root/rpmbuild/RPMS/x86_64/bash*

RUN systemctl enable jenkins.service

### Kick it off
CMD ["/usr/sbin/init"]
