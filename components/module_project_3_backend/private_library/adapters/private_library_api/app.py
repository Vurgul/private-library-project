from evraz.classic.http_api import App
from evraz.classic.http_auth import Authenticator
from private_library.application import services

from . import controllers, auth


def create_app(
    users: services.UserService,
    authorization: services.Authorization,
    library: services.Library,
) -> App:

    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)
    authenticator.set_strategies(auth.jwt_strategy)

    app = App()
    app.register(controllers.Users(
        authorization=authorization,
        users=users
        )
    )

    app.register(controllers.Authorization(
        authorization=authorization
        )
    )

    app.register(controllers.Library(
        authorization=authorization,
        library=library
        )
    )
    return app
