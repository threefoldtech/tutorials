from Jumpscale import j

JSBASE = j.application.JSBaseClass


class OwnHub(j.application.JSBaseClass):
    def __init__(self):
        """
        used colors and styles
        # font style
            self._CEND = "\33[0m"
            self._CBOLD = "\33[1m"
            # font colors
            self._CRED = "\33[31m"
            self._CGREEN = "\33[32m"
            self._CYELLOW = "\33[33m"
            self._CGREY = "\33[90m"
            self._CWHITE2 = "\33[97m"
        """
        self.__jslocation__ = "j.tutorials.ownhub"
        self.name = "ownhub"
        JSBASE.__init__(self)

    ## Entry point
    def run(self):
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
        # Begining
        self._print_headline(
            """ This tutorial will guide you build, install, sandbox builders with your own hub or zhub """
        )

        # Ask for ownhub instance
        ownhub_instance = self._get_input("Do you have an instance of ownhub (y/[n])? ")

        if ownhub_instance == "y":
            self._builder_example()
            return

        # ownhub on system or remote machine
        ownhub_loc_text = """Please choose and ENTER the mode of setup your ownhub:
            1- Local on current system (This will build, install, start ownhub server .. It will take few minutes)
            2- On a remote zos container (This will deploy ownhub on a zos container, you must have zos-node's ip)
            Choose (default 2): """

        setup_mode = self._get_input(ownhub_loc_text)

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

    ## helper styling functions
    def _get_input(self, text, color="\33[97m", style="\33[1m"):
        """
        for input from user Text color: self._CWHITE2 - Text style: self._CBOLD
        : param color: defines text color
        : param style: defines text style
        : check:
        : https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python for more 
        """
        input_from_user = input(style + color + "\n" + text + " ")
        return input_from_user

    def _print_headline(self, text, color="\33[32m", style="\33[1m"):
        """
        print headline texts Text color: self._CGREEN - Text style: self._CBOLD
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n***" + text + "***")

    def _print_headline2(self, text, color="\33[33m", style="\33[1m"):
        """
        print headline texts Text color: self._CYELLOW - Text style: self._CBOLD
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n" + text)

    def _print_command(self, text, color="\33[33m", style="\33[0m"):
        """
        print command before execution: self._CYELLOW - Text style: self._CEND
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n>> " + text)

    def _print_explain(self, text, color="\33[32m", style="\33[0m"):
        """
        print explinations to some commands: self._CGREEN - Text style: self._CEND
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n" + text)

    def _print_execution(self, text, color="\33[90m", style="\33[0m"):
        """
        print execution log for commands: self._CGREY - Text style: self._CEND
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n" + text)

    def _print_warining(self, text, color="\33[31m", style="\33[1m"):
        """
        print warnings for dangerous commands: self._CRED - Text style: self._CBOLD
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n***" + text + "***")

    ## helper core functions
    # zhub client
    def _create_zhub_client(self):
        """
        create zhubclient with its you online secret and id
        """
        self._print_explain("Initially 0-hub client will be installed to be used to create flists")

        # install zos zhub client
        zhub_install_cmd = (
            "pip3 install -e 'git+https://github.com/threefoldtech/0-hub#egg=zerohub&subdirectory=client'"
        )
        self._print_command(zhub_install_cmd)
        j.sal.process.execute(zhub_install_cmd)

        self._get_input("ENTER any key for the next step: (Creating zhub client instance)... ")

        # Creating zhub client instance
        if not j.clients.zhub.exists("tutorials"):
            # generate zhub
            zhub_gen_text = "No 0-hub client was found. Do you want to continue to create 0-hub client ([y]/n)? "
            generate_zhub = self._get_input(zhub_gen_text)

            if not generate_zhub == "n":
                # get iyo params (client_secr, client id)
                iyo_client_id = self._get_input("Provide itsyouonline application id: ")
                iyo_client_secret = self._get_input("Provide itsyouonline corresponding secret: ")

                self._print_explain("Creating itsyouonline client using the following command... ")

                self._print_command(
                    """iyo_client = j.clients.itsyouonline.get("tutorials", application_id=iyo_client_id, secret=iyo_client_secret)"""
                )
                iyo_client = j.clients.itsyouonline.get(
                    "tutorials",
                    baseurl="https://itsyou.online/api",
                    application_id=iyo_client_id,
                    secret=iyo_client_secret,
                )
                iyo_client.save()
                self._print_execution(iyo_client)

                self._get_input("ENTER any key for the next step: (generate token)... ")

                self._print_explain(
                    "Generating token from itsyouonline client to be used for authenticating zhub client"
                )

                self._print_command("token = iyo.jwt_get().jwt")
                token = iyo_client.jwt_get().jwt

                # generate zhub client with name tutorials
                self._get_input("ENTER any key for the next step: (zhub client)... ")
                self._print_explain("Creating 0-hub client")
                self._print_command("""zhub_client = j.clients.zhub.get("tutorials", token_=token)""")
                zhub_client = j.clients.zhub.get("tutorials", token_=token)
                zhub_client.save()

                self._get_input("ENTER any key for the next step: (authenticate zhub client)... ")
                self._print_explain("Authenticating 0-hub client to be used... ")
                self._print_command("zhub_client.authenticate()")
                zhub_client.authenticate()
                self._print_explain("0-hub client ready to be used")
            else:
                raise RuntimeError("0-hub client is exists required to continue the tutorial please run cleanup")
            return zhub_client

    # creat ownhub locally
    def _ownhub_local(self):
        """
        Deploy ownhub on local machine
        """
        self._print_headline2("Deploying the hub on local container")
        container_ip = self._get_input("Please input your container ip: ")
        self._print_command('j.builders.apps.hub.in_docker("%s")' % container_ip)
        j.builders.apps.hub.in_docker(container_ip)
        self._get_input("ENTER any key for the next step: (Install ownhub)... ")
        self._print_command("j.builders.apps.hub.install(reset=True)")
        j.builders.apps.hub.install(reset=True)
        self._get_input("ENTER any key for the next step: (Start ownhub) ...")
        self._print_command("j.builders.apps.hub.start()")
        j.builders.apps.hub.start()
        self._print_headline("Done and ownhub available at http://%s:5555" % container_ip)
        self._print_headline2("Congratulations you now have your own hub!")

    # make an flist from ownhub
    def _ownhub_sandbox(self, zhub_client):
        """
        sandbox your ownhub to create it on remote zos machine
        : param: zhub_client get it from self._create_zhub_client()
        """
        merged_flist = self._get_input(
            "Do you have a ready flist of the ownHub to create the container with locally (y/[n])? "
        )
        if merged_flist == "y":
            flist_root_url = self._get_input("First ENTER the link to the merged flist: ")
            ip_node = self._get_input("Then ENTER the node's IP to create the container on: ")
            jwt = self._get_input("Then ENTER the node's jwt (if required): ")
            self._create_container(flist_root_url, ip_node, jwt)
            self._print_headline("Done and ownhub available at http://%s:5555" % ip_node)
            self._print_headline2(
                "Congratulations you now have your zos container with odoo!, wait for it initalize then use it."
            )
            return

        # Sandbox hub
        self._get_input("ENTER any key for the next step: (create sandbox)... ")
        self._print_explain("Build, install, then sandbox your ownHub's flist to be used locally.")
        self._print_explain("Sandbox ownHub and upload to hub.grid.tf to merge with jumpscale flist.")
        self._print_command("j.builders.apps.hub.sandbox(zhub_client=zhub_client, flist_create=True, reset=True)")
        self._print_explain(
            """The sandbox function invokes multiple other functions to generate the flist:
        - build: downloads and builds from source code the binaries required to be added in the flist (including dependencies)
        - install: copies the binaries to proper locations locally (in /sandbox directory) and makes any required configurations
        - sandbox: sandbox all the needed files and configurations and creates an flist that is uploaded to the remote hub
        Creating flist and uploading flist to hub.grid.tf... 
        """
        )
        j.builders.apps.hub.sandbox(zhub_client=zhub_client, flist_create=True, reset=True)

        self._print_explain(
            "Flist created and uploaded on https://hub.grid.tf/HUB_USERNAME/zerohub.flist where HUN_USERNAME is your username on hub.grid.tf"
        )

        # Merge flist with jumpscale flist
        self._get_input("ENTER any key for the next step: (Merge flist with jumpscale flist)... ")
        self._print_explain(
            """nNow you should merge the flist generated with a jumpscale flist!
        You can do the merge manually by visiting https://hub.grid.tf/merge

        based on: https://hub.grid.tf/HUB_USERNAME/zerohub.flist
        merge with:  https://hub.grid.tf/tf-autobuilder/threefoldtech-jumpscaleX-autostart-development.flist

        Once the merge is done, get the url created for the merged flist to create a container with it.
        """
        )

        # Create container
        flist_root_url = self._get_input("ENTER the url once you have recieved the merged flist's url: ")
        counter = 0
        while not flist_root_url and counter < 6:
            flist_root_url = self._get_input("ENTER again the merged flist's url: ")
            counter += 1

        ip_node = self._get_input("Then ENTER the node's IP to create the container on: ")
        jwt = self._get_input("Then ENTER the node's jwt (if required): ")
        self._create_container(flist_root_url, ip_node, jwt)

        self._print_headline("Done and ownhub available at http://%s:5555" % ip_node)
        self._print_headline("Congratulations you now have your own hub!, wait for it initalize then use it")

    # Deploy on a zos-container
    def _create_container(self, root_url, ip_node, jwt):
        """
        deploy flist on a remote zos machine
        : param: root_url: link for a merged ready flist
        : ip_node: remote node ip
        : jwt: remote node password
        """
        self._print_explain("Creating a zos container")
        self._print_command('cl = j.clients.zos.get("zhub", host=ip_node, password=jwt)')
        cl = j.clients.zos.get("zhub", host=ip_node, password=jwt)

        self._print_command(
            """cl.client.container.create(
                name="tutorials", 
                root_url=root_url, 
                nics=[{"type": "default", "name": "defaultnic", "id": " None"}], 
                port={5555: 5555}, 
                env={"IP_PORT": ip_node + ":5555"}
            ).get()"""
        )

        cl.client.container.create(
            name="tutorials",
            root_url=root_url,
            nics=[{"type": "default", "name": "defaultnic", "id": " None"}],
            port={5555: 5555, 8069: 8069},
            env={"IP_PORT": ip_node + ":5555"},
        ).get()

    def _builder_example(self):
        """
        We have ownhub - will build, install, start, sandbox then
        """
        self._print_headline2("OK, now we have our ownhub - we will use it to build/deploy odoo builder")

        # get odoo docker ip to depoly on
        odoo_ip = self._get_input("Please input your container ip: ")

        # odoo explination
        self._print_headline2(
            "In this part we will take `BuilderOdoo` as an example, we will go through its life cycle"
        )

        # 3- Install Odoo
        self._get_input("Press ENTER to continue the next part: (Installation)... ")
        self._print_explain("Install Method calls build at first- this may take a few minutes... ")
        self._print_command("j.builders.apps.odoo.install(reset=True)")
        self._get_input("Press ENTER to install... ")
        j.builders.apps.odoo.install(reset=True)

        # 4- Start Odoo
        self._get_input("Press ENTER to continue the next part: (Starting Odoo)... ")
        self._print_command("j.builders.apps.odoo.start()")
        j.builders.apps.odoo.start()

        self._print_headline("Congratulations now you have Odoo check it on\n\t http://%s:8069" % odoo_ip)

        # 5- Sandbox Odoo
        self._get_input("Press ENTER to continue the next part: (Sandboxing Odoo)... ")

        # 6- Check if you have already a merged ready flist
        merged_flist = self._get_input("Do you have a ready flist for Odoo to create a zos-container (y/[n])? ")

        if merged_flist == "y":
            flist_url = self._get_input("Please ENTER the link to the merged flist: ")
            ip_node = self._get_input("Please ENTER the node's IP to create the container on: ")
            jwt = self._get_input("Please ENTER the node's jwt (if required): ")

            # 7- Creating the container
            self._create_container(flist_url, ip_node, jwt)
            self._print_headline(
                "Congratulations! Container creation done and odoo available at: http://%s:8069\nPlease wait for few moments then use it"
                % ip_node
            )
            return

        hub_name = self._get_input(
            """Do you want to generate the flist using 
            1- zhub
            2- ownhub
            choose (1/[2])? """
        )

        if hub_name == "1":
            zhub_client = self._create_zhub_client()
            j.builders.apps.odoo.sandbox(zhub_client=zhub_client, flist_create=True, reset=True)

            self._print_explain(
                "Flist created and uploaded on https://hub.grid.tf/HUB_USERNAME/odoo.flist where HUB_USERNAME is your username on hub.grid.tf"
            )

            # Merge flist with jumpscale flist
            self._get_input("ENTER any key for the next step: (Merge flist with jumpscale flist)... ")
            self._print_explain(
                """Now you should merge the flist generated with a jumpscale flist!
            You can do the merge manually by visiting https://hub.grid.tf/merge

            based on: https://hub.grid.tf/HUB_USERNAME/odoo.flist
            merge with:  https://hub.grid.tf/tf-autobuilder/threefoldtech-jumpscaleX-autostart-development.flist

            Once the merge is done, get the url created for the merged flist to create a container with it./n
            """
            )

        else:
            self._print_explain(
                "This will create an ownhub-client which is an instance from zhub."
                + "\nThen sandbox BuilderOdoo, makes flist, uploads it to your localhub."
            )
            self._print_command('own_hub_client = j.clients.zhub.get("tutorials", url="http://%s:5555/api)' % odoo_ip)
            self._get_input("ENTER any key to sandbox... ")

            own_hub_client = j.clients.zhub.get("tutorials", url="http://%s:5555/api" % odoo_ip)
            self._print_command(
                "j.builders.apps.odoo.sandbox(zhub_client=own_hub_client, flist_create=True, reset=True)"
            )
            j.builders.apps.odoo.sandbox(zhub_client=own_hub_client, flist_create=True, reset=True)
            self._print_explain(
                """
                Now you should merge the flist generated with a jumpscale flist!
                at: http://{odoo_ip}:5555
                You can do the merge manually by visiting https://{odoo_ip}:5555/merge

                based on: https://{odoo_ip}/Administrator/odoo.flist
                merge with:  https://hub.grid.tf/tf-autobuilder/threefoldtech-jumpscaleX-autostart-development.flist

                Once the merge is done, get the url created for the merged flist to create a container with it.
            """.format(
                    odoo_ip=odoo_ip
                )
            )

        # Create container
        flist_root_url = self._get_input("ENTER the url once you have recieved the merged flist's url: ")
        counter = 0
        while not flist_root_url and counter < 6:
            flist_root_url = self._get_input("ENTER again the merged flist's url: ")
            counter += 1
        ip_node = self._get_input("Then ENTER the node's IP to create the container on: ")
        jwt = self._get_input("Then ENTER the node's jwt (if required): ")
        self._create_container(flist_root_url, ip_node, jwt)
        self._print_headline("Done and your odoo available at http://%s:8069" % ip_node)
        self._print_headline(
            "Congratulations you now have your zos container with odoo!, wait for it initalize then use it"
        )

