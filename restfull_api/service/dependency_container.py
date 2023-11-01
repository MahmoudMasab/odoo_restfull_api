from simple_dependency_injection.dependency_container import DependencyContainer

from ..repositories.auth_repository import AuthRepository
from ..service.auth_service import IAuthService

def config_generator() -> IAuthService:
    return AuthRepository()

dependency_container = DependencyContainer()
dependency_container.register_dependency(    
    IAuthService, config_generator,
    singleton=True)