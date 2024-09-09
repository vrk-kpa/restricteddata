"""Add temporary_member table

Revision ID: 3aa74eb7aaee
Revises: 
Create Date: 2024-09-09 07:16:50.806419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aa74eb7aaee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
            "temporary_member",
            sa.Column("id", sa.UnicodeText, primary_key=True),
            sa.Column("user_id", sa.UnicodeText, nullable=False),
            sa.Column("organization_id", sa.UnicodeText, nullable=False),
            sa.Column("expires", sa.DateTime),
            sa.Column("member_id", sa.UnicodeText, sa.ForeignKey("member.id", ondelete="CASCADE")))


def downgrade():
    op.drop_table("temporary_member")

