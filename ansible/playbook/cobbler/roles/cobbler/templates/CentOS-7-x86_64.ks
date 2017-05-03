install 
url --url=http://{{ inventory_hostname }}/cobbler/ks_mirror/CentOS-7-x86_64/
lang en_US.UTF-8 
keyboard --vckeymap=us --xlayouts='us'
network  --bootproto=dhcp --device=enp0s3 --ipv6=auto --activate
rootpw 123456
authconfig --enableshadow --enablemd5 
selinux --disabled 
firewall --disabled 
timezone Asia/Shanghai --isUtc
bootloader --location=mbr --boot-drive=sda
firstboot --disabled 
logging --level=info 
zerombr 
clearpart --all
clearpart --none --initlabel
autopart --type=lvm
reboot
%packages
@base
@core
@hardware-monitoring
@development
%end
%post
echo "nameserver 210.73.88.1" >> /etc/resolv.conf

mkdir -p /application/tools
mkdir -p /server/{backup,scripts}
touch "Pls keep this server clean."

useradd simple
echo "123456"|passwd --stdin simple

echo "oldboy ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

 
/bin/cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
%end
