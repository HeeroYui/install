when you write rm -rf * on your home!!!
----------------------------------------


1: Dump jour journal of your ext4 hdd (before stop computer)
```
debugfs -R "dump <8> /PATH/journal.copy" /dev/DEVICE 
```

2: Umount your partition

3: Get the timestamp of the last time you want data history
```
date -d "-3day" +%s
```

4: Create a new directory to store data
```
mkdir your_folder
```

5: Extract data:
```
ext4magic /dev/nvme0n1p5 -j /tmp/JOURNAL.copy -a `date -d "-3day" +%s` -M -d your_folder/
```

