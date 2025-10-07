# Quick Entry UI Specification - Production-Ready Design

**Version:** 2.0
**Date:** 2025-01-05
**Purpose:** Complete UI/UX specification for quick entry preview/confirmation flow

---

## 🎯 Core Principles

1. **Show, Don't Tell** - No raw JSON, only clean UI elements
2. **Progressive Disclosure** - Essential fields first, details on expand
3. **Smart Defaults** - Pre-fill everything possible
4. **Visual Honesty** - Clearly mark estimated vs confirmed data
5. **Instant Feedback** - Real-time validation and help
6. **Mobile-First** - Touch-friendly, thumb-reachable

---

## 📱 UI Architecture

### Response Structure from Backend

```typescript
interface QuickEntryPreview {
  success: boolean;
  entry_type: "meal" | "workout" | "activity" | "note" | "measurement";
  confidence: number; // 0.0 - 1.0
  data: {
    primary_fields: Record<string, any>;  // Show by default
    secondary_fields: Record<string, any>; // Show in expand section
    estimated: boolean;
    needs_clarification: boolean;
  };
  validation: {
    errors: string[];
    warnings: string[];
    missing_critical: string[];
  };
  suggestions: string[];
  semantic_context?: {
    similar_count: number;
    suggestions: Array<{
      similarity: number;
      created_at: string;
      [key: string]: any;
    }>;
  };
}
```

---

## 🍽️ MEAL ENTRY UI

### Case 1: Detailed Entry (High Confidence)

**Input:** "6oz grilled chicken, 1 cup brown rice, 2 cups broccoli"

**UI Layout:**

```
┌─────────────────────────────────────────────┐
│ 🍽️ Meal Entry                              │
├─────────────────────────────────────────────┤
│                                             │
│ Meal Name                                   │
│ ┌─────────────────────────────────────────┐ │
│ │ Grilled chicken with rice and broccoli  │ │ [Editable input]
│ └─────────────────────────────────────────┘ │
│                                             │
│ Meal Type                                   │
│ ┌──────┬──────┬──────┬──────┐             │
│ │Breakfast Lunch Dinner Snack│             │ [Segmented control]
│ │        [✓]                  │             │
│ └──────┴──────┴──────┴──────┘             │
│                                             │
│ Foods                                       │
│ ┌─────────────────────────────────────────┐ │
│ │ • Grilled chicken breast (6 oz)         │ │ [Chips/Tags]
│ │ • Brown rice, cooked (1 cup)            │ │
│ │ • Broccoli, steamed (2 cups)            │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Nutrition                                   │
│ ┌────────────┬────────────┬────────────┐  │
│ │  558 cal   │   63g PRO  │   57g CARB │  │ [Cards with icons]
│ └────────────┴────────────┴────────────┘  │
│                                             │
│ ⚡ Estimated • 90% confidence               │ [Badge]
│                                             │
│ ▼ More details                              │ [Expand button]
│                                             │
│ ✅ Save Entry    ✏️ Edit                   │ [Actions]
└─────────────────────────────────────────────┘
```

**Expanded View:**

```
┌─────────────────────────────────────────────┐
│ ▲ Less details                              │
│                                             │
│ Detailed Nutrition                          │
│ ┌─────────────────────────────────────────┐ │
│ │ Fat: 8.6g                               │ │
│ │ Fiber: 9g                               │ │
│ │ Sugar: 3g                               │ │
│ │ Sodium: 150mg                           │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Individual Foods                            │
│ ┌─────────────────────────────────────────┐ │
│ │ Grilled chicken breast (6 oz)           │ │ [Expandable card]
│ │ • 280 cal • 53g PRO • 0g CARB • 6g FAT │ │
│ │                                         │ │
│ │ Brown rice, cooked (1 cup)              │ │
│ │ • 218 cal • 5g PRO • 46g CARB • 2g FAT │ │
│ │                                         │ │
│ │ Broccoli, steamed (2 cups)              │ │
│ │ • 55 cal • 4g PRO • 11g CARB • 1g FAT  │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Tags                                        │
│ ┌─────────────────────────────────────────┐ │
│ │ [high-protein] [high-fiber] [balanced]  │ │ [Chips]
│ └─────────────────────────────────────────┘ │
│                                             │
│ Quality Scores                              │
│ ┌─────────────────────────────────────────┐ │
│ │ Meal Quality:  ⭐⭐⭐⭐⭐⭐⭐⭐ 8.5/10    │ │ [Visual rating]
│ │ Macro Balance: ⭐⭐⭐⭐⭐⭐⭐⭐⭐ 9/10    │ │
│ │ Goal Adherence:⭐⭐⭐⭐⭐⭐⭐ 7.5/10      │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**Interaction States:**

- **Click meal name**: Inline edit
- **Click meal type**: Change selection
- **Click nutrition card**: Quick edit modal
- **Click food chip**: Edit individual food
- **Tap "More details"**: Smooth accordion expand
- **Tap "Edit"**: Switch entire card to edit mode with all fields editable

---

### Case 2: Vague Entry (Low Confidence - Needs Clarification)

**Input:** "chicken and rice"

**UI Layout:**

```
┌─────────────────────────────────────────────┐
│ 🍽️ Meal Entry                              │
│                                             │
│ ⚠️ Missing Details                          │ [Warning banner]
│ Add portions for accurate tracking          │
│                                             │
├─────────────────────────────────────────────┤
│ Meal Name                                   │
│ ┌─────────────────────────────────────────┐ │
│ │ Chicken and rice                        │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Foods - Add Portions                        │
│ ┌─────────────────────────────────────────┐ │
│ │ Chicken                                 │ │ [Input with placeholder]
│ │ ┌─────────────────────────────────────┐ │ │
│ │ │ e.g., "6 oz" or "170g"              │ │ │ [Placeholder text]
│ │ └─────────────────────────────────────┘ │ │
│ │                                         │ │
│ │ Rice                                    │ │
│ │ ┌─────────────────────────────────────┐ │ │
│ │ │ e.g., "1 cup" or "195g"             │ │ │
│ │ └─────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ 💡 Quick Estimate                           │ [Suggestion box]
│ ┌─────────────────────────────────────────┐ │
│ │ Typical serving:                        │ │
│ │ • 4-6oz chicken (250-375 cal)           │ │
│ │ • 1 cup rice (200-220 cal)              │ │
│ │ • Total: ~450-600 calories              │ │
│ │                                         │ │
│ │ [Use This Estimate]                     │ │ [Button]
│ └─────────────────────────────────────────┘ │
│                                             │
│ ✅ Save Anyway    ✏️ Add Details           │
└─────────────────────────────────────────────┘
```

**If user clicks "Use This Estimate":**
- Pre-fill: 5oz chicken, 1 cup rice
- Calculate macros automatically
- Mark as estimated
- Allow editing

**If user clicks "Save Anyway":**
- Save with null nutrition values
- Show warning: "Entry saved without nutrition tracking"
- Suggest adding details later

---

### Case 3: With Image

**Input:** "lunch" + [photo of meal]

**UI Layout:**

```
┌─────────────────────────────────────────────┐
│ 🍽️ Meal Entry                              │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │                                         │ │
│ │          [Meal Photo]                   │ │ [Image preview]
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ 🤖 AI Detected:                             │
│ • Grilled chicken breast                    │
│ • Steamed broccoli                          │
│ • Sweet potato                              │
│                                             │
│ Meal Name                                   │
│ ┌─────────────────────────────────────────┐ │
│ │ Chicken, broccoli, and sweet potato     │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ⚠️ Add Portions for Accuracy                │ [Warning]
│                                             │
│ [Continue with portion inputs...]          │
└─────────────────────────────────────────────┘
```

---

### Case 4: Similar Meals (Semantic Context)

**When similar past meals found:**

```
┌─────────────────────────────────────────────┐
│ 🔍 You've logged something similar          │ [Info banner]
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ 📅 3 days ago (89% similar)              │ │ [Card]
│ │ Grilled chicken with brown rice          │ │
│ │ • 480 cal • 48g PRO • 45g CARB          │ │
│ │ Quality: ⭐⭐⭐⭐⭐⭐⭐⭐ 8.5/10            │ │
│ │                                         │ │
│ │ [Copy This] [View Original]             │ │ [Actions]
│ └─────────────────────────────────────────┘ │
│                                             │
│ [Show 2 more similar meals]                │ [Expand]
└─────────────────────────────────────────────┘
```

**If user clicks "Copy This":**
- Pre-fill all fields from that meal
- Allow editing before saving
- Mark as "Based on previous entry"

---

## 🏋️ WORKOUT ENTRY UI

### Case 1: Detailed Workout

**Input:** "bench press 4x8 @ 185lbs, incline db press 3x10 @ 70lbs"

**UI Layout:**

```
┌─────────────────────────────────────────────┐
│ 💪 Workout Entry                            │
├─────────────────────────────────────────────┤
│ Workout Name                                │
│ ┌─────────────────────────────────────────┐ │
│ │ Chest Press Workout                     │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Duration & Effort                           │
│ ┌─────────────────────┬──────────────────┐ │
│ │ 45 min              │ RPE: [Slider]    │ │ [Input + Slider]
│ │                     │ ⚡⚡⚡⚡⚡⚡⚡⚡○○ │ │
│ └─────────────────────┴──────────────────┘ │
│                                             │
│ Exercises                                   │
│ ┌─────────────────────────────────────────┐ │
│ │ Bench Press                             │ │ [Exercise card]
│ │ 4 sets × 8 reps @ 185 lbs              │ │
│ │ Volume: 5,920 lbs                       │ │
│ │                                         │ │
│ │ [Edit] [Delete]                         │ │ [Actions]
│ │                                         │ │
│ │ Incline DB Press                        │ │
│ │ 3 sets × 10 reps @ 70 lbs              │ │
│ │ Volume: 2,100 lbs                       │ │
│ │                                         │ │
│ │ [Edit] [Delete]                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ [+ Add Exercise]                            │ [Button]
│                                             │
│ Total Volume: 8,020 lbs 💪                  │ [Summary badge]
│                                             │
│ ▼ More details                              │
│                                             │
│ ✅ Save Workout    ✏️ Edit                 │
└─────────────────────────────────────────────┘
```

**Expanded View:**

```
┌─────────────────────────────────────────────┐
│ ▲ Less details                              │
│                                             │
│ Muscle Groups                               │
│ [Chest] [Triceps] [Shoulders]               │ [Chips]
│                                             │
│ Stats                                       │
│ • Estimated Calories: 250                   │
│ • Recovery Needed: 36 hours                 │
│ • Progressive Overload: 📈 Improving        │ [Badge with icon]
│                                             │
│ Tags                                        │
│ [push] [upper-body] [high-volume]           │
└─────────────────────────────────────────────┘
```

**Exercise Edit Modal:**

```
┌─────────────────────────────────────────────┐
│ Edit Exercise                               │
├─────────────────────────────────────────────┤
│ Exercise Name                               │
│ ┌─────────────────────────────────────────┐ │
│ │ Bench Press                    [Search] │ │ [Autocomplete]
│ └─────────────────────────────────────────┘ │
│                                             │
│ Sets & Reps                                 │
│ ┌──────┬──────┬──────────────┐            │
│ │ Sets │ Reps │ Weight (lbs) │            │
│ ├──────┼──────┼──────────────┤            │
│ │  4   │  8   │    185       │            │ [Table]
│ └──────┴──────┴──────────────┘            │
│                                             │
│ [+ Add Set]                                 │
│                                             │
│ Rest Time (optional)                        │
│ ┌─────────────────────────────────────────┐ │
│ │ 90 seconds                              │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Notes (optional)                            │
│ ┌─────────────────────────────────────────┐ │
│ │ Felt strong today                       │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ [Cancel]                        [Save]      │
└─────────────────────────────────────────────┘
```

---

## 🏃 ACTIVITY ENTRY UI

**Input:** "ran 5 miles in 40 minutes"

**UI Layout:**

```
┌─────────────────────────────────────────────┐
│ 🏃 Activity Entry                           │
├─────────────────────────────────────────────┤
│ Activity Type                               │
│ ┌──────────────────────────────────────────┐│
│ │[🏃Running][🚴Cycling][🏊Swimming][⚡Other]│ [Tabs]
│ └──────────────────────────────────────────┘│
│                                             │
│ Distance & Time                             │
│ ┌─────────────────────┬──────────────────┐ │
│ │ Distance            │ Duration         │ │
│ │ ┌─────────────────┐ │ ┌──────────────┐ │ │
│ │ │ 5.0 mi          │ │ │ 40 min       │ │ │
│ │ └─────────────────┘ │ └──────────────┘ │ │
│ │ [mi / km toggle]    │                  │ │
│ └─────────────────────┴──────────────────┘ │
│                                             │
│ Pace                                        │
│ ┌─────────────────────────────────────────┐ │
│ │ 🎯 8:00 /mile  •  4:58 /km              │ │ [Auto-calculated]
│ └─────────────────────────────────────────┘ │
│                                             │
│ Calories                                    │
│ ┌─────────────────────────────────────────┐ │
│ │ ⚡ 550 calories (estimated)              │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ▼ More details                              │
│                                             │
│ ✅ Save Activity    ✏️ Edit                │
└─────────────────────────────────────────────┘
```

---

## 📝 NOTE ENTRY UI

**Input:** "Feeling great today! Hit a new PR on bench press."

**UI Layout:**

```
┌─────────────────────────────────────────────┐
│ 📝 Note Entry                               │
├─────────────────────────────────────────────┤
│ Title (optional)                            │
│ ┌─────────────────────────────────────────┐ │
│ │ New PR Day!                             │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Note                                        │
│ ┌─────────────────────────────────────────┐ │
│ │ Feeling great today! Hit a new PR on    │ │
│ │ bench press.                            │ │ [Textarea]
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Sentiment                                   │
│ 😊 Positive • 95% confident                 │ [Badge with emoji]
│                                             │
│ AI Detected Themes                          │
│ [motivation] [progress] [workout]           │ [Chips]
│                                             │
│ ▼ More details                              │
│                                             │
│ ✅ Save Note    ✏️ Edit                    │
└─────────────────────────────────────────────┘
```

**Expanded:**

```
│ Related Goals                               │
│ • Build muscle                              │
│ • Increase strength                         │
│                                             │
│ Action Items                                │
│ • Continue progressive overload             │
```

---

## ⚖️ MEASUREMENT ENTRY UI

**Input:** "175.2 lbs, 15.5% body fat"

**UI Layout:**

```
┌─────────────────────────────────────────────┐
│ ⚖️ Body Measurement                         │
├─────────────────────────────────────────────┤
│ Weight                                      │
│ ┌─────────────────────────────────────────┐ │
│ │ 175.2 lbs                               │ │
│ │                                         │ │
│ │ [lbs / kg toggle]                       │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Body Fat %                                  │
│ ┌─────────────────────────────────────────┐ │
│ │ 15.5%                                   │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ 📊 Trend: ↓ Down 0.5 lbs from last week    │ [Trend badge]
│                                             │
│ ▼ Add measurements (chest, waist, etc.)    │
│                                             │
│ ✅ Save Measurement    ✏️ Edit             │
└─────────────────────────────────────────────┘
```

---

## 🎨 Design System

### Colors

```
Primary Actions:
- Save: #10B981 (Green)
- Edit: #3B82F6 (Blue)
- Delete: #EF4444 (Red)

Badges:
- Estimated: #F59E0B (Amber)
- Confident: #10B981 (Green)
- Warning: #F59E0B (Amber)
- Error: #EF4444 (Red)

Sentiment:
- Positive: #10B981 (Green) 😊
- Neutral: #6B7280 (Gray) 😐
- Negative: #EF4444 (Red) 😔

Nutrition Cards:
- Calories: #8B5CF6 (Purple)
- Protein: #EF4444 (Red)
- Carbs: #F59E0B (Amber)
- Fat: #3B82F6 (Blue)
```

### Typography

```
Headings: Inter, 600 weight
Body: Inter, 400 weight
Numbers: SF Mono (monospace for precise values)
```

### Spacing

```
Card padding: 20px
Element spacing: 12px
Button height: 44px (thumb-friendly)
Input height: 44px
```

---

## 🔄 Edit Mode

When user clicks "Edit" button, transform card:

```
BEFORE (View Mode):
┌─────────────────────┐
│ Calories: 558       │ [Static text]
└─────────────────────┘

AFTER (Edit Mode):
┌─────────────────────┐
│ Calories            │
│ ┌─────────────────┐ │
│ │ 558           ✏️│ │ [Editable input]
│ └─────────────────┘ │
└─────────────────────┘
```

All fields become editable inline. Save/Cancel buttons appear at bottom.

---

## ✅ Validation & Errors

### Show Errors Inline:

```
┌─────────────────────────────────────────────┐
│ Calories                                    │
│ ┌─────────────────────────────────────────┐ │
│ │ abc                                     │ │ [Red border]
│ └─────────────────────────────────────────┘ │
│ ❌ Must be a number                         │ [Error text]
└─────────────────────────────────────────────┘
```

### Warning Banner:

```
┌─────────────────────────────────────────────┐
│ ⚠️ Missing critical information             │ [Yellow banner]
│ Add portions for accurate nutrition tracking│
└─────────────────────────────────────────────┘
```

---

## 📱 Mobile Optimizations

1. **Bottom Sheet** - Entry appears as bottom sheet (not modal)
2. **Swipe Actions** - Swipe food items to delete
3. **Haptic Feedback** - Vibrate on successful save
4. **Keyboard Aware** - Scroll to keep focused field visible
5. **Number Pad** - Show number keyboard for numeric inputs

---

## 🎬 Animations

1. **Card Entrance**: Slide up from bottom (300ms ease-out)
2. **Expand/Collapse**: Smooth height transition (200ms)
3. **Save Success**: Check mark animation + brief haptic
4. **Error Shake**: Gentle shake on validation error

---

## 🧪 Test Cases

1. ✅ Meal with all portions → Show complete nutrition
2. ✅ Meal without portions → Show warning + quick estimate option
3. ✅ Workout with exercises → Show exercise cards
4. ✅ Activity with pace → Auto-calculate and display
5. ✅ Note with sentiment → Show emoji badge
6. ✅ Measurement with trend → Show trend indicator
7. ✅ Similar past entries → Show context cards
8. ✅ Low confidence → Show warning banner
9. ✅ Edit mode → Transform all fields to inputs
10. ✅ Validation errors → Show inline errors

---

## 🚀 Implementation Priority

**Phase 1 (MVP):**
1. Meal entry (detailed + vague cases)
2. Workout entry (basic exercises)
3. Edit mode for all fields
4. Validation and errors

**Phase 2:**
5. Activity entry
6. Note entry
7. Measurement entry
8. Semantic context (similar entries)

**Phase 3:**
9. Advanced animations
10. Mobile optimizations
11. Accessibility (screen readers, keyboard nav)

---

## 💻 Code Example (React/TypeScript)

```tsx
interface MealPreviewProps {
  data: QuickEntryPreview;
  onSave: () => void;
  onEdit: () => void;
}

function MealPreview({ data, onSave, onEdit }: MealPreviewProps) {
  const [expanded, setExpanded] = useState(false);
  const primary = data.data.primary_fields;
  const secondary = data.data.secondary_fields;

  return (
    <Card className="meal-preview">
      <CardHeader>
        <Heading>🍽️ Meal Entry</Heading>
        {data.data.estimated && (
          <Badge variant="warning">⚡ Estimated</Badge>
        )}
      </CardHeader>

      <CardBody>
        {/* Meal Name */}
        <FormField label="Meal Name">
          <Input
            value={primary.meal_name}
            onChange={(e) => updateField('meal_name', e.target.value)}
          />
        </FormField>

        {/* Meal Type */}
        <FormField label="Meal Type">
          <SegmentedControl
            value={primary.meal_type}
            options={['breakfast', 'lunch', 'dinner', 'snack']}
            onChange={(v) => updateField('meal_type', v)}
          />
        </FormField>

        {/* Foods */}
        <FormField label="Foods">
          <FoodChips foods={primary.foods} />
        </FormField>

        {/* Nutrition */}
        <NutritionCards
          calories={primary.calories}
          protein={primary.protein_g}
          carbs={secondary.carbs_g}
        />

        {/* Expand Button */}
        <Button
          variant="ghost"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? '▲ Less details' : '▼ More details'}
        </Button>

        {/* Expanded Section */}
        {expanded && (
          <Collapse>
            <DetailedNutrition data={secondary} />
            <QualityScores data={secondary} />
          </Collapse>
        )}

        {/* Validation */}
        {data.validation.warnings.length > 0 && (
          <Alert variant="warning">
            {data.validation.warnings[0]}
          </Alert>
        )}

        {/* Suggestions */}
        {data.suggestions.length > 0 && (
          <SuggestionBox>
            {data.suggestions.map(s => <li key={s}>{s}</li>)}
          </SuggestionBox>
        )}
      </CardBody>

      <CardFooter>
        <Button variant="primary" onClick={onSave}>
          ✅ Save Entry
        </Button>
        <Button variant="secondary" onClick={onEdit}>
          ✏️ Edit
        </Button>
      </CardFooter>
    </Card>
  );
}
```

---

**END OF SPECIFICATION**

This spec provides everything needed for a polished, production-ready quick entry UI. All edge cases are covered, and the design prioritizes user experience while maintaining data accuracy.
