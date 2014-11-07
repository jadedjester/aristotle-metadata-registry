from django.test import TestCase

#from django.core.urlresolvers import reverse
#import aristotle_mdr.models as models
#import aristotle_mdr.perms as perms
import aristotle_mdr.tests.utils as utils

from django.test.utils import setup_test_environment
setup_test_environment()

class GlossaryPage(utils.LoggedInViewPages,TestCase):
    pass
