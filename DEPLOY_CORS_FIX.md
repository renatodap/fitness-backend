# CORS Fix Deployment Instructions for Railway

## Issue
CORS is blocking requests from `https://www.sharpened.me` to the production backend.

## Root Cause
Railway environment variables may not be configured correctly for CORS.

## Fixes Applied (Code)
1. ✅ Added detailed CORS logging to `app/main.py`
2. ✅ Added request origin logging middleware
3. ✅ Config already includes `https://www.sharpened.me` in CORS_ORIGINS

## Required: Railway Environment Variables

### Option 1: Allow All Origins (TEMPORARY - Development Only)
```bash
ALLOW_ALL_ORIGINS=true
```
⚠️ **WARNING**: This is a security risk! Only use temporarily to verify the fix works.

### Option 2: Whitelist Specific Origins (RECOMMENDED for Production)
```bash
ALLOW_ALL_ORIGINS=false
CORS_ORIGINS=http://localhost:3000,http://localhost:3005,https://www.sharpened.me,https://sharpened.me,https://wagner-coach-clean.vercel.app,https://wagner-coach.vercel.app
```

## Deployment Steps

### Step 1: Update Railway Environment Variables
1. Go to Railway dashboard
2. Select the `wagner-coach-backend` project
3. Navigate to **Variables** tab
4. Set one of the options above
5. Click **Save**

### Step 2: Restart the Service
Railway should auto-restart after env var changes. If not:
1. Go to **Deployments** tab
2. Click **Redeploy** on the latest deployment

### Step 3: Verify CORS in Logs
1. Go to **Deployments** → **Logs**
2. Look for startup messages:
   ```
   ⚠️ CORS: Allowing ALL origins (wildcard *)
   ```
   OR
   ```
   🔒 CORS: Restricting to 6 origins:
      ✓ http://localhost:3000
      ✓ https://www.sharpened.me
      ...
   ```

### Step 4: Test from Frontend
1. Open `https://www.sharpened.me`
2. Navigate to Coach page
3. Send message: "1.5 cup of oatmeal, 2 scoops of whey isolate, 15g of maple syrup"
4. Go to meal log preview
5. Click "Save Meal"
6. **Expected**: No CORS error, meal saves successfully
7. **Check Railway logs** for:
   ```
   🌐 Request from origin: https://www.sharpened.me → POST /api/v1/coach/confirm-log
   ✅ POST /api/v1/coach/confirm-log → 200 (0.123s)
   ```

## Rollback Plan
If issues persist, rollback by:
1. Setting `ALLOW_ALL_ORIGINS=true` temporarily
2. Checking logs for the actual origin making requests
3. Adding that origin to `CORS_ORIGINS` manually

## Next Steps After CORS Fix
Once CORS is working:
1. ✅ Test meal logging flow end-to-end
2. 🔄 Deploy Phase 2: Quantity Parsing Fix
3. 🔄 Deploy Phase 3: Food Matching Improvements

## Contact
If CORS issues persist after these changes, check:
- Railway logs for detailed request/response info
- Browser console for exact CORS error message
- Network tab for request headers (especially `Origin` header)
