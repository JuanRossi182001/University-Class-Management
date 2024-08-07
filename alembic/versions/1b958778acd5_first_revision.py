"""first revision

Revision ID: 1b958778acd5
Revises: 
Create Date: 2024-04-29 12:42:37.585710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b958778acd5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ### 
    op.create_table('Carrers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('duration_in_years', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Subjects',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('semester', sa.VARCHAR(), nullable=True),
    sa.Column('carrer_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['carrer_id'], ['Carrers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Classrooms',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Hours',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('start_hour', sa.TIMESTAMP(), nullable=True),
    sa.Column('end_hour', sa.TIMESTAMP(), nullable=True),
    sa.Column('subject_id', sa.INTEGER(), nullable=True),
    sa.Column('classroom_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['classroom_id'], ['Classrooms.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['Subjects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    
    
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Subjects')
    op.drop_table('Hours')
    op.drop_table('Classrooms')
    op.drop_table('Carrers')
    # ### end Alembic commands ###
