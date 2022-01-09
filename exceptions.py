

class ActionNotSpecified(Exception):
    """Raises when an input command has no action in it"""
    pass


class TargetNotSpecified(Exception):
    """Raises when an input command has no target in it"""
    pass


class TooManyArgs(Exception):
    """Raises there are too many arguments for command structure"""
    pass


class InvalidTarget(Exception):
    """Raises when target is not valid"""
    pass

class InvalidArgNum(Exception):
    """Raises when target is not valid"""
    pass
