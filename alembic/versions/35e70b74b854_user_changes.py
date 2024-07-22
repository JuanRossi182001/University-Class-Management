"""User Changes

Revision ID: 35e70b74b854
Revises: 7b8477ed9196
Create Date: 2024-07-22 17:57:31.368799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '35e70b74b854'
down_revision: Union[str, None] = '7b8477ed9196'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carrers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('duration_in_years', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('semester', sa.String(), nullable=True),
    sa.Column('carrer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['carrer_id'], ['carrers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('Users', 'role_id')
    op.add_column('Users', sa.Column('role_id', postgresql.ARRAY(sa.Integer), nullable=True))
    op.drop_constraint('fk_users_roles', 'Users', type_='foreignkey')
    op.drop_table('roles')
    op.create_foreign_key(None, 'Hours', 'subjects', ['subject_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('fk_users_roles', 'Users', 'roles', ['role_id'], ['id'])
    op.drop_constraint(None, 'Hours', type_='foreignkey')
    op.create_foreign_key('Hours_subject_id_fkey', 'Hours', 'Subjects', ['subject_id'], ['id'])
    op.create_table('Subjects',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Subjects_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('semester', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('carrer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['carrer_id'], ['Carrers.id'], name='Subjects_carrer_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Subjects_pkey')
    )
    op.drop_column('Users', 'role_id')
    op.add_column('Users', sa.Column('role_id', sa.Integer, nullable=True))
    op.create_table('Carrers',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Carrers_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('duration_in_years', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Carrers_pkey')
    )
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey')
    )
    op.drop_table('subjects')
    op.drop_table('carrers')
    # ### end Alembic commands ###
