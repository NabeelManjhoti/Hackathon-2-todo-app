"""Add conversation and message tables for AI chatbot

Revision ID: 001_add_chatbot_tables
Revises:
Create Date: 2026-02-14

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_add_chatbot_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create conversations and messages tables with indexes and trigger."""

    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create indexes for conversations
    op.create_index('idx_conversation_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversation_created_at', 'conversations', ['created_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', postgresql.JSONB(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('user', 'assistant', 'system')", name='check_message_role'),
    )

    # Create indexes for messages
    op.create_index('idx_message_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_message_timestamp', 'messages', ['timestamp'])
    op.create_index('idx_message_conversation_timestamp', 'messages', ['conversation_id', 'timestamp'])

    # Create trigger function to update conversation.updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_conversation_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE conversations
            SET updated_at = NEW.timestamp
            WHERE id = NEW.conversation_id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger on messages table
    op.execute("""
        CREATE TRIGGER trigger_update_conversation_timestamp
        AFTER INSERT ON messages
        FOR EACH ROW
        EXECUTE FUNCTION update_conversation_timestamp();
    """)


def downgrade() -> None:
    """Drop conversations and messages tables, trigger, and function."""

    # Drop trigger
    op.execute("DROP TRIGGER IF EXISTS trigger_update_conversation_timestamp ON messages")

    # Drop trigger function
    op.execute("DROP FUNCTION IF EXISTS update_conversation_timestamp()")

    # Drop messages table (indexes dropped automatically)
    op.drop_table('messages')

    # Drop conversations table (indexes dropped automatically)
    op.drop_table('conversations')
