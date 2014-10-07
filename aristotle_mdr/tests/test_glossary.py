from django.test import TestCase, Client
from aristotle_mdr import models, perms
from django.utils import timezone
from django.core.urlresolvers import reverse
from aristotle_mdr.tests import utils

from django.test.utils import setup_test_environment
setup_test_environment()

class GlossaryPage(utils.LoggedInViewPages,TestCase):
    pass
