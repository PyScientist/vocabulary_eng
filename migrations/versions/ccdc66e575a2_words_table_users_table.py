"""words table, users table

Revision ID: ccdc66e575a2
Revises: 
Create Date: 2024-05-16 11:15:38.282049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccdc66e575a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('nickname', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_nickname'), ['nickname'], unique=True)

    op.create_table('words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('speach_part', sa.String(length=30), nullable=False),
    sa.Column('translations', sa.String(length=256), nullable=False),
    sa.Column('definition', sa.String(length=300), nullable=False),
    sa.Column('importance', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(length=30), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('words', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_words_creation_date'), ['creation_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_words_importance'), ['importance'], unique=False)
        batch_op.create_index(batch_op.f('ix_words_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_words_speach_part'), ['speach_part'], unique=False)
        batch_op.create_index(batch_op.f('ix_words_topic'), ['topic'], unique=False)
        batch_op.create_index(batch_op.f('ix_words_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('words', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_words_user_id'))
        batch_op.drop_index(batch_op.f('ix_words_topic'))
        batch_op.drop_index(batch_op.f('ix_words_speach_part'))
        batch_op.drop_index(batch_op.f('ix_words_name'))
        batch_op.drop_index(batch_op.f('ix_words_importance'))
        batch_op.drop_index(batch_op.f('ix_words_creation_date'))

    op.drop_table('words')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_nickname'))
        batch_op.drop_index(batch_op.f('ix_users_name'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    # ### end Alembic commands ###