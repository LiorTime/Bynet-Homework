#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-------------------------
import hashlib
#-------------------------


# In[32]:


def hash_file(filename): #This function returns the SHA-1 hash of the file passed into it
    h = hashlib.md5() # make a hash object in md5 algorithm
    with open(filename,'rb') as file: # open file for reading in binary mode
        chunk = 0
        while chunk != b'': # loop till the end of the file
           # read only 1024 bytes at a time
            chunk = file.read(1024) # read only 1024 bytes at a time
            h.update(chunk)
    return h.hexdigest() # return the hex representation of digest


# In[33]:


hMessage = hash_file("testfile.txt")
print(hMessage)


# In[ ]:




