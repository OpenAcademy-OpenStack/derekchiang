from glanceclient import Client as GlanceClient
from novaclient.v1_1.client import Client as NovaClient
from keystoneclient.v2_0.client import Client as KeystoneClient
import simplejson as json


def read_config(filename):
    with open(filename) as f:
        return json.loads(f.read())

if __name__ == '__main__':
    config = read_config("config.json")
    keystone = KeystoneClient(username=config['username'],
                              password=config['password'],
                              auth_url=config['authUrl'],
                              tenant_name=config['tenantName'])
    glance = GlanceClient('1', endpoint=config[
        'glancePublicUrl'], token=keystone.auth_token)
    nova = NovaClient(config['username'], config['password'],
                      config['tenantName'], auth_url=config['authUrl'])

    for flavor in nova.flavors.list():
        print flavor

    # Use the first flavor by default
    # fl = nova.flavors.list()[0]
    # for image in glance.images.list():
    #     if 'ubuntu' in image.name:
    #         with open(config['userdata']) as f:
    #             nova.servers.create(name=image.name,
    #                                 image=image.id, flavor=fl,
    #                                 userdata=f)
    #         while True:
    #             for s in nova.servers.list():
    #                 if s.name == image.name and s.status != 'BOOTING':
    #                     break
    #             time.sleep(5)
    # time.sleep(10)  # Wait for the ping script to complete

    #         return
