import sys,os,json,time
from hashlib import sha1


# Mount point for Kindle. It is assumed the script is executed in the home folder of the device
KINDLE_MOUNT = '.'

# Relative path to collection json file
COLLECTIONS = 'system/collections.json'
# Relative path to documents folder
KINDLE_DOCS = 'documents'

# for the computation of the sha1 identifier
KINDEL_ABS = '/mnt/us/documents'

# Dictionary for storing collections
kindleC = {}


def setKindleMountPoint():
    ''' 
    In case the script is not run in the root folder of the Kindle device, the Kindle Mount Point has to be updated because relative paths won`t work anymore 
    '''
    global KINDLE_MOUNT,COLLECTIONS,KINDLE_DOCS
    if len(sys.argv)>1:
        # An alternative mount point has been supplied
        KINDLE_MOUNT = sys.argv[1]
    
    COLLECTIONS = os.path.join(KINDLE_MOUNT,COLLECTIONS)
    KINDLE_DOCS = os.path.join(KINDLE_MOUNT,KINDLE_DOCS)
    
def loadCollections():
    ''' Loads Kindle collections in dictionary '''
    global kindleC
    try:
        cf = open(COLLECTIONS,'r')
        kindleC = json.load(cf)
        cf.close()
    except:
        print 'WARNING: %s could not be loaded. Creating a new version.'%COLLECTIONS
        
def saveCollections():
    ''' Dump kindle collections dictionary back into json file '''
    cf = open(COLLECTIONS,'wb')
    json.dump(kindleC,cf)
    cf.close()


def lastAccess():
    ''' Returns a lastaccess value in milliseconds '''
    return int(time.time()*1000)
    

def isPdfFile(f):
    ''' Only add non hidden pdf files. f is the absolute path '''
    if f[-3:]=='pdf' and f[0]!='.':
        return True
    else:
        return False    

def updateCollections():
    '''
    The source folder is traversed, all pdf documents encountered are added to a collection with the name of the folder.
    '''
    for root, dirs, files in os.walk(KINDLE_DOCS):
        
        
        # list of asin numbers of all documents in the current folder
        asinFiles = []
        
        # name of the collection, the current folder 
        # cName = '%s@en-US'%root.split('/')[-1]
        # alternatively one could use the relative path 
        cName = '%s@en-US'%os.path.relpath(root,KINDLE_DOCS) 
            
        
        # determine if there are pdf files in the current folde
        # if not, no collection for that folder is created
        filesToAdd = False
        if len(files)!=0:
            for f in files:
                #only add not hidden pdf files 
                if isPdfFile(f):
                    filesToAdd =  True                
                
        if filesToAdd: #there are files to process

            if cName in kindleC: # collection exists
                # account for the documents that alrady exist in the collection
                kindleC[cName]['lastAccess'] = lastAccess()    
            else: # collection doesn't exist
                kindleC[cName] = {'items':[], 'lastAccess':lastAccess()}
            
            #relative path to current folder
            relPath = os.path.relpath(root,KINDLE_DOCS)
            
            # traverse all files in the current directory    
            for f in files:
                if isPdfFile(f):
                    # determine the kindle specific absolute path
                    absPdfPath = '%s/%s/%s'%(KINDEL_ABS,relPath,f)
                    # compute the unique identifier, kindle uses the sha1 hashcode preceded by a * 
                    # the device specific absolute path is used, e.g. '/mnt/us/documents/research/test.pdf'
                    asin = '*%s'%sha1(absPdfPath).hexdigest()
                    # if the document is not already in the collection we add it
                    if asin not in kindleC[cName]['items']:
                        kindleC[cName]['items'].append(asin) 
                        
                    asinFiles.append(asin) 
            
        # remove collections that contain no documents and remove references that don't exist anymore
        if cName in kindleC:
            for asin in kindleC[cName]['items']:
                # if asin is not among the files in the folder, remove it from the collection
                if asin not in asinFiles:
                    kindleC[cName]['items'].remove(asin) 
                    # print 'remove',asin,'from',cName
                    
            if len(kindleC[cName]['items']) == 0:
                del kindleC[cName]
                # print 'remove col' ,cName


if __name__ == '__main__':

    # If the script is not executed in the root folder of the mounted Kindle
    setKindleMountPoint()
    
    # Check if path are correct
    if not (os.path.exists(COLLECTIONS) and os.path.exists(KINDLE_DOCS)):
        print 'ERROR: unknown path to Kindle mounting point. Please set `KINDLE_MOUNT` to correct path (e.g. /Volumes/Kindle)'
        sys.exit() 
        
    # Load collections
    loadCollections()    
    # Add new files to the collection dictionary 
    updateCollections()    
    # Save updated collections back into json
    saveCollections()
    
    # display reminder to restart kindle 
    print 'REMINDER: COLLECTIONS WILL NOT BE UPDATED UNLESS YOU RESTART YOUR KINDLE NOW! HOLD THE SWITCH FOR 20 SECONDS AND THEN RELEASE. THEN WAIT 20 SECONDS; THE SCREEN WILL FLASH AND THEN THE DEVICE WILL RESTART' 

