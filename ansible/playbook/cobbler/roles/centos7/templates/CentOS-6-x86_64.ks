install 
url --url=http://{{ inventory_hostname }}/cobbler/ks_mirror/CentOS-6-x86_64/
lang en_US.UTF-8 
keyboard us 
network --onboot yes --device eth0 --bootproto dhcp --noipv6
rootpw 123456
authconfig --enableshadow --enablemd5 
selinux --disabled 
firewall --disabled 
timezone --utc Asia/Shanghai 
bootloader --location=mbr --driveorder=sda 
firstboot --disabled 
logging --level=info 
zerombr 
clearpart --all 
part /boot --fstype=ext4 --size=100 --asprimary
part swap --size=512
part / --fstype=ext4 --size=1 --grow --asprimary
unsupported_hardware
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
