import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
import sqlalchemy as sa
from app import app, db
from app.models import Users, Words


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Users(nickname = 'pinky', name = 'Tilda', email = 'pinky@majnoon.com')
        u.set_password('dog')
        self.assertFalse(u.check_password('cat'))
        self.assertTrue(u.check_password('dog'))

    def test_follow(self):
        u1 = Users(nickname = 'brain', name = 'Tor', email = 'brain@majnoon.com')
        u2 = Users(nickname = 'viper', name='Lokky', email = 'viper@majnoon.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        following = db.session.scalars(u1.following.select()).all()
        followers = db.session.scalars(u1.followers.select()).all()
        self.assertEqual(following, [])
        self.assertEqual(followers, [])
        u1.follow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)
        u1_following = db.session.scalars(u1.following.select()).all()
        u2_followers = db.session.scalars(u2.followers.select()).all()
        self.assertEqual(u1_following[0].name, 'Lokky')
        self.assertEqual(u2_followers[0].name, 'Tor')


if __name__ == '__main__':
    unittest.main(verbosity=2)