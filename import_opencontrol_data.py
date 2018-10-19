from io import BytesIO
import os
import requests
import sys
import yaml
import zipfile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings") # magic that manage.py does
import django
django.setup()
from scorecard.models import *


def fetch_zip_archive_and_extract_yaml_files(url):
    response = requests.get(url)
    bio = BytesIO(response.content)
    z = zipfile.ZipFile(bio)
    ret = {}
    for path in z.namelist():
        if not path.endswith('.yaml') or path.endswith('opencontrol.yaml'):
            # not a file we care about
            continue
        y = yaml.load(z.open(path))
        filename = path.split('/')[-1]
        label = filename[:-5] # chop off the '.yaml'
        ret[label] = y
    return ret


def import_standard(standard_label, definition):
    standard, _ = Standard.objects.get_or_create(label=standard_label, name=definition['name'])
    standard.save()

    # The other keys in the standard definition are all controls
    del definition['name']

    for control_label in definition.keys():
        control = definition[control_label]
        # yaml automatically converts to numbers if possible, we want it to always be a string
        control_label = str(control_label)
        family, _ = ControlFamily.objects.get_or_create(label=control['family'])
        family.save()

        name = control['name']
        con, _ = Control.objects.get_or_create(label=control_label, name=name, standard=standard, family=family)
        con.save()


def import_system(definition):
    product, _ = Product.objects.get_or_create(name=definition['name'])
    product.save()

    for control in definition['satisfies']:
        standard = Standard.objects.get(name=control['standard_key'])
        try:
            cont_obj = Control.objects.get(standard=standard, label=control['control_key'])
        except:
            continue # TODO: we don't know about this control yet?!
        product_control, _ = ProductControl.objects.get_or_create(product=product, control=cont_obj)
        product_control.status = control['implementation_status']
        product_control.save()


# Import Standards
OC_STANDARDS = 'https://github.com/opencontrol/standards/archive/master.zip'
standards = fetch_zip_archive_and_extract_yaml_files(OC_STANDARDS)
for standard in standards:
    import_standard(standard, standards[standard])


# TODO: Import Certifications
#OC_CERTIFICATIONS = 'https://github.com/opencontrol/certifications/archive/master.zip'

# Import the stable 'opencontrol' branch of our ComplianceAsCode repo
REDHAT_OPENCONTROL = 'https://github.com/ComplianceAsCode/redhat/archive/opencontrol.zip'
systems = fetch_zip_archive_and_extract_yaml_files(REDHAT_OPENCONTROL)
for system in systems:
    import_system(systems[system])


