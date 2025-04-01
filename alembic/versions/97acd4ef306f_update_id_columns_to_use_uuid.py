"""Update id columns to use UUID

Revision ID: 97acd4ef306f
Revises: 
Create Date: 2025-04-01 19:58:29.125857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '97acd4ef306f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create UUID extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    
    # First, add temporary UUID columns
    op.add_column('users', sa.Column('uuid_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('stories', sa.Column('uuid_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('stories', sa.Column('uuid_user_id', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Generate UUIDs for temporary columns
    op.execute("UPDATE users SET uuid_id = uuid_generate_v4()")
    op.execute("UPDATE stories SET uuid_id = uuid_generate_v4()")
    op.execute("UPDATE stories SET uuid_user_id = uuid_generate_v4() WHERE user_id IS NOT NULL")
    
    # Drop existing primary key constraints and foreign keys
    op.drop_constraint('stories_user_id_fkey', 'stories', type_='foreignkey')
    op.drop_constraint('users_pkey', 'users', type_='primary')
    op.drop_constraint('stories_pkey', 'stories', type_='primary')
    
    # Drop old columns and rename new ones
    op.drop_column('users', 'id')
    op.drop_column('stories', 'id')
    op.drop_column('stories', 'user_id')
    
    op.alter_column('users', 'uuid_id', new_column_name='id', nullable=False)
    op.alter_column('stories', 'uuid_id', new_column_name='id', nullable=False)
    op.alter_column('stories', 'uuid_user_id', new_column_name='user_id', nullable=True)
    
    # Add back primary key and foreign key constraints
    op.create_primary_key('users_pkey', 'users', ['id'])
    op.create_primary_key('stories_pkey', 'stories', ['id'])
    op.create_foreign_key('stories_user_id_fkey', 'stories', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # This is a complex operation that would require temporary columns again
    # For simplicity, we'll just indicate that downgrade is not supported
    op.execute("-- WARNING: Downgrade from UUID to INTEGER not implemented")
    pass
