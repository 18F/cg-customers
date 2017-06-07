import pytest
import pytz
import reversion
from datetime import timedelta, datetime
from model_mommy import mommy
from reversion.models import Version

from packages.models import Package
from projects.models import Project


@pytest.mark.django_db
def test_project_reversion(admin_client):
    """
    This test checks that between revisions of projects. This will be used for
    auditing and NOT the original intention of showing events.
    """
    # SETUP create two packages
    with reversion.create_revision():
        pkg1 = mommy.make(Package, package_name="first customer pkg")
        pkg1.save()
        print(pkg1.id)
    with reversion.create_revision():
        pkg2 = mommy.make(Package, package_name="second customer pkg")
        pkg2.save()
        print(pkg2.id)


    # create the first revision of Project
    with reversion.create_revision():
        key = mommy.make(Project, project_name="first name")
        reversion.set_date_created(datetime(2017, 4, 30, tzinfo=pytz.UTC))
    # try to get the object from the database.
    key_from_db = Project.objects.get(pk=key.pk)
    assert key.project_name == key_from_db.project_name

    # change a field and save it.
    with reversion.create_revision():
        key_from_db.project_name = "updated name"
        key_from_db.save()
        reversion.set_date_created(datetime(2017, 5, 15, tzinfo=pytz.UTC))

    # change a field again and save it.
    with reversion.create_revision():
        key_from_db.project_name = "no name"
        key_from_db.save()
        reversion.set_date_created(datetime(2017, 6, 1, tzinfo=pytz.UTC))

    # create an unrelated project with just one revision.
    with reversion.create_revision():
        unrelated_key = mommy.make(Project, project_name="unrelated project")
        reversion.set_date_created(datetime(2017, 7, 30, tzinfo=pytz.UTC))

    # refresh the value from the database.
    key.refresh_from_db()

    # django sanity check: the first object should equal the new one.
    assert key.project_name == "no name"
    assert key_from_db.project_name == "no name"

    # Get all the revisions for all projects.
    all_versions = Version.objects.get_for_model(Project)
    assert len(all_versions) == 4

    # Get only the revisions for the one that we made 3 revisions for.
    # (excludes the unrelated project.)
    versions = Version.objects.get_for_object(key)
    assert len(versions) == 3
