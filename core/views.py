from datetime import timedelta

from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import (
    Realisation,
    Signalement,
    JournalSecurite,
    DemandeDevis,
)


def home(request):
    realisations = Realisation.objects.filter(publiee=True)

    message_signalement = None
    message_devis = None

    if request.method == "POST":
        formulaire = request.POST.get("formulaire", "").strip()

        if formulaire == "signalement":
            motif = request.POST.get("motif", "").strip()
            message = request.POST.get("message", "").strip()

            motifs_valides = {
                choix[0]
                for choix in Signalement.MOTIF_CHOICES
            }

            if motif in motifs_valides and message:
                if not request.session.session_key:
                    request.session.create()

                session_key = request.session.session_key
                ip = request.META.get("REMOTE_ADDR")

                limite = timezone.now() - timedelta(minutes=10)

                nombre_recent = Signalement.objects.filter(
                    session_key=session_key,
                    date_creation__gte=limite,
                ).count()

                if nombre_recent >= 3:
                    message_signalement = (
                        "Vous avez atteint la limite de 3 signalements "
                        "en 10 minutes. Merci de patienter avant "
                        "d'envoyer un nouveau signalement."
                    )
                else:
                    Signalement.objects.create(
                        session_key=session_key,
                        adresse_ip=ip,
                        motif=motif,
                        message=message,
                    )

                    JournalSecurite.objects.create(
                        type_evenement="signalement",
                        adresse_ip=ip,
                        description=(
                            f"Signalement reçu : {motif}. "
                            f"Message : {message[:500]}"
                        ),
                    )

                    message_signalement = (
                        "Merci. Votre signalement a bien été enregistré."
                    )

        elif formulaire == "devis":
            nom = request.POST.get("nom", "").strip()
            telephone = request.POST.get("telephone", "").strip()
            ville = request.POST.get("ville", "").strip()
            type_plafond = request.POST.get(
                "type_plafond",
                "",
            ).strip()
            description = request.POST.get(
                "description",
                "",
            ).strip()
            photo = request.FILES.get("photo")

            if (
                nom
                and telephone
                and ville
                and type_plafond
                and description
            ):
                demande = DemandeDevis(
                    nom=nom,
                    telephone=telephone,
                    ville=ville,
                    type_plafond=type_plafond,
                    description=description,
                    photo=photo,
                )

                try:
                    demande.full_clean()
                    demande.save()

                    message_devis = (
                        "Merci ! Votre demande de devis a bien été envoyée."
                    )


                except ValidationError:
                    message_devis = (
                        "La photo envoyée n'est pas valide. "
                        "Merci de sélectionner une image correcte."
                    )

    return render(
        request,
        "home.html",
        {
            "realisations": realisations,
            "message_signalement": message_signalement,
            "message_devis": message_devis,
        },
    )
