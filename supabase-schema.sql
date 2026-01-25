-- ============================================
-- EVERFRESH MESSAGING - SUPABASE SCHEMA
-- Run this in Supabase SQL Editor
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- CONTACTS TABLE
-- Stores customer/salesman contact info
-- ============================================
CREATE TABLE contacts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    business_name VARCHAR(100),
    avatar_url TEXT,
    role VARCHAR(20) DEFAULT 'customer' CHECK (role IN ('customer', 'salesman', 'admin')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- CONVERSATIONS TABLE
-- Links two contacts in a chat
-- ============================================
CREATE TABLE conversations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    participant_1 UUID REFERENCES contacts(id) ON DELETE CASCADE,
    participant_2 UUID REFERENCES contacts(id) ON DELETE CASCADE,
    last_message_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Ensure unique conversation between two people
    UNIQUE(participant_1, participant_2)
);

-- Index for faster lookups
CREATE INDEX idx_conversations_participants ON conversations(participant_1, participant_2);
CREATE INDEX idx_conversations_last_message ON conversations(last_message_at DESC);

-- ============================================
-- MESSAGES TABLE
-- Stores all chat messages
-- ============================================
CREATE TABLE messages (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id UUID REFERENCES contacts(id) ON DELETE SET NULL,

    -- Message content
    content TEXT,

    -- Media attachments (array of R2 URLs)
    media JSONB DEFAULT '[]',
    -- Format: [{"url": "https://...", "type": "image", "name": "photo.jpg", "size": 12345}]

    -- File attachments
    files JSONB DEFAULT '[]',
    -- Format: [{"url": "https://...", "name": "doc.pdf", "size": 12345, "type": "application/pdf"}]

    -- Message metadata
    status VARCHAR(20) DEFAULT 'sent' CHECK (status IN ('sending', 'sent', 'delivered', 'read', 'failed')),
    reply_to UUID REFERENCES messages(id) ON DELETE SET NULL,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for fast queries
CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at DESC);
CREATE INDEX idx_messages_sender ON messages(sender_id);

-- ============================================
-- MESSAGE READ RECEIPTS
-- Track who has read which messages
-- ============================================
CREATE TABLE message_reads (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    message_id UUID REFERENCES messages(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    read_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(message_id, contact_id)
);

-- ============================================
-- ROW LEVEL SECURITY (RLS)
-- Secure data access
-- ============================================

-- Enable RLS on all tables
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE message_reads ENABLE ROW LEVEL SECURITY;

-- Contacts: Users can read all contacts, update only their own
CREATE POLICY "Contacts are viewable by everyone" ON contacts
    FOR SELECT USING (true);

CREATE POLICY "Users can update own contact" ON contacts
    FOR UPDATE USING (auth.uid()::text = id::text);

-- Conversations: Users can only see their own conversations
CREATE POLICY "Users can view own conversations" ON conversations
    FOR SELECT USING (
        auth.uid()::text = participant_1::text OR
        auth.uid()::text = participant_2::text
    );

CREATE POLICY "Users can create conversations" ON conversations
    FOR INSERT WITH CHECK (
        auth.uid()::text = participant_1::text OR
        auth.uid()::text = participant_2::text
    );

-- Messages: Users can see messages in their conversations
CREATE POLICY "Users can view messages in their conversations" ON messages
    FOR SELECT USING (
        conversation_id IN (
            SELECT id FROM conversations
            WHERE participant_1::text = auth.uid()::text
               OR participant_2::text = auth.uid()::text
        )
    );

CREATE POLICY "Users can send messages to their conversations" ON messages
    FOR INSERT WITH CHECK (
        conversation_id IN (
            SELECT id FROM conversations
            WHERE participant_1::text = auth.uid()::text
               OR participant_2::text = auth.uid()::text
        )
    );

-- ============================================
-- REAL-TIME SUBSCRIPTIONS
-- Enable real-time for messages
-- ============================================
ALTER PUBLICATION supabase_realtime ADD TABLE messages;
ALTER PUBLICATION supabase_realtime ADD TABLE conversations;

-- ============================================
-- HELPER FUNCTIONS
-- ============================================

-- Function to update conversation's last_message_at
CREATE OR REPLACE FUNCTION update_conversation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations
    SET last_message_at = NOW()
    WHERE id = NEW.conversation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update conversation timestamp
CREATE TRIGGER on_new_message
    AFTER INSERT ON messages
    FOR EACH ROW
    EXECUTE FUNCTION update_conversation_timestamp();

-- Function to get or create conversation between two contacts
CREATE OR REPLACE FUNCTION get_or_create_conversation(contact_a UUID, contact_b UUID)
RETURNS UUID AS $$
DECLARE
    conv_id UUID;
BEGIN
    -- Check if conversation exists (in either order)
    SELECT id INTO conv_id FROM conversations
    WHERE (participant_1 = contact_a AND participant_2 = contact_b)
       OR (participant_1 = contact_b AND participant_2 = contact_a);

    -- If not, create it
    IF conv_id IS NULL THEN
        INSERT INTO conversations (participant_1, participant_2)
        VALUES (contact_a, contact_b)
        RETURNING id INTO conv_id;
    END IF;

    RETURN conv_id;
END;
$$ LANGUAGE plpgsql;
