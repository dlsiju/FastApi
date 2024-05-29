"""Third commit

Revision ID: 6d52eb1d168d
Revises: 114e4e70a18d
Create Date: 2024-05-29 16:59:04.768561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d52eb1d168d'
down_revision: Union[str, None] = '114e4e70a18d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('bank', sa.String(), nullable=True),
    sa.Column('balance', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_balance'), 'account', ['balance'], unique=False)
    op.create_index(op.f('ix_account_bank'), 'account', ['bank'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_account_bank'), table_name='account')
    op.drop_index(op.f('ix_account_balance'), table_name='account')
    op.drop_table('account')
    # ### end Alembic commands ###