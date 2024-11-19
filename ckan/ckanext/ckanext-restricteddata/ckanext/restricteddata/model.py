import secrets

from datetime import datetime
from ckan.plugins import toolkit
from sqlalchemy import types, Column, ForeignKey
from sqlalchemy.orm import relationship
from ckan.model import meta, Member
from ckan.model.types import make_uuid

class TemporaryMember(toolkit.BaseModel):
    __tablename__ = "temporary_member"
    id = Column("id", primary_key=True, default=make_uuid)
    user_id = Column("user_id", types.UnicodeText, nullable=False)
    organization_id = Column("organization_id", types.UnicodeText, nullable=False)
    expires = Column("expires", types.DateTime)
    member_id = Column("member_id", types.UnicodeText, ForeignKey("member.id", ondelete="CASCADE"))
    member = relationship(Member, cascade="all, delete, delete-orphan", single_parent=True)

    def __init__(self, user_id: str, organization_id: str, expires: datetime, member_id: str):
        self.user_id = user_id
        self.organization_id = organization_id
        self.expires = expires
        self.member_id = member_id

    @classmethod
    def purge_expired(cls):
        now = datetime.now()
        all_expired = meta.Session.query(cls).filter(cls.expires <= now).all()
        for expired in all_expired:
            member = Member.get(expired.member_id)
            meta.Session.delete(expired)
            member.delete()
        meta.Session.commit()

    @classmethod
    def get(cls, user_id: str, organization_id: str):
        now = datetime.now()
        return (meta.Session.query(cls)
                .filter(cls.user_id == user_id)
                .filter(cls.organization_id == organization_id)
                .where(cls.expires > now)
                .first())


class PahaAuthenticationToken(toolkit.BaseModel):
    __tablename__ = "paha_authentication_token"
    id = Column("id", primary_key=True, default=make_uuid)
    secret = Column("secret", types.UnicodeText, nullable=False)
    user_id = Column("user_id", types.UnicodeText, nullable=False)
    expires = Column("expires", types.DateTime)

    def __init__(self, user_id, expires):
        self.secret = secrets.token_urlsafe(128)
        self.user_id = user_id
        self.expires = expires

    @classmethod
    def purge_expired(cls):
        now = datetime.now()
        all_expired = meta.Session.query(cls).filter(cls.expires <= now).all()
        for expired in all_expired:
            meta.Session.delete(expired)
        meta.Session.commit()

    @classmethod
    def get(cls, secret: str):
        now = datetime.now()
        return (meta.Session.query(cls)
                .filter(cls.secret == secret)
                .where(cls.expires > now)
                .first())
