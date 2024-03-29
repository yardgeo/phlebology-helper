"""add state fields

Revision ID: 0a0cfb6815c6
Revises: d6874accfa9d
Create Date: 2021-04-20 18:55:50.427216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a0cfb6815c6'
down_revision = 'd6874accfa9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('series',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('study_id', sa.String(length=128), nullable=True),
    sa.Column('orientation', sa.String(length=128), nullable=True),
    sa.Column('original_state', sa.JSON(), nullable=True),
    sa.Column('dynamic_state', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('instance', sa.Column('series_id', sa.String(length=128), nullable=True))
    op.drop_constraint('instance_study_id_fkey', 'instance', type_='foreignkey')
    op.create_foreign_key(None, 'instance', 'series', ['series_id'], ['id'])
    op.drop_column('instance', 'study_id')
    op.drop_column('instance', 'orientation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instance', sa.Column('orientation', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('instance', sa.Column('study_id', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'instance', type_='foreignkey')
    op.create_foreign_key('instance_study_id_fkey', 'instance', 'study', ['study_id'], ['id'])
    op.drop_column('instance', 'series_id')
    op.drop_table('series')
    # ### end Alembic commands ###
