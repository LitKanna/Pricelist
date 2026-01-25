# Everfresh - Supabase + Cloudflare R2 Setup Guide

## Quick Overview

| Service | Purpose | Free Tier |
|---------|---------|-----------|
| Supabase | Database + Auth + Real-time | 500MB DB, 1GB storage |
| Cloudflare R2 | Media storage (images/videos) | 10GB, zero egress |

---

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up with **GitHub** (easiest)
3. Click **"New Project"**
4. Fill in:
   - **Name:** `everfresh`
   - **Database Password:** (save this somewhere safe!)
   - **Region:** Singapore (closest to Sydney)
5. Click **"Create new project"**
6. Wait 2-3 minutes for setup

### Get Your Credentials

1. Go to **Settings** (gear icon) → **API**
2. Copy these values:

```
Project URL: https://xxxxxxxx.supabase.co
anon public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Step 2: Create Database Tables

1. In Supabase, go to **SQL Editor** (left sidebar)
2. Click **"New query"**
3. Copy the entire contents of `supabase-schema.sql`
4. Paste into the editor
5. Click **"Run"** (or Cmd+Enter)
6. You should see "Success. No rows returned"

### Verify Tables Created

Go to **Table Editor** → You should see:
- contacts
- conversations
- messages
- message_reads

---

## Step 3: Enable Storage

1. Go to **Storage** (left sidebar)
2. Click **"New bucket"**
3. Name: `everfresh-media`
4. **Check** "Public bucket" (allows direct image URLs)
5. Click **"Create bucket"**

### Set Storage Policy

1. Click on `everfresh-media` bucket
2. Go to **Policies** tab
3. Click **"New policy"** → **"For full customization"**
4. Policy name: `Allow public read`
5. Allowed operation: **SELECT**
6. Policy definition: `true`
7. Click **"Review"** → **"Save policy"**

Repeat for uploads:
1. **"New policy"** → **"For full customization"**
2. Policy name: `Allow authenticated uploads`
3. Allowed operation: **INSERT**
4. Policy definition: `true` (for now, tighten later)
5. Click **"Review"** → **"Save policy"**

---

## Step 4: Create Cloudflare R2 Bucket (Optional - for scaling)

> Note: For now, Supabase Storage works great. R2 is for when you need massive scale.

1. Go to [cloudflare.com](https://cloudflare.com)
2. Sign up / Login
3. Dashboard → **R2 Object Storage**
4. Click **"Create bucket"**
5. Name: `everfresh-media`
6. Click **"Create bucket"**

### Enable Public Access (for direct URLs)

1. Click on your bucket
2. Go to **Settings** tab
3. Under **Public access**, click **"Allow Access"**
4. Copy the public URL: `https://pub-xxxx.r2.dev`

---

## Step 5: Configure Your App

1. Copy `config.example.js` to `config.js`
2. Fill in your credentials:

```javascript
const CONFIG = {
    SUPABASE_URL: 'https://your-project-id.supabase.co',
    SUPABASE_ANON_KEY: 'your-anon-key-here',
    R2_PUBLIC_URL: 'https://pub-xxxx.r2.dev', // Optional
    R2_BUCKET: 'everfresh-media',
};
```

---

## Step 6: Test the Connection

Open browser console and run:

```javascript
// Initialize
initSupabase(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);

// Create a test contact
const contact = await getOrCreateContact('+61400111222', 'Test Customer');
console.log('Contact created:', contact);

// Should show the contact object with an ID
```

---

## File Structure

```
pricelist/
├── config.js              # Your credentials (DO NOT COMMIT)
├── config.example.js      # Template for credentials
├── supabase-client.js     # Database functions
├── supabase-schema.sql    # Database schema
├── messages.html          # Web app (will be updated)
└── .gitignore            # Add config.js here!
```

---

## Security Checklist

- [ ] Add `config.js` to `.gitignore`
- [ ] Never commit API keys to GitHub
- [ ] Enable Row Level Security (RLS) - already in schema
- [ ] Set up proper storage policies

---

## Next Steps

Once you've completed steps 1-5, let me know and I'll:

1. Update `messages.html` to use Supabase
2. Add real-time message sync
3. Add file upload with progress
4. Make it all work seamlessly!

---

## Troubleshooting

### "relation does not exist" error
→ Run the SQL schema again in SQL Editor

### "permission denied" error
→ Check RLS policies are set up correctly

### Images not loading
→ Make sure storage bucket is public

### Real-time not working
→ Check that tables are added to `supabase_realtime` publication
