"""Unofficial API for duolingo.com"""
import re
import json
import random

import requests
from werkzeug.datastructures import MultiDict

__version__ = "0.3"
__author__ = "Kartik Talwar"
__email__ = "hi@kartikt.com"
__url__ = "https://github.com/KartikTalwar/duolingo"


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Duolingo(object):
    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.user_url = "https://duolingo.com/users/%s" % self.username
        self.session = requests.Session()
        self.leader_data = None

        if password:
            self._login()

        self.user_data = Struct(**self._get_data())

    def _make_req(self, url, data=None):
        if data:
            req = requests.Request('POST', url, data=data, cookies=self.session.cookies)
        else:
            req = requests.Request('GET', url, cookies=self.session.cookies)
        prepped = req.prepare()
        return self.session.send(prepped)

    def _login(self):
        """
        Authenticate through ``https://www.duolingo.com/login``.
        """
        login_url = "https://www.duolingo.com/login"
        data = {"login": self.username, "password": self.password}
        print(data)
        response= requests.get(login_url,data)
        # attempt = self._make_req(login_url, data).json()
        if response.status_code == 200:
            return True

        raise Exception("Login failed "+response.status_code+response.reason)


    def buy_item(self, item_name, abbr):
        url = 'https://www.duolingo.com/store/purchase_item'
        data = {'item_name': item_name, 'learning_language': abbr}
        request = self._make_req(url, data)

        """
        status code '200' indicates that the item was shopped
        returns a text like: {"streak_freeze":"2017-01-10 02:39:59.594327"}
        """

        if request.status_code == 400 and item_name == 'streak_freeze':
            """
            Duolingo returns a "400" error if one tries to buy a "Streak on Ice" and
            the profile is already equipped with the streak
            There is a slight chance that another problem raised the 400 error,
            but most likely the existing extension is the problem
            """
            raise Exception('Already equipped with streak freeze.')
        if not request.ok:
            # any other error:
            raise Exception('Not possible to buy item.')

    def buy_streak_freeze(self):
        """
        figure out the users current learning language
        use this one as parameter for the shop
        """
        lang = self.get_abbreviation_of(self.get_user_info()['learning_language_string'])
        if lang is None:
            raise Exception('No learning language found')
        try:
            self.buy_item('streak_freeze', lang)
            return True
        except Exception as e:
            if e.args[0] == 'Already equipped with streak freeze.':
                # we are good
                return False
            else:
                # unknown exception, raise it again
                raise Exception(e.args)

    def _get_data(self):
        """
        Get user's data from ``https://www.duolingo.com/users/<username>``.
        """
        get = self._make_req(self.user_url).json()
        return get
    #
    @staticmethod
    def _make_dict(keys, array):
        data = {}

        for key in keys:
            if type(array) == dict:
                data[key] = array[key]
            else:
                data[key] = getattr(array, key, None)

        return data

    def get_abbreviation_of(self, name):
        """Get abbreviation of a language."""
        for language in self.user_data.languages:
            if language['language_string'] == name:
                return language['language']
        return None
    def get_user_info(self):
        """Get user's informations."""
        fields = ['username', 'bio', 'id', 'num_following', 'cohort',
                  'language_data', 'num_followers', 'learning_language_string',
                  'created', 'contribution_points', 'gplus_id', 'twitter_id',
                  'admin', 'invites_left', 'location', 'fullname', 'avatar',
                  'ui_language']

        return self._make_dict(fields, self.user_data)



if __name__ == '__main__':
    d = Duolingo('addi390582', '132457')
    ret = d.buy_streak_freeze()
    print ret

        # == '__main__'/:
   #  from pprint import pprint
   #
   #  duolingo = Duolingo('ferguslongley')
   #  knowntopic = duolingo.get_known_topics('it')
   #
   #  pprint(knowntopic)