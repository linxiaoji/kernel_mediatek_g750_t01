#!/proj/map/bin/python/bin/python
# Copyright Statement:
#
# This software/firmware and related documentation ("MediaTek Software") are
# protected under relevant copyright laws. The information contained herein
# is confidential and proprietary to MediaTek Inc. and/or its licensors.
# Without the prior written permission of MediaTek inc. and/or its licensors,
# any reproduction, modification, use or disclosure of MediaTek Software,
# and information contained herein, in whole or in part, shall be strictly prohibited.

# MediaTek Inc. (C) 2010. All rights reserved.
#
# BY OPENING THIS FILE, RECEIVER HEREBY UNEQUIVOCALLY ACKNOWLEDGES AND AGREES
# THAT THE SOFTWARE/FIRMWARE AND ITS DOCUMENTATIONS ("MEDIATEK SOFTWARE")
# RECEIVED FROM MEDIATEK AND/OR ITS REPRESENTATIVES ARE PROVIDED TO RECEIVER ON
# AN "AS-IS" BASIS ONLY. MEDIATEK EXPRESSLY DISCLAIMS ANY AND ALL WARRANTIES,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NONINFRINGEMENT.
# NEITHER DOES MEDIATEK PROVIDE ANY WARRANTY WHATSOEVER WITH RESPECT TO THE
# SOFTWARE OF ANY THIRD PARTY WHICH MAY BE USED BY, INCORPORATED IN, OR
# SUPPLIED WITH THE MEDIATEK SOFTWARE, AND RECEIVER AGREES TO LOOK ONLY TO SUCH
# THIRD PARTY FOR ANY WARRANTY CLAIM RELATING THERETO. RECEIVER EXPRESSLY ACKNOWLEDGES
# THAT IT IS RECEIVER'S SOLE RESPONSIBILITY TO OBTAIN FROM ANY THIRD PARTY ALL PROPER LICENSES
# CONTAINED IN MEDIATEK SOFTWARE. MEDIATEK SHALL ALSO NOT BE RESPONSIBLE FOR ANY MEDIATEK
# SOFTWARE RELEASES MADE TO RECEIVER'S SPECIFICATION OR TO CONFORM TO A PARTICULAR
# STANDARD OR OPEN FORUM. RECEIVER'S SOLE AND EXCLUSIVE REMEDY AND MEDIATEK'S ENTIRE AND
# CUMULATIVE LIABILITY WITH RESPECT TO THE MEDIATEK SOFTWARE RELEASED HEREUNDER WILL BE,
# AT MEDIATEK'S OPTION, TO REVISE OR REPLACE THE MEDIATEK SOFTWARE AT ISSUE,
# OR REFUND ANY SOFTWARE LICENSE FEES OR SERVICE CHARGE PAID BY RECEIVER TO
# MEDIATEK FOR SUCH MEDIATEK SOFTWARE AT ISSUE.
#
# The following software/firmware and/or related documentation ("MediaTek Software")
# have been modified by MediaTek Inc. All revisions are subject to any receiver's
# applicable license agreements with MediaTek Inc.


import os,glob,re,sys,getopt
#check the command line validity
def Usage():
    print """
    Usage:mediatek/build/android/tools/%s [options] project

    Options:
    -h,--help      Print this message and exit

    Attention:
        for emulator,please use generic for the project argument
    """ % sys.argv[0]

try:
    opts,args = getopt.getopt(sys.argv[1:],"h",["help"])
except getopt.GetoptError:
    Usage()
    sys.exit(1)
if len(args) != 1:
    Usage()
    sys.exit(1)
for o,a in opts:
    if o in ("-h","--help"):
        Usage()
        sys.exit()

if not os.path.exists("./mediatek/config/%s/ProjectConfig.mk" % args[0]):
    print "Error!the argument  %s is not a correct project name!" % args[0]
    print "enter -h or --help for the help infomation!"
    sys.exit(1)

#base = "out/target/common/obj/JAVA_LIBRARIES/framework_intermediates/classes/"
dest_cls = "vendor/mediatek/" + sys.argv[1] + "/cls"
dest_jar = "vendor/mediatek/" + sys.argv[1] + "/jar"
dest_obj = "vendor/mediatek/" + sys.argv[1] + "/obj"
switch_txt = "vendor/mediatek/" + sys.argv[1] + "/switch.txt"

#os.system("rm -rf %s"%dest_cls)
os.system("mkdir -p %s"%dest_cls)
os.system("mkdir -p %s"%dest_jar)
os.system("mkdir -p %s"%dest_obj)

movepath = [
]

def aidlcopy(root,path):
  if not os.path.isdir(path): return
  subaidl = glob.glob(os.path.join(path,"*.aidl"))
  for aidl in subaidl:
    rpath = root.sub("",aidl)
    os.system("cp -f %s %s"%(aidl, os.path.join(dest_cls,rpath)))
  subdir = glob.glob(os.path.join(path,"*"))
  for dir in subdir: aidlcopy(root,dir)

for item in movepath:
  src  = item[1]
  name = item[0]
  base = item[2]
  if not os.path.exists(src):
    os.system("mkdir -p %s" % src)
    classesjar = src[:-8] + "classes.jar"
    os.system("unzip %s -d %s" % (classesjar,src))
  print "%s: copying classes"%name
  os.system("rm -rf .tmp")
  for path in item[3]:
    os.system("mkdir -p %s"%(os.path.join(".tmp",path)))
    os.system("mkdir -p %s"%(os.path.join(dest_cls,path)))
    os.system("cp -R %s %s"%(os.path.join(src,path,"*"),os.path.join(".tmp",path)))
    os.system("cp -R %s %s"%(os.path.join(src,path,"*"),os.path.join(dest_cls,path)))
    print "%s: copying aidls"%name
    aidlcopy(re.compile(re.escape(base+("/" if base[-1]!="/" else ""))),base)
  print "%s: making jar"%name
  os.system("jar -cvf %s -C .tmp ."%(os.path.join(dest_jar,name+".jar")))

#copy the init to switch

if os.path.exists(switch_txt):
   shellcommand = "cat " + switch_txt
   copyItem = os.popen(shellcommand)
   for item in copyItem:
      _src = item.strip().split(":")[0]
      _des = item.strip().split(":")[1]
      if os.path.exists(_des):
         os.system("rm -rf %s" % _des)
      result = os.system("cp -a %s %s" % (_src,_des))
      if result != 0:
         print "switch cp has a wrong in class.py"
         sys.exit(1)

