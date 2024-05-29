"""Second commit

Revision ID: 114e4e70a18d
Revises: d4b16c14f6fe
Create Date: 2024-05-29 15:28:26.814298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '114e4e70a18d'
down_revision: Union[str, None] = 'd4b16c14f6fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_address_country', table_name='address')
    op.create_index(op.f('ix_address_country'), 'address', ['country'], unique=False)
    op.drop_index('ix_address_street', table_name='address')
    op.create_index(op.f('ix_address_street'), 'address', ['street'], unique=False)
    op.drop_index('ix_address_zip_code', table_name='address')
    op.create_index(op.f('ix_address_zip_code'), 'address', ['zip_code'], unique=False)
    op.drop_index('ix_user_name', table_name='user')
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.create_index('ix_user_name', 'user', ['name'], unique=True)
    op.drop_index(op.f('ix_address_zip_code'), table_name='address')
    op.create_index('ix_address_zip_code', 'address', ['zip_code'], unique=True)
    op.drop_index(op.f('ix_address_street'), table_name='address')
    op.create_index('ix_address_street', 'address', ['street'], unique=True)
    op.drop_index(op.f('ix_address_country'), table_name='address')
    op.create_index('ix_address_country', 'address', ['country'], unique=True)
    # ### end Alembic commands ###