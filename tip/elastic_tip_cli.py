from sys import argv
import getopt
from elastic_tip import ElasticTip


class CLI:

    def __init__(self):
        self._arguments = []
        self._cli_head = """
Elastic Threat Intelligence Platform
                   -----------------
                   community project
===================================="""
        self._tip = None
        self._mod = None

    def cli(self):
        if argv[1] == "help":
            self._help()
        elif argv[1] == "run":
            self._run_cli()
        elif argv[1] == "init":
            pass
        elif argv[1] == "verify":
            self._verify_cli()
        else:
            self._help()

    def _run_cli(self):
        try:
            opts, args = getopt.getopt(argv[2:], "hm:e:Tu:p:i:c:",
                                       ["help", "modules=", "modules-list", "es-hosts=", "tls", "user", "passwd", "index=", "ca-cert=", "no-verify"])
        except getopt.GetoptError as err:
            print(err)
            exit(1)
        else:
            self._tip = ElasticTip()

        for opt, arg in opts:
            if opt in ["-h", "--help"]:
                self._run_help()
                exit()
            elif opt in ["--modules-list"]:
                print(self._cli_head)
                print("IOC Modules:")
                for mod in self._tip.modules:
                    spaces = " "
                    for i in range(0, (20 - len(mod))):
                        spaces += " "
                    print("  {}{}{}".format(mod, spaces, self._tip.modules[mod]["ref"]))
                exit()
            elif opt in ["-m", "--modules"]:
                if arg == "*":
                    for mod in self._tip.modules:
                        self._tip.modules[mod]["enabled"] = True
                else:
                    for mod in arg.split(","):
                        try:
                            # Enable the module
                            self._tip.modules["{}".format(mod)]["enabled"] = True
                        except KeyError:
                            print("Module {} does not exist".format(mod))
            elif opt in ["-e", "--es-hosts"]:
                self._tip.eshosts = arg.split(",")
            elif opt in ["-u", "--user"]:
                self._tip.esuser = arg
            elif opt in ["-p", "--passwd"]:
                self._tip.espass = arg
            elif opt in ["-i", "--index"]:
                self._tip.index = arg
            elif opt in ["-T", "--tls"]:
                self._tip.tls["use"] = False
            elif opt in ["-c", "--ca-cert"]:
                self._tip.tls["cacert"] = arg
            elif opt in ["--no-verify"]:
                self._tip.tls["verify"] = False

        self._tip.run()

    def _init_cli(self):
        pass

    def _verify_cli(self):
        try:
            opts, args = getopt.getopt(argv[2:], "he:Tu:p:i:c:",
                                       ["help", "es-hosts=", "tls", "user", "passwd", "index=", "ca-cert=", "no-verify"])
        except getopt.GetoptError as err:
            print(err)
            exit(1)
        else:
            self._tip = ElasticTip()
            for opt, arg in opts:
                if opt in ["-h", "--help"]:
                    self._verify_help()
                    exit()
                elif opt in ["-e", "--es-hosts"]:
                    self._tip.eshosts = arg.split(",")
                elif opt in ["-u", "--user"]:
                    self._tip.esuser = arg
                elif opt in ["-p", "--passwd"]:
                    self._tip.espass = arg
                elif opt in ["-i", "--index"]:
                    self._tip.index = arg
                elif opt in ["-T", "--tls"]:
                    self._tip.tls["use"] = False
                elif opt in ["-c", "--ca-cert"]:
                    self._tip.tls["cacert"] = arg
                elif opt in ["--no-verify"]:
                    self._tip.tls["verify"] = False

            self._tip.verify_tip()

    def _help(self):
        print(self._cli_head)
        print("python tip/elastic_tip_cli.py [command] [options]")
        print("")
        print("Commands:")
        print("    help")
        print("    run")
        print("    init")
        print("    verify")

    def _run_help(self):
        print(self._cli_head)
        print("python tip/elastic_tip_cli.py run [options]")
        print("")
        print("Options")
        print("    -h, --help                Print help output")
        print("    -e, --es-hosts <value>    Comma seperated list of Elasticsearch hosts to use")
        print("    -u, --user <value>        Username to use for Authentication to ES")
        print("    -p, --passwd <value>      Password to use for Authentication to ES")
        print("    --modules-list            List module names and the reference link")
        print("    -m, --modules <values>    Modules to enable:")
        tip = ElasticTip()
        for mod in tip.modules:
            print("                                  {}".format(mod))
        print("    -T, --tls                 Use TLS/SSL when connecting to Elasticsearch")
        print("    -c, --ca-cert <value>     Use the cert specified by path")
        print("    --no-verify               Don't verify the TLS/SSL certificate")

    def _verify_help(self):
        print(self._cli_head)
        print("python tip/elastic_tip_cli.py verify [options]")
        print("")
        print("Options")
        print("    -h, --help                Print help output")
        print("    -e, --es-hosts <value>    Comma seperated list of Elasticsearch hosts to use")
        print("    -u, --user <value>        Username to use for Authentication to ES")
        print("    -p, --passwd <value>      Password to use for Authentication to ES")
        print("    -T, --tls                 Use TLS/SSL when connecting to Elasticsearch")
        print("    -c, --ca-cert <value>     Use the cert specified by path")
        print("    --no-verify               Don't verify the TLS/SSL certificate")


tip_cli = CLI()
tip_cli.cli()