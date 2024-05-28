"""first migrations

Revision ID: 8a4ef1b5d3f0
Revises: 04bcfacff489
Create Date: 2024-05-27 18:47:02.840550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a4ef1b5d3f0'
down_revision: Union[str, None] = '04bcfacff489'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
