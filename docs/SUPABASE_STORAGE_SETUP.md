# Supabase Storage Setup for Multimodal Embeddings

## Overview

This guide shows how to create Supabase Storage buckets for the multimodal vector database system.

## Required Storage Buckets

### 1. user-images (Meal photos, food labels, nutrition labels)
- **Purpose:** Store meal photos, food label scans, nutrition label images
- **Max file size:** 10 MB
- **Allowed MIME types:** image/jpeg, image/png, image/webp, image/heic
- **Public:** No (private, user-only access)

### 2. user-photos (Progress photos, body measurements)
- **Purpose:** Store progress photos, body transformation images
- **Max file size:** 10 MB
- **Allowed MIME types:** image/jpeg, image/png, image/webp, image/heic
- **Public:** No (private, user-only access)

### 3. user-audio (Voice notes, workout audio)
- **Purpose:** Store voice memos, workout audio logs
- **Max file size:** 50 MB
- **Allowed MIME types:** audio/mpeg, audio/wav, audio/m4a, audio/webm
- **Public:** No (private, user-only access)

### 4. user-videos (Workout form videos, exercise demonstrations)
- **Purpose:** Store workout form videos, exercise demonstrations
- **Max file size:** 100 MB
- **Allowed MIME types:** video/mp4, video/webm, video/quicktime
- **Public:** No (private, user-only access)

### 5. user-documents (PDFs, meal plans, workout programs)
- **Purpose:** Store PDF meal plans, workout programs, lab results
- **Max file size:** 20 MB
- **Allowed MIME types:** application/pdf
- **Public:** No (private, user-only access)

---

## Setup Instructions

### Option 1: Via Supabase Dashboard (Recommended)

1. Go to **Supabase Dashboard** → **Storage**
2. Click **New bucket**
3. Create each bucket with these settings:

**user-images:**
```
Name: user-images
Public: No
File size limit: 10485760 (10 MB)
Allowed MIME types: image/jpeg,image/png,image/webp,image/heic
```

**user-photos:**
```
Name: user-photos
Public: No
File size limit: 10485760 (10 MB)
Allowed MIME types: image/jpeg,image/png,image/webp,image/heic
```

**user-audio:**
```
Name: user-audio
Public: No
File size limit: 52428800 (50 MB)
Allowed MIME types: audio/mpeg,audio/wav,audio/m4a,audio/webm
```

**user-videos:**
```
Name: user-videos
Public: No
File size limit: 104857600 (100 MB)
Allowed MIME types: video/mp4,video/webm,video/quicktime
```

**user-documents:**
```
Name: user-documents
Public: No
File size limit: 20971520 (20 MB)
Allowed MIME types: application/pdf
```

4. After creating buckets, set up **RLS policies** for each bucket:

---

## Storage RLS Policies

Add these policies to each bucket via **SQL Editor**:

```sql
-- ============================================================================
-- USER-IMAGES BUCKET POLICIES
-- ============================================================================

-- Users can upload to their own folder
CREATE POLICY "Users can upload to their own folder (user-images)"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'user-images'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can read from their own folder
CREATE POLICY "Users can read from their own folder (user-images)"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'user-images'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can update their own files
CREATE POLICY "Users can update their own files (user-images)"
ON storage.objects FOR UPDATE
USING (
  bucket_id = 'user-images'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can delete their own files
CREATE POLICY "Users can delete their own files (user-images)"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'user-images'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- ============================================================================
-- USER-PHOTOS BUCKET POLICIES (same structure)
-- ============================================================================

CREATE POLICY "Users can upload to their own folder (user-photos)"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'user-photos'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can read from their own folder (user-photos)"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'user-photos'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update their own files (user-photos)"
ON storage.objects FOR UPDATE
USING (
  bucket_id = 'user-photos'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete their own files (user-photos)"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'user-photos'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- ============================================================================
-- USER-AUDIO BUCKET POLICIES
-- ============================================================================

CREATE POLICY "Users can upload to their own folder (user-audio)"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'user-audio'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can read from their own folder (user-audio)"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'user-audio'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update their own files (user-audio)"
ON storage.objects FOR UPDATE
USING (
  bucket_id = 'user-audio'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete their own files (user-audio)"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'user-audio'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- ============================================================================
-- USER-VIDEOS BUCKET POLICIES
-- ============================================================================

CREATE POLICY "Users can upload to their own folder (user-videos)"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'user-videos'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can read from their own folder (user-videos)"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'user-videos'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update their own files (user-videos)"
ON storage.objects FOR UPDATE
USING (
  bucket_id = 'user-videos'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete their own files (user-videos)"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'user-videos'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- ============================================================================
-- USER-DOCUMENTS BUCKET POLICIES
-- ============================================================================

CREATE POLICY "Users can upload to their own folder (user-documents)"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'user-documents'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can read from their own folder (user-documents)"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'user-documents'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update their own files (user-documents)"
ON storage.objects FOR UPDATE
USING (
  bucket_id = 'user-documents'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete their own files (user-documents)"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'user-documents'
  AND auth.uid()::text = (storage.foldername(name))[1]
);
```

---

## File Organization

Files will be stored in this structure:

```
bucket-name/
  ├── {user_id}/
  │   ├── meals/
  │   │   ├── {timestamp}_{filename}.jpg
  │   │   └── {timestamp}_{filename}.png
  │   ├── workouts/
  │   │   └── {timestamp}_{filename}.mp4
  │   ├── progress/
  │   │   └── {timestamp}_{filename}.jpg
  │   ├── voice/
  │   │   └── {timestamp}_{filename}.m4a
  │   └── documents/
  │       └── {timestamp}_{filename}.pdf
```

---

## Testing

After setup, test upload with Python:

```python
from supabase import create_client
import base64

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Upload test image
with open('test_image.jpg', 'rb') as f:
    file_data = f.read()

result = supabase.storage.from_('user-images').upload(
    f'{user_id}/meals/{timestamp}_test.jpg',
    file_data,
    {'content-type': 'image/jpeg'}
)

print(f"Uploaded: {result}")

# Get public URL (if needed)
url = supabase.storage.from_('user-images').get_public_url(
    f'{user_id}/meals/{timestamp}_test.jpg'
)
print(f"URL: {url}")
```

---

## Security Notes

1. **All buckets are PRIVATE** - files only accessible by owner
2. **RLS policies enforce user isolation** - users can only access their own folders
3. **File size limits prevent abuse** - prevents storage bombing
4. **MIME type validation** - only allowed file types can be uploaded
5. **Service role bypass** - background workers use service_role key to access all files for embedding generation

---

## Cost Estimation

**Supabase Storage Pricing (as of 2025):**
- Free tier: 1 GB storage, 2 GB bandwidth
- Pro: $0.021/GB storage, $0.09/GB bandwidth

**Estimated usage for 1000 users:**
- Average: 50 MB per user (10 meal photos, 5 progress photos, 10 voice notes)
- Total: ~50 GB storage
- Cost: ~$1.05/month storage

**This is INSANELY cheap for revolutionary multimodal AI.**
