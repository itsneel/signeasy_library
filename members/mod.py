from members import models
from members import exceptions


def get_member(member_id):
    members = models.Member.objects.filter(pk=member_id)
    if not members:
        raise exceptions.MemberNotFoundError
    return members[0]