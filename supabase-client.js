// ============================================
// EVERFRESH - SUPABASE CLIENT
// Handles all database operations for messaging
// ============================================

// Initialize Supabase client
// Make sure to include: <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

let supabase = null;
let currentUser = null;

/**
 * Initialize Supabase connection
 */
function initSupabase(url, anonKey) {
    supabase = window.supabase.createClient(url, anonKey);
    console.log('Supabase initialized');
    return supabase;
}

/**
 * Get or create a contact by phone number
 */
async function getOrCreateContact(phone, name, role = 'customer') {
    // Check if exists
    let { data: contact, error } = await supabase
        .from('contacts')
        .select('*')
        .eq('phone', phone)
        .single();

    if (error && error.code !== 'PGRST116') {
        console.error('Error fetching contact:', error);
        return null;
    }

    // Create if doesn't exist
    if (!contact) {
        const { data: newContact, error: createError } = await supabase
            .from('contacts')
            .insert({ phone, name, role })
            .select()
            .single();

        if (createError) {
            console.error('Error creating contact:', createError);
            return null;
        }
        contact = newContact;
    }

    return contact;
}

/**
 * Set current user (salesman)
 */
async function setCurrentUser(phone, name) {
    currentUser = await getOrCreateContact(phone, name, 'salesman');
    return currentUser;
}

/**
 * Get all conversations for current user
 */
async function getConversations() {
    if (!currentUser) return [];

    const { data, error } = await supabase
        .from('conversations')
        .select(`
            id,
            last_message_at,
            participant_1 (id, name, phone, avatar_url, business_name),
            participant_2 (id, name, phone, avatar_url, business_name),
            messages (
                id,
                content,
                media,
                created_at,
                sender_id
            )
        `)
        .or(`participant_1.eq.${currentUser.id},participant_2.eq.${currentUser.id}`)
        .order('last_message_at', { ascending: false })
        .limit(1, { foreignTable: 'messages' });

    if (error) {
        console.error('Error fetching conversations:', error);
        return [];
    }

    // Transform to simpler format
    return data.map(conv => {
        const otherPerson = conv.participant_1.id === currentUser.id
            ? conv.participant_2
            : conv.participant_1;
        const lastMessage = conv.messages[0];

        return {
            id: conv.id,
            contact: otherPerson,
            lastMessage: lastMessage?.content || (lastMessage?.media?.length ? 'Photo' : ''),
            lastMessageAt: conv.last_message_at,
            unread: 0 // TODO: Calculate from message_reads
        };
    });
}

/**
 * Get messages for a conversation
 */
async function getMessages(conversationId, limit = 50, offset = 0) {
    const { data, error } = await supabase
        .from('messages')
        .select(`
            id,
            content,
            media,
            files,
            status,
            created_at,
            sender_id,
            sender:contacts!sender_id (id, name, phone)
        `)
        .eq('conversation_id', conversationId)
        .order('created_at', { ascending: false })
        .range(offset, offset + limit - 1);

    if (error) {
        console.error('Error fetching messages:', error);
        return [];
    }

    // Reverse to show oldest first
    return data.reverse().map(msg => ({
        id: msg.id,
        content: msg.content,
        media: msg.media || [],
        files: msg.files || [],
        status: msg.status,
        createdAt: msg.created_at,
        senderId: msg.sender_id,
        sender: msg.sender,
        direction: msg.sender_id === currentUser?.id ? 'out' : 'in'
    }));
}

/**
 * Send a message
 */
async function sendMessage(conversationId, content, media = [], files = []) {
    if (!currentUser) {
        console.error('No current user set');
        return null;
    }

    const { data, error } = await supabase
        .from('messages')
        .insert({
            conversation_id: conversationId,
            sender_id: currentUser.id,
            content: content || null,
            media: media,
            files: files,
            status: 'sent'
        })
        .select()
        .single();

    if (error) {
        console.error('Error sending message:', error);
        return null;
    }

    return data;
}

/**
 * Start a new conversation with a contact
 */
async function startConversation(contactPhone, contactName) {
    if (!currentUser) return null;

    // Get or create the contact
    const contact = await getOrCreateContact(contactPhone, contactName, 'customer');
    if (!contact) return null;

    // Use database function to get or create conversation
    const { data, error } = await supabase
        .rpc('get_or_create_conversation', {
            contact_a: currentUser.id,
            contact_b: contact.id
        });

    if (error) {
        console.error('Error creating conversation:', error);
        return null;
    }

    return { conversationId: data, contact };
}

/**
 * Subscribe to new messages in a conversation (real-time)
 */
function subscribeToMessages(conversationId, onNewMessage) {
    const subscription = supabase
        .channel(`messages:${conversationId}`)
        .on(
            'postgres_changes',
            {
                event: 'INSERT',
                schema: 'public',
                table: 'messages',
                filter: `conversation_id=eq.${conversationId}`
            },
            (payload) => {
                const msg = payload.new;
                onNewMessage({
                    id: msg.id,
                    content: msg.content,
                    media: msg.media || [],
                    files: msg.files || [],
                    status: msg.status,
                    createdAt: msg.created_at,
                    senderId: msg.sender_id,
                    direction: msg.sender_id === currentUser?.id ? 'out' : 'in'
                });
            }
        )
        .subscribe();

    return subscription;
}

/**
 * Unsubscribe from messages
 */
function unsubscribeFromMessages(subscription) {
    if (subscription) {
        supabase.removeChannel(subscription);
    }
}

/**
 * Subscribe to conversation list updates
 */
function subscribeToConversations(onUpdate) {
    const subscription = supabase
        .channel('conversations')
        .on(
            'postgres_changes',
            {
                event: '*',
                schema: 'public',
                table: 'conversations'
            },
            () => {
                // Refresh conversation list
                onUpdate();
            }
        )
        .subscribe();

    return subscription;
}

/**
 * Upload file to Supabase Storage (proxy to R2 or direct)
 * Returns the public URL
 */
async function uploadFile(file, folder = 'media') {
    const fileName = `${folder}/${Date.now()}-${file.name}`;

    const { data, error } = await supabase.storage
        .from('everfresh-media')
        .upload(fileName, file, {
            cacheControl: '3600',
            upsert: false
        });

    if (error) {
        console.error('Error uploading file:', error);
        return null;
    }

    // Get public URL
    const { data: urlData } = supabase.storage
        .from('everfresh-media')
        .getPublicUrl(fileName);

    return {
        url: urlData.publicUrl,
        name: file.name,
        size: file.size,
        type: file.type.startsWith('image/') ? 'image' :
              file.type.startsWith('video/') ? 'video' : 'file'
    };
}

/**
 * Upload multiple files
 */
async function uploadFiles(files) {
    const uploads = await Promise.all(
        Array.from(files).map(file => uploadFile(file))
    );
    return uploads.filter(u => u !== null);
}

/**
 * Delete a message
 */
async function deleteMessage(messageId) {
    const { error } = await supabase
        .from('messages')
        .delete()
        .eq('id', messageId)
        .eq('sender_id', currentUser?.id); // Can only delete own messages

    return !error;
}

/**
 * Delete a conversation
 */
async function deleteConversation(conversationId) {
    const { error } = await supabase
        .from('conversations')
        .delete()
        .eq('id', conversationId);

    return !error;
}

// Export for use
if (typeof module !== 'undefined') {
    module.exports = {
        initSupabase,
        setCurrentUser,
        getOrCreateContact,
        getConversations,
        getMessages,
        sendMessage,
        startConversation,
        subscribeToMessages,
        unsubscribeFromMessages,
        subscribeToConversations,
        uploadFile,
        uploadFiles,
        deleteMessage,
        deleteConversation
    };
}
