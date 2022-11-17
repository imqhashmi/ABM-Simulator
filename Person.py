import datetime
from dateutil.relativedelta import relativedelta
import datetime as dt
import pandas as pd
import os
import random
import threading
import sys

class Person():
    """Person Agent."""
    def __init__(self, pid, age, gender, race,  x, y, uid, loc_type, state, model):
        self.model = model
        # Agent parameters
        self.pid = pid
        self.age=age
        self.gender=gender
        self.race=race
        self.location = uid
        self.hid = uid   # a person always starts from home
        self.loc_type = loc_type
        self.x = x
        self.y = y
        self.hx = x
        self.hy = y
        self.state = state

        code_dir = 'ABM-Simulator'
        # load movements
        self.movements = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'input', 'movements.csv'))
        self.movements.drop(self.movements[self.movements.start == self.movements.end].index, inplace=True)
        self.movements = self.movements[self.movements['age']==self.age]
        self.move_count = 0

    def print(self):
        print(self.pid, self.x, self.y, self.location, self.loc_type, self.state)

    def set_model(self, model):
        self.model = model

    def get_location(self, loc_type):
        if loc_type == 'house':
            return (self.hid, loc_type, self.hx, self.hy)
        elif loc_type == 'workplace':
            locs = list(self.model.workplaces.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'restaurant':
            locs = list(self.model.restaurants.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'worship':
            locs = list(self.model.worships.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'grocery':
            locs = list(self.model.grocerys.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'mall':
            locs = list(self.model.malls.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'school':
            locs = list(self.model.schools.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'outdoor':
            locs = list(self.model.outdoors.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'bank':
            locs = list(self.model.banks.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'hospital':
            locs = list(self.model.hospitals.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        return None

    def get_route(self):
        mlist = []
        for row in self.movements.itertuples():
            start = getattr(row, 'start')
            end = getattr(row, 'end')
            start_loc = self.get_location(start)
            end_loc = self.get_location(end)
            if start_loc != None or end_loc != None:
                if start_loc!=end_loc:
                    mlist.append(start_loc)
                    mlist.append(end_loc)
        return mlist

    def infect(self):
        if (self.state == "susceptible"):
            neighbors = self.model.Locations[self.location]
            for neighbor in neighbors:
                neighbor_person = self.model.persons[neighbor]
                if neighbor_person.state == "infected":
                    if self.model.randomTrue(0.005):
                        self.state = "infected"
                        break
    def move(self, next):
        if next:
            #remove from current location
            self.model.Locations[self.location].remove(self.pid)
            self.location = next[0]
            self.x = next[2]
            self.y = next[3]
            self.loc_type = next[1]
            self.model.Locations[self.location].append(self.pid)
            self.move_count+=1
            # print(self.pid, 'moved to', self.loc_type)
            self.infect()

    def step(self):
        routes = self.get_route()
        if routes != []:
            for i, route in enumerate(routes):
                self.move(route)
