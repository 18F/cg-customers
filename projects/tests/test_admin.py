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
    This test checks that between revisions of projects, you can see the
    difference in associated packages.
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
        key = mommy.make(Project, project_name="first name", package_type_id=pkg1.id)
        reversion.set_date_created(datetime(2017, 4, 30, tzinfo=pytz.UTC))
    # try to get the object from the database.
    key_from_db = Project.objects.get(pk=key.pk)
    assert key.project_name == key_from_db.project_name
    assert key.package_type_id == pkg1.id

    # change a field and save it.
    with reversion.create_revision():
        key_from_db.project_name = "updated name"
        key_from_db.package_type_id=pkg2.id
        key_from_db.save()
        reversion.set_date_created(datetime(2017, 5, 15, tzinfo=pytz.UTC))

    # change a field again and save it.
    with reversion.create_revision():
        key_from_db.project_name = "no name"
        key_from_db.package_type_id=pkg2.id
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
    assert key.package_type_id == pkg2.id
    assert key_from_db.project_name == "no name"
    assert key_from_db.package_type_id == pkg2.id

    # Get all the revisions for all projects.
    all_versions = Version.objects.get_for_model(Project)
    assert len(all_versions) == 4

    # Get only the revisions for the one that we made 3 revisions for.
    # (excludes the unrelated project.)
    versions = Version.objects.get_for_object(key)
    assert len(versions) == 3

    filtered_versions = get_active_projects_for_date_range(
        datetime(2017, 5, 1, tzinfo=pytz.UTC),
        datetime(2017, 6, 1, tzinfo=pytz.UTC),
        versions)
    assert len(filtered_versions) == 2
    # First one is the one from 5/15 which changed to package 2.
    assert filtered_versions[0].field_dict["project_name"] == "updated name"
    assert filtered_versions[0].field_dict["package_type_id"] == pkg2.id
    # Second one is the one from 4/30 which was at pkackage 1.
    # We return this one because it was the package that was still active as of
    # May 1st.
    assert filtered_versions[1].field_dict["project_name"] == "first name"
    assert filtered_versions[1].field_dict["package_type_id"] == pkg1.id


def get_active_projects_for_date_range(start, end, versions):
    """
    get_active_projects_for_date_range will return a list of sorted projects
    that represent which projects were active throughout the range.

    The start date is inclusive and the end date is not inclusive.

    Example given May 1 - June 1, it will get all the projects in that range.
    However, if there is a project that existed before the range
    (e.g. project last changed on April 15) and that project was not changed on
    May 1, this function will pull in that previous project (April 15)
    because it was the active project as-of May 1st.
    """
    filtered_versions = [version for version in versions
        if start <= version.revision.date_created < end]
    if len(filtered_versions) > 0:
        # Get the last element (which is the first revision)
        # within the date range.
        first_revision = filtered_versions[len(filtered_versions)-1]
        if start <= first_revision.revision.date_created < (start + timedelta(days=1)):
            # the revision was created within the first day of our start date.
            # (currently, the resolution of changes we want is per day).
            # in this case, there's nothing else to do.
            pass
        else:
            # we may need to look earlier for what was previous config.
            for version in versions:
                if version.revision.date_created < start:
                    filtered_versions.append(version)
                    break
    return filtered_versions
