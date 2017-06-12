import pytest
import pytz
import reversion
from datetime import timedelta, datetime
from model_mommy import mommy
from reversion.models import Version

from customer_info.models import Org


@pytest.mark.django_db
def test_project_reversion(admin_client):
    """
    This test checks that between revisions of projects. This will be used for
    auditing and NOT the original intention of showing events.
    """

    # create the first revision of Org
    with reversion.create_revision():
        key = mommy.make(Org, name="first name")
        reversion.set_date_created(datetime(2017, 4, 30, tzinfo=pytz.UTC))
    # try to get the object from the database.
    key_from_db = Org.objects.get(pk=key.pk)
    assert key.name == key_from_db.name

    # change a field and save it.
    with reversion.create_revision():
        key_from_db.name = "updated name"
        key_from_db.save()
        reversion.set_date_created(datetime(2017, 5, 15, tzinfo=pytz.UTC))

    # change a field again and save it.
    with reversion.create_revision():
        key_from_db.name = "no name"
        key_from_db.save()
        reversion.set_date_created(datetime(2017, 6, 1, tzinfo=pytz.UTC))

    # create an unrelated project with just one revision.
    with reversion.create_revision():
        unrelated_key = mommy.make(Org, name="unrelated project")
        reversion.set_date_created(datetime(2017, 7, 30, tzinfo=pytz.UTC))

    # refresh the value from the database.
    key.refresh_from_db()

    # django sanity check: the first object should equal the new one.
    assert key.name == "no name"
    assert key_from_db.name == "no name"

    # Get all the revisions for all projects.
    all_versions = Version.objects.get_for_model(Org)
    assert len(all_versions) == 4

    # Get only the revisions for the one that we made 3 revisions for.
    # (excludes the unrelated project.)
    versions = Version.objects.get_for_object(key)
    assert len(versions) == 3
