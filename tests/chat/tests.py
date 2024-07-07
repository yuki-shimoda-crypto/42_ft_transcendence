from chat.models import ChatGroup, GroupMessage
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class ChatGroupModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpass1"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpass2"
        )

    def test_create_chat_group(self):
        group = ChatGroup.objects.create(is_private=False)
        assert group.is_private is False
        assert group.members.count() == 0
        assert group.users_online.count() == 0

    def test_add_members_to_chat_group(self):
        group = ChatGroup.objects.create(is_private=False)
        group.members.add(self.user1, self.user2)
        assert group.members.count() == 2

    def test_add_users_online_to_chat_group(self):
        group = ChatGroup.objects.create(is_private=False)
        group.users_online.add(self.user1, self.user2)
        assert group.users_online.count() == 2

    def test_str_representation(self):
        group = ChatGroup.objects.create(is_private=False)
        assert str(group) == group.group_name


class GroupMessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.group = ChatGroup.objects.create(is_private=False)

    def test_create_group_message(self):
        message = GroupMessage.objects.create(
            group=self.group, author=self.user, body="Test message"
        )
        assert message.author == self.user
        assert message.body == "Test message"
        assert message.created is not None

    def test_str_representation(self):
        message = GroupMessage.objects.create(
            group=self.group, author=self.user, body="Test message"
        )
        assert str(message) == f"{self.user.username} : {message.body}"

    def test_message_ordering(self):
        message1 = GroupMessage.objects.create(
            group=self.group, author=self.user, body="Message 1"
        )
        message2 = GroupMessage.objects.create(
            group=self.group, author=self.user, body="Message 2"
        )
        messages = list(GroupMessage.objects.all())
        assert messages[0] == message2
        assert messages[1] == message1
