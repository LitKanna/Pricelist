-- ============================================
-- EVERFRESH - TEST DATA
-- Run this in Supabase SQL Editor to add sample data
-- ============================================

-- First, create the salesman (this matches what the app creates)
INSERT INTO contacts (phone, name, role)
VALUES ('+61400000001', 'Everfresh Sales', 'salesman')
ON CONFLICT (phone) DO UPDATE SET name = EXCLUDED.name
RETURNING id;

-- Create some test customers
INSERT INTO contacts (phone, name, business_name, role) VALUES
('+61400111222', 'John Smith', 'John''s Restaurant', 'customer'),
('+61400333444', 'Mary Johnson', 'Mary''s Cafe', 'customer'),
('+61400555666', 'Peter Wong', 'Peter''s Grocery', 'customer'),
('+61400777888', 'Sarah Lee', 'ABC Produce', 'customer')
ON CONFLICT (phone) DO NOTHING;

-- Get IDs for creating conversations
DO $$
DECLARE
    salesman_id UUID;
    john_id UUID;
    mary_id UUID;
    peter_id UUID;
    sarah_id UUID;
    conv1_id UUID;
    conv2_id UUID;
    conv3_id UUID;
BEGIN
    -- Get salesman ID
    SELECT id INTO salesman_id FROM contacts WHERE phone = '+61400000001';

    -- Get customer IDs
    SELECT id INTO john_id FROM contacts WHERE phone = '+61400111222';
    SELECT id INTO mary_id FROM contacts WHERE phone = '+61400333444';
    SELECT id INTO peter_id FROM contacts WHERE phone = '+61400555666';
    SELECT id INTO sarah_id FROM contacts WHERE phone = '+61400777888';

    -- Create conversations
    INSERT INTO conversations (participant_1, participant_2, last_message_at)
    VALUES (salesman_id, john_id, NOW() - INTERVAL '2 minutes')
    ON CONFLICT DO NOTHING
    RETURNING id INTO conv1_id;

    IF conv1_id IS NULL THEN
        SELECT id INTO conv1_id FROM conversations
        WHERE (participant_1 = salesman_id AND participant_2 = john_id)
           OR (participant_1 = john_id AND participant_2 = salesman_id);
    END IF;

    INSERT INTO conversations (participant_1, participant_2, last_message_at)
    VALUES (salesman_id, mary_id, NOW() - INTERVAL '1 hour')
    ON CONFLICT DO NOTHING
    RETURNING id INTO conv2_id;

    IF conv2_id IS NULL THEN
        SELECT id INTO conv2_id FROM conversations
        WHERE (participant_1 = salesman_id AND participant_2 = mary_id)
           OR (participant_1 = mary_id AND participant_2 = salesman_id);
    END IF;

    INSERT INTO conversations (participant_1, participant_2, last_message_at)
    VALUES (salesman_id, peter_id, NOW() - INTERVAL '1 day')
    ON CONFLICT DO NOTHING
    RETURNING id INTO conv3_id;

    IF conv3_id IS NULL THEN
        SELECT id INTO conv3_id FROM conversations
        WHERE (participant_1 = salesman_id AND participant_2 = peter_id)
           OR (participant_1 = peter_id AND participant_2 = salesman_id);
    END IF;

    -- Add messages to John's conversation
    IF conv1_id IS NOT NULL THEN
        INSERT INTO messages (conversation_id, sender_id, content, created_at) VALUES
        (conv1_id, salesman_id, 'Hi John! Here''s today''s price list', NOW() - INTERVAL '1 hour'),
        (conv1_id, john_id, 'Thanks! Let me check', NOW() - INTERVAL '30 minutes'),
        (conv1_id, john_id, 'I want 5kg okra and 2kg curry leaf', NOW() - INTERVAL '2 minutes');
    END IF;

    -- Add messages to Mary's conversation
    IF conv2_id IS NOT NULL THEN
        INSERT INTO messages (conversation_id, sender_id, content, created_at) VALUES
        (conv2_id, salesman_id, 'Good morning Mary!', NOW() - INTERVAL '2 hours'),
        (conv2_id, mary_id, 'Hi! Do you have fresh coriander today?', NOW() - INTERVAL '1 hour 30 minutes'),
        (conv2_id, salesman_id, 'Yes, just got a fresh batch!', NOW() - INTERVAL '1 hour');
    END IF;

    -- Add messages to Peter's conversation
    IF conv3_id IS NOT NULL THEN
        INSERT INTO messages (conversation_id, sender_id, content, created_at) VALUES
        (conv3_id, peter_id, 'Thanks for the delivery yesterday', NOW() - INTERVAL '1 day'),
        (conv3_id, salesman_id, 'You''re welcome! See you next week', NOW() - INTERVAL '23 hours');
    END IF;

    RAISE NOTICE 'Test data inserted successfully!';
END $$;

-- Verify the data
SELECT 'Contacts:' as info;
SELECT id, name, phone, role FROM contacts ORDER BY created_at;

SELECT 'Conversations:' as info;
SELECT c.id,
       p1.name as participant_1,
       p2.name as participant_2,
       c.last_message_at
FROM conversations c
JOIN contacts p1 ON c.participant_1 = p1.id
JOIN contacts p2 ON c.participant_2 = p2.id;

SELECT 'Messages:' as info;
SELECT m.id,
       s.name as sender,
       m.content,
       m.created_at
FROM messages m
JOIN contacts s ON m.sender_id = s.id
ORDER BY m.created_at;
