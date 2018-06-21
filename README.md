# Rubbish
Reversibly remove files from a Linux filesystem  

## Features
* Remove files and save them in a special directory  
* Restore files back to their original location  
* List files in the bin and show its size  

## Usage
```
$ ./rubbish put a b c  
3 out of 3 files moved to bin.    

$ ./rubbish list  
Size: 4,0K  
1: /home/user/scripts/rubbish/a (DELETED AT 2018-06-21 17:24:27)  
2: /home/user/scripts/rubbish/b (DELETED AT 2018-06-21 17:24:27)  
3: /home/user/scripts/rubbish/c (DELETED AT 2018-06-21 17:24:27)   

$ ./rubbish restore 1 2 3  
Restored 3 out of 3 files.

# Or alternatively  

$ ./rubbish restore /home/user/scripts/rubbish/a /home/user/scripts/rubbish/b  
Restored 2 out of 2 files.
```  

## TODO
- [ ] Configuration file and additional functionality like bin max size
