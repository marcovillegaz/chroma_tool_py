class Sequence:
    all = []

    def __init__(self, name):
        # Run validation to reacive arguments
        assert type(name) is str, f"{name} must be a string!"

        # Assign to self object (instance attributes)
        self.name = name

        # Action to execute
        Sequence.all.append(self)

        @classmethod
        def execute(cls):
            """Execute an integration sequence"""
