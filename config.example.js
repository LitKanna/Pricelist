// ============================================
// EVERFRESH - CONFIGURATION
// Copy this to config.js and fill in your credentials
// ============================================

const CONFIG = {
    // Supabase - Get from: supabase.com → Project Settings → API
    SUPABASE_URL: 'https://your-project-id.supabase.co',
    SUPABASE_ANON_KEY: 'your-anon-key-here',

    // Cloudflare R2 - Get from: Cloudflare Dashboard → R2
    // Note: For browser uploads, we'll use Supabase Storage as proxy
    // or R2 presigned URLs via a Supabase Edge Function
    R2_PUBLIC_URL: 'https://your-r2-public-url.r2.dev',
    R2_BUCKET: 'everfresh-media',

    // App Settings
    APP_NAME: 'Everfresh',
    MAX_FILE_SIZE: 50 * 1024 * 1024, // 50MB
    ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    ALLOWED_VIDEO_TYPES: ['video/mp4', 'video/quicktime', 'video/webm'],
    ALLOWED_FILE_TYPES: ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
};

// Don't modify below this line
if (typeof module !== 'undefined') {
    module.exports = CONFIG;
}
