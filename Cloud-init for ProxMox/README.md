# Шаблон в ProxMox VE на основе cloud-init образа Ubuntu 20.04

- Скачиваем образ Ubuntu 20.04 на сервере Proxmox
```
wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
```
- Устанавливаем libguestfs-tools
```
sudo apt update -y && sudo apt install libguestfs-tools -y
```
- Ставим в образ агента qemu
```
virt-customize -a focal-server-cloudimg-amd64.img --install qemu-guest-agent
```
- Создаем виртуальную машину с нужными нам параметрами и импортируем диск
```
sudo qm create 9000 --name "ubuntu-2004-cloudinit-template" --memory 1024 --cores 1 --net0 virtio,bridge=vmbr0
sudo qm importdisk 9000 focal-server-cloudimg-amd64.img VM

sudo qm set 9000 --scsihw virtio-scsi-pci --scsi0 /vm/images/9000/vm-9000-disk-0.raw
sudo qm set 9000 --ide2 VM:cloudinit --boot c --bootdisk scsi0 --serial0 socket --vga serial0 --agent 1
sudo qm set 9000 --hotplug disk,network,usb,memory,cpu
```
- Настраиваем Cloud-Init
```
qm set 9000 --ciuser alex  --ipconfig0 ip=192.168.0.250/24,gw=192.168.0.1 --nameserver 192.168.0.1 --searchdomain 192.168.0.1 
```
   - Пароль можно задать через опцию --cipassword 
      - Не забываем задать SSH public key
      - Через веб интерфейс
      - Через опцию --sshkey с укзанием файла
      ```
      qm set 9000 --sshkey sshkey
      ```

- Запускаем нашу виртуальную машину и устанавливаем необходимый нам софт
```
sudo apt install bash-completion, net-tools, qemu-guest-agent
```
- Редактируем файл /etc/cloud/cloud.cfg добавляя установленные нами пакеты
~~~
# Install packages
package_upgrade: true
packages:
 - qemu-quest-agent
 - net-tools
 - bash-completion
~~~
- Преобразовываем нашу машинку в шаблон
```
sudo qm template 9000
```