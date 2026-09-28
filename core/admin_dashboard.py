from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import (
    Realisation,
    JournalSecurite,
    Visiteur,
    Signalement,
)


@staff_member_required
def dashboard(request):
    contexte = {
        "total_visiteurs": Visiteur.objects.count(),
        "visiteurs_en_ligne": Visiteur.objects.filter(
            en_ligne=True,
            bloque=False,
        ).count(),
        "visiteurs_bloques": Visiteur.objects.filter(
            bloque=True,
        ).count(),
        "total_signalements": Signalement.objects.count(),
        "signalements_nouveaux": Signalement.objects.filter(
            statut="nouveau",
        ).count(),
        "signalements_traites": Signalement.objects.filter(
            statut="traite",
        ).count(),
        "total_realisations": Realisation.objects.count(),
        "realisations_publiees": Realisation.objects.filter(
            publiee=True,
        ).count(),
        "evenements_securite": JournalSecurite.objects.count(),
        "signalements_recents": Signalement.objects.all()[:5],
        "visiteurs_recents": Visiteur.objects.all()[:5],
    }

    return render(
        request,
        "admin/core/dashboard.html",
        contexte,
    )


from django.urls import path


def dashboard_urls():
    return [
        path(
            "tableau-de-bord/",
            dashboard,
            name="tableau_de_bord",
        ),
    ]
