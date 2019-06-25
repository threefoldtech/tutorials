from Jumpscale import j

JSBASE = j.application.JSBaseClass


class OwnHub(j.application.JSBaseClass):
    def __init__(self):
        self.__jslocation__ = "j.tutorials.ownhub"
        self.name = "ownhub"
        JSBASE.__init__(self)

    def run(self):
        """
        Run
        """

        """
        Creating the own-hub flist
        optional tutorial: prerequisit = zhub_client with name tutorials with a token_ by iyo
        1.Generate flist (using builder)
            - Build & install using hub builder
            - sandbox using hub builder
        2. Merge flist created with JSX flist

        Deploy ownhub on a container locally with the merged flist
        1. Create a new container with the merged flist, pass params for IP_PORT
        2. Use it (access it) with IP_node:5555 from the browser

        Using the own-hub
        1. Access the hub with IP_node:5555 from the browser
        2. Use as a regular hub to upload flist {example}

        """
        # TODO validation on inputs

        # TODO if condition to start the ownhub locally without using an flist or creating container
        # setup_mode = input(
        #     """
        # Please choose and enter the mode of setup:
        #     1- On a new container
        #     2- Local on current system
        # """
        # )
        # if setup_mode == 1:
        # elif setup_mode == 2:
        # else:

        merged_flist = input("Do you have a ready flist of the ownHub to create the container with locally (y/n)? ")
        if merged_flist == "y":
            flist_root_url = input("First enter the link to the merged flist: ")
            ip_node = input("Then enter the node's IP to create the container on locally ")
            self.create_container(flist_root_url, ip_node)
            print("Done and ownhub available at %s:5555" % ip_node)
            return

        print("Initially 0-hub client will be installed to be used to create flists")
        print("pip3 install -e 'git+https://github.com/threefoldtech/0-hub#egg=zerohub&subdirectory=client'")
        print("Installing zerohub...")
        cmd = "pip3 install -e 'git+https://github.com/threefoldtech/0-hub#egg=zerohub&subdirectory=client'"
        j.sal.process.execute(cmd)
        input("Enter any key for the next step! ")

        # Creating zhub client instance
        if not j.clients.zhub.exists("tutorials"):
            generate_zhub = input("No 0-hub client was found. Do you want to continue to create 0-hub client (y/n)? ")
            if generate_zhub == "y":
                # TODO
                # get iyo params (client_secr, client id)
                iyo_client_id = input("Provide itsyouonline application id: ")
                iyo_client_secret = input("Provide itsyouonline corresponding secret: ")
                # get iyo client
                print(
                    '>> iyo_client = j.clients.itsyouonline.get("tutorials", application_id=iyo_client_id, secret=iyo_client_secret)'
                )
                print("**Creating itsyouonline client using the following command...")
                iyo_client = j.clients.itsyouonline.get(
                    "tutorials",
                    baseurl="https://itsyou.online/api",
                    application_id=iyo_client_id,
                    secret=iyo_client_secret,
                )
                print("**Created itsyouonline client...")
                print(iyo_client)

                input("Enter any key for the next step! *generate token* \n")
                print(">> token = iyo.jwt_get().jwt")
                print("Generating token from itsyouonline client to be used for authenticating zhub client\n\n\n")
                token = iyo_client.jwt_get().jwt

                # generate zhub client with name tutorials
                input("Enter any key for the next step! *zhub client* \n")
                print('>> zhub_client = j.clients.zhub.get("tutorials", token_=token)')
                print("**Creating 0-hub client...\n\n\n")
                zhub_client = j.clients.zhub.get("tutorials", token_=token)

                input("Enter any key for the next step! *authenticate zhub client*")
                print(">> zhub_client.authenticate()")
                print("Authenticating 0-hub client to be used...")
                zhub_client.authenticate()
                print("0-hub client ready to be used\n\n\n")

            else:
                raise RuntimeError("0-hub client required to continue the tutorial")

        if not zhub_client:
            zhub_client = j.clients.zhub.get("tutorials")

        # Sandbox hub
        input("Enter any key for the next step! *create sandbox*")
        print("Build, install, then sandbox your ownHub's flist to be used locally")
        print("Sandbox ownHub and upload to hub.grid.tf to merge with jumpscale flist")
        print(">> j.builders.apps.hub.sandbox(zhub_client=zhub_client, flist_create=True, reset=True) ")
        print(
            """
        The sandbox function invokes multiple other functions to generate the flist:
            - build: downloads and builds from source code the binaries required to be added in the flist (including dependencies)
            - install: copies the binaries to proper locations locally (in /sandbox directory) and makes any required configurations
            - sandbox: sandbox all the needed files and configurations and creates an flist that is uploaded to the remote hub
        Creating flist and uploading flist to hub.grid.tf ...
        """
        )
        j.builders.apps.hub.sandbox(zhub_client=zhub_client, flist_create=True, reset=True)
        print(
            "Flist created and uploaded on https://hub.grid.tf/HUB_USERNAME/zerohub.flist where HUN_USERNAME is your username on hub.grid.tf\n\n\n"
        )

        # Merge flist with jumpscale flist
        input("Enter any key for the next step! ")
        print(
            """
        Now you should merge the flist generated with a jumpscale flist!
        You can do the merge manually by visiting https://hub.grid.tf/merge

        based on: https://hub.grid.tf/HUB_USERNAME/zerohub.flist
        merge with:  https://hub.grid.tf/tf-autobuilder/threefoldtech-jumpscaleX-autostart-development.flist

        

        Once the merge is done, get the url created for the merged flist to create a container with it.
        """
        )

        # Create container
        flist_root_url = input("Enter the url once you have recieved the merged flist's url!")
        counter = 0
        while not flist_root_url and counter < 6:
            flist_root_url = input("Enter again the merged flist's url!")
            counter += 1
        ip_node = input("Then enter the node's IP to create the container on locally ")
        self.create_container(flist_root_url, ip_node)

        print("Done and ownhub available at %s:5555" % ip_node)
        print("Congratulations you now have your own hub!")

    def create_container(self, root_url, ip_node):
        cl = j.clients.zos.get("zhub", host=ip_node)

        cl.client.container.create(
            name="tutorials",
            root_url="your_flist_after_merge",
            nics=[{"type": "default", "name": "defaultnic", "id": " None"}],
            port={2015: 2015, 8080: 80, 5555: 5555},
            env={"IP_PORT": ip_node + ":5555"},
        ).get()

    def cleanup(self):
        """
        Cleanup a previous run of the tutorial
        """
        if j.clients.iyo.exists("tutorials"):
            j.clients.iyo.exists("tutorials").delete()

        j.clients.zhub.get("tutorials").delete()
        j.builders.hub.reset()

