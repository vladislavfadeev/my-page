import hmac
import hashlib
import secrets
import time
from urllib.parse import urlencode

import requests
from flask import current_app, session, request, redirect, url_for, abort
from flask_login import login_user

from app.extensions import db
from app.auth.models import User
from app.config import Config


PROVIDERS = {
    'google': {
        'authorize_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'userinfo_url': 'https://www.googleapis.com/oauth2/v3/userinfo',
        'scope': 'openid email profile',
    },
    'github': {
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'userinfo_url': 'https://api.github.com/user',
        'scope': 'read:user user:email',
    },
}


def _provider_creds(name):
    creds = Config.OAUTH.get(name) or {}
    if not creds.get('client_id') or not creds.get('client_secret'):
        abort(404)
    return creds


def _login_or_create(provider, provider_id, username, email=None, avatar_url=None):
    user = User.query.filter_by(provider=provider, provider_id=str(provider_id)).first()
    if user is None:
        user = User(provider=provider, provider_id=str(provider_id))
        db.session.add(user)
    user.username = username or user.username or f'{provider}_{provider_id}'
    if email:
        user.email = email
    if avatar_url:
        user.avatar_url = avatar_url
    db.session.commit()
    login_user(user)
    return user


def start(provider):
    if provider not in PROVIDERS:
        abort(404)
    cfg = PROVIDERS[provider]
    creds = _provider_creds(provider)
    state = secrets.token_urlsafe(16)
    session[f'oauth_state_{provider}'] = state
    session['oauth_next'] = request.args.get('next') or request.referrer
    params = {
        'client_id': creds['client_id'],
        'redirect_uri': url_for('auth.oauth_callback', provider=provider, _external=True),
        'response_type': 'code',
        'scope': cfg['scope'],
        'state': state,
    }
    return redirect(f"{cfg['authorize_url']}?{urlencode(params)}")


def callback(provider):
    if provider not in PROVIDERS:
        abort(404)
    cfg = PROVIDERS[provider]
    creds = _provider_creds(provider)
    if request.args.get('state') != session.pop(f'oauth_state_{provider}', None):
        abort(400)
    code = request.args.get('code')
    if not code:
        abort(400)

    token_resp = requests.post(
        cfg['token_url'],
        data={
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'code': code,
            'redirect_uri': url_for('auth.oauth_callback', provider=provider, _external=True),
            'grant_type': 'authorization_code',
        },
        headers={'Accept': 'application/json'},
        timeout=10,
    )
    token = token_resp.json().get('access_token')
    if not token:
        abort(400)

    info = requests.get(
        cfg['userinfo_url'],
        headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'},
        timeout=10,
    ).json()

    if provider == 'google':
        _login_or_create(
            provider='google',
            provider_id=info['sub'],
            username=info.get('name') or info.get('email'),
            email=info.get('email'),
            avatar_url=info.get('picture'),
        )
    elif provider == 'github':
        email = info.get('email')
        if not email:
            emails = requests.get(
                'https://api.github.com/user/emails',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10,
            ).json()
            primary = next((e for e in emails if e.get('primary')), None)
            email = primary['email'] if primary else None
        _login_or_create(
            provider='github',
            provider_id=info['id'],
            username=info.get('name') or info.get('login'),
            email=email,
            avatar_url=info.get('avatar_url'),
        )

    return redirect(session.pop('oauth_next', None) or url_for('blog.index'))


def telegram_callback():
    if not Config.TG_AUTH_BOT_TOKEN:
        abort(404)

    data = {k: v for k, v in request.args.items() if k not in ('hash', 'next')}
    received_hash = request.args.get('hash')
    if not received_hash:
        abort(400)

    auth_date = int(data.get('auth_date', 0))
    if abs(time.time() - auth_date) > 86400:
        abort(400)

    secret = hashlib.sha256(Config.TG_AUTH_BOT_TOKEN.encode()).digest()
    check = '\n'.join(f'{k}={data[k]}' for k in sorted(data))
    expected = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, received_hash):
        abort(400)

    username = data.get('username') or ' '.join(filter(None, [data.get('first_name'), data.get('last_name')]))
    _login_or_create(
        provider='telegram',
        provider_id=data['id'],
        username=username or f"tg_{data['id']}",
        avatar_url=data.get('photo_url'),
    )
    nxt = request.args.get('next') or session.pop('oauth_next', None) or ''
    return redirect(nxt if nxt.startswith('/') else url_for('blog.index'))
