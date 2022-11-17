from datetime import datetime, date, timedelta, time
from dateutil.parser import parse
import random
from pandas.core.common import flatten
from shapely.geometry import Point, mapping, shape
import os
import geopandas as gpd
from geopandas import GeoDataFrame as gdf
from geopandas import points_from_xy
import pandas as pd
import numpy as np
import time
import Person
import matplotlib.pyplot as plt
import plotly.express as px
import plotly as py
import plotly.graph_objects as go
import threading
import plotly
import multiprocessing as mp
from multiprocessing import Manager, Pool, Lock
import distutils.dir_util
import asyncio
import sys

class Model():
    def __init__(self, ZIP):
        self.ZIP = ZIP
        self.startdate = date(2020, 3, 1)
        self.currentdate = self.startdate
        self.enddate = date(2020, 3, 31)

        self.step = 0
        self.Lock_down = True
        self.output = []
        self.SEIR = []

        self.move_count = 0
        self.part = 0
        self.current_time = datetime.now()
        code_dir = "ABM-Simulator"
        population = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'input', 'persons250.csv'))

        LG = gpd.read_file(os.path.join(os.path.dirname(os.getcwd()), code_dir,  'input',  ZIP + '.geojson'))
        LG = LG[['UID', 'type', 'x', 'y']]
        self.Locations = {}

        Locs = LG['UID'].unique().tolist()
        for loc in Locs:
            self.Locations[loc] = []

        self.workplaces = {}
        LLG = LG.loc[LG['type'] == 'workplace']
        for index, row in LLG.iterrows():
            self.workplaces[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.restaurants = {}
        LLG = LG.loc[LG['type'] == 'restaurant']
        for index, row in LLG.iterrows():
            self.restaurants[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.worships = {}
        LLG = LG.loc[LG['type'] == 'worship']
        for index, row in LLG.iterrows():
            self.worships[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.grocerys = {}
        LLG = LG.loc[LG['type'] == 'grocery']
        for index, row in LLG.iterrows():
            self.grocerys[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.malls = {}
        LLG = LG.loc[LG['type'] == 'mall']
        for index, row in LLG.iterrows():
            self.malls[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.schools = {}
        LLG = LG.loc[LG['type'] == 'school']
        for index, row in LLG.iterrows():
            self.schools[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.outdoors = {}
        LLG = LG.loc[LG['type'] == 'outdoor']
        for index, row in LLG.iterrows():
            self.outdoors[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.banks = {}
        LLG = LG.loc[LG['type'] == 'bank']
        for index, row in LLG.iterrows():
            self.banks[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.hospitals = {}
        LLG = LG.loc[LG['type'] == 'hospital']
        for index, row in LLG.iterrows():
            self.hospitals[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.persons = {}
        for row in population.itertuples():
            pid = getattr(row, "pid")
            hid = getattr(row, "hid")
            age = getattr(row, "age")
            gender = getattr(row, "gender")
            race = getattr(row, "race")
            housex = getattr(row, "x")
            housey = getattr(row, "y")

            if self.randomTrue(0.98):
                initial_state = "susceptible"
            else:
                initial_state = "infected"
            person = Person.Person(pid, age, gender, race, housex, housey, hid, "house", initial_state, self)
            self.persons[pid] = person
            self.Locations[hid].append(pid) #add occupants to the building

        self.update()
        self.running = True
        while self.running:
            self.doTimeStep()

    def randomTrue(self, prob):
        r = random.uniform(0, 1)
        if r < prob:
            return True
        else:
            return False

    def get_time(self):
        t = datetime.now()
        d = datetime.now() - self.current_time
        self.current_time = datetime.now()
        return '[' + str(d.seconds) + 'sec' ' ' + str(t).split(' ')[1].split('.')[0] + ']'

    def doTimeStep(self):
        self.currentdate = self.startdate + timedelta(days=self.step)

        for key, person in self.persons.items():
            person.step()

        self.step += 1
        self.update()
        print('Step: ', self.step, '---', self.currentdate, '|', 'Time', self.get_time())
        d = self.enddate - self.startdate

        if self.currentdate >= self.enddate:
            self.running = False
            self.save()

    def update(self):
        output = {'step': self.step, 'susceptible': 0, 'infected': 0}
        for key, person in self.persons.items():
            output[person.state] += 1
        self.output.append(output)

    def save(self):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        outdir = os.path.join(os.getcwd(), 'output', dt_string, 'run1', self.ZIP, )
        distutils.dir_util.mkpath(outdir)
        df = pd.DataFrame(self.output)
        df.to_csv(os.path.join(outdir, 'output.csv'), index=False)

if __name__ == '__main__':
    model = Model('33613')