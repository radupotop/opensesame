class IPTablesError(Exception):
    """
    Generic IPTables error.
    """


class ParseIPError(IPTablesError):
    pass
