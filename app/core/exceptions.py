class ProjectError(Exception):
    def __init__(self, message: str | None):
        self.message = message
    pass

class InternalError(ProjectError):
    pass

class NoteNotFound(ProjectError):
    pass

class UserNotFound(ProjectError):
    pass

class UserCredentialsMismatch(ProjectError):
    pass

class CredentialsException(ProjectError):
    pass