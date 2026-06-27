from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Rolle"
    )

    projects_view = models.BooleanField(default=False, verbose_name="Projekte anzeigen", help_text="Benutzer darf Projekte einsehen.")
    projects_archived_view = models.BooleanField(default=False, verbose_name="Archivierte Projekte anzeigen", help_text="Benutzer darf archivierte Projekte einsehen.")
    projects_detail_view = models.BooleanField(default=False, verbose_name="Projektdetails anzeigen", help_text="Benutzer darf Details des Projekts einsehen.")
    projects_add = models.BooleanField(default=False, verbose_name="Projekt erstellen", help_text="Benutzer darf neue Projekte anlegen.")
    projects_contact_add = models.BooleanField(default=False, verbose_name="Projektkontakt verknüpfen", help_text="Benutzer darf Kontakte mit dem Projekt verknüpfen.")
    projects_contact_delete = models.BooleanField(default=False, verbose_name="Projektkontakt entfernen", help_text="Benutzer darf Kontakte aus dem Projekt entfernen.")
    projects_location_add = models.BooleanField(default=False, verbose_name="Projektstandort verknüpfen", help_text="Benutzer darf Standorte mit dem Projekt verknüpfen.")
    projects_location_delete = models.BooleanField(default=False, verbose_name="Projektstandort entfernen", help_text="Benutzer darf Standorte aus dem Projekt entfernen.")
    projects_edit = models.BooleanField(default=False, verbose_name="Projekte bearbeiten", help_text="Benutzer darf Projekte ändern.")

    projects_user_add = models.BooleanField(default=False, verbose_name="Projektmitarbeiter erstellen", help_text="Benutzer darf Mitarbeiter im Projekt hinzufügen.")
    projects_user_delete = models.BooleanField(default=False, verbose_name="Projektmitarbeiter entfernen", help_text="Benutzer darf Mitarbeiter aus dem Projekt entfernen.")

    projects_finance_view = models.BooleanField(default=False, verbose_name="Projektfinanzen anzeigen", help_text="Benutzer darf Projektfinanzen einsehen.")
    projects_finance_income_add = models.BooleanField(default=False, verbose_name="Projekteinnahmen erfassen", help_text="Benutzer darf Einnahmen hinzufügen.")
    projects_finance_expense_add = models.BooleanField(default=False, verbose_name="Projektausgaben erfassen", help_text="Benutzer darf Ausgaben hinzufügen.")

    projects_time_tracking_view = models.BooleanField(default=False, verbose_name="Projektzeiten anzeigen", help_text="Benutzer darf Projektzeiten sehen.")
    projects_time_tracking_edit = models.BooleanField(default=False, verbose_name="Projektzeiten bearbeiten", help_text="Benutzer darf Projektzeiten ändern.")
    projects_time_tracking_delete = models.BooleanField(default=False, verbose_name="Projektzeiten löschen", help_text="Benutzer darf Projektzeiten löschen.")

    projects_documents_view = models.BooleanField(default=False, verbose_name="Projektdokumente anzeigen", help_text="Benutzer darf Dokumente sehen.")
    projects_documents_add = models.BooleanField(default=False, verbose_name="Projektdokumente hinzufügen", help_text="Benutzer darf Dokumente hochladen.")
    projects_documents_delete = models.BooleanField(default=False, verbose_name="Projektdokumente löschen", help_text="Benutzer darf Dokumente löschen.")

    projects_inventory_inventory_view = models.BooleanField(default=False, verbose_name="Projektinventar anzeigen", help_text="Benutzer darf Projektinventar sehen.")
    projects_inventory_inventory_add = models.BooleanField(default=False, verbose_name="Projektinventar hinzufügen", help_text="Benutzer darf Inventar hinzufügen.")
    projects_inventory_inventory_edit = models.BooleanField(default=False, verbose_name="Projektinventar bearbeiten", help_text="Benutzer darf Inventar ändern.")
    projects_inventory_inventory_delete = models.BooleanField(default=False, verbose_name="Projektinventar löschen", help_text="Benutzer darf Inventar löschen.")

    projects_inventory_shopping_add = models.BooleanField(default=False, verbose_name="Einkauf hinzufügen", help_text="Benutzer darf Einkaufspositionen erstellen.")
    projects_inventory_shopping_edit = models.BooleanField(default=False, verbose_name="Einkauf bearbeiten", help_text="Benutzer darf Einkaufspositionen ändern.")
    projects_inventory_shopping_delete = models.BooleanField(default=False, verbose_name="Einkauf löschen", help_text="Benutzer darf Einkaufspositionen löschen.")
    #projects_inventory_shopping_buy = models.BooleanField(default=False, verbose_name="Einkäufe durchführen", help_text="Benutzer darf Einkäufe als erledigt markieren.")


    # =====================
    # Inventar
    # =====================
    inventory_view = models.BooleanField(default=False, verbose_name="Inventar anzeigen", help_text="Benutzer darf Inventar einsehen.")
    inventory_add = models.BooleanField(default=False, verbose_name="Inventar hinzufügen", help_text="Benutzer darf Inventareinträge erstellen.")
    inventory_edit = models.BooleanField(default=False, verbose_name="Inventar bearbeiten", help_text="Benutzer darf Inventareinträge ändern.")
    inventory_delete = models.BooleanField(default=False, verbose_name="Inventar löschen", help_text="Benutzer darf Inventareinträge löschen.")


    # =====================
    # Rechnungen
    # =====================
    invoices_view = models.BooleanField(default=False, verbose_name="Rechnungsbereich anzeigen", help_text="Benutzer darf Rechnungen verwalten.")

    invoices_customers_view = models.BooleanField(default=False, verbose_name="Kunden anzeigen", help_text="Benutzer darf Kunden sehen.")
    invoices_customers_detail_view = models.BooleanField(default=False, verbose_name="Kundendetails anzeigen", help_text="Benutzer darf Details des Kunden sehen.")
    invoices_customers_add = models.BooleanField(default=False, verbose_name="Kunden erstellen", help_text="Benutzer darf Kunden anlegen.")
    invoices_customers_edit = models.BooleanField(default=False, verbose_name="Kunden bearbeiten", help_text="Benutzer darf Kunden ändern.")
    invoices_customers_archive = models.BooleanField(default=False, verbose_name="Kunden archivieren", help_text="Benutzer darf Kunden archivieren.")
    invoices_customers_activate = models.BooleanField(default=False, verbose_name="Kunden reaktivieren", help_text="Benutzer darf Kunden wieder aktivieren.")

    invoices_items_view = models.BooleanField(default=False, verbose_name="Artikel anzeigen", help_text="Benutzer darf Artikel sehen.")
    invoices_items_add = models.BooleanField(default=False, verbose_name="Artikel erstellen", help_text="Benutzer darf Artikel erstellen.")
    invoices_items_edit = models.BooleanField(default=False, verbose_name="Artikel bearbeiten", help_text="Benutzer darf Artikel ändern.")
    invoices_items_delete = models.BooleanField(default=False, verbose_name="Artikel löschen", help_text="Benutzer darf Artikel löschen.")

    invoices_invoices_view = models.BooleanField(default=False, verbose_name="Rechnungen anzeigen", help_text="Benutzer darf Rechnungen sehen.")
    invoices_invoices_project_add = models.BooleanField(default=False, verbose_name="Projekt-Rechnung erstellen", help_text="Benutzer darf Rechnungen aus Projekten erstellen.")
    invoices_invoices_customer_add = models.BooleanField(default=False, verbose_name="Kunden-Rechnung erstellen", help_text="Benutzer darf Rechnungen für Kunden erstellen.")
    invoices_invoices_invoices_view = models.BooleanField(default=False, verbose_name="Rechnungsdetails anzeigen", help_text="Benutzer darf Rechnungsdetails sehen.")
    invoices_invoices_invoices_item_add = models.BooleanField(default=False, verbose_name="Rechnungsposition hinzufügen", help_text="Benutzer darf Positionen hinzufügen.")
    invoices_invoices_invoices_item_delete = models.BooleanField(default=False, verbose_name="Rechnungsposition löschen", help_text="Benutzer darf Positionen löschen.")
    invoices_invoices_invoices_preview = models.BooleanField(default=False, verbose_name="Rechnungsvorschau anzeigen", help_text="Benutzer darf Vorschauen öffnen.")
    invoices_invoices_invoices_download = models.BooleanField(default=False, verbose_name="Rechnung herunterladen", help_text="Benutzer darf Rechnungen herunterladen.")
    invoices_invoices_invoices_cancel = models.BooleanField(default=False, verbose_name="Rechnung stornieren", help_text="Benutzer darf Rechnungen stornieren.")
    invoices_invoices_invoices_paid = models.BooleanField(default=False, verbose_name="Rechnung auf bezahlt setzen", help_text="Benutzer darf Rechnungsstatus ändern.")
    invoices_invoices_invoices_delete = models.BooleanField(default=False, verbose_name="Rechnungen löschen", help_text="Benutzer darf Rechnungen löschen.")
    invoices_invoices_invoices_overdue = models.BooleanField(default=False, verbose_name="Überfällige Rechnungen anzeigen", help_text="Benutzer darf überfällige Rechnungen einsehen.")

    invoices_offers_view = models.BooleanField(default=False, verbose_name="Angebote anzeigen", help_text="Benutzer darf Angebote sehen.")
    invoices_offers_add = models.BooleanField(default=False, verbose_name="Angebot erstellen", help_text="Benutzer darf Angebote für Kunden erstellen.")
    invoices_offers_offers_view = models.BooleanField(default=False, verbose_name="Angebotsdetails anzeigen", help_text="Benutzer darf Angebotsdetails sehen.")
    invoices_offers_offers_item_add = models.BooleanField(default=False, verbose_name="Angebotsposition hinzufügen", help_text="Benutzer darf Positionen hinzufügen.")
    invoices_offers_offers_item_delete = models.BooleanField(default=False, verbose_name="Angebotsposition löschen", help_text="Benutzer darf Positionen löschen.")
    invoices_offers_offers_preview = models.BooleanField(default=False, verbose_name="Angebotsvorschau anzeigen", help_text="Benutzer darf Vorschauen öffnen.")
    invoices_offers_offers_download = models.BooleanField(default=False, verbose_name="Angebot herunterladen", help_text="Benutzer darf Angebote herunterladen.")
    invoices_offers_offers_status = models.BooleanField(default=False, verbose_name="Angebotsstatus bearbeiten", help_text="Benutzer darf Angebotsstatus ändern.")
    invoices_offers_offers_delete = models.BooleanField(default=False, verbose_name="Angebote löschen", help_text="Benutzer darf Angebote löschen.")
    
    invoices_reminders_view = models.BooleanField(default=False, verbose_name="Mahnungen anzeigen", help_text="Benutzer darf Mahnungen einsehen.")
    invoices_reminders_add = models.BooleanField(default=False, verbose_name="Mahnungen hinzufügen", help_text="Benutzer darf Mahnungen erstellen.")
    invoices_reminders_reminders_view = models.BooleanField(default=False, verbose_name="Erinnerungen anzeigen", help_text="Benutzer darf Zahlungserinnerungen einsehen.")
    invoices_reminders_reminders_cancel = models.BooleanField(default=False, verbose_name="Erinnerungen stornieren", help_text="Benutzer darf Zahlungserinnerungen stornieren.")
    invoices_reminders_reminders_delete = models.BooleanField(default=False, verbose_name="Erinnerungen löschen", help_text="Benutzer darf Zahlungserinnerungen löschen.")
    invoices_reminders_reminders_download = models.BooleanField(default=False, verbose_name="Erinnerungen herunterladen", help_text="Benutzer darf Zahlungserinnerungen herunterladen.")
    invoices_reminders_reminders_paid = models.BooleanField(default=False, verbose_name="Erinnerungen als bezahlt markieren", help_text="Benutzer darf Zahlungserinnerungen als bezahlt markieren.")
    invoices_reminders_reminders_expire = models.BooleanField(default=False, verbose_name="Erinnerungen ablaufen lassen", help_text="Benutzer darf Zahlungserinnerungen als abgelaufen markieren.")

    # =====================
    # Benutzerverwaltung
    # =====================
    users_view = models.BooleanField(default=False, verbose_name="Benutzer anzeigen", help_text="Benutzer darf Mitarbeiter sehen.")
    users_add = models.BooleanField(default=False, verbose_name="Benutzer erstellen", help_text="Benutzer darf neue Mitarbeiter anlegen.")
    users_edit = models.BooleanField(default=False, verbose_name="Benutzer bearbeiten", help_text="Benutzer darf Mitarbeiter bearbeiten.")
    users_archive = models.BooleanField(default=False, verbose_name="Benutzer archivieren", help_text="Benutzer darf Mitarbeiter deaktivieren.")
    users_activate = models.BooleanField(default=False, verbose_name="Benutzer aktivieren", help_text="Benutzer darf Mitarbeiter aktivieren.")

    users_groups_add = models.BooleanField(default=False, verbose_name="Rollen erstellen", help_text="Benutzer darf neue Rollen erstellen.")
    users_groups_edit = models.BooleanField(default=False, verbose_name="Rollen bearbeiten", help_text="Benutzer darf Rollen und Berechtigungen ändern.")
    users_groups_delete = models.BooleanField(default=False, verbose_name="Rollen löschen", help_text="Benutzer darf Rollen entfernen.")


    # =====================
    # Einstellungen
    # =====================
    settings_view = models.BooleanField(default=False, verbose_name="Einstellungsübersicht anzeigen", help_text="Benutzer darf Einstellungskategorien sehen.")
    settings_detail_view = models.BooleanField(default=False, verbose_name="Einstellungen anzeigen", help_text="Benutzer darf Systemeinstellungen sehen.")
    settings_add = models.BooleanField(default=False, verbose_name="Einstellungen erstellen", help_text="Benutzer darf neue Einstellungen hinzufügen.")
    settings_delete = models.BooleanField(default=False, verbose_name="Einstellungen löschen", help_text="Benutzer darf Einstellungen entfernen.")
    settings_update_check = models.BooleanField(default=False, verbose_name="Updates prüfen", help_text="Benutzer darf nach Updates suchen.")
    settings_update_apply = models.BooleanField(default=False, verbose_name="Updates installieren", help_text="Benutzer darf Updates installieren.")

    # =====================
    # Zeiterfassung
    # =====================
    #time_tracking_own_view = models.BooleanField(default=False, verbose_name="Eigene Zeiten anzeigen", help_text="Benutzer darf eigene Arbeitszeiten sehen.")
    #time_tracking_own_add = models.BooleanField(default=False, verbose_name="Eigene Zeiten erfassen", help_text="Benutzer darf eigene Arbeitszeiten hinzufügen.")
    #time_tracking_own_edit = models.BooleanField(default=False, verbose_name="Eigene Zeiten bearbeiten", help_text="Benutzer darf eigene Arbeitszeiten ändern.")
    #time_tracking_own_delete = models.BooleanField(default=False, verbose_name="Eigene Zeiten löschen", help_text="Benutzer darf eigene Arbeitszeiten löschen.")

    #time_tracking_all_view = models.BooleanField(default=False, verbose_name="Alle Zeiten anzeigen", help_text="Benutzer darf Arbeitszeiten aller Benutzer sehen.")
    #time_tracking_all_add = models.BooleanField(default=False, verbose_name="Alle Zeiten erfassen", help_text="Benutzer darf Arbeitszeiten für andere Benutzer hinzufügen.")
    #time_tracking_all_edit = models.BooleanField(default=False, verbose_name="Alle Zeiten bearbeiten", help_text="Benutzer darf Arbeitszeiten anderer Benutzer ändern.")
    #time_tracking_all_delete = models.BooleanField(default=False, verbose_name="Alle Zeiten löschen", help_text="Benutzer darf Arbeitszeiten anderer Benutzer löschen.")


    # =====================
    # Finanzen
    # =====================
    #finance_view = models.BooleanField(default=False, verbose_name="Finanzen anzeigen", help_text="Benutzer darf Finanzdaten sehen.")
    #finance_export = models.BooleanField(default=False, verbose_name="Finanzen exportieren", help_text="Benutzer darf Finanzdaten exportieren.")


    # =====================
    # Investments
    # =====================
    #invests_view = models.BooleanField(default=False, verbose_name="Investitionen anzeigen", help_text="Benutzer darf Investitionen sehen.")
    #invests_add = models.BooleanField(default=False, verbose_name="Investitionen erstellen", help_text="Benutzer darf neue Investitionen anlegen.")
    #invests_edit = models.BooleanField(default=False, verbose_name="Investitionen bearbeiten", help_text="Benutzer darf Investitionen ändern.")
    #invests_delete = models.BooleanField(default=False, verbose_name="Investitionen löschen", help_text="Benutzer darf Investitionen entfernen.")


    class Meta:
        verbose_name = "Rolle"
        verbose_name_plural = "Rollen"

    def __str__(self):
        return self.name




class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    def has_permission(self, permission):

        if self.user.is_superuser:
            return True

        if not self.role:
            return False

        return getattr(
            self.role,
            permission.replace(".", "_"),
            False
        )

    def __str__(self):
        return self.user.username