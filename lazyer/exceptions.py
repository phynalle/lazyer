class NodeException(Exception):
    pass


class AlreadyMapped(NodeException):
    pass


class NotMapped(NodeException):
    pass


class DuplicatedKey(NodeException):
    pass


class TemplateException(Exception):
    pass


class EmptyTemplate(TemplateException):
    pass
