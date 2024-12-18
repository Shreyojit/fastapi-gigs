"""initial migrations

Revision ID: 80f5a82430af
Revises: 8612f2b9a90c
Create Date: 2024-11-28 21:36:27.034008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80f5a82430af'
down_revision: Union[str, None] = '8612f2b9a90c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'country',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'country',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
