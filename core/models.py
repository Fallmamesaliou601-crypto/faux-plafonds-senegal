from django.core.validators import FileExtensionValidator
from django.db import models


class Realisation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    photo = models.ImageField(
        upload_to="realisations/photos/",
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to="realisations/videos/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "webm", "mov"]
            )
        ]
    )

    date_creation = models.DateTimeField(auto_now_add=True)
    publiee = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Réalisation"
        verbose_name_plural = "Réalisations"

    def __str__(self):
        return self.titre

class JournalSecurite(models.Model):
    TYPE_CHOICES = [
        ("connexion", "Connexion"),
        ("signalement", "Signalement"),
        ("blocage", "Blocage"),
        ("alerte", "Alerte de sécurité"),
    ]

    type_evenement = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    adresse_ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    description = models.TextField()

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    traite = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Journal de sécurité"
        verbose_name_plural = "Journal de sécurité"

    def __str__(self):
        return f"{self.get_type_evenement_display()} - {self.date_creation}"


class Visiteur(models.Model):
    session_key = models.CharField(
        max_length=40,
        unique=True
    )

    adresse_ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True
    )

    premiere_visite = models.DateTimeField(
        auto_now_add=True
    )

    derniere_visite = models.DateTimeField(
        auto_now=True
    )

    page_actuelle = models.CharField(
        max_length=500,
        blank=True
    )

    bloque = models.BooleanField(
        default=False
    )


    en_ligne = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ["-derniere_visite"]
        verbose_name = "Visiteur"
        verbose_name_plural = "Visiteurs"

    def __str__(self):
        return f"{self.adresse_ip or 'IP inconnue'} - {self.derniere_visite}"


class Signalement(models.Model):
    MOTIF_CHOICES = [
        ("bug", "Bug ou problème technique"),
        ("abus", "Abus ou comportement indésirable"),
        ("securite", "Problème de sécurité"),
        ("autre", "Autre"),
    ]

    STATUT_CHOICES = [
        ("nouveau", "Nouveau"),
        ("en_cours", "En cours"),
        ("traite", "Traité"),
    ]

    session_key = models.CharField(
        max_length=40,
        blank=True
    )

    adresse_ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    motif = models.CharField(
        max_length=20,
        choices=MOTIF_CHOICES
    )

    message = models.TextField()

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="nouveau"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_traitement = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"

    def __str__(self):
        return f"{self.get_motif_display()} - {self.date_creation}"


class DemandeDevis(models.Model):
    STATUT_CHOICES = [
        ("nouveau", "Nouveau"),
        ("en_cours", "En cours"),
        ("devis_envoye", "Devis envoyé"),
        ("termine", "Terminé"),
    ]

    nom = models.CharField(max_length=150)

    telephone = models.CharField(max_length=30)

    ville = models.CharField(max_length=100)

    type_plafond = models.CharField(
        max_length=150
    )

    description = models.TextField()

    photo = models.ImageField(
        upload_to="demandes_devis/",
        blank=True,
        null=True,
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="nouveau",
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    date_modification = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Demande de devis"
        verbose_name_plural = "Demandes de devis"

    def __str__(self):
        return f"{self.nom} - {self.telephone}"
