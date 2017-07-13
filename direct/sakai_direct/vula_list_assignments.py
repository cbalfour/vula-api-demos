#!/usr/bin/env python

# Print out a list of the sites and their associated assignments

import getpass
from sakai_direct import *

sakai_url = 'https://vula.uct.ac.za/direct'

if __name__ == "__main__":

    user = input("Enter username: ")
    passwd = getpass.getpass("Enter password: ")

    vula = Sakai(sakai_url)
    if not vula.is_active_session():
        vula.login(user, passwd)


    sites = SakaiSites(vula)
    for site in sites.get_sites():
        print (site)
        print ("-" * 20)

        assignments = site.get_assignments()
        for assignment in assignments.get_assignments():
            print ("\t%s" % assignment)

