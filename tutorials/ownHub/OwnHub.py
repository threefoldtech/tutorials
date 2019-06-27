from Jumpscale import j

JSBASE = j.application.JSBaseClass


class OwnHub(j.application.JSBaseClass):
    def __init__(self):
        self.__jslocation__ = "j.tutorials.ownhub"
        self.name = "ownhub"
        JSBASE.__init__(self)
        # font style
        self.CEND = "\33[0m"
        self.CBOLD = "\33[1m"
        # font colors
        self.CRED = "\33[31m"
        self.CGREEN = "\33[32m"
        self.CYELLOW = "\33[33m"
        self.CGREY = "\33[90m"
        self.CWHITE2 = "\33[97m"

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
        print(
            self.CBOLD
            + self.CGREEN
            + """This tutorial will guide you build, install, sandbox builders with your own hub\n"""
        )

        ownhub_instance = input(self.CBOLD + self.CWHITE2 + "Do you have your instance of ownhub (y/[n])?")

        if ownhub_instance == "y":
            print(self.CEND + self.CGREEN + "\nDeploying the hub on local container\n")
            self._builder_example()
            return

        setup_mode = input(
            self.CBOLD
            + self.CWHITE2
            + """\nPlease choose and enter the mode of setup your ownhub:
            1- Local on current system (This will build, install, start ownhub server will take a few minutes)
            2- On a remote zos container (This will deploy ownhub on a zos container, you must have zos's node's ip)
            Choose (default 2): """
        )
        if setup_mode == "1":
            self._ownhub_local()
            self._builder_example()
            return

        ## zhub client
        zhub_client = self._create_zhub_client()
        ## sandbox hub
        self._ownhub_sandbox(zhub_client)
        ## builder example
        self._builder_example()

    # create zhubclient with its you online secret and id
    def _create_zhub_client(self):
        print(self.CEND + self.CGREEN + "\nInitially 0-hub client will be installed to be used to create flists\n")
        print(
            self.CEND
            + self.CYELLOW
            + ">> pip3 install -e 'git+https://github.com/threefoldtech/0-hub#egg=zerohub&subdirectory=client'\n"
        )
        print(self.CEND + self.CGREY + "Installing zerohub...")
        cmd = "pip3 install -e 'git+https://github.com/threefoldtech/0-hub#egg=zerohub&subdirectory=client'"
        j.sal.process.execute(cmd)
        input(self.CBOLD + self.CWHITE2 + "\nEnter any key for the next step: (Creating zhub client instance) \n")
        # Creating zhub client instance
        if not j.clients.zhub.exists("tutorials"):
            generate_zhub = input(
                self.CBOLD
                + self.CWHITE2
                + "No 0-hub client was found. Do you want to continue to create 0-hub client ([y]/n)? "
            )
            if not generate_zhub == "n":
                # get iyo params (client_secr, client id)
                iyo_client_id = input("\nProvide itsyouonline application id: ")
                iyo_client_secret = input("Provide itsyouonline corresponding secret: ")
                # get iyo client
                print(self.CEND + self.CGREEN + "\nCreating itsyouonline client using the following command...")
                print(
                    self.CEND
                    + self.CYELLOW
                    + '\n>> iyo_client = j.clients.itsyouonline.get("tutorials", application_id=iyo_client_id, secret=iyo_client_secret)\n'
                )
                iyo_client = j.clients.itsyouonline.get(
                    "tutorials",
                    baseurl="https://itsyou.online/api",
                    application_id=iyo_client_id,
                    secret=iyo_client_secret,
                )
                iyo_client.save()
                print("**Created itsyouonline client...")
                print(iyo_client)

                input(self.CBOLD + self.CWHITE2 + "Enter any key for the next step: (generate token) \n")
                print(
                    self.CEND
                    + self.CGREEN
                    + "Generating token from itsyouonline client to be used for authenticating zhub client\n"
                )
                print(self.CEND + self.CYELLOW + ">> token = iyo.jwt_get().jwt\n")
                token = iyo_client.jwt_get().jwt

                # generate zhub client with name tutorials
                input(self.CBOLD + self.CWHITE2 + "Enter any key for the next step: (zhub client) \n")
                print(self.CEND + self.CGREEN + "\n**Creating 0-hub client...\n")
                print(self.CEND + self.CYELLOW + '>> zhub_client = j.clients.zhub.get("tutorials", token_=token)\n')
                zhub_client = j.clients.zhub.get("tutorials", token_=token)
                zhub_client.save()
                input(self.CBOLD + self.CWHITE2 + "Enter any key for the next step: (authenticate zhub client)\n")
                print(self.CEND + self.CGREEN + "Authenticating 0-hub client to be used...\n")
                print(self.CEND + self.CYELLOW + ">> zhub_client.authenticate()\n")
                zhub_client.authenticate()
                print(self.CEND + self.CGREEN + "0-hub client ready to be used\n")
            else:
                raise RuntimeError("0-hub client is exists required to continue the tutorial please run cleanup")
            return zhub_client

    # creat ownhub on local machine
    def _ownhub_local(self):
        print(self.CEND + self.CGREEN + "\nDeploying the hub on local container\n")
        docker_ip = input(self.CBOLD + self.CWHITE2 + "Please input your docker ip: ")
        print(self.CEND + self.CYELLOW + '\n>> j.builders.apps.hub.in_docker("%s")\n' % docker_ip)
        j.builders.apps.hub.in_docker(docker_ip)
        input(self.CBOLD + self.CWHITE2 + "Enter any key for the next step: (Install ownhub) \n")
        print(self.CEND + self.CYELLOW + ">> j.builders.apps.hub.install(reset=True)\n")
        print(self.CGREY)
        j.builders.apps.hub.install(reset=True)
        input(self.CBOLD + self.CWHITE2 + "Enter any key for the next step: (Start ownhub) \n")
        print(self.CEND + self.CYELLOW + ">> j.builders.apps.hub.start()\n")
        j.builders.apps.hub.start()
        print(self.CBOLD + self.CGREEN + "\nDone and ownhub available at http://%s:5555\n" % docker_ip)
        print(self.CBOLD + self.CGREEN + "Congratulations you now have your own hub!\n")

    # make an flist from ownhub
    def _ownhub_sandbox(self, zhub_client):
        merged_flist = input(
            self.CBOLD
            + self.CWHITE2
            + "Do you have a ready flist of the ownHub to create the container with locally (y/[n])? "
        )
        if merged_flist == "y":
            flist_root_url = input("First enter the link to the merged flist: ")
            ip_node = input("Then enter the node's IP to create the container on: ")
            jwt = input("Then enter the node's jwt if required: ")
            self._create_container(flist_root_url, ip_node, jwt)
            print("Done and ownhub available at http://%s:5555" % ip_node)
            print(
                self.CBOLD
                + self.CGREEN
                + "Congratulations you now have your zos container with odoo!, wait for it initalize then use it\n"
            )
            return

        # Sandbox hub
        input(self.CBOLD + self.CWHITE2 + "Enter any key for the next step: (create sandbox)\n")
        print(self.CEND + self.CGREEN + "\nBuild, install, then sandbox your ownHub's flist to be used locally\n")
        print(self.CEND + self.CGREEN + "Sandbox ownHub and upload to hub.grid.tf to merge with jumpscale flist")
        print(
            self.CEND
            + self.CYELLOW
            + "\n>> j.builders.apps.hub.sandbox(zhub_client=zhub_client, flist_create=True, reset=True)\n"
        )
        print(
            self.CEND
            + self.CGREEN
            + """The sandbox function invokes multiple other functions to generate the flist:
        - build: downloads and builds from source code the binaries required to be added in the flist (including dependencies)
        - install: copies the binaries to proper locations locally (in /sandbox directory) and makes any required configurations
        - sandbox: sandbox all the needed files and configurations and creates an flist that is uploaded to the remote hub
        Creating flist and uploading flist to hub.grid.tf ...
        """
        )
        j.builders.apps.hub.sandbox(zhub_client=zhub_client, flist_create=True, reset=True)

        print(
            self.CEND
            + self.CGREEN
            + "\nFlist created and uploaded on https://hub.grid.tf/HUB_USERNAME/zerohub.flist where HUN_USERNAME is your username on hub.grid.tf\n\n\n"
        )

        # Merge flist with jumpscale flist
        input(self.CBOLD + self.CWHITE2 + "\nEnter any key for the next step: (Merge flist with jumpscale flist)\n")
        print(
            self.CEND
            + self.CGREEN
            + """Now you should merge the flist generated with a jumpscale flist!
        You can do the merge manually by visiting https://hub.grid.tf/merge

        based on: https://hub.grid.tf/HUB_USERNAME/zerohub.flist
        merge with:  https://hub.grid.tf/tf-autobuilder/threefoldtech-jumpscaleX-autostart-development.flist

        

        Once the merge is done, get the url created for the merged flist to create a container with it./n
        """
        )

        # Create container
        flist_root_url = input(
            self.CBOLD + self.CWHITE2 + "\nEnter the url once you have recieved the merged flist's url!\n"
        )
        counter = 0
        while not flist_root_url and counter < 6:
            flist_root_url = input(self.CBOLD + self.CWHITE2 + "\nEnter again the merged flist's url!\n")
            counter += 1
        ip_node = input(self.CBOLD + self.CWHITE2 + "Then enter the node's IP to create the container on")
        jwt = input("Then enter the node's jwt if required: ")
        self._create_container(flist_root_url, ip_node, jwt)

        print(self.CBOLD + self.CGREEN + "\nDone and ownhub available at http://%s:5555\n" % ip_node)
        print(
            self.CBOLD + self.CGREEN + "Congratulations you now have your own hub!, wait for it initalize then use it\n"
        )

    # deploy on a container
    def _create_container(self, root_url, ip_node, jwt):
        print(self.CEND + self.CGREEN + "\nCreating a zos container\n")
        print(self.CEND + self.CYELLOW + 'cl = j.clients.zos.get("zhub", host=ip_node, password=jwt)\n')
        cl = j.clients.zos.get("zhub", host=ip_node, password=jwt)
        print(
            self.CEND
            + self.CYELLOW
            + """cl.client.container.create(
            name="tutorials",
            root_url=root_url,
            nics=[{"type": "default", "name": "defaultnic", "id": " None"}],
            port={5555: 5555},
            env={"IP_PORT": ip_node + ":5555"},
            ).get()
        """
        )
        cl.client.container.create(
            name="tutorials",
            root_url=root_url,
            nics=[{"type": "default", "name": "defaultnic", "id": " None"}],
            port={5555: 5555, 8069: 8069},
            env={"IP_PORT": ip_node + ":5555"},
        ).get()

    # builder lifecycle example
    def _builder_example(self):
        # intro
        print(self.CBOLD + self.CYELLOW + "OK, now we have our ownhub - we will use it to build/deploy odoo builder\n")
        odoo_ip = input(self.CBOLD + self.CWHITE2 + "Please input your docker ip: ")
        print(
            self.CEND
            + self.CGREEN
            + "\nIn this part we will take `builder odoo` as an example, we will go through its life cycles\n"
        )
        input(self.CBOLD + self.CWHITE2 + "\nPress enter to the next part: Installation\n")
        # install
        print(self.CEND + self.CGREEN + "\nInstall Method calls build at first- this may take a few minutes\n")
        print(self.CEND + self.CYELLOW + "\n>> j.builders.apps.odoo.install()\n")
        input(self.CBOLD + self.CWHITE2 + "\nPress enter to install\n")
        j.builders.apps.odoo.install(reset=True)
        # test
        # input(self.CBOLD + self.CWHITE2 + "\nPress enter to the next part: Test the installation\n")
        # print(self.CEND + self.CYELLOW + "\n>> j.builders.apps.odoo.test()\n")
        # j.builders.apps.odoo.test()
        # start
        input(self.CBOLD + self.CWHITE2 + "\nPress enter to the next part: starting the server\n")
        print(self.CEND + self.CYELLOW + "\n>> j.builders.apps.odoo.start()\n")
        j.builders.apps.odoo.start()
        print(self.CBOLD + self.CGREEN + "\nCongratulations now you have Odoo check it on http://%s:8069\n" % odoo_ip)
        # sandbox
        input(
            self.CBOLD
            + self.CWHITE2
            + "Press enter to the next part: sandboxing and making an flist to deploy it on a remote zos container\n"
        )
        # now we have odoo flist, deploying it on a remote node
        merged_flist = input(
            self.CBOLD + self.CWHITE2 + "Do you have a ready flist of the odoo to create the zos container (y/[n])? "
        )
        if merged_flist == "y":
            flist_url = input("First enter the link to the merged flist: ")
            ip_node = input("Then enter the node's IP to create the container on ")
            jwt = input("Then enter the node's jwt if required: ")
            self._create_container(flist_url, ip_node, jwt)
            print(self.CBOLD + self.CGREEN + "Done and odoo available at http://%s:8069" % ip_node)
            return

        hub_name = input(
            self.CBOLD
            + self.CWHITE2
            + """Do you want to generate the flist using 
            1- zhub
            2- ownhub
            choose (1/[2])? """
        )
        if hub_name == "1":
            zhub_client = self._create_zhub_client()
            j.builders.apps.odoo.sandbox(zhub_client=zhub_client, flist_create=True, reset=True)

            print(
                self.CEND
                + self.CGREEN
                + "\nFlist created and uploaded on https://hub.grid.tf/HUB_USERNAME/odoo.flist where HUN_USERNAME is your username on hub.grid.tf\n\n\n"
            )

            # Merge flist with jumpscale flist
            input(self.CBOLD + self.CWHITE2 + "\nEnter any key for the next step: (Merge flist with jumpscale flist)\n")
            print(
                self.CEND
                + self.CGREEN
                + """Now you should merge the flist generated with a jumpscale flist!
            You can do the merge manually by visiting https://hub.grid.tf/merge

            based on: https://hub.grid.tf/HUB_USERNAME/odoo.flist
            merge with:  https://hub.grid.tf/tf-autobuilder/threefoldtech-jumpscaleX-autostart-development.flist

            Once the merge is done, get the url created for the merged flist to create a container with it./n
            """
            )

        else:
            print(self.CEND + self.CYELLOW + "\n>> j.builders.apps.odoo.sandbox()\n")
            own_hub_client = j.clients.zhub.get("tutorials", url="http://%s:5555/api" % odoo_ip)
            j.builders.apps.odoo.sandbox(zhub_client=own_hub_client, flist_create=True, reset=True)
            print(
                self.CEND
                + self.CGREEN
                + """\n
            Now you should merge the flist generated with a jumpscale flist!
            at: http://{odoo_ip}:5555
            You can do the merge manually by visiting https://{odoo_ip}:5555/merge

            based on: https://{odoo_ip}/Administrator/odoo.flist
            merge with:  https://hub.grid.tf/tf-autobuilder/threefoldtech-jumpscaleX-autostart-development.flist

            Once the merge is done, get the url created for the merged flist to create a container with it.\n
            """.format(
                    odoo_ip=odoo_ip
                )
            )

        # Create container
        flist_root_url = input(
            self.CBOLD + self.CWHITE2 + "\nEnter the url once you have recieved the merged flist's url!\n"
        )
        counter = 0
        while not flist_root_url and counter < 6:
            flist_root_url = input(self.CBOLD + self.CWHITE2 + "\nEnter again the merged flist's url!\n")
            counter += 1
        ip_node = input(self.CBOLD + self.CWHITE2 + "\nThen enter the node's IP to create the container on")
        jwt = input("Then enter the node's jwt if required: ")
        self._create_container(flist_root_url, ip_node, jwt)
        print(self.CBOLD + self.CGREEN + "\nDone and your odoo available at http://%s:8069\n" % ip_node)
        print(
            self.CBOLD
            + self.CGREEN
            + "Congratulations you now have your zos container with odoo!, wait for it initalize then use it\n"
        )

    # delete all stuff
    def cleanup(self):
        """
        Cleanup a previous run of the tutorial
        """
        if j.clients.itsyouonline.exists("tutorials"):
            j.clients.itsyouonline.delete("tutorials")

        if j.clients.zhub.exists("tutorials"):
            j.clients.zhub.delete("tutorials")

        j.builders.apps.hub.stop()
        j.builders.apps.hub.reset()

        if j.clients.zos.exists("tutorials"):
            j.clients.zos.get("zhub").containers.get("tutorials").stop()
