# Уменьшение размера для будующего образа RedOS Murom

- Определяем имя LV для подкачки:
```
$ lvs
LV   VG       Attr       LSize
root ro_redos -wi-ao---- <12,50g
swap ro_redos -wi-ao----   1,50g
```

- Отключаем том подкачки:
```
$ swapoff /dev/ro_redos/swap
```

- Уменьшаем размер подкачки на 1 GiB:
```
$ lvresize -L-1GiB /dev/ro_redos/swap
```

- Форматируем раздел подкачки:
```
$ mkswap /dev/ro_redos/swap
```

- Включаем том подкачки:
```
$ swapon /dev/volgroup0/swap_lv1
```

- Проверяем новый размер подкачки:
```
$ free -h
```
