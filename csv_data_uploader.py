# encoding:utf-8
import csv
import collections
from datetime import datetime
import logging

from db_models import DBModelAdder

class CSVDataUploader:
    
    def __init__(self, prefix="data/"):
        self.prefix = prefix

    def cvs_to_db(self):
        adder = DBModelAdder()
        adder.start()
        adder.done()