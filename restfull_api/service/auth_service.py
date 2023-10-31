

from odoo import api, models
from ..repositories.auth_repository import AuthRepository

class AuthService:
    @staticmethod
    def signUp():
        return AuthRepository.signUp()
    @staticmethod
    def signIn():
        return AuthRepository.signIn()
    @staticmethod
    def logout():
        return AuthRepository.logout()
    @staticmethod
    def sendCode():
        return AuthRepository.sendCode()
    @staticmethod
    def validatorToken():
        return AuthRepository.validatorToken()
    @staticmethod
    def validatorRefreshToken():
        return AuthRepository.validatorRefreshToken()
    @staticmethod
    def validatorConfirmToken():
        return AuthRepository.validatorConfirmToken()
    @staticmethod
    def validatorResetToken():
        return AuthRepository.validatorResetToken()
    @staticmethod
    def refreshToken():
        return AuthRepository.refreshToken()
    @staticmethod
    def logoutAllDevice():
        return AuthRepository.logoutAllDevice()
    @staticmethod
    def confirmCode():
        return AuthRepository.confirmCode()
    @staticmethod
    def confirmResetPassword():
        return AuthRepository.confirmResetPassword()
    @staticmethod
    def changePassword():
        return AuthRepository.changePassword()