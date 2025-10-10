# 🚀 Onboarding UI Speed Run Plan - 1-2 Days Instead of 5-8

**Goal:** Build production-ready onboarding UI in WORLD RECORD time  
**Time Estimate:** 1-2 days (vs. typical 5-8 days)  
**Strategy:** Maximum leverage, zero waste, component reuse

---

## 🎯 Speed Run Strategy

### Key Insight: You Already Have 80% of What You Need

✅ **Backend:** 100% complete - all APIs ready  
✅ **API Client:** `frontend/lib/api.ts` exists and works  
✅ **Component Library:** shadcn/ui pattern already used (Tailwind + CVA)  
✅ **Form Library:** `react-hook-form` + `zod` already installed  
✅ **State Management:** `@tanstack/react-query` already setup  
✅ **Styling:** TailwindCSS already configured  

**You need:** 20% new code (forms + flow logic)

---

## 🏗️ Architecture Decision: NO EXTRA LAYER NEEDED

### Should you add a layer between frontend/backend?

**Answer: NO - Keep it simple**

**Reasons:**
1. ✅ Backend APIs are already well-designed (Pydantic validation)
2. ✅ Frontend has `api.ts` with interceptors (auth, error handling)
3. ✅ React Query handles caching, loading, error states
4. ✅ Adding GraphQL/tRPC would add 2-3 days of setup
5. ✅ Type safety achieved with TypeScript interfaces matching backend

**What you DO need:**
- ✅ TypeScript types matching backend Pydantic models
- ✅ Centralized form validation (Zod schemas)
- ✅ Consistent error handling (already in api.ts)

**Adding a layer would SLOW YOU DOWN, not speed you up.**

---

## ⚡ The Speed Run Plan

### Phase 1: Foundation (2-3 hours)

#### Step 1.1: Add API Functions (30 min)
**File:** `frontend/lib/api.ts`

```typescript
export const onboardingApi = {
  // Start onboarding
  start: async () => {
    const response = await api.post('/onboarding/start')
    return response.data
  },

  // Get progress
  getProgress: async () => {
    const response = await api.get('/onboarding/progress')
    return response.data
  },

  // Update step
  updateStep: async (data: { step: number; data: any }) => {
    const response = await api.post('/onboarding/update-step', data)
    return response.data
  },

  // Complete onboarding
  complete: async (data: { profile_data: BusinessProfile }) => {
    const response = await api.post('/onboarding/complete', data)
    return response.data
  },
}

export const profileApi = {
  // Get profile
  get: async () => {
    const response = await api.get('/profile')
    return response.data
  },

  // Update profile
  update: async (data: Partial<BusinessProfile>) => {
    const response = await api.patch('/profile', data)
    return response.data
  },
}
```

#### Step 1.2: Add TypeScript Types (30 min)
**File:** `frontend/types/onboarding.ts`

```typescript
export interface BusinessProfile {
  business_name: string
  industry: string
  website_url?: string
  target_audience: string
  audience_pain_points: string[]
  audience_demographics?: {
    age_range?: string
    location?: string
    income_level?: string
  }
  brand_voice: string
  brand_values: string[]
  brand_personality: string
  content_goals: string[]
  key_topics: string[]
  content_style_preferences: string
  competitors: string[]
  unique_selling_points: string[]
  current_follower_count?: number
  posting_frequency: string
  best_performing_topics?: string[]
  preferred_colors: string[]
  visual_style: string
  example_copy_they_like?: string
  example_hooks?: string[]
}

export interface OnboardingProgress {
  user_id: string
  current_step: number
  total_steps: number
  completed: boolean
  partial_data: Record<string, any>
}
```

#### Step 1.3: Add Zod Validation Schemas (1 hour)
**File:** `frontend/lib/validation.ts`

```typescript
import { z } from 'zod'

export const step1Schema = z.object({
  business_name: z.string().min(2, 'Business name required'),
  industry: z.string().min(2, 'Industry required'),
  website_url: z.string().url().optional().or(z.literal('')),
  target_audience: z.string().min(5, 'Describe your target audience'),
  audience_pain_points: z.array(z.string()).min(1, 'Add at least 1 pain point'),
})

export const step2Schema = z.object({
  brand_voice: z.string().min(2, 'Select brand voice'),
  brand_values: z.array(z.string()).min(1, 'Add at least 1 value'),
  brand_personality: z.string().min(5, 'Describe brand personality'),
  example_copy_they_like: z.string().optional(),
})

export const step3Schema = z.object({
  content_goals: z.array(z.string()).min(1, 'Select at least 1 goal'),
  key_topics: z.array(z.string()).min(1, 'Add at least 1 topic'),
  content_style_preferences: z.string().min(2, 'Select content style'),
  posting_frequency: z.string().min(2, 'Select posting frequency'),
})

export const step4Schema = z.object({
  preferred_colors: z.array(z.string()).min(1, 'Pick at least 1 color'),
  visual_style: z.string().min(2, 'Select visual style'),
})

export const step5Schema = z.object({
  competitors: z.array(z.string()).optional(),
  unique_selling_points: z.array(z.string()).min(1, 'Add at least 1 USP'),
  example_hooks: z.array(z.string()).optional(),
})

export const completeProfileSchema = z.object({
  ...step1Schema.shape,
  ...step2Schema.shape,
  ...step3Schema.shape,
  ...step4Schema.shape,
  ...step5Schema.shape,
})
```

#### Step 1.4: Hooks for Onboarding Logic (1 hour)
**File:** `frontend/hooks/use-onboarding.ts`

```typescript
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { onboardingApi } from '@/lib/api'

export function useOnboarding() {
  const queryClient = useQueryClient()

  const { data: progress, isLoading } = useQuery({
    queryKey: ['onboarding-progress'],
    queryFn: onboardingApi.getProgress,
    retry: false,
  })

  const startMutation = useMutation({
    mutationFn: onboardingApi.start,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['onboarding-progress'] })
    },
  })

  const updateStepMutation = useMutation({
    mutationFn: onboardingApi.updateStep,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['onboarding-progress'] })
    },
  })

  const completeMutation = useMutation({
    mutationFn: onboardingApi.complete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['onboarding-progress'] })
      queryClient.invalidateQueries({ queryKey: ['profile'] })
    },
  })

  return {
    progress,
    isLoading,
    startOnboarding: startMutation.mutateAsync,
    updateStep: updateStepMutation.mutateAsync,
    completeOnboarding: completeMutation.mutateAsync,
    isUpdating: updateStepMutation.isPending || completeMutation.isPending,
  }
}
```

---

### Phase 2: Core Components (3-4 hours)

#### Step 2.1: Reusable Form Components (1 hour)
**File:** `frontend/components/forms/form-field.tsx`

```typescript
'use client'

import { UseFormRegister, FieldError } from 'react-hook-form'

export function FormInput({
  label,
  name,
  register,
  error,
  ...props
}: {
  label: string
  name: string
  register: UseFormRegister<any>
  error?: FieldError
} & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">{label}</label>
      <input
        {...register(name)}
        {...props}
        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
      />
      {error && <p className="text-sm text-red-600">{error.message}</p>}
    </div>
  )
}

export function FormTextarea({ label, name, register, error, ...props }: any) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">{label}</label>
      <textarea
        {...register(name)}
        {...props}
        rows={3}
        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
      />
      {error && <p className="text-sm text-red-600">{error.message}</p>}
    </div>
  )
}

export function FormSelect({ label, name, register, error, options, ...props }: any) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">{label}</label>
      <select
        {...register(name)}
        {...props}
        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Select...</option>
        {options.map((opt: any) => (
          <key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className="text-sm text-red-600">{error.message}</p>}
    </div>
  )
}

export function FormTagInput({ label, name, value, onChange, placeholder }: any) {
  const [input, setInput] = useState('')
  
  const addTag = () => {
    if (input.trim()) {
      onChange([...value, input.trim()])
      setInput('')
    }
  }
  
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">{label}</label>
      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
          placeholder={placeholder}
          className="flex-1 px-3 py-2 border rounded-lg"
        />
        <button type="button" onClick={addTag} className="px-4 py-2 bg-blue-600 text-white rounded-lg">
          Add
        </button>
      </div>
      <div className="flex flex-wrap gap-2">
        {value.map((tag: string, i: number) => (
          <span key={i} className="px-3 py-1 bg-gray-100 rounded-full text-sm">
            {tag}
            <button
              type="button"
              onClick={() => onChange(value.filter((_: any, idx: number) => idx !== i))}
              className="ml-2 text-red-600"
            >
              ×
            </button>
          </span>
        ))}
      </div>
    </div>
  )
}
```

#### Step 2.2: Progress Indicator (30 min)
**File:** `frontend/components/onboarding/progress-indicator.tsx`

```typescript
export function ProgressIndicator({ currentStep, totalSteps }: { currentStep: number; totalSteps: number }) {
  const steps = [
    { number: 1, label: 'Business Basics' },
    { number: 2, label: 'Brand Voice' },
    { number: 3, label: 'Content Strategy' },
    { number: 4, label: 'Visual Identity' },
    { number: 5, label: 'Competitive Edge' },
  ]

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-8">
        {steps.map((step, idx) => (
          <div key={step.number} className="flex items-center flex-1">
            <div className="flex flex-col items-center">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                  step.number < currentStep
                    ? 'bg-green-500 text-white'
                    : step.number === currentStep
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-500'
                }`}
              >
                {step.number < currentStep ? '✓' : step.number}
              </div>
              <span className="text-xs mt-2 text-center">{step.label}</span>
            </div>
            {idx < steps.length - 1 && (
              <div
                className={`h-1 flex-1 mx-4 ${
                  step.number < currentStep ? 'bg-green-500' : 'bg-gray-200'
                }`}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
```

#### Step 2.3: Wizard Container (1 hour)
**File:** `frontend/components/onboarding/onboarding-wizard.tsx`

```typescript
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useOnboarding } from '@/hooks/use-onboarding'
import { ProgressIndicator } from './progress-indicator'
import { toast } from 'sonner'

export function OnboardingWizard({ children }: { children: React.ReactNode[] }) {
  const router = useRouter()
  const { progress, isLoading, startOnboarding, updateStep, completeOnboarding } = useOnboarding()
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState<Record<string, any>>({})

  useEffect(() => {
    if (!progress && !isLoading) {
      startOnboarding()
    } else if (progress) {
      setCurrentStep(progress.current_step)
      setFormData(progress.partial_data || {})
    }
  }, [progress, isLoading])

  const handleStepComplete = async (stepData: any) => {
    try {
      const newData = { ...formData, ...stepData }
      setFormData(newData)
      
      await updateStep({ step: currentStep, data: stepData })
      
      if (currentStep < 5) {
        setCurrentStep(currentStep + 1)
        toast.success(`Step ${currentStep} completed!`)
      } else {
        // Final step - complete onboarding
        await completeOnboarding({ profile_data: newData })
        toast.success('Onboarding complete! 🎉')
        router.push('/dashboard')
      }
    } catch (error) {
      toast.error('Failed to save progress')
    }
  }

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <ProgressIndicator currentStep={currentStep} totalSteps={5} />
        
        <div className="bg-white rounded-lg shadow-lg p-8">
          {children[currentStep - 1] &&
            React.cloneElement(children[currentStep - 1] as React.ReactElement, {
              onComplete: handleStepComplete,
              onBack: handleBack,
              initialData: formData[`step_${currentStep}`],
              canGoBack: currentStep > 1,
            })}
        </div>
      </div>
    </div>
  )
}
```

---

### Phase 3: Step Components (4-5 hours)

**Strategy:** Copy-paste pattern for all 5 steps (DRY later)

#### Step 3.1: Step 1 - Business Basics (1 hour)
**File:** `frontend/components/onboarding/steps/step-1-business-basics.tsx`

```typescript
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { step1Schema } from '@/lib/validation'
import { FormInput, FormTextarea, FormTagInput } from '@/components/forms/form-field'

export function Step1BusinessBasics({
  onComplete,
  onBack,
  initialData,
  canGoBack,
}: any) {
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm({
    resolver: zodResolver(step1Schema),
    defaultValues: initialData || {
      audience_pain_points: [],
    },
  })

  const painPoints = watch('audience_pain_points') || []

  return (
    <form onSubmit={handleSubmit(onComplete)} className="space-y-6">
      <h2 className="text-2xl font-bold">Step 1: Business Basics</h2>
      <p className="text-gray-600">Tell us about your business and audience</p>

      <FormInput
        label="Business Name"
        name="business_name"
        register={register}
        error={errors.business_name}
        placeholder="e.g., AI Tools Inc"
      />

      <FormInput
        label="Industry"
        name="industry"
        register={register}
        error={errors.industry}
        placeholder="e.g., SaaS, E-commerce, Coaching"
      />

      <FormInput
        label="Website URL (optional)"
        name="website_url"
        type="url"
        register={register}
        error={errors.website_url}
        placeholder="https://..."
      />

      <FormTextarea
        label="Target Audience"
        name="target_audience"
        register={register}
        error={errors.target_audience}
        placeholder="e.g., Small business owners aged 30-50 who struggle with time management"
      />

      <FormTagInput
        label="Audience Pain Points"
        name="audience_pain_points"
        value={painPoints}
        onChange={(v: string[]) => setValue('audience_pain_points', v)}
        placeholder="e.g., Time management, High costs"
      />

      <div className="flex justify-between pt-4">
        {canGoBack && (
          <button type="button" onClick={onBack} className="px-6 py-2 border rounded-lg">
            Back
          </button>
        )}
        <button type="submit" className="px-6 py-2 bg-blue-600 text-white rounded-lg ml-auto">
          Continue
        </button>
      </div>
    </form>
  )
}
```

#### Step 3.2-3.5: Other Steps (3-4 hours)
**Copy the pattern above for:**
- `step-2-brand-voice.tsx` (brand_voice, brand_values, brand_personality, example_copy)
- `step-3-content-strategy.tsx` (content_goals, key_topics, content_style, posting_frequency)
- `step-4-visual-identity.tsx` (preferred_colors, visual_style)
- `step-5-competitive-edge.tsx` (competitors, USPs, example_hooks)

**Each takes ~45-60 min with copy-paste**

---

### Phase 4: Main Page & Integration (2-3 hours)

#### Step 4.1: Onboarding Page (1 hour)
**File:** `frontend/app/onboarding/page.tsx`

```typescript
'use client'

import { OnboardingWizard } from '@/components/onboarding/onboarding-wizard'
import { Step1BusinessBasics } from '@/components/onboarding/steps/step-1-business-basics'
import { Step2BrandVoice } from '@/components/onboarding/steps/step-2-brand-voice'
import { Step3ContentStrategy } from '@/components/onboarding/steps/step-3-content-strategy'
import { Step4VisualIdentity } from '@/components/onboarding/steps/step-4-visual-identity'
import { Step5CompetitiveEdge } from '@/components/onboarding/steps/step-5-competitive-edge'

export default function OnboardingPage() {
  return (
    <OnboardingWizard>
      <Step1BusinessBasics />
      <Step2BrandVoice />
      <Step3ContentStrategy />
      <Step4VisualIdentity />
      <Step5CompetitiveEdge />
    </OnboardingWizard>
  )
}
```

#### Step 4.2: Profile Management Page (1 hour)
**File:** `frontend/app/profile/page.tsx`

```typescript
'use client'

import { useQuery, useMutation } from '@tanstack/react-query'
import { profileApi } from '@/lib/api'
import { useForm } from 'react-hook-form'
import { toast } from 'sonner'

export default function ProfilePage() {
  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: profileApi.get,
  })

  const updateMutation = useMutation({
    mutationFn: profileApi.update,
    onSuccess: () => {
      toast.success('Profile updated!')
    },
  })

  const { register, handleSubmit } = useForm({
    values: profile?.profile_data,
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">Business Profile</h1>
      
      <form onSubmit={handleSubmit((data) => updateMutation.mutate(data))} className="space-y-6">
        {/* Reuse form components from onboarding steps */}
        
        <button
          type="submit"
          disabled={updateMutation.isPending}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg"
        >
          {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
        </button>
      </form>
    </div>
  )
}
```

#### Step 4.3: First-Time User Redirect (30 min)
**File:** `frontend/app/dashboard/page.tsx`

Add at the top:

```typescript
import { useQuery } from '@tanstack/react-query'
import { profileApi } from '@/lib/api'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function DashboardPage() {
  const router = useRouter()
  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: profileApi.get,
    retry: false,
  })

  useEffect(() => {
    if (!isLoading && !profile) {
      // No profile = needs onboarding
      router.push('/onboarding')
    }
  }, [profile, isLoading, router])

  if (isLoading) return <div>Loading...</div>
  if (!profile) return null // Redirecting...

  return (
    // ... existing dashboard code
  )
}
```

---

## ⏱️ Time Breakdown

### World Record Speed (1-2 Days)

**Day 1: Core Infrastructure (6-8 hours)**
- Foundation (2-3 hrs) - API, types, hooks, validation
- Core Components (3-4 hrs) - Forms, wizard, progress
- Step 1-2 (1 hr) - First two steps working

**Day 2: Complete Steps + Polish (6-8 hours)**
- Steps 3-5 (3-4 hrs) - Copy-paste pattern
- Integration (2-3 hrs) - Pages, redirects, testing
- Polish (1 hr) - Error handling, UX tweaks

**Total: 12-16 hours = 1.5-2 days**

### Traditional Speed (5-8 Days)
- Day 1: Planning & design mockups
- Day 2-3: Component library setup
- Day 4-5: Building forms
- Day 6-7: Integration & testing
- Day 8: Polish & bug fixes

**Savings: 3-6 days** 🚀

---

## 🎯 Speed Run Tactics

### 1. **Copy-Paste Everything**
- Step 1 template → Copy to Steps 2-5
- Change field names only
- DRY later (not now)

### 2. **Use What's Already There**
- `react-hook-form` (already installed)
- `zod` (already installed)
- `@tanstack/react-query` (already installed)
- TailwindCSS (already setup)

### 3. **Skip the Fancy Stuff**
- No animations (add later)
- No custom illustrations (use emojis)
- Basic styling (Tailwind utility classes)
- No micro-interactions

### 4. **Parallel Work Pattern**
```
Morning: Steps 1-2 (forms)
Afternoon: Steps 3-5 (copy-paste)
Evening: Integration + testing
```

### 5. **Testing as You Go**
```bash
# Run dev server in one terminal
npm run dev

# Test each step immediately after building
# Don't wait until the end
```

---

## 🚨 Common Speed Killers (AVOID THESE)

❌ **Custom component library** - Use Tailwind classes  
❌ **Perfect design** - Make it functional first  
❌ **Over-engineering** - No fancy state management  
❌ **Testing before done** - Test after each step, not at end  
❌ **Refactoring early** - Make it work, then make it pretty  

---

## ✅ Success Criteria

### Minimum Viable Onboarding (MVP)
- [ ] 5 steps with forms
- [ ] Progress indicator
- [ ] Save & continue later
- [ ] Complete onboarding flow
- [ ] Redirect new users
- [ ] Profile page (basic)

### Production Ready Checklist
- [ ] Form validation working
- [ ] Error messages show
- [ ] Loading states visible
- [ ] Success notifications
- [ ] Mobile responsive (Tailwind handles this)
- [ ] Can complete full flow
- [ ] Context injection works (backend already does this)

---

## 🎬 Execution Order

**EXACTLY this order for maximum speed:**

1. ✅ Update `frontend/lib/api.ts` (30 min)
2. ✅ Create `frontend/types/onboarding.ts` (30 min)
3. ✅ Create `frontend/lib/validation.ts` (1 hr)
4. ✅ Create `frontend/hooks/use-onboarding.ts` (1 hr)
5. ✅ Create `frontend/components/forms/form-field.tsx` (1 hr)
6. ✅ Create `frontend/components/onboarding/progress-indicator.tsx` (30 min)
7. ✅ Create `frontend/components/onboarding/onboarding-wizard.tsx` (1 hr)
8. ✅ Create `frontend/components/onboarding/steps/step-1-business-basics.tsx` (1 hr)
9. ✅ **TEST STEP 1** (make sure it works before continuing)
10. ✅ Copy-paste to create Steps 2-5 (3-4 hrs total)
11. ✅ Create `frontend/app/onboarding/page.tsx` (1 hr)
12. ✅ Create `frontend/app/profile/page.tsx` (1 hr)
13. ✅ Update `frontend/app/dashboard/page.tsx` (30 min)
14. ✅ **FULL INTEGRATION TEST** (1 hr)

---

## 🏆 Why This Will Work

1. ✅ **Backend is done** - No waiting on APIs
2. ✅ **Dependencies installed** - No package hunting
3. ✅ **Patterns exist** - Copy approval workflow pattern
4. ✅ **Clear structure** - No architecture decisions needed
5. ✅ **Copy-paste friendly** - 5 steps = 1 template × 5

**You're not building from scratch. You're filling in a template.**

---

## 📊 Expected Results

### Before (5-8 days):
```
Day 1: Setup & design
Day 2-3: Components
Day 4-5: Forms
Day 6-7: Integration
Day 8: Testing
```

### After (1-2 days):
```
Day 1 AM: Setup (3 hrs)
Day 1 PM: Core components (3 hrs)
Day 2 AM: All 5 steps (4 hrs)
Day 2 PM: Integration + testing (3 hrs)
DONE: 13 hours total ✅
```

---

## 🚀 Ready to Execute?

**Start with:**
```bash
cd frontend
npm install  # Make sure all deps are installed
npm run dev  # Start dev server
```

**Then follow the execution order above, one file at a time.**

**Don't overthink. Just code. You'll have it done in 1-2 days.** 🎯
