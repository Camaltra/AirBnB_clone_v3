#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.user import User

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print(first_state_id)
print("User: {}".format(storage.get(User, 'fa44780d-ac48-41ab-9dd0-ac54a15755cf')))
