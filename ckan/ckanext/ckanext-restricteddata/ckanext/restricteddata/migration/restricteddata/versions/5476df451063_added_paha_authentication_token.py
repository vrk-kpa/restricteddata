"""Added paha_authentication_token

Revision ID: 5476df451063
Revises: 3aa74eb7aaee
Create Date: 2024-11-13 13:41:02.311416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5476df451063'
down_revision = '3aa74eb7aaee'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
            "paha_authentication_token",
            sa.Column("id", sa.UnicodeText, primary_key=True),
            sa.Column("user_id", sa.UnicodeText, nullable=False),
            sa.Column("secret", sa.UnicodeText, nullable=False),
            sa.Column("expires", sa.DateTime))


def downgrade():
    op.drop_table("paha_authentication_token")
