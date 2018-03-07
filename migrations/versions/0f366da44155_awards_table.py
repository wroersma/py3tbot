"""awards table

Revision ID: 0f366da44155
Revises: 7f3e4393105c
Create Date: 2018-02-16 18:22:06.025244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f366da44155'
down_revision = '7f3e4393105c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('award',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('award_name', sa.String(length=128), nullable=True),
    sa.Column('username', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_award_award_name'), 'award', ['award_name'], unique=False)
    op.create_index(op.f('ix_award_timestamp'), 'award', ['timestamp'], unique=False)
    op.drop_table('post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('language', sa.VARCHAR(length=5), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index(op.f('ix_award_timestamp'), table_name='award')
    op.drop_index(op.f('ix_award_award_name'), table_name='award')
    op.drop_table('award')
    # ### end Alembic commands ###
