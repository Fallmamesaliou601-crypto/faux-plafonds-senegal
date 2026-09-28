from django.http import HttpResponseForbidden

from .models import Visiteur


class VisiteurMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key
        ip = request.META.get("REMOTE_ADDR")

        visiteur, created = Visiteur.objects.get_or_create(
            session_key=session_key,
            defaults={
                "adresse_ip": ip,
                "page_actuelle": request.path,
                "user_agent": request.META.get(
                    "HTTP_USER_AGENT",
                    ""
                ),
            },
        )

        if not created:
            visiteur.adresse_ip = ip
            visiteur.page_actuelle = request.path
            visiteur.user_agent = request.META.get(
                "HTTP_USER_AGENT",
                ""
            )

        if visiteur.bloque:
            visiteur.en_ligne = False
            visiteur.save(
                update_fields=[
                    "adresse_ip",
                    "page_actuelle",
                    "user_agent",
                    "en_ligne",
                    "derniere_visite",
                ]
            )

            return HttpResponseForbidden(
                "Accès refusé."
            )

        visiteur.en_ligne = True

        visiteur.save(
            update_fields=[
                "adresse_ip",
                "page_actuelle",
                "user_agent",
                "en_ligne",
                "derniere_visite",
            ]
        )

        response = self.get_response(request)

        return response
