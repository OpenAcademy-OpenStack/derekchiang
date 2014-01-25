from glanceclient import Client as GlanceClient
from novaclient.v1_1.client import Client as NovaClient
import simplejson as json


def read_config(filename):
    with open(filename) as f:
        return json.loads(f.read())

if __name__ == '__main__':
    config = read_config("config.json")
    glance = GlanceClient('1', endpoint=config[
        'glancePublicUrl'], token=config['authToken'])
    nova = NovaClient(config['username'], config['password'],
                      config['tenantName'], auth_url=config['authUrl'])

    fl = nova.flavors.list()[0]
    for image in glance.images.list():
        if 'ubuntu' in getattr(image, 'name'):
            nova.servers.create(name=getattr(image, 'name'),
                                image=getattr(image, 'id'), flavor=fl)

