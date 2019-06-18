from Jumpscale import j

JSBASE = j.application.JSBaseClass


class Filestash(j.application.JSBaseClass):

    def __init__(self):
        self.__jslocation__ = "j.tutorials.filestash"
        self.name = "filestash"
        JSBASE.__init__(self)

    def run(self):
        """
        Create and run a filestash server
        kosmos 'j.tutorials.filestash.run()'
        :return: filestash and minio servers url
        """
        if not j.clients.zos.exists("tutorials"):
            raise RuntimeError("zos client tutorials doesn't exist")
        print("** Ping node")
        node = j.clients.zos.get("tutorials")
        node.client.ping()

        print("## Create volume filestash on storage pool zos-cache")
        pool = node.storagepools.get('zos-cache')
        volume = pool.create(self.name)

        print("** Create container filestash on node")
        quake3 = node.containers.create(
            # the name of the container
            name=self.name,
            # the URL that points to the flist you want to use
            flist='https://hub.grid.tf/tf-official-apps/filestash_with_minio_autostart.flist',
            # the ports that will be exposed
            ports={"9000": 9000, "8334": 8334},
            # volume we wish to mount, so that the container has
            # access to our custom server-config and pak0.pk3 file
            mounts={volume.path: '/data'},
            env= {
                "MINIO_ACCESS_KEY": "minio_admin",
                "MINIO_SECRET_KEY": "minio_password",
        })
        filestash_url = "%s:8334" % node.host
        minio_url = "%s:9000" % node.host
        print("## Filestash server is now running on {} and minio is running on {}".format(filestash_url, minio_url))

        return filestash_url, minio_url

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
