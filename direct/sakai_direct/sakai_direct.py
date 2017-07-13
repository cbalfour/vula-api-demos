#!/usr/bin/env python

import requests
import json 
from datetime import datetime

class CacheFileNotFoundError(Exception): 
    pass

class NoGradebookError(Exception):
    pass

class AssignmentNotFoundError(Exception):
    pass

class SiteNotFoundError(Exception):
    pass

def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp/1000.0) 

class SakaiSites(object):

    def __init__(self, sakai):
        self.sakai = sakai
        self.__get_sites()
        
    def __get_sites(self):

        url = "%s/site.json" % self.sakai.url
        self.sites= []

        # Sakai has a limit on the number of sites it returns 
        # per request. Depending on the number of sites the 
        # user has access to, it might be necessary to make 
        # a number of requests.

        for i in range(0, 1000, 50):

            payload = { '_start': i, '_limit': i+50 }
            r = requests.get(
                url, 
                cookies=self.sakai.get_cookie_jar(), 
                params = payload
            )

            data = r.json()

            if len(data['site_collection']) == 0: break

            for site_data in data['site_collection']:
                site_id = site_data['id']
                site = SakaiSite(self.sakai, site_id)
                if not site in self.sites:
                    self.sites.append(site)

            for key in data.keys():
                    
                if not hasattr(self, key):
                    setattr(self, key, data[key])
                else:
                    if key == 'site_collection':
                        self.site_collection += data['site_collection']


    def get_sites(self):
        return self.sites

    def get_site(self, site_id):
        site =  next((site for site in self.sites if site.get_id() == site_id), None)
        if site:
            return site 
        raise SiteNotFoundError("Site not found.")


class SakaiSite(object):

    def __init__(self, sakai, site_id):
        self.site_id = site_id
        self.sakai = sakai
        self.__get_site()

    def __get_site(self):
        url = "%s/site/%s.json" % (self.sakai.url, self.site_id)
        r = requests.get(url, cookies = self.sakai.get_cookie_jar())
        data = r.json()
        for key in data.keys():
            setattr(self, key, data[key])

    def get_term(self):
        if 'term' in self.props.keys():
            return int(self.props['term'])
        return None

    def get_created_time(self):
        return convert_timestamp(self.createdTime['time'])

    def get_contact_email(self):
        return self.contactEmail

    def get_contact_name(self):
        return self.contactName

    def get_description(self):
        return self.description

    def get_short_desciption(self):
        return self.shortDescription

    def get_owner(self):
        return self.owner

    def get_title(self):
        return self.title

    def get_type(self):
        return self.type

    def is_published(self):
        return self.published

    def get_id(self):
        return self.id

    def get_modified_time(self):
        return convert_timestamp(self.modified_time['time'])

    def get_gradebook(self):
        return SakaiGradebook(self.sakai, self.site_id)

    def get_membership(self):
        return SakaiMembership(self.sakai, self.site_id)

    def get_assignments(self):
        return SakaiAssignments(self.sakai, self.site_id)

    def __repr__(self):
        return "%s (%s)" % (self.title, self.id)


class SakaiAssignments(object):

    def __init__(self, sakai, site_id):
        self.site_id = site_id
        self.sakai = sakai
        self.__get_assignments()
        
    def __get_assignments(self):

        # This url seems to fetch all assignments andnot just those
        # in the site specified
        url = "%s/assignment/site/%s.json" % (self.sakai.url, self.site_id)

        r = requests.get(url, cookies=self.sakai.get_cookie_jar())
        data = r.json()
            
        for key in data.keys():
            setattr(self, key, data[key])

        self.assignments = []
        for assignment_data in self.assignment_collection:
            assignment_id = assignment_data['id']
            assignment = SakaiAssignment(self.sakai, assignment_id, assignment_data=assignment_data)
            if not assignment in self.assignments:
                self.assignments.append(assignment)

    def get_assignments(self):
        return self.assignments

    def get_assignment_by_name(self, name):
        assignment =  next((assignment for assignment in self.assignments if assignment.get_title() == name), None)
        if not assignment:
            raise AssignmentNotFoundError("Assignment not found")

        return assignment


class SakaiMembership(object):

    def __init__(self, sakai, site_id):
        self.site_id = site_id
        self.sakai = sakai
        self.__get_membership()
        
    def __get_membership(self):

        url = "%s/membership/site/%s.json" % (self.sakai.url, self.site_id)

        r = requests.get(url, cookies=self.sakai.get_cookie_jar())
        data = r.json()
            
        for key in data.keys():
            setattr(self, key, data[key])

        self.members = []
        for member_data in self.membership_collection:
            member_id = member_data['userId']
            member = SakaiMember(self.sakai, member_id, member_data)
            if not member in self.members:
                self.members.append(member)

    def get_members_by_userid(self, user_id):
        return [ member for member in self.members if member.userId.lower() == user_id.lower() ]


    def get_member_by_userid(self, user_id):
        member =  next((member for member in self.members if member.userId == user_id), None)
        return member

    def get_members_by_usereid(self, user_eid):
        return [ member for member in self.members if member.userEid.lower() == user_eid.lower() ]

    def get_members(self):
        return self.members


class SakaiAssignment:

    def __init__(self, sakai, assignment_id, assignment_data=None):
        self.sakai = sakai
        self.assignment_id = assignment_id
        self.assignment_data = assignment_data
        self.__get_assignment()

    def __get_assignment(self):
        if not self.assignment_data:
            url = "%s/assignment/item/%s.json" % (self.sakai.url, self.assignment_id)
            r = requests.get(url, cookies=self.sakai.get_cookie_jar())
            if r.status_code != 200:
                raise AssignmentNotFoundError("Assignment not found.")
            data = r.json()
        else:
            data = self.assignment_data

        for key in data.keys():
            setattr(self, key, data[key])

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def get_id(self):
        return self.id

    def get_grade_scale(self):
        return self.gradeScale

    def get_grade_scale_max_points(self):
        return float(self.gradeScaleMaxPoints)

    def get_due_time(self):
        return convert_timestamp(self.dueTime['time'])

    def get_title(self):
        return self.title

    def get_status(self):
        return self.status

    def is_draft(self):
        return self.draft

    def get_close_time(self):
        return convert_timestamp(self.closeTime['time'])

    def get_time_last_modified(self):
        return convert_timestamp(self.timeLastModified['time'])

    def is_resubmittable(self):
        return self.allowResubmission

    def get_submission_type(self):
        return self.submissionType

    def get_status(self):
        return self.status

    def __repr__(self):
        return "%s" % (self.title)

# We are not able to query /direct/member so we need to provide the data
# as a parameter

class SakaiMember:

    def __init__(self, sakai, member_id, member_data):
        self.sakai = sakai
        self.member_id = member_id
        self.member_data = member_data
        self.__get_member()

    def __get_member(self):
        for key in self.member_data.keys():
            setattr(self, key, self.member_data[key])

    def __eq__(self, other):
        if self.userId.lower() == other.userId.lower():
            return True
        elif self.userEid.lower() == other.userEid.lower():
            return True
        return False

    def is_active(self):
        return self.active

    def get_email(self):
        return self.userEmail

    def get_display_name(self):
        return self.DisplayName

    def get_role(self):
        return self.memberRole

    def get_last_login_time(self):
        return convert_timestamp(self.lastLoginTime)

    def get_user_eid(self):
        return self.userEid

    def get_user_id(self):
        return self.userId

    def __repr__(self):
        return "%s (%s)" % (self.entityTitle, self.userEid)

class SakaiGradebook(object):

    def __init__(self, sakai, site_id):
        self.site_id = site_id
        self.sakai = sakai
        self.__get_gradebook()
        
    def __get_gradebook(self):

        url = "%s/gradebook/site/%s.json" % (self.sakai.url, self.site_id)

        r = requests.get(url, cookies=self.sakai.get_cookie_jar())
        if r.status_code != 200:
            raise NoGradebookError("No gradebook")
        data = r.json()
            
        for key in data.keys():
            setattr(self, key, data[key])

    def get_assignment_names(self):
        assignment_names = []
        for assignment in self.assignments:
            if not assignment['itemName'] in assignment_names:
                assignment_names.append(assignment['itemName'])
        return assignment_names
        

    def get_grades_for_assignment(self, assignment_name):
        return [ grade for grade in self.assignments if grade['itemName'] == assignment_name ]

    def get_grades_for_user(self, user_id):
        return [ grade for grade in self.assignments if grade['userId'] == user_id ]


class Sakai(object): 

    def __init__(self, url):
        self.url = url
        self._cookiejar = requests.cookies.RequestsCookieJar()

    def login(self, username, password):
        self.__username = username
        payload =  { '_username': username, '_password': password }
        r = requests.post(self.url + '/session', data=payload)
        self._cookiejar = r.cookies

    def is_active_session(self):
        r = requests.get(self.url + '/session.json', cookies=self._cookiejar)
        data = r.json()
        session = data['session_collection'][0]
        if session['active'] == True and session['userId']:
            return True
        return False


    def get_sites(self, course_only=True):
        sites = {}
        r = requests.get(self.url + '/site.json', cookies=self._cookiejar)
        data = r.json()
        for site_data in data['site_collection']:
            site_type = site_data['type']
            if course_only and site_type != 'course': continue
            site_id = site_data['id']
            try:
                site_title = site_data['title']
            except:
                site_title = None
            sites[site_id] = { 'site_title': site_title, 'site_type': site_type } 

        return sites

    def get_assignments(self, site_id):
        assignments = {}
        r = requests.get(self.url + '/assignment/site/%s.json' % site_id, cookies=self._cookiejar)
        data = r.json()
        for assignment_data in data['assignment_collection']:
            assignment_id = assignment_data['id']
            assignment_title = assignment_data['title']
            assignments[assignment_id] = { 'assignment_title': assignment_title }
        return assignments

    def get_membership(self, site_id):
        members = {}
        url = self.url + '/membership/site/%s.json' % site_id


        data = None
        try:
            with open('%s-members.json' % site_id) as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
                r = requests.get(url, cookies=self._cookiejar)
                data = r.json()

        for member_data in data['membership_collection']:
            user_id = member_data['userId']
            display_id = member_data['userDisplayId']
            role = member_data['memberRole']
            members[user_id] = { 'username': display_id, 'role': role }
        return members

    def get_site_term(self, site_id):
        url = self.url + "/site/%s.json" % (site_id)
        r = requests.get(url, cookies=self._cookiejar)
        data = r.json()
        #print (data['props'])
        site_term = data['props']['term']
        return int(site_term)

    def get_gradebook(self, site_id):
        gradebook = {}

        url = self.url + "/gradebook/site/%s.json" % (site_id)

        data = None
        try:
            with open('%s-gradebook.json' % site_id) as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
                r = requests.get(url, cookies=self._cookiejar)
                if r.status_code != 200:
                    raise Exception("No gradebook")
                data = r.json()

        for grade_data in data['assignments']:
            assignment_name = grade_data['itemName']
            user_id = grade_data['userId']
            if not assignment_name in gradebook.keys():
                gradebook[assignment_name] = {}

            if not user_id in gradebook[assignment_name].keys():
                gradebook[assignment_name][user_id] = { 'grade': grade_data['grade'] } 

        return gradebook 


    def get_cookie_jar(self):
        return self._cookiejar

    def get_session_id(self):
        return self._cookiejar['JSESSIONID']
        

if __name__ == "__main__":
    pass
