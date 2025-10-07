# CORS Troubleshooting Guide - Quick Entry

## 🔥 Recent Changes Pushed

### Frontend (Commit `22f25e0`)
- ✅ Added comprehensive error handling for CORS/network errors
- ✅ Better error messages showing backend URL
- ✅ Distinguishes between network, CORS, and HTTP errors
- ✅ Logs errors to console for debugging

### Backend (Commit `a6fe9c3`)
- ✅ Made CORS configuration flexible with environment variable support
- ✅ Added `cors_origins_list` property to parse comma-separated origins
- ✅ Added `ALLOW_ALL_ORIGINS` flag for debugging
- ✅ Added CORS debug logging on startup

---

## 🚀 Railway Configuration

### Step 1: Check Railway Logs
After Railway redeploys, check the logs. You should see:

```
Starting Fitness Backend
Environment: production
Debug mode: False
CORS Origins: ['http://localhost:3000', 'https://www.sharpened.me', 'https://sharpened.me']
Allow All Origins: False
```

If the CORS Origins line is missing or shows a different value, the environment variable isn't being read correctly.

### Step 2: Set Environment Variables in Railway

**Option A: Use Default (Recommended)**
The backend code has default CORS origins. If Railway is reading the code correctly, it should work automatically.

**Option B: Set Explicit Environment Variable**
In Railway dashboard, add:

```bash
CORS_ORIGINS=http://localhost:3000,https://www.sharpened.me,https://sharpened.me
```

**Option C: Temporary Debug Mode (ONLY FOR TESTING)**
To verify if CORS is the issue, temporarily set:

```bash
ALLOW_ALL_ORIGINS=true
```

⚠️ **WARNING**: This allows ALL origins. Only use for debugging, then remove it!

### Step 3: Verify Environment Variables Are Available

In Railway, make sure the environment variables are:
1. Set in the correct service (fitness-backend)
2. Not marked as "secret" or "build-time only"
3. Available at runtime

---

## 🐛 Debugging CORS Issues

### Frontend Error Messages

You'll now see detailed error messages:

**CORS Error:**
```
Cannot connect to backend at https://fitness-backend-production-5e77.up.railway.app.
This is likely a CORS or network issue.
Check that the backend is running and CORS is configured correctly.
```

**HTTP Error:**
```
Backend error (500): Internal Server Error
```

**Parse Error:**
```
Backend error (404): Not Found
```

### Backend Logs

Check Railway logs for:

```
Starting Fitness Backend
CORS Origins: ['http://localhost:3000', 'https://www.sharpened.me', 'https://sharpened.me']
```

If you see `ALLOW_ALL_ORIGINS: True`, you have debugging mode enabled.

### Browser Console

Open browser DevTools and check:

1. **Network Tab**: Look at the OPTIONS preflight request
   - Should return 200 OK
   - Should have `Access-Control-Allow-Origin` header

2. **Console Tab**: Look for detailed error messages
   - Frontend now logs fetch errors

---

## 🔍 Common Issues

### Issue 1: Railway Not Reading Environment Variables

**Symptom**: CORS Origins line missing from logs or shows wrong value

**Solution**:
1. In Railway dashboard, verify environment variables are set
2. Trigger a redeploy (Railway should auto-deploy on git push)
3. Check logs again

### Issue 2: Environment Variables Not Available at Runtime

**Symptom**: Backend starts but CORS doesn't work

**Solution**:
1. Make sure env vars are NOT build-time only
2. Restart the Railway service
3. Check logs to confirm origins are loaded

### Issue 3: Wrong CORS Format

**Symptom**: CORS Origins shows empty list or single string

**Solution**:
- Use comma-separated format: `origin1,origin2,origin3`
- No spaces between origins (or they'll be stripped)
- Make sure Railway isn't adding quotes around the value

### Issue 4: OPTIONS Preflight Failing

**Symptom**: Browser shows CORS error on OPTIONS request

**Solution**:
1. Verify backend is responding to OPTIONS requests
2. Check that `allow_methods=["*"]` is set
3. Temporarily enable `ALLOW_ALL_ORIGINS=true` to test

---

## ✅ Testing Checklist

### Backend Deployment
- [ ] Railway shows successful deployment
- [ ] Backend logs show CORS Origins list
- [ ] Backend responds to GET / endpoint
- [ ] Backend logs show correct environment

### CORS Configuration
- [ ] CORS_ORIGINS environment variable is set (or using defaults)
- [ ] ALLOW_ALL_ORIGINS is false (unless debugging)
- [ ] Origins include https://www.sharpened.me
- [ ] Origins include https://sharpened.me

### Frontend Testing
- [ ] Navigate to https://www.sharpened.me/quick-entry-optimized
- [ ] Input box is centered
- [ ] Type text and submit
- [ ] Check browser console for errors
- [ ] Verify error message is detailed (not generic)

### CORS Headers
- [ ] OPTIONS request returns 200 OK
- [ ] Response includes Access-Control-Allow-Origin header
- [ ] Response includes Access-Control-Allow-Methods header
- [ ] Response includes Access-Control-Allow-Headers header

---

## 🔧 Quick Fixes

### Fix 1: Force Railway Redeploy

```bash
# In fitness-backend directory
git commit --allow-empty -m "Force Railway redeploy"
git push
```

### Fix 2: Enable Debug Mode Temporarily

In Railway, set:
```
ALLOW_ALL_ORIGINS=true
```

Test the app. If it works, CORS is definitely the issue.

Then remove `ALLOW_ALL_ORIGINS` and set proper origins:
```
CORS_ORIGINS=http://localhost:3000,https://www.sharpened.me,https://sharpened.me
```

### Fix 3: Check Railway Service URL

Make sure frontend is using the correct Railway URL:

In `.env.local` or Vercel environment variables:
```
NEXT_PUBLIC_BACKEND_URL=https://fitness-backend-production-5e77.up.railway.app
```

---

## 📊 Expected Behavior

### Working CORS Flow

1. **User submits in frontend**
2. **Browser sends OPTIONS preflight request**
   - Backend responds with CORS headers
   - Status: 200 OK
3. **Browser sends actual POST request**
   - Backend processes request
   - Returns JSON response
4. **Frontend shows confirmation modal**
5. **User confirms**
6. **Data saves to database**

### Failed CORS Flow

1. **User submits in frontend**
2. **Browser sends OPTIONS preflight request**
   - Backend doesn't respond or missing CORS headers
   - Browser blocks request
3. **Frontend shows error:**
   ```
   Cannot connect to backend at {URL}.
   This is likely a CORS or network issue.
   ```

---

## 🎯 Next Steps

1. **Check Railway Logs**
   - Verify CORS Origins are loaded correctly
   - Look for any startup errors

2. **Test with ALLOW_ALL_ORIGINS (temporary)**
   - Set `ALLOW_ALL_ORIGINS=true` in Railway
   - Test the app
   - If it works, CORS is confirmed as the issue

3. **Set Proper CORS_ORIGINS**
   - Remove `ALLOW_ALL_ORIGINS`
   - Set explicit `CORS_ORIGINS` in Railway
   - Redeploy and test

4. **Verify Frontend Environment**
   - Check Vercel environment variables
   - Make sure `NEXT_PUBLIC_BACKEND_URL` points to Railway

---

## 📝 Summary

**What We Fixed:**
- ✅ Frontend: Better error messages for debugging
- ✅ Backend: Flexible CORS configuration via environment variables
- ✅ Backend: CORS debug logging on startup
- ✅ Backend: `ALLOW_ALL_ORIGINS` flag for testing

**What You Need to Do:**
1. Check Railway logs after redeploy
2. Verify CORS Origins are loaded correctly
3. Test the app at https://www.sharpened.me/quick-entry-optimized
4. If still failing, temporarily enable `ALLOW_ALL_ORIGINS=true` to confirm CORS is the issue

**The error messages will now tell you exactly what's wrong! 🔍**
