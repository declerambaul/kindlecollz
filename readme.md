# kindlecollz

(This is dating from 2010 so it might be outdated)

A simple script for handling collections of pdf files on the Amazon Kindle.

The Kindle is a great reading device, unfortunately so far it is rather painful to use it for a large collection of documents -  for example when dealing with many research papers. 

Assuming that the documents are pdf files and that they are properly named and stored in a meaningful directory structure, this script will generate a collection for every folder that contains pdfs. The name of a collection is the relative path starting from the `document/` folder. Existing collections are not changed, new collections are created if they didn't exist before and new documents are added to collections that existed before. Requires python version 2.6  (only because of the `json` package).
 
As Amazon doesn't seem to support this functionality yet, this is a hack which also requires that the Kindle be restarted to update the system. This is quite annoying, but there doesn't seem to be another way until Amazon releases its `Kindle Development Kit`. At which point this script will hopefully become obsolete.


# Usage

$python2.6 KindleForResearch.py [kindle mount point]

Note that if the script is saved in the root folder of the Kindle (e.g. /Volumes/Kindle), the mount point is not necessary. 

Please feel free to use and extend the script in any way you want. If you already have a valued collection of collections, it might also be a good idea to backup this file before you give this a try.
