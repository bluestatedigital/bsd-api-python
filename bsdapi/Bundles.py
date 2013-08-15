class Bundles:

    def __init__(self, bundles):
        self.bundles = bundles

    def __str__(self):
        return ','.join(self.bundles)
