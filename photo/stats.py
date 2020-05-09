"""Provide the class Stats that collects some statistics.
"""

import datetime


class Stats(object):

    def __init__(self, items):
        self.count = 0
        self.selected = 0
        self.oldest = datetime.datetime.max
        self.newest = datetime.datetime.min
        self.by_date = {}
        self.by_tag = {}
        for i in items:
            self.count += 1
            if i.selected:
                self.selected += 1
            if i.createDate:
                if i.createDate < self.oldest:
                    self.oldest = i.createDate
                if i.createDate > self.newest:
                    self.newest = i.createDate
                date = i.createDate.toordinal()
                self.by_date.setdefault(date, 0)
                self.by_date[date] += 1
            for tag in i.tags:
                self.by_tag.setdefault(tag, 0)
                self.by_tag[tag] += 1

    def __bool__(self):
        return bool(self.count)

    def __str__(self):
        s = "Count: %d\nSelected: %d\n" % (self.count, self.selected)
        if self.newest >= self.oldest:
            s += "Oldest: %s\n" % str(self.oldest)
            s += "Newest: %s\n" % str(self.newest)
        if self.by_date:
            s += "By date:\n"
            for d in sorted(self.by_date.keys()):
                s += ("  %s: %d\n" 
                      % (datetime.date.fromordinal(d), self.by_date[d]))
        if self.by_tag:
            s += "By tag:\n"
            for t in sorted(self.by_tag.keys()):
                s += ("  %s: %d\n" % (t, self.by_tag[t]))
        return s
