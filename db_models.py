import datetime
import collections
import numpy as np
import csv

import logging

from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Boolean, ForeignKey, ColumnDefault, Float
from sqlalchemy import and_, or_, desc, asc, bindparam, text, Interval
from sqlalchemy.sql import func, select, update, literal_column, column, join
from sqlalchemy.dialects.postgresql import aggregate_order_by

from meta import app as application, db, db_session

class DBModelAdder:

    def __init__(self):
        self.session = None

    def start(self):
        self.session = db_session()

    def done(self):
        self.session.commit()
        self.session.close()  

    def execute(self, stmnt):
        self.session.execute(stmnt)

    def add(self, inst):
        self.session.add(inst)  
