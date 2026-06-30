

class DomainException(Exception):
    """Base exception cho tất cả các lỗi nghiệp vụ trong domain layer"""

    def __init__(self, message: str, code: str | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
    
class NotFoundError(DomainException):
    """Exception cho trường hợp không tìm thjaays bản ghi trong database"""
    pass


class PermissionError(DomainException):
    """Exception cho trường hợp người dùng cố truy cập dữ liệu không thuộc về mình"""
    pass

class ValidationError(DomainException):
    """Exception cho trường hợp dữ liệu không hợp lệ"""
    pass

class ConflictError(DomainException):
    """Exception cho trương hợp dữ liệu bị trung lặp """
    pass


class BusinessLogicError(DomainException):
    """Exception cho trường hợp lỗi nghiệp vụ"""
    pass



