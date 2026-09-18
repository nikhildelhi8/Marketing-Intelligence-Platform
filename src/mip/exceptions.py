class MIPError(Exception):
    pass

class ValidationError(MIPError):
    pass 


class RepositoryError(MIPError):
    pass 

class NotFoundError(MIPError):
    pass

