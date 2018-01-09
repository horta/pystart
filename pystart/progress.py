class progress_indicator(object):
    def __init__(self, desc):
        self._desc = desc

    def __enter__(self):
        print(self._desc + "...")

    def __exit__(self, *args, **kwargs):
        print("Done!")
