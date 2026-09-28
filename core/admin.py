from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html

from .models import Realisation, JournalSecurite, Visiteur, Signalement, DemandeDevis


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = (
        "photo_preview",
        "titre",
        "publiee",
        "date_creation",
    )

    list_editable = ("publiee",)

    list_filter = ("publiee", "date_creation")
    search_fields = ("titre", "description")
    readonly_fields = ("photo_preview",)

    @admin.display(description="Aperçu")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" '
                'style="width:180px;height:120px;'
                'object-fit:cover;border-radius:10px;'
                'border:1px solid #ddd;" />',
                obj.photo.url,
            )

        return "Aucune photo"


@admin.register(JournalSecurite)
class JournalSecuriteAdmin(admin.ModelAdmin):
    list_display = (
        "type_evenement",
        "adresse_ip",
        "description",
        "traite",
        "date_creation",
    )

    list_filter = (
        "type_evenement",
        "traite",
        "date_creation",
    )

    search_fields = (
        "adresse_ip",
        "description",
    )

    list_editable = ("traite",)

    readonly_fields = ("date_creation",)

    ordering = ("-date_creation",)


@admin.register(Visiteur)
class VisiteurAdmin(admin.ModelAdmin):
    list_display = (
        "statut",
        "adresse_ip",
        "page_actuelle",
        "premiere_visite",
        "derniere_visite",
        "bloque",
    )

    list_filter = (
        "en_ligne",
        "bloque",
        "premiere_visite",
        "derniere_visite",
    )

    search_fields = (
        "adresse_ip",
        "user_agent",
        "page_actuelle",
    )

    list_editable = ("bloque",)

    readonly_fields = (
        "session_key",
        "premiere_visite",
        "derniere_visite",
    )

    ordering = ("-derniere_visite",)

    def save_model(self, request, obj, form, change):
        ancien_blocage = False

        if change:
            ancien_obj = Visiteur.objects.get(pk=obj.pk)
            ancien_blocage = ancien_obj.bloque

        super().save_model(request, obj, form, change)

        if obj.bloque and not ancien_blocage:
            JournalSecurite.objects.create(
                type_evenement="blocage",
                adresse_ip=obj.adresse_ip,
                description=(
                    f"Visiteur bloqué. "
                    f"Session : {obj.session_key}"
                ),
            )

    @admin.display(description="Statut")
    def statut(self, obj):
        if obj.bloque:
            return "🚫 Bloqué"

        if obj.en_ligne:
            return "🟢 En ligne"

        return "⚪ Hors ligne"


@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = (
        "motif",
        "statut",
        "adresse_ip",
        "message_court",
        "date_creation",
        "date_traitement",
    )

    list_filter = (
        "motif",
        "statut",
        "date_creation",
        "date_traitement",
    )

    search_fields = (
        "adresse_ip",
        "message",
        "session_key",
    )


    readonly_fields = (
        "session_key",
        "adresse_ip",
        "date_creation",
        "date_traitement",
    )

    ordering = ("-date_creation",)

    def save_model(self, request, obj, form, change):
        ancien_statut = None

        if change:
            ancien_obj = Signalement.objects.get(pk=obj.pk)
            ancien_statut = ancien_obj.statut

        if obj.statut == "traite" and ancien_statut != "traite":
            from django.utils import timezone
            obj.date_traitement = timezone.now()

        elif obj.statut != "traite":
            obj.date_traitement = None

        super().save_model(request, obj, form, change)

    @admin.display(description="Message")
    def message_court(self, obj):
        if len(obj.message) > 80:
            return obj.message[:80] + "..."
        return obj.message


@admin.register(DemandeDevis)
class DemandeDevisAdmin(admin.ModelAdmin):

    @admin.display(description="Photo")
    def photo_apercu(self, obj):
        if obj.photo:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" '
                'style="width:80px;height:60px;object-fit:cover;border-radius:6px;cursor:pointer;">'
                '</a>',
                obj.photo.url,
                obj.photo.url,
            )
        return "Aucune photo"
    @admin.display(description="Statut")
    def statut_colore(self, obj):
        couleurs = {
            "nouveau": "#198754",
            "en_cours": "#fd7e14",
            "devis_envoye": "#0d6efd",
            "termine": "#6c757d",
        }

        couleur = couleurs.get(obj.statut, "#212529")

        return format_html(
            '<strong style="color:{};">{}</strong>',
            couleur,
            obj.get_statut_display(),
        )

    @admin.display(description="Date de la demande")
    def date_demande(self, obj):
        return obj.date_creation.strftime("%d/%m/%Y à %H:%M")

    list_display = (
        "nom",
        "telephone",
        "ville",
        "photo_apercu",
        "type_plafond",
        "statut_colore",
        "date_demande",
    )

    list_filter = (
        "statut",
        "ville",
        "type_plafond",
        "date_creation",
    )

    search_fields = (
        "nom",
        "telephone",
        "ville",
        "type_plafond",
        "description",
    )

    readonly_fields = (
        "photo_apercu",
        "date_creation",
        "date_modification",
    )

    ordering = (
        "-date_creation",
    )
