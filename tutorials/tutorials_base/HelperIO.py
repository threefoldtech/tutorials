class HelperIO:
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

    ## helper styling functions
    @staticmethod
    def _get_input(text, color="\33[97m", style="\33[1m"):
        """
        for input from user Text color: self._CWHITE2 - Text style: self._CBOLD
        : param color: defines text color
        : param style: defines text style
        : check:
        : https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python for more 
        """
        input_from_user = input(style + color + "\n" + text + " ")
        return input_from_user

    @staticmethod
    def _print_headline(text, color="\33[32m", style="\33[1m"):
        """
        print headline texts Text color: self._CGREEN - Text style: self._CBOLD
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n***" + text + "***")

    @staticmethod
    def _print_headline2(text, color="\33[33m", style="\33[1m"):
        """
        print headline texts Text color: self._CYELLOW - Text style: self._CBOLD
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n" + text)

    @staticmethod
    def _print_command(text, color="\33[33m", style="\33[0m"):
        """
        print command before execution: self._CYELLOW - Text style: self._CEND
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n>> " + text)

    @staticmethod
    def _print_explain(text, color="\33[32m", style="\33[0m"):
        """
        print explinations to some commands: self._CGREEN - Text style: self._CEND
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n" + text)

    @staticmethod
    def _print_execution(text, color="\33[90m", style="\33[0m"):
        """
        print execution log for commands: self._CGREY - Text style: self._CEND
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n" + text)

    @staticmethod
    def _print_warining(text, color="\33[31m", style="\33[1m"):
        """
        print warnings for dangerous commands: self._CRED - Text style: self._CBOLD
        : param color: defines text color
        : param style: defines text style
        : check:
        """
        print(style + color + "\n***" + text + "***")

