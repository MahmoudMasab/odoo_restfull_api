class RouteEndPoint:
     signUp ='/api/auth/signUp'
     signIn ='/api/auth/signIn'
     logout ='/api/auth/logout'
     logoutAllDevice ='/api/auth/logoutAllDevice'
     refreshToken ='/api/auth/refreshToken'
     sendCode ='/api/auth/sendCode'
     registerConfirmCode ='/api/auth/register/confirmCode'
     confirmResetPassword ='/api/auth/confirmResetPassword'
     changePassword ='/api/auth/changePassword'
     
     def checkIsExitRouteEndPoint(routeEndPoint):
        routeEndPoints = [
          RouteEndPoint.signUp,
          RouteEndPoint.signIn,
          RouteEndPoint.logout,
          RouteEndPoint.logoutAllDevice,
          RouteEndPoint.refreshToken,
          RouteEndPoint.sendCode,
          RouteEndPoint.registerConfirmCode,
          RouteEndPoint.confirmResetPassword,
          RouteEndPoint.changePassword,
        ]
        return any(ele in routeEndPoint for ele in routeEndPoints)
     