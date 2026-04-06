"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from datetime import datetime

class User():
    def __init__(self, user_id, name = "", age = 0):
    	self.user_id = user_id
    	self.name = name
    	self.age = age
    	self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)
    def total_listening_seconds(self) -> int:
        t = 0
        for s in self.sessions:
            t += s.duration_listened_seconds
        return t

    def total_listening_minutes(self) -> float:
        t = 0
        for s in self.sessions:
            t += s.duration_listened_minutes()
        return t
    def unique_tracks_listened(self) -> list:
        return {session.track.track_id for session in self.sessions}

class FreeUser(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.MAX_SKIPS_PER_HOUR = 6

class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.sub_users = []

    def add_sub_user(self, user):
        self.sub_users.append(user)
    def all_members(self):
        l = [self]
        l += self.sub_users
        return l

class FamilyMember(User):
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent

