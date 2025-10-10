# ⚡ Onboarding Speed Run - Execution Checklist

**Time Goal:** 12-16 hours (1-2 days)  
**Start:** Mark the time you begin!

---

## 🎬 Phase 1: Foundation (2-3 hours)

### [ ] 1.1 API Functions (30 min)
**File:** `frontend/lib/api.ts`

Add to bottom of file:
```typescript
export const onboardingApi = { /* ... */ }
export const profileApi = { /* ... */ }
```

**Test:** No compile errors

---

### [ ] 1.2 TypeScript Types (30 min)
**File:** `frontend/types/onboarding.ts` (NEW)

```bash
mkdir -p frontend/types
```

**Test:** Import works in other files

---

### [ ] 1.3 Validation Schemas (1 hour)
**File:** `frontend/lib/validation.ts` (NEW)

**Test:** No compile errors

---

### [ ] 1.4 Onboarding Hook (1 hour)
**File:** `frontend/hooks/use-onboarding.ts` (NEW)

```bash
mkdir -p frontend/hooks
```

**Test:** Import works

---

## 🧩 Phase 2: Core Components (3-4 hours)

### [ ] 2.1 Form Components (1 hour)
**File:** `frontend/components/forms/form-field.tsx` (NEW)

```bash
mkdir -p frontend/components/forms
```

**Test:** Import FormInput works

---

### [ ] 2.2 Progress Indicator (30 min)
**File:** `frontend/components/onboarding/progress-indicator.tsx` (NEW)

```bash
mkdir -p frontend/components/onboarding/steps
```

**Test:** Renders in browser

---

### [ ] 2.3 Wizard Container (1 hour)
**File:** `frontend/components/onboarding/onboarding-wizard.tsx` (NEW)

**Test:** No compile errors

---

### [ ] 2.4 Quick Test (30 min)
Create a test page to verify components render:

```typescript
// frontend/app/test-onboarding/page.tsx
import { ProgressIndicator } from '@/components/onboarding/progress-indicator'

export default function TestPage() {
  return <ProgressIndicator currentStep={2} totalSteps={5} />
}
```

Visit: `http://localhost:3000/test-onboarding`

**Expected:** Progress bar with step 2 highlighted

---

## 📝 Phase 3: Step Components (4-5 hours)

### [ ] 3.1 Step 1 - Business Basics (1 hour)
**File:** `frontend/components/onboarding/steps/step-1-business-basics.tsx` (NEW)

**Test:** Form renders with all fields

---

### [ ] 3.2 Step 2 - Brand Voice (1 hour)
**File:** `frontend/components/onboarding/steps/step-2-brand-voice.tsx` (NEW)

**Copy-paste Step 1, change:**
- Title
- Field names (brand_voice, brand_values, brand_personality, example_copy)
- Validation schema (step2Schema)

---

### [ ] 3.3 Step 3 - Content Strategy (1 hour)
**File:** `frontend/components/onboarding/steps/step-3-content-strategy.tsx` (NEW)

**Copy-paste Step 1, change:**
- Title
- Field names (content_goals, key_topics, content_style, posting_frequency)
- Validation schema (step3Schema)

---

### [ ] 3.4 Step 4 - Visual Identity (1 hour)
**File:** `frontend/components/onboarding/steps/step-4-visual-identity.tsx` (NEW)

**Copy-paste Step 1, change:**
- Title
- Field names (preferred_colors, visual_style)
- Validation schema (step4Schema)

---

### [ ] 3.5 Step 5 - Competitive Edge (1 hour)
**File:** `frontend/components/onboarding/steps/step-5-competitive-edge.tsx` (NEW)

**Copy-paste Step 1, change:**
- Title
- Field names (competitors, unique_selling_points, example_hooks)
- Validation schema (step5Schema)

---

## 🔗 Phase 4: Integration (2-3 hours)

### [ ] 4.1 Onboarding Page (1 hour)
**File:** `frontend/app/onboarding/page.tsx` (NEW)

```bash
mkdir -p frontend/app/onboarding
```

**Test:** Visit `http://localhost:3000/onboarding`

**Expected:**
- Progress bar shows
- Step 1 form displays
- Can fill out form
- "Continue" button works
- Moves to Step 2

---

### [ ] 4.2 Full Flow Test (30 min)
**Test the complete flow:**

1. Visit `/onboarding`
2. Fill out Step 1 → Click Continue
3. Fill out Step 2 → Click Continue
4. Fill out Step 3 → Click Continue
5. Fill out Step 4 → Click Continue
6. Fill out Step 5 → Click Continue
7. Should redirect to `/dashboard`

**Check backend:**
```bash
# Check if profile was created
curl -X GET http://localhost:8000/api/v1/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### [ ] 4.3 Profile Page (1 hour)
**File:** `frontend/app/profile/page.tsx` (NEW)

```bash
mkdir -p frontend/app/profile
```

**Test:** Visit `http://localhost:3000/profile`

**Expected:**
- Profile data loads
- Can edit fields
- "Save Changes" works
- Toast notification shows

---

### [ ] 4.4 First-Time User Redirect (30 min)
**File:** `frontend/app/dashboard/page.tsx` (EDIT)

Add profile check at top of component.

**Test:** 
1. Create new user (no profile)
2. Visit `/dashboard`
3. Should auto-redirect to `/onboarding`

---

## ✅ Final Checklist

### Functionality
- [ ] Can start onboarding
- [ ] Can fill all 5 steps
- [ ] Can go back to previous steps
- [ ] Progress saves (refresh page, should resume)
- [ ] Completes successfully
- [ ] Redirects to dashboard
- [ ] Profile page loads
- [ ] Can edit profile
- [ ] New users auto-redirect to onboarding

### UI/UX
- [ ] Progress indicator updates
- [ ] Form validation shows errors
- [ ] Loading states show
- [ ] Success/error toasts show
- [ ] Mobile responsive (test on narrow window)
- [ ] All buttons work
- [ ] No console errors

### Backend Integration
- [ ] API calls succeed
- [ ] Profile created in database
- [ ] Embeddings generated
- [ ] Context injection works (test by creating carousel)

---

## 🐛 Common Issues & Fixes

### Issue: TypeScript errors on imports
**Fix:** Make sure `tsconfig.json` has path aliases:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

### Issue: "Module not found"
**Fix:** Restart dev server:
```bash
# Ctrl+C to stop
npm run dev
```

### Issue: API calls fail (CORS error)
**Fix:** Check backend is running:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Issue: Form doesn't submit
**Fix:** Check browser console for validation errors

### Issue: Redirect not working
**Fix:** Clear localStorage and cookies, try again

---

## 📊 Time Tracking

**Phase 1 Foundation:** _____ hours (goal: 2-3)  
**Phase 2 Components:** _____ hours (goal: 3-4)  
**Phase 3 Steps:** _____ hours (goal: 4-5)  
**Phase 4 Integration:** _____ hours (goal: 2-3)  

**Total:** _____ hours (goal: 12-16)

---

## 🚀 Speed Tips

1. **Don't refactor as you go** - Make it work first
2. **Copy-paste aggressively** - DRY later
3. **Test after each phase** - Don't wait until end
4. **Use AI completion** - GitHub Copilot helps
5. **Skip styling details** - Functional > Pretty
6. **Save often** - Git commit after each phase

---

## 🎯 Success = Working End-to-End

**You're done when:**
```
New User → /dashboard → Auto-redirect to /onboarding
       → Fill 5 steps → Complete
       → Back to /dashboard
       → Create carousel
       → AI uses business context ✅
```

**That's it! No more, no less.**

---

## 🔥 Emergency Fast-Track

**If running out of time, cut these:**

1. ~~Profile edit page~~ (users can redo onboarding)
2. ~~Back button~~ (users can refresh)
3. ~~Progress save/resume~~ (do it all in one go)
4. ~~Fancy validation messages~~ (just show required)

**Keep these (essential):**
- ✅ 5 step forms
- ✅ Progress indicator
- ✅ Complete flow
- ✅ Redirect new users

---

## 📝 Code Snippets for Copy-Paste

### Quick Test Component
```typescript
// Test any component quickly
export default function TestPage() {
  return (
    <div className="p-8">
      <h1>Testing Component</h1>
      {/* Drop component here */}
    </div>
  )
}
```

### Quick API Test
```typescript
// Test API calls in browser console
fetch('http://localhost:8000/api/v1/onboarding/start', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('auth_token'),
    'Content-Type': 'application/json'
  }
}).then(r => r.json()).then(console.log)
```

### Quick Form Debug
```typescript
// Add to any step component to see form state
console.log('Form values:', watch())
console.log('Form errors:', errors)
```

---

## ✨ Motivation

**Remember:**
- Backend is DONE ✅
- All APIs work ✅
- You just need UI ✅
- 12-16 hours of focused work ✅
- Then it's COMPLETE ✅

**You got this! 🚀**
