from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import LoginForm
from .models import GameLibrary, Profile
from django.conf import settings
import datetime
# Create your tests here.

class LibraryTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        user.save()
        p = Profile(user=user, nickname='tester')
        p.save()
        for i in range(1,5):
            game_name = 'test game %s' % i
            g = GameLibrary(name=game_name)
            g.save()
            user.profile.played_games.add(g)


    def test_recent_games_displayed_if_user_logged_in(self):
        self.client.login(username='test_user', password='test_password')
        recent_games = User.objects.get(username='test_user').profile.played_games.order_by('creation_date')[0:3]
        response = self.client.get(reverse('games:library'))
        for game in recent_games:
            self.assertIn(game, response.context['games'])

    def test_search_works_correctly(self):
        game = GameLibrary.objects.get(name='test game 1')
        response = self.client.post(reverse('games:library'), {'query':'test game 1'})
        self.assertIn(game, response.context['games'])


    def test_user_redirected_to_game_when_thumbnail_clicked(self):
        pass

    def test_recently_added_games_displayed_if_anonymous_user(self):
        response = self.client.get(reverse('games:library'))
        displayed_games = response.context['games']
        recent_games = GameLibrary.objects.order_by('creation_date')[:3]
        for game in displayed_games:
            self.assertIn(game, recent_games)



class LoginTests(LiveServerTestCase):
    #add tests for login view, which will just be for authentication.

    def __init__(self, *args, **kwargs):
        super(LoginTests, self).__init__(*args, **kwargs)
        if settings.DEBUG == False:
            settings.DEBUG = True

    def setUp(self):
        self.driver = webdriver.Firefox()
        super(LoginTests ,self).setUp()
        user = User.objects.create_user(username='test_user', password='test_password')
        user.save()
        p = Profile(user=user, nickname='tester')
        p.save()
        for i in range(1,5):
            game_name = 'test game %s' % i
            g = GameLibrary(name=game_name)
            g.save()
            user.profile.played_games.add(g)

    #
    # def tearDown(self):
    #     self.driver.close()
    #     super(LoginTests, self).tearDown()

    def test_authorised_user_redirected_to_library_when_form_filled_in(self):
        '''
        when the form is filled in and submitted user should be redirected to
        the game library page.
        '''
        self.driver.get(
            '%s%s' % (self.live_server_url, "/signIn")
        )
        username = self.driver.find_element_by_id("id_username")
        username.send_keys('test_user')
        password = self.driver.find_element_by_id("id_password")
        password.send_keys('test_password')
        self.driver.find_element_by_id("signInForm").submit()
        self.assertIn('library', self.driver.title)
    #forms

class LoginFormTest(TestCase):

    def test_login_form_works(self):
        '''
        Test that the login form works.
        '''
        form = LoginForm({'username':'test', 'password':'test'})
        self.assertTrue(form.is_valid())

    # def test_blank_form_doesnt_work(self):
    #     form = LoginForm({})
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(form.errors, {
    #     'username': ['required'],
    #     'password': ['required'],
    #     })



#
# class Game(TestCase):
#     #add tests for the game view, which will serve the js file with the correct game
#     pass
