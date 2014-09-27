from django.test import TestCase, Client
from aristotle_mdr import models, perms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse

from django.test.utils import setup_test_environment
setup_test_environment()

class ViewersPostingAndCommenting(TestCase):

    def setUp(self):
        self.wg1 = models.Workgroup.objects.create(name="Test WG 1")
        self.wg2 = models.Workgroup.objects.create(name="Test WG 2")
        self.viewer1 = User.objects.create_user('vicky','','viewer') #viewer 1 always posts
        self.viewer2 = User.objects.create_user('viewer2','','viewer')
        self.manager = User.objects.create_user('mandy','','manger')
        self.wg1.giveRoleToUser('Viewer',self.viewer1)
        self.wg1.giveRoleToUser('Viewer',self.viewer2)
        self.wg1.giveRoleToUser('Manager',self.manager)

    def test_ViewerCanAlterPost(self):
        post = models.DiscussionPost(author=self.viewer1,workgroup=self.wg1,title="test",body="test")
        self.assertTrue(perms.user_can_alter_post(self.viewer1,post))
        self.assertTrue(perms.user_can_alter_post(self.manager,post))
        self.assertFalse(perms.user_can_alter_post(self.viewer2,post))

    def test_ViewerCanAlterComment(self):
        post = models.DiscussionPost(author=self.viewer1,workgroup=self.wg1,title="test",body="test")
        comment = models.DiscussionComment(author=self.viewer2,post=post,body="test")
        self.assertFalse(perms.user_can_alter_comment(self.viewer1,comment))
        self.assertTrue(perms.user_can_alter_comment(self.manager,comment))
        self.assertTrue(perms.user_can_alter_comment(self.viewer2,comment))
