import click
import logging
import ckan.logic as logic
from ckan.plugins import toolkit

get_action = logic.get_action
ValidationError = toolkit.ValidationError
log = logging.getLogger(__name__)

image_path = toolkit.config.get('ckan.site_url') + '/images/categories'

# *
#   Default categories
# *

default_categories = [
    {
        "approval_status": "approved",
        "description": "Rakennettu ympäristö, kartat, alueellinen data (data, joka kattaa tietyn maantieteellisen alueen)",
        "description_translated": {
            "en": "Built-up environment, maps, regional data (data that covers a specific geographic area)",
            "fi": "Rakennettu ympäristö, kartat, alueellinen data (data, joka kattaa tietyn maantieteellisen alueen)",
            "sv": "Bebyggd miljö, kartor, regional data (data som täcker en viss geografisk region)"
        },
        "display_name": "Alueet ja kaupungit",
        "image_url": image_path + "/alueet-ja-kaupungit.svg",
        "name": "alueet-ja-kaupungit",
        "state": "active",
        "title": "Alueet ja kaupungit",
        "title_translated": {
                "en": "Regions & Cities",
                "fi": "Alueet ja kaupungit",
                "sv": "Regioner & städer"
        }
    },
    {
        "approval_status": "approved",
        "description": "Energiapolitiikka, energiateollisuus, energiankulutus, uusiutuva energia",
        "description_translated": {
            "fi": "Energiapolitiikka, energiateollisuus, energiankulutus, uusiutuva energia",
            "en": "Energy policy, energy industry, energy consumption, renewable energy",
            "sv": "Energipolitik, energiindustri, oljeindustri, energiförbrukning, förnybar energi"
        },
        "display_name": "Energia",
        "image_url": image_path + "/energia.svg",
        "name": "energia",
        "state": "active",
        "title": "Energia",
        "title_translated": {
                "fi": "Energia",
                "en": "Energy",
                "sv": "Energi"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Vaalit ja äänestäminen, politiikka, hallinto ja päätöksenteko, \
            vieraanvaraisuus ja lahjat, julkisen sektorin data, sanastot",
        "description_translated": {
            "fi": "Vaalit ja äänestäminen, politiikka, hallinto ja päätöksenteko, vieraanvaraisuus ja lahjat, \
             julkisen sektorin data, sanastot",
            "en": "Elections and voting, politics, government and decision-making, \
             hospitality and gifts, public sector data, glossaries",
            "sv": "Val och omröstning, politik, regering och beslutsfattande, \
            gästfrihet och gåvor, offentlig sektors data, ordförråd"
        },
        "display_name": "Hallinto ja julkinen sektori",
        "image_url": image_path + "/hallinto-ja-julkinen-sektori.svg",
        "name": "hallinto-ja-julkinen-sektori",
        "state": "active",
        "title": "Hallinto ja julkinen sektori",
        "title_translated": {
                "fi": "Hallinto ja julkinen sektori",
                "en": "Government & Public Sector",
                "sv": "Regering & offentlig sektor"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Ulkopolitiikka, kansainväliset järjestöt ja sopimukset, \
            konfliktit ja rauha, asevoimat",
        "description_translated": {
            "en": "Foreign policy, international organisations and agreements, \
            conflicts and peace, military forces",
            "fi": "Ulkopolitiikka, kansainväliset järjestöt ja sopimukset, \
            konfliktit ja rauha, asevoimat",
            "sv": "Utrikespolitik, internationella organisationer och avtal, \
            konflikter och fred, väpnade styrkor"
        },
        "display_name": "Kansainväliset asiat",
        "image_url": image_path + "/kansainvaliset-asiat.svg",
        "name": "kansainvaliset-asiat",
        "state": "active",
        "title": "Kansainväliset asiat",
        "title_translated": {
                "en": "International Issues",
                "fi": "Kansainväliset asiat",
                "sv": "Internationella frågor"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Opetus ja koulutus, varhaiskasvatus, urheilu ja liikunta",
        "description_translated": {
            "en": "School and education, early childhood education and care, sports",
            "fi": "Opetus ja koulutus, varhaiskasvatus, urheilu ja liikunta",
            "sv": "Undervisning och utbildning, förskolepedagogik, sport"
        },
        "display_name": "Koulutus ja urheilu",
        "image_url": image_path + "/koulutus-ja-urheilu.svg",
        "name": "koulutus-ja-urheilu",
        "state": "active",
        "title": "Koulutus ja urheilu",
        "title_translated": {
                "en": "Education & Sport",
                "fi": "Koulutus ja urheilu",
                "sv": "Utbildning & sport"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Kirjastot, kulttuuri, museot, musiikki, taide ja teatteri, vapaa-aika",
        "description_translated": {
            "fi": "Kirjastot, kulttuuri, museot, musiikki, taide ja teatteri, vapaa-aika",
            "en": "GLAM (Galleries, Libraries, Arts, Museums), music and theater, leisure time activities",
            "sv": "Biblioteker, kultur, museer, konst och teater, fritid"
        },
        "display_name": "Kulttuuri, taide ja vapaa-aika",
        "image_url": image_path + "/kulttuuri-taide-ja-vapaa-aika.svg",
        "name": "kulttuuri-taide-ja-vapaa-aika",
        "state": "active",
        "title": "Kulttuuri, taide ja vapaa-aika",
        "title_translated": {
                "fi": "Kulttuuri, taide ja vapaa-aika",
                "en": "Arts, Culture & Leisure",
                "sv": "Konst, kultur & fritid"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",

        "description": "Liikennepolitiikka, liikennevälineet ja -muodot, julkinen liikenne, kävely ja pyöräily",
        "description_translated": {
            "fi": "Liikennepolitiikka, liikennevälineet ja -muodot, julkinen liikenne, kävely ja pyöräily",
            "en": "Transport policy, means and forms of transport, public transport, walking and cycling",
            "sv": "Trafikpolitik, trafikmedel och transportsätt, kollektivtrafik, promenad och cykling"
        },
        "display_name": "Liikenne",
        "image_url": image_path + "/liikenne.svg",
        "name": "liikenne",
        "state": "active",
        "title": "Liikenne",
        "title_translated": {
                "fi": "Liikenne",
                "en": "Transport",
                "sv": "Trafik"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Maatalous, metsätalous, kalastus ja kaikki niihin liittyvä politiikka, \
            sääntely, ohjeistukset, toiminta, jne. Elintarvikkeet ja elintarviketeknologia",
        "description_translated": {
            "fi": "Maatalous, metsätalous, kalastus ja kaikki niihin liittyvä politiikka, sääntely, \
            ohjeistukset, toiminta, jne. Elintarvikkeet ja elintarviketeknologia",
            "en": "Agriculture, forestry, fishery and politics, regulations, instructions, \
            actions etc. related to those. Food products and food technology",
            "sv": "Jordbruk, skogsbruk, fiskeri och alla politiker, reglering, anvisningar, \
            verksamheter och andra samhörande saker. Livsmedelsprodukter och livsmedelsteknik"
        },
        "display_name": "Maatalous, kalastus, metsätalous ja elintarvikkeet",
        "image_url": image_path + "/maatalous-kalastus-metsatalous-ja-elintarvikkeet.svg",
        "name": "maatalous-kalastus-metsatalous-ja-elintarvikkeet",
        "state": "active",
        "title": "Maatalous, kalastus, metsätalous ja elintarvikkeet",
        "title_translated": {
                "fi": "Maatalous, kalastus, metsätalous ja elintarvikkeet",
                "en": "Agriculture, Fisheries, Forestry & Foods",
                "sv": "Jordbruk, fiske, skogsbruk & livsmedel"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Matkailu ja turismi, matkailukohteet, nähtävyydet ja tilastot",
        "description_translated": {
            "fi": "Matkailu ja turismi, matkailukohteet, nähtävyydet ja tilastot",
            "en": "Tourism, travel, tourist destinations, sights and statistics",
            "sv": "Turism, turistmål, sevärdheter och statistik"
        },
        "display_name": "Matkailu ja turismi",
        "image_url": image_path + "/matkailu-ja-turismi.svg",
        "name": "matkailu-ja-turismi",
        "state": "active",
        "title": "Matkailu ja turismi",
        "title_translated": {
                "fi": "Matkailu ja turismi",
                "en": "Tourism & Travel",
                "sv": "Turism & resor"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Lakiasiat, lainopilliset ammatit, oikeusjärjestelmä, yleinen turvallisuus",
        "description_translated": {
            "fi": "Lakiasiat, lainopilliset ammatit, oikeusjärjestelmä, yleinen turvallisuus",
            "en": "Legal matters, legal professions, legal system, general safety",
            "sv": "Juridiska frågor, juridiska yrken, rättssystem, allmän säkerhet"
        },
        "display_name": "Oikeus, oikeusjärjestelmä ja yleinen turvallisuus",
        "image_url": image_path + "/oikeus-oikeusjarjestelma-ja-yleinen-turvallisuus.svg",
        "name": "oikeus-oikeusjarjestelma-ja-yleinen-turvallisuus",
        "state": "active",
        "title": "Oikeus, oikeusjärjestelmä ja yleinen turvallisuus",
        "title_translated": {
                "fi": "Oikeus, oikeusjärjestelmä ja yleinen turvallisuus",
                "en": "Justice, Legal System & Public Safety",
                "sv": "Rättvisa, rättssystem & säkerhet"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Rakennettu ympäristö, tiet, rautatiet. liikenneväylät, sähköverkot, muu infrastruktuuri",
        "description_translated": {
            "fi": "Rakennettu ympäristö, tiet, rautatiet. liikenneväylät, sähköverkot, muu infrastruktuuri",
            "en": "Built-up areas, roads and railroads, power grid and other infrastructure",
            "sv": "Byggd miljö, vägar och järnvägar, trafikleder, elnät "
        },
        "display_name": "Rakennettu ympäristö ja infrastruktuuri",
        "image_url": image_path + "/rakennettu-ymparisto-ja-infrastruktuuri.svg",
        "name": "rakennettu-ymparisto-ja-infrastruktuuri",
        "state": "active",
        "title": "Rakennettu ympäristö ja infrastruktuuri",
        "title_translated": {
                "fi": "Rakennettu ympäristö ja infrastruktuuri",
                "en": "Built-up areas & Infrastructure",
                "sv": "Byggda områden & infrastruktur"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Talouspolitiikka, verotus, rahoitus ja investoinnit, kulutus, \
            kauppa ja kauppapolitiikka, tariffit, elinkeinot ja yritykset",
        "description_translated": {
            "fi": "Talouspolitiikka, verotus, rahoitus ja investoinnit, kulutus, \
            kauppa ja kauppapolitiikka, tariffit, elinkeinot ja yritykset",
            "en": "Economic policy, taxation, financing and investments, consumption, \
            trade and trade policy, tariffs, business",
            "sv": "Ekonomisk politik, beskattning, finansiering och investeringar, \
            handel och handelspolitik, tariffer, näringar och företag"
        },
        "display_name": "Talous ja rahoitus",
        "image_url": image_path + "/talous-ja-rahoitus.svg",
        "name": "talous-ja-rahoitus",
        "state": "active",
        "title": "Talous ja rahoitus",
        "title_translated": {
                "fi": "Talous ja rahoitus",
                "en": "Economy & Finance",
                "sv": "Ekonomi & finans"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Lääketiede, sairaustiedot, ravitsemus, terveydenhuollon ammatit",
        "description_translated": {
            "fi": "Lääketiede, sairaustiedot, ravitsemus, terveydenhuollon ammatit",
            "en": "Medicine, medical records, nutrition, health care occupations",
            "sv": "Medicin, hälsouppgifter, näring, yrke inom hälsovård"
        },
        "display_name": "Terveys",
        "image_url": image_path + "/terveys.svg",
        "name": "terveys",
        "state": "active",
        "title": "Terveys",
        "title_translated": {
                "fi": "Terveys",
                "en": "Health",
                "sv": "Hälsa"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Tutkimukset (myös kysely- ja haastattelututkimukset), tutkimustieto ja -tulokset, teknologia",
        "description_translated": {
            "fi": "Tutkimukset (myös kysely- ja haastattelututkimukset), tutkimustieto ja -tulokset, teknologia",
            "en": "Research (including questionnaires and interviews), research data and results, technology",
            "sv": "Undersökningar (innehåller enkäter och intervjuundersökningar), forskningsdata och -resultat, teknologi"
        },
        "display_name": "Tiede ja teknologia",
        "image_url": image_path + "/tiede-ja-teknologia.svg",
        "name": "tiede-ja-teknologia",
        "state": "active",
        "title": "Tiede ja teknologia",
        "title_translated": {
                "fi": "Tiede ja teknologia",
                "en": "Science & Technology",
                "sv": "Forskning & teknologi"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Väestön koostumus, työllisyys, sosiaalipolitiikka, asuminen, maahanmuutto, sosiaaliturva",
        "description_translated": {
            "en": "Population demographics, employment, social policy, housing, immigration, social security",
            "fi": "Väestön koostumus, työllisyys, sosiaalipolitiikka, asuminen, maahanmuutto, sosiaaliturva",
            "sv": "Befolkningens sammansättning, sysselsättning, socialpolitik, invandring, social trygghet"
        },
        "display_name": "Väestö ja yhteiskunta",
        "image_url": image_path + "/vaesto-ja-yhteiskunta.svg",
        "name": "vaesto-ja-yhteiskunta",
        "state": "active",
        "title": "Väestö ja yhteiskunta",
        "title_translated": {
                "en": "Population & Society",
                "fi": "Väestö ja yhteiskunta",
                "sv": "Befolkning & samhälle"
        },
        "type": "group"
    },
    {
        "approval_status": "approved",
        "description": "Sää, luonnonympäristö, ympäristön pilaantuminen, jäte- ja vesihuolto",
        "description_translated": {
            "fi": "Sää, luonnonympäristö, ympäristön pilaantuminen, jäte- ja vesihuolto",
            "en": "Weather, natural environment, deterioration of the environment, waste and water management",
            "sv": "Väder, naturmiljö, försämring av miljön, avfallshantering & vattenförvaltning"
        },
        "display_name": "Ympäristö ja luonto",
        "image_url": image_path + "/ymparisto-ja-luonto.svg",
        "name": "ymparisto-ja-luonto",
        "state": "active",
        "title": "Ympäristö ja luonto",
        "title_translated": {
                "fi": "Ympäristö ja luonto",
                "en": "Environment & Nature",
                "sv": "Miljö & natur"
        },
        "type": "group"
    }
]


def create(context, dryrun):
    site_user = toolkit.get_action('get_site_user')({'ignore_auth': True})
    flask_app = context.meta['flask_app']

    if dryrun:
        click.secho('Dryrun')

    for category in default_categories:
        click.secho('Creating category [' + category.get('name', '') + ']')
        log.debug(category)
        if dryrun:
            click.secho('DRYRUN - category not created', fg='yellow')
        else:
            try:
                # Current user is tested agains sysadmin role during model
                # dictization, thus we need request context
                with flask_app.test_request_context():
                    res = get_action(u'group_create')({'ignore_auth': True, 'user': site_user['name']},
                                                        category)
                    click.secho('Category [' + res.get('name', '') + '] created', fg='green')
            except ValidationError:
                click.secho('Group [' + category['name'] +
                            '] already exists, skipping')

    click.secho("create_default_categories - DONE", fg="green")


def delete(context, dryrun, purge):
    site_user = toolkit.get_action('get_site_user')({'ignore_auth': True})
    flask_app = context.meta['flask_app']
    if dryrun:
       click.secho('Dryrun')

    for category in default_categories:
        # Current user is tested agains sysadmin role during model
        # dictization, thus we need request context
        with flask_app.test_request_context():
            data_dict = {'id': category['name']}
            try:
                found = get_action(u'group_show')({'ignore_auth': True, 'user': site_user['name']},
                                                        data_dict)
                if found:
                    click.secho('Category [' + found.get('name') + '] exists')
                    if dryrun:
                        click.secho('DRYRUN - Category [' + found.get('name') + '] not deleted', fg='yellow')
                    else:
                        if purge:
                            get_action(u'group_purge')({'ignore_auth': True, 'user': site_user['name']},
                                                    data_dict)
                            click.secho('Category [' + found.get('name') + '] purged', fg='green')
                        else:
                            get_action(u'group_delete')({'ignore_auth': True, 'user': site_user['name']},
                                                    data_dict)
                            click.secho('Category [' + found.get('name') + '] deleted', fg='green')
            except logic.NotFound:
                click.secho('Category not found, skipping')

    click.secho("delete_default_categories - DONE", fg="green")
