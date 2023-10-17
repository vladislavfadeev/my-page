from flask import session, request
from datetime import datetime
import re
from jinja2 import evalcontextfilter, Markup
 
 
def add_context(app):
    @app.context_processor
    def inject_lang():
        lang = session.get('lang') if not request.args.get('lang') else request.args.get('lang')
        return {'lang': lang}
 
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
 
    @app.template_filter()
    @evalcontextfilter
    def nl2br(eval_ctx, value):
        """Converts newlines in text to HTML-tags"""
 
        value = re.sub(r'\r\n|\r|\n', '\n', value)  # normalize newlines
        paras = re.split('\n{2,}', value)
        paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
        paras = u'\n\n'.join(paras)
        return Markup(paras)