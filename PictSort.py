import os
import hashlib
import glob
import sys
import datetime
import shutil
import logging

logformatter='%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(filename='run.log',format=logformatter,level=logging.DEBUG)

filelist={}

def checkDir(path0):
    picfiles=glob.glob(os.path.join(path0,"*"))
    for fl in picfiles:
        if os.path.isdir(fl):
            checkDir(fl) #recursively check sub directory
            #if directory is empty,remove this
            tmplist=glob.glob(os.path.join(fl,'*'))
            if len(tmplist)==0:
                #shutil.rmtree(fl)
                logging.info("Directory empty "+fl)
            continue
        #
        h=hashlib.new('MD5')
        bindata=[]
        with open(fl,'rb') as f:
            bindata=f.read()
        h.update(bindata)
        hashhex=h.hexdigest()
        print(fl,datetime.datetime.fromtimestamp(os.path.getmtime(fl)),hashhex)
        if hashhex not in filelist.keys():
            filelist[hashhex]=[os.path.getmtime(fl),fl]
        else:
            print('Duplicate file '+fl,end='')
            delfile=''
            if os.path.getmtime(fl) < (filelist[hashhex][0]-10):
                #found file is accessed previously
                print(" is older than "+filelist[hashhex][1],end='')
                delfile=filelist[hashhex][1]
                filelist[hashhex]=[os.path.getmtime(fl),fl]
            else:
                #found file is newer
                delfile=fl
            #move file to duplicated folder
            dstfile=delfile.replace("Source","Duplicated")
            dstdir=os.path.dirname(dstfile)
            if (os.path.exists(dstdir)==False):
                os.makedirs(dstdir)
            shutil.move(delfile,dstfile)            
            logging.info("Duplicate file "+delfile+" -> "+dstfile+ " :source "+filelist[hashhex][1])
            print("")
        #

if __name__=='__main__':
    checkDir(sys.argv[1])


