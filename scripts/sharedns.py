#!/usr/bin/env python
# Program: sharedns.py
# Purpose: Provides a list of PIDs sharing each namespace.
# Author: Matty < matty91 at gmail dot com >
# Current Version: 1.0
# Date: 02-22-2018
# License:
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

import os
import re
from collections import defaultdict


def build_namespaces():
    """
       Grab the namespaces for each pid in /proc and stash
       them away for future use. Here is the ns format in
       /proc/PID/ns: pid -> pid:[4026531836]
    """
    namespaces = defaultdict(float)
    namespace_pids = defaultdict(list)
    ns_ignore_list = ["pid_for_children"]

    for pid in os.listdir("/proc"):
         ns_path = "/proc/" + pid + "/ns"
         if pid.isdigit():
              # Read in the list of ns files and create two dicts:
              # namespaces contains the namespace ids and its type (pid, uts, etc.)
              # namespace_pids - contains a list of pids referencing the ns id
              for namespace in os.listdir(ns_path):
                  if namespace not in ns_ignore_list:
                      id = os.readlink(ns_path + "/" + namespace)
                      nstype, nsid = id.replace(":["," ").replace("]","").split()
                      namespaces[nsid] = nstype
                      namespace_pids[nsid].append(pid)
    return(namespaces, namespace_pids)


def find_shared_namespace(namespaces, namespace_pids):
   """
      Iterate over the two dicts and display all of the
      pids that share a namespace id.       
   """
   print("%-20s  %-10s  %-20s" % ("Namespace ID", "Namespace", "Pids Sharing Namespace"))

   for nsid, nstype in namespaces.iteritems():
       print("%-20s  %-10s  %-20s" % (nsid, nstype, ",".join(namespace_pids[nsid])))


def main():
    """
       Here's where the fun begins.
    """
    namespaces, namespace_pids = build_namespaces()
    find_shared_namespace(namespaces, namespace_pids)


if __name__ == "__main__":
    main()
