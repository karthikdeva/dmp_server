from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth.views import LoginView
from django_otp.forms import OTPAuthenticationForm
# import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "DMP Admin"
admin.site.site_title = "DMP Admin Portal"
admin.site.index_title = "Welcome to DMP Portal"
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **args):
        if current_user.is_anonymous:
            raise werkzeug.exceptions.Unauthorized()
        else:
            return next(root, info, **args)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^report_builder/', include('report_builder.urls')),
    url(r'^accounts/login/$', LoginView.as_view(authentication_form=OTPAuthenticationForm)),
    # path('api/food/', include('app.restraturent.api.urls')),
    # path('api/accounts/', include('app.accounts.urls')),
    # path('api/v1/', include('app.accounts.api.urls')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),

]
urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

# urlpatterns += [re_path(r'^.*',TemplateView.as_view(template_name="index.html"))]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)