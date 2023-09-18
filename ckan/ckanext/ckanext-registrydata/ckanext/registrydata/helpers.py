from ckan.plugins import toolkit
from ckan.lib import i18n
from ckanext.scheming.helpers import lang
from logging import getLogger
from datetime import datetime, timedelta
import iso8601
import requests


log = getLogger(__name__)
_ = toolkit._

_LOCALE_ALIASES = {'en_GB': 'en'}


def scheming_field_only_default_required(field, lang):
    return bool(field
                and field.get('only_default_lang_required')
                and lang == toolkit.config.get('ckan.locale_default', 'en'))


def add_locale_to_source(kwargs, locale):
    copy = kwargs.copy()
    source = copy.get('data-module-source', None)
    if source:
        copy.update({'data-module-source': source + '_' + locale})
        return copy
    return copy


def is_boolean_selected(value, selected):
    try:
        return toolkit.asbool(value) is toolkit.asbool(selected)
    except ValueError:
        return


def scheming_language_text_or_empty(text, prefer_lang=None):
    """
    :param text: {lang: text} dict or text string
    :param prefer_lang: choose this language version if available
    Convert "language-text" to users' language by looking up
    language in dict or using gettext if not a dict
    """
    if not text:
        return ''

    if hasattr(text, 'get'):
        try:
            if prefer_lang is None:
                prefer_lang = lang()
        except TypeError:
            pass  # lang() call will fail when no user language available
        else:
            if prefer_lang in _LOCALE_ALIASES:
                prefer_lang = _LOCALE_ALIASES[prefer_lang]
            try:
                return text[prefer_lang]
            except KeyError:
                return ''

    t = _(text)
    if isinstance(t, str):
        return t.decode('utf-8')
    return t


def get_lang_prefix():
    language = i18n.get_lang()
    if language in _LOCALE_ALIASES:
        language = _LOCALE_ALIASES[language]

    return language


def call_toolkit_function(fn, args, kwargs):
    return getattr(toolkit, fn)(*args, **kwargs)


NEWS_CACHE = None


def get_homepage_news(count=4, cache_duration=timedelta(days=1), language=None):
    global NEWS_CACHE
    log.debug('Fetching homepage news')
    if NEWS_CACHE is None or datetime.now() - NEWS_CACHE[0] > cache_duration:
        log.debug('Updating news cache')
        news_endpoint_url = toolkit.config.get('ckanext.registrydata.news.endpoint_url')
        news_ssl_verify = toolkit.asbool(toolkit.config.get('ckanext.registrydata.news.ssl_verify', True))
        news_tags = toolkit.config.get('ckanext.registrydata.news.tags')
        news_url_template = toolkit.config.get('ckanext.registrydata.news.url_template')

        if not news_endpoint_url:
            log.warning('ckanext.registrydata.news.endpoint_url not set')
            news = []
        else:
            log.debug('Fetching from %s', news_endpoint_url)
            try:
                news_items = requests.get(news_endpoint_url, verify=news_ssl_verify).json()
                log.debug('Received %i news items', len(news_items))

                tags = set(t.strip() for t in news_tags.split(',')) if news_tags else None
                if tags:
                    log.debug('Filtering with tags: %s', repr(tags))
                    news_items = [n for n in news_items if any(t.get('slug') in tags for t in n.get('tags', []))]

                news = [{'title': {tl: t for tl, t in list(item.get('title', {}).items()) if t != 'undefined'},
                         'content': {tl: t for tl, t in list(item.get('content', {}).items()) if t != 'undefined'},
                         'published': iso8601.parse_date(item.get('publishedAt')),
                         'brief': item.get('brief', {}),
                         'image': '',
                         'image_alt': '',
                         'tags': [tag for tag in item.get('tags', []) if tag.get('slug') in news_tags],
                         'url': {lang: news_url_template.format(**{'id': item.get('id'), 'language': lang})
                                 for lang in list(item.get('title').keys())}}
                        for item in news_items]
                news.sort(key=lambda x: x['published'], reverse=True)

                log.debug('Updating news cache with %i news', len(news))
                news_cache_timestamp = datetime.now()
                NEWS_CACHE = (news_cache_timestamp, news)

            except Exception as e:
                # Fetch failed for some reason, keep old value until cache invalidates
                log.error(e)
                news = [] if NEWS_CACHE is None else NEWS_CACHE[1]

    else:
        log.debug('Returning cached news')
        news_cache_timestamp, news = NEWS_CACHE

    if language:
        news = [n for n in news if language in n.get('title', {}) and language in n.get('content', {})]

    return news[:count]


def get_site_name():
    return toolkit.config.get('ckanext.registrydata.site_name')
