import os

from Jumpscale import j

JSBASE = j.application.JSBaseClass


class Quake3(j.application.JSBaseClass):

    def __init__(self):
        self.__jslocation__ = "j.tutorials.quake3"
        self.name = "quake3"
        JSBASE.__init__(self)

    def run(self, pk_location="/tmp/pak0.pk3"):
        """
        Create and run a quake3 server
        kosmos 'j.tutorials.quake3.run()'

        :param pk_location: local location of pak0.pk3 from your legally bought software
        :type pk_location: string
        :return: quake3 server url
        """
        if not j.clients.zos.exists("tutorials"):
            raise RuntimeError("zos client tutorials doesn't exist")
        print("** Ping node")
        node = j.clients.zos.get("tutorials")
        node.client.ping()

        print("## Create volume quake3 on storage pool zos-cache")
        pool = node.storagepools.get('zos-cache')
        volume = pool.create(self.name)

        pk = volume.path+'/pak0.pk3'
        print("** Upload pk to {}".format(pk))
        content = j.sal.fs.readFile(pk_location, binary=True)
        node.upload_content(pk, content)

        cfg = volume.path+'/my-server.cfg'
        print("## Upload server config to {}".format(cfg))
        config = j.sal.fs.readFile(os.path.dirname( os.path.realpath(__file__)) + '/quake3-server.cfg')
        node.upload_content(cfg, config)

        print("** Create container quake3 on node")
        quake3 = node.containers.create(
            # the name of the container
            name=self.name,
            # the URL that points to the flist you want to use
            flist='https://hub.grid.tf/glendc/glendc-quake3-latest.flist',
            # the UDP port that is to be exposed
            ports={"27960|udp":27960},
            # volume we wish to mount, so that the container has
            # access to our custom server-config and pak0.pk3 file
            mounts={volume.path: '/data'},
        )
        quake3_public_url = "%s:27960" % node.host
        print("## Quake3 server is now running on {}".format(quake3_public_url))

        return quake3_public_url

    def cleanup(self):
        """
        Cleanup a previous run of the tutorial by stopping the created container and removing the storagepool volume.
        """
        node = j.clients.zos.get("tutorials")
        try:
            node.containers.get(self.name).stop()
            pool = node.storagepools.get('zos-cache')
            volume = pool.get(self.name)
            volume.delete()
        except LookupError:
            pass
