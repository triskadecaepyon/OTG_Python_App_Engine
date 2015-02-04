import sys
from google.appengine.ext import ndb
import datetime
import re
sys.path.insert(0, 'support_packages')
sys.path.insert(0, 'backend_python_files')

from google.appengine.api import users, memcache

# How to get backend python files and support packages into
# the worker.py file
# from backend_python_files import [insert package name]
# from support_packages import [insert package name]

DEFAULT_SCHEMA_NAME = 'default'

# --------------------------------------------------------------------------
# DataStore Models
#
# App Engine Data Store Models in this area
# use of stream_key is to immediately grab the index schema, unless
# another is needed.
#
# Each of the below models give a simplified view of some of the more common
# types of properties used in the data store.
# --------------------------------------------------------------------------

def stream_key(streambook_name=DEFAULT_SCHEMA_NAME):
    """Constructs a Datastore key for a Stream entity with stream name."""
    return ndb.Key('OTG', streambook_name)


class OTG_model_user(ndb.Model):
    """Models an individual user"""
    user = ndb.UserProperty()
    name = ndb.StringProperty(indexed=True)
    added_date = ndb.DateTimeProperty(auto_now_add=True)


class OTG_model_items(ndb.Model):
    uniqueID = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    #link to a taste profile


# --------------------------------------------------------------------------
# Worker Role definitions and functions
# Memcache general strategy function
# Care must be taken, as stale cache values can cause odd behavior.
# --------------------------------------------------------------------------


def check_memcache_for_key(key):
    data = memcache.get(key)
    if data is not None:
        return data
    else:
        return None


def add_to_memcache(key, data, optional_time=60, optional_namespace=None):
    memcache.add(key, data, optional_time, min_compress_len=0, namespace=optional_namespace)


def get_memcache(key):
    data = check_memcache_for_key(key)

    if data is not None:
        return data
    else:
        return None


def set_memcache(key, data, optional_time=60, optional_namespace=None, optional_strategy=None):
    check_data = check_memcache_for_key(key)

    if check_data is not None:
        return "Already In Memcache"
    else:
        add_to_memcache(key, data, optional_time, optional_namespace)
        return True


# --------------------------------------------------------------------------
# Worker Role definitions and functions
# User functions
# --------------------------------------------------------------------------

"""
Register User: allows for the creation of a data store element with users.
For different users, retrieve specific user information using the user name
for additional web app functionality.
"""


def register_user(user):
    print "registering user"
    found_id = False
    # Check if the user exists already
    user_query = OTG_model_user.query(OTG_model_user.user == user)
    for key in user_query.iter(keys_only=True):
        if key:
            found_id = True

    if found_id:
        print "user already registered"
        return
    else:
        print "create new user in data store"
        # Access the main data store schema
        user_store = OTG_model_user(parent=stream_key(DEFAULT_SCHEMA_NAME))

        user_store.name = users.User.email(user)
        user_store.user = user

        user_store.put()