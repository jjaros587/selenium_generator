from src.generator.DriverManger import DriverManager


class Handler:

    def __call__(self, test_instance, commands, data):
        self.test = test_instance
        self.commands = commands
        self.data = data

    def do(self, instance, steps, data=None):
        self.__call__(instance, steps, data)
        for command in self.commands:
            [[key, value]] = command.items()
            self.mapping[key](self, value)

    def _run_driver(self, command):
        self.test.driver = DriverManager.run_driver(command)

    def _close_driver(self, *args, **kwargs):
        self.test.driver.close()

    def _page_object(self, command):
        my_class = getattr(globals()[command['class']], command['class'])
        instance = my_class(self.test.driver)
        self._call_method(instance, command['method'], command['params'])

    def _call_method(self, class_instance, method, params):
        getattr(class_instance, method)(**self._feed_params(params))

    def _feed_params(self, params):
        # if params not in self.data:
        #     raise ValueError("SPATNE PARAMETRY TESTU!")
        values = dict()
        for item in params:
            values.update({item: self.data[item]})
        return values

    mapping = {
        "runDriver": _run_driver,
        "closeDriver": _close_driver,
        "pageObject": _page_object
    }
