"""init

Revision ID: d6bd4abb5de5
Revises: bf1b91b0ecbb
Create Date: 2024-11-23 23:10:37.858708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6bd4abb5de5'
down_revision: Union[str, None] = 'bf1b91b0ecbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tariffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('cargo_type', sa.String(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'cargo_type', name='_date_cargo_uc')
    )
    op.create_index(op.f('ix_tariffs_id'), 'tariffs', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tariffs_id'), table_name='tariffs')
    op.drop_table('tariffs')
    # ### end Alembic commands ###
