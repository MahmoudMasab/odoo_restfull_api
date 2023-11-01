from abc import ABC, abstractmethod

class IAuthService(ABC):
    @abstractmethod
    def signUp(self):
        pass
    @abstractmethod
    def signIn(self):
        pass
    @abstractmethod
    def logout(self):
        pass
    @abstractmethod
    def sendCode(self):
        pass
    @abstractmethod
    def validatorToken(self):
        pass
    @abstractmethod
    def validatorRefreshToken(self):
        pass
    @abstractmethod
    def validatorConfirmToken(self):
        pass
    @abstractmethod
    def validatorResetToken(self):
        pass
    @abstractmethod
    def refreshToken(self):
        pass
    @abstractmethod
    def logoutAllDevice(self):
        pass
    @abstractmethod
    def confirmCode(self):
        pass
    @abstractmethod
    def confirmResetPassword(self):
        pass
    @abstractmethod
    def changePassword(self):
        pass
    
    
 