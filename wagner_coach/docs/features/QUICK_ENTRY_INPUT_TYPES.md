# Quick Entry Optimized - Comprehensive Input Types Guide

## Overview
This document catalogs **every single type of input** a user might give to the quick-entry-optimized system, including all combinations, edge cases, and data formats.

---

## 🎯 Core Input Modalities

### 1. **Text Input**
The primary input method via the textarea.

#### 1.1 Direct Text Entry
- **Plain descriptions**: "Chicken salad for lunch"
- **Detailed narratives**: "Had a grilled chicken breast (6oz) with brown rice (1 cup) and steamed broccoli (2 cups) for lunch today. Felt satisfied and energized."
- **Short notes**: "Tired today"
- **Structured data**: "Weight: 175.2 lbs, Body fat: 15.5%"

#### 1.2 Meal Text Inputs
```
BREAKFAST:
- "Oatmeal with banana and protein powder"
- "3 eggs, 2 slices whole wheat toast, avocado"
- "Greek yogurt 200g with berries and honey"
- "Protein shake: 2 scoops whey, almond milk, peanut butter"
- "Skipped breakfast" (null entry)

LUNCH:
- "Chicken salad wrap with veggies"
- "Subway footlong turkey on wheat"
- "Chipotle bowl: chicken, brown rice, black beans, veggies, guac"
- "Leftovers from yesterday"
- "Meal prep container #3"

DINNER:
- "Steak 8oz with sweet potato and asparagus"
- "Salmon fillet, quinoa, roasted vegetables"
- "Pizza - 3 slices pepperoni"
- "Takeout: Chinese food, general tso's chicken with fried rice"

SNACKS:
- "Protein bar"
- "Apple with peanut butter"
- "Handful of almonds"
- "Chips and salsa"
- "Cookie"

SUPPLEMENTS:
- "Creatine 5g, multivitamin, fish oil"
- "Pre-workout before gym"
- "Vitamin D 5000 IU"
```

#### 1.3 Activity Text Inputs
```
RUNNING:
- "Ran 5 miles in 40 minutes"
- "Morning jog, felt good"
- "5k race: 22:15 finish time"
- "Easy recovery run 3 miles"
- "Interval training: 8x400m"

CYCLING:
- "Bike ride 20 miles"
- "Indoor cycling class 45 minutes"
- "Commute by bike: 12 miles round trip"

WALKING:
- "Walked 10,000 steps"
- "Evening walk with dog"
- "Walked to grocery store and back"

SWIMMING:
- "Swam 1000m freestyle"
- "Pool workout: laps for 30 minutes"

SPORTS:
- "Basketball pickup game 1 hour"
- "Tennis match - won 2 sets"
- "Soccer practice"
- "Volleyball - beach, 2 hours"

OTHER CARDIO:
- "Jump rope 10 minutes"
- "Rowing machine 5k"
- "Stairmaster 20 minutes"
- "Elliptical 45 minutes"
```

#### 1.4 Workout Text Inputs
```
STRENGTH TRAINING:
- "Bench press 4x8 at 185lbs, shoulder press 3x10 at 95lbs"
- "Leg day: squats 5x5 at 225, leg press, leg curls, calf raises"
- "Pull workout: deadlifts 3x5 at 315, rows, lat pulldowns, bicep curls"
- "Push day complete"
- "Upper body pump"

SPECIFIC EXERCISES:
- "100 pushups"
- "Max pullups: got 15"
- "Plank hold 3 minutes"
- "Bodyweight circuit"

WORKOUT PROGRAMS:
- "Starting Strength week 3 day 1"
- "PPL Push day"
- "Arnold split - chest/back"
- "5/3/1 main lifts done"

HOME/GYM:
- "Home workout - dumbbells only"
- "Gym session crushed it"
- "Hotel gym improvised workout"
```

#### 1.5 Measurement Text Inputs
```
WEIGHT:
- "175.2 lbs"
- "Weighed in at 80.5 kg"
- "Morning weight: 178"

BODY COMPOSITION:
- "Body fat: 15.5%"
- "Lean mass: 145 lbs"
- "DEXA scan results: 12% BF"

MEASUREMENTS:
- "Waist: 32 inches"
- "Arms: 15.5 in, chest: 42 in"
- "All measurements taken"

PROGRESS:
- "Progress photos taken"
- "Visible abs finally!"
- "Veins popping in arms"
```

#### 1.6 Note Text Inputs
```
FEELINGS:
- "Feeling great today"
- "Low energy, might be overtraining"
- "Motivated after watching fitness video"
- "Stressed about work, hard to stick to routine"

GOALS:
- "New goal: bench 225 by summer"
- "Want to lose 10 lbs by wedding"
- "Aiming for sub-20min 5k"

REFLECTIONS:
- "This week went really well"
- "Need to focus more on sleep"
- "Meal prep is saving me so much time"
- "Consistency is key - seeing results"

PLANS:
- "Planning to start cutting next week"
- "Going to try intermittent fasting"
- "New program starts Monday"

OBSERVATIONS:
- "Recovery feeling better with extra sleep"
- "Noticed strength gains on bench"
- "Cardio endurance improving"
```

#### 1.7 Nutrition-Specific Patterns
```
MACROS EXPLICIT:
- "450 calories, 45g protein, 40g carbs, 8g fat"
- "P: 120g, C: 200g, F: 60g"
- "2200 calories total today"

PORTIONS:
- "6 oz chicken breast"
- "1 cup rice"
- "2 tablespoons olive oil"
- "100g quinoa"
- "Medium apple"
- "Large sweet potato"

BRANDED FOODS:
- "Quest bar chocolate chip"
- "Optimum Nutrition gold standard whey"
- "Chobani Greek yogurt vanilla"
- "Clif Bar peanut butter"

RESTAURANTS/CHAINS:
- "Chipotle chicken bowl"
- "McDonald's Big Mac meal"
- "Starbucks grande latte"
- "Pizza Hut medium pepperoni"

COOKING METHODS:
- "Grilled chicken"
- "Baked salmon"
- "Steamed broccoli"
- "Fried eggs"
- "Raw carrots"
```

---

## 🎤 Voice Input

### 2. **Voice/Audio Recordings**

#### 2.1 Voice Notes (Speech-to-Text)
Users can record voice memos that get transcribed via Whisper API.

**Common voice input patterns:**
```
QUICK LOGS:
- "Just finished a five mile run"
- "Ate chicken and rice for lunch"
- "Feeling tired today, might need a rest day"

DETAILED NARRATIVES:
- "Hey, so I just had the most amazing workout. Hit a new PR on bench press,
   185 pounds for 8 reps. Feeling super strong. Also did shoulder press and
   some accessory work. Total gym time was about an hour and fifteen minutes."

ON-THE-GO:
- "Walking into restaurant now, probably gonna order salmon"
- "At the gym, about to start leg day"
- "Just weighed myself, 176 point 3"

EMOTIONAL:
- "Really struggling with motivation today"
- "So pumped, saw my abs in the mirror!"
- "This diet is getting hard"

STREAM OF CONSCIOUSNESS:
- "Had a protein shake this morning, then went to the gym, did chest and
   triceps, felt pretty good, energy was high, came home, made eggs and
   toast, now I'm about to go for a walk"
```

#### 2.2 Audio File Uploads
Users can upload pre-recorded audio files:
- Voice memos from phone
- Audio notes from meetings/coaching sessions
- Recorded workout commentary
- Meal descriptions captured while cooking

**Supported audio formats:**
- `.m4a` (iOS voice memos)
- `.mp3`
- `.wav`
- `.webm` (browser recordings)
- Other standard audio formats

---

## 📸 Image Input

### 3. **Photo Uploads**

#### 3.1 Meal Photos
```
FULL MEALS:
- Plate of food (breakfast/lunch/dinner)
- Restaurant dish
- Meal prep containers
- Buffet/potluck plate
- Home-cooked meal

INDIVIDUAL FOODS:
- Single apple
- Protein shake in shaker
- Piece of meat on cutting board
- Salad bowl
- Sandwich

PACKAGED FOODS:
- Nutrition label (front)
- Nutrition facts (back)
- Protein bar wrapper
- Supplement bottle
- Restaurant menu item

COOKING PROCESS:
- Ingredients laid out
- Food being prepared
- Multiple meal prep containers

BEVERAGES:
- Coffee cup
- Smoothie
- Protein shake
- Water bottle with measurements
- Alcohol (beer, wine, cocktail)
```

#### 3.2 Workout/Activity Photos
```
PROGRESS PHOTOS:
- Mirror selfie (front)
- Mirror selfie (side)
- Back pose
- Flexing biceps
- Abs/core shot
- Legs
- Before/after comparison

GYM SCREENSHOTS:
- Workout app screenshot (Strava, MyFitnessPal, etc.)
- Fitness tracker data (Apple Watch, Garmin, Fitbit)
- Treadmill/machine display
- Stopwatch/timer

EXERCISE FORM:
- Mid-squat
- Deadlift setup
- Bench press form check
- Yoga pose
- Running posture

EQUIPMENT:
- Weights being used
- Gym setup
- Home gym equipment
- Running shoes (worn out)
```

#### 3.3 Measurement Photos
```
SCALE READINGS:
- Digital scale display
- Smart scale with body composition
- Bathroom scale analog

BODY MEASUREMENTS:
- Tape measure on waist
- Calipers on body part
- Measuring various body parts

WEARABLE DATA:
- Fitness tracker screen
- Smartwatch display
- Heart rate monitor reading
```

#### 3.4 Notes/Documents as Photos
```
WRITTEN NOTES:
- Handwritten food journal
- Workout log notebook
- Meal plan written down
- Goals list

PRINTED MATERIALS:
- Workout program printout
- Meal plan from nutritionist
- Lab results
- Doctor's notes
```

#### 3.5 Image Quality Variations
```
LIGHTING:
- Bright restaurant lighting
- Dim home lighting
- Natural outdoor light
- Flash photography
- Backlit images

ANGLES:
- Overhead (bird's eye)
- 45-degree angle
- Straight on
- Close-up
- Wide shot with context

FOCUS:
- Sharp and clear
- Slightly blurry
- Partial focus (bokeh effect)
- Low resolution
- Zoomed in crop
```

---

## 📄 PDF Input

### 4. **PDF Uploads**

#### 4.1 Meal Plans
- Nutritionist-created meal plans
- Macro-friendly recipes
- Restaurant nutritional information PDFs
- Meal prep guides

#### 4.2 Workout Programs
- Training program PDFs (5/3/1, PPL, etc.)
- Exercise instruction sheets
- Coaching program documents
- Gym workout cards

#### 4.3 Health Documents
- Lab results
- Body composition scans (DEXA, InBody)
- Doctor's recommendations
- Nutrition consultation notes

#### 4.4 Research/Articles
- Fitness articles saved as PDF
- Research papers on training/nutrition
- Supplement guides

---

## 🔄 Combined/Multimodal Input

### 5. **Text + Image Combinations**

#### 5.1 Meal with Caption
```
TEXT: "Lunch at Chipotle"
IMAGE: Photo of burrito bowl
```

#### 5.2 Workout with Photo Evidence
```
TEXT: "New PR: 225 bench press"
IMAGE: Screenshot of workout app showing lift
```

#### 5.3 Progress Check-in
```
TEXT: "8 weeks into cut, down 12 lbs"
IMAGE: Progress photo comparison
```

#### 5.4 Corrected Vision Analysis
```
TEXT: "Actually this was 6oz chicken, not 8oz"
IMAGE: Meal photo
(User correcting AI's initial estimate)
```

---

### 6. **Text + Voice Combinations**

```
TEXT: "Morning workout"
VOICE: "Did bench press four sets of eight at 185, shoulder press three
        sets of ten at 95, and some tricep work"
```

---

### 7. **Image + Voice Combinations**

```
IMAGE: Photo of complex meal
VOICE: "This is chicken tikka masala with basmati rice and naan bread,
        probably around 800 calories total"
```

---

### 8. **All Three: Text + Voice + Image**

```
TEXT: "Post-workout meal"
VOICE: "Just crushed leg day, feeling great, this should help recovery"
IMAGE: Photo of protein shake and chicken breast
```

---

### 9. **Multiple Images**

```
- Multiple meal photos from the day
- Before/after progress photos
- Different angles of same meal
- Nutrition label + actual food
- Multiple workout screenshots
```

---

### 10. **Multiple Files (Images + PDFs)**

```
IMAGE: Food photo
PDF: Restaurant nutrition info
TEXT: "Had the grilled salmon"
```

---

## 🎛️ Log Type Selector

### 11. **Manual Type Override**

Users can manually select the entry type instead of relying on auto-detection:

#### 11.1 Auto-detect (default)
```
SELECTED: Auto-detect ✨
INPUT: "Chicken salad 450 calories"
RESULT: System classifies as "meal"
```

#### 11.2 Meal 🍽️
```
SELECTED: Meal
INPUT: "Ran 5 miles" (misleading text)
RESULT: Forces system to extract meal data (will likely ask for clarification)
```

#### 11.3 Workout 💪
```
SELECTED: Workout
INPUT: "Bench press 4x8 at 185"
RESULT: Treated as strength training workout
```

#### 11.4 Activity 🏃
```
SELECTED: Activity
INPUT: "Basketball for an hour"
RESULT: Logged as cardio activity
```

#### 11.5 Note 📝
```
SELECTED: Note
INPUT: "Feeling really motivated today"
RESULT: Saved as general note/reflection
```

#### 11.6 Measurement 📊
```
SELECTED: Measurement
INPUT: "175.2"
RESULT: Recorded as weight measurement
```

---

## 🔢 Data Format Variations

### 12. **Numeric Inputs**

#### 12.1 Calories
```
- "450 calories"
- "450 cal"
- "450 kcal"
- "450"
- "~450" (approximate)
- "400-500 calories" (range)
```

#### 12.2 Macros
```
PROTEIN:
- "45g protein"
- "45 grams protein"
- "45g P"
- "P: 45"

CARBS:
- "40g carbs"
- "40 grams carbohydrates"
- "40g C"
- "C: 40"

FAT:
- "8g fat"
- "8 grams fat"
- "8g F"
- "F: 8"

FIBER:
- "6g fiber"
- "6 grams fibre"
```

#### 12.3 Time/Duration
```
- "45 minutes"
- "45 min"
- "45m"
- "1 hour"
- "1h 15m"
- "75 minutes"
- "01:15:00" (digital format)
```

#### 12.4 Distance
```
- "5 miles"
- "5 mi"
- "8 kilometers"
- "8 km"
- "8k"
- "5.2 miles" (decimal)
- "3.1 mi (5k)"
```

#### 12.5 Weight (Exercise)
```
- "185 lbs"
- "185 pounds"
- "185#"
- "85 kg"
- "185" (assumed lbs)
- "2 plates" (gym slang for 225 lbs)
- "Bodyweight" or "BW"
```

#### 12.6 Weight (Body)
```
- "175.2 lbs"
- "175.2 pounds"
- "80.5 kg"
- "175.2" (assumed lbs)
```

#### 12.7 Sets and Reps
```
- "4x8" (4 sets of 8 reps)
- "4 sets of 8"
- "4 sets x 8 reps"
- "3x10-12" (rep range)
- "5x5"
- "AMRAP" (as many reps as possible)
- "3x8-10@185" (weight included)
- "4 x 8 @ 185 lbs"
```

#### 12.8 Body Fat Percentage
```
- "15.5%"
- "15.5 percent"
- "15.5% body fat"
```

#### 12.9 RPE (Rate of Perceived Exertion)
```
- "RPE 8"
- "8/10"
- "Felt like an 8"
- "Easy" (RPE 3-4)
- "Moderate" (RPE 5-6)
- "Hard" (RPE 7-8)
- "Max effort" (RPE 10)
```

---

## 🕐 Temporal Context

### 13. **Time References**

#### 13.1 Meal Times
```
- "breakfast"
- "morning meal"
- "lunch"
- "afternoon snack"
- "dinner"
- "post-workout meal"
- "pre-bed snack"
- "midnight snack"
```

#### 13.2 Workout Timing
```
- "morning workout"
- "6 AM lift"
- "lunch break run"
- "evening gym session"
- "late night workout"
```

#### 13.3 Relative Times
```
- "just now"
- "an hour ago"
- "this morning"
- "earlier today"
- "yesterday" (retroactive logging)
- "last night"
```

---

## 💬 Conversational Patterns

### 14. **Natural Language Variations**

#### 14.1 Casual/Informal
```
- "grabbed some chipotle lol"
- "crushed it at the gym today 💪"
- "meh, skipped workout"
- "ate wayyy too much pizza"
- "lazy day, just walked the dog"
```

#### 14.2 Formal/Structured
```
- "Consumed 450 calories consisting of grilled chicken breast (6oz),
   brown rice (1 cup), and steamed broccoli (2 cups)"
- "Completed resistance training session: upper body push movements"
- "Recorded body weight measurement: 175.2 pounds"
```

#### 14.3 Questions/Uncertainty
```
- "Not sure on calories but chicken salad"
- "Maybe 5 miles? Didn't track exactly"
- "Think it was around 450 calories"
- "Does walking count as cardio?"
```

#### 14.4 Emotional Context
```
- "Really proud of this meal prep!"
- "Struggling with motivation :("
- "Best workout in weeks!!"
- "Feeling defeated, ate way off plan"
```

---

## 🌍 Language & Units

### 15. **International Variations**

#### 15.1 Metric vs Imperial
```
WEIGHT (BODY):
- Imperial: lbs, pounds
- Metric: kg, kilograms

WEIGHT (EXERCISE):
- Imperial: lbs, pounds
- Metric: kg, kilograms

DISTANCE:
- Imperial: miles, yards, feet
- Metric: kilometers, meters

VOLUME:
- Imperial: cups, tablespoons, ounces (oz)
- Metric: milliliters (mL), liters (L), grams (g)

HEIGHT:
- Imperial: feet, inches
- Metric: centimeters (cm), meters (m)
```

#### 15.2 Date Formats
```
- US: MM/DD/YYYY
- International: DD/MM/YYYY
- ISO: YYYY-MM-DD
```

---

## ⚠️ Edge Cases & Challenges

### 16. **Ambiguous Inputs**

#### 16.1 Multi-Category Ambiguity
```
INPUT: "Ran to the gym, did bench press, ate chicken after"
CONTAINS: Activity + Workout + Meal
EXPECTED: System should ask or split into multiple entries
```

#### 16.2 Minimal Information
```
- "Ate food"
- "Worked out"
- "Tired"
- "Good day"
```

#### 16.3 Conflicting Information
```
TEXT: "Had a light salad"
IMAGE: Photo of massive burrito
```

#### 16.4 Sarcasm/Humor
```
- "Definitely didn't eat an entire pizza" (user ate entire pizza)
- "Meal prep game weak" (with photo of impressive meal prep)
```

#### 16.5 Abbreviations & Slang
```
FOOD:
- "chx" = chicken
- "broc" = broccoli
- "sammie" = sandwich
- "cals" = calories
- "pro" = protein

EXERCISE:
- "deads" = deadlifts
- "bis" = biceps
- "tris" = triceps
- "delts" = deltoids/shoulders
- "quads" = quadriceps
- "PR" = personal record
- "AMRAP" = as many reps as possible
- "EMOM" = every minute on the minute
- "WOD" = workout of the day

GENERAL:
- "bf%" = body fat percentage
- "BW" = bodyweight
- "RM" = rep max (e.g., "1RM" = one rep max)
```

---

## 🎨 Metadata & Context

### 17. **Additional Context Fields**

#### 17.1 Notes Field (Separate from Main Input)
Users can add feelings/reflections separate from the main log:

```
MAIN INPUT: "Chicken salad 450 calories"
NOTES: "Felt really satisfied, no cravings after"
```

#### 17.2 Tags (Potential Future Feature)
```
- #mealprep
- #cheatmeal
- #preworkout
- #newPR
- #restday
- #recovery
```

#### 17.3 Location Context
```
- "At home"
- "Restaurant: Chipotle"
- "Planet Fitness gym"
- "Hotel gym while traveling"
```

#### 17.4 Social Context
```
- "With friends"
- "Family dinner"
- "Alone"
- "Date night"
- "Team practice"
```

---

## 🔁 Correction & Edit Patterns

### 18. **User Corrections During Confirmation**

After AI processes the entry, users can edit fields in the confirmation modal:

#### 18.1 Calorie Corrections
```
AI DETECTED: 450 calories
USER EDITS: 500 calories
```

#### 18.2 Portion Corrections
```
AI DETECTED: 6 oz chicken
USER EDITS: 8 oz chicken
```

#### 18.3 Type Corrections
```
AI CLASSIFIED: Meal
USER CHANGES: Activity (user described meal but meant to log the cooking as activity)
```

#### 18.4 Macro Adjustments
```
AI EXTRACTED: 45g protein, 40g carbs, 8g fat
USER EDITS: 50g protein, 35g carbs, 10g fat
```

#### 18.5 Adding Missing Fields
```
AI EXTRACTED: Meal name, calories
USER ADDS: Protein, carbs, fat, notes
```

---

## 🚫 Null/Empty Inputs

### 19. **Edge Cases with No Data**

#### 19.1 Completely Empty
```
TEXT: (empty)
IMAGE: (none)
AUDIO: (none)
RESULT: Error - "Please enter text or attach a file"
```

#### 19.2 Whitespace Only
```
TEXT: "   " (spaces/tabs)
RESULT: Treated as empty
```

#### 19.3 Placeholder Text
```
TEXT: "Describe what you ate, did, or how you feel..."
RESULT: Should be filtered out
```

---

## 🌟 Complex Real-World Examples

### 20. **Multi-Part Entries**

#### 20.1 Full Day Summary
```
TEXT: "Full day of eating:
Breakfast - oatmeal with protein powder and berries, 400 cals
Lunch - chicken salad wrap, 500 cals
Dinner - salmon with quinoa and veggies, 600 cals
Snacks - protein bar, apple with PB, 300 cals
Total: 1800 calories"
```

#### 20.2 Complete Workout Log
```
TEXT: "Push day:
Bench press: 4x8 @ 185 lbs
Incline DB press: 3x10 @ 60 lbs
Shoulder press: 3x10 @ 95 lbs
Lateral raises: 3x12 @ 25 lbs
Tricep pushdowns: 3x15 @ 50 lbs
Duration: 75 minutes
RPE: 8/10
Notes: New PR on bench!"
```

#### 20.3 Race/Event Recap
```
TEXT: "5k race today!
Time: 22:15
Distance: 3.1 miles (5k)
Pace: 7:10/mile
Place: 23rd overall
Felt: Great, beat my PR by 30 seconds
Weather: Cool and perfect
Notes: New race shoes helped a lot"
```

#### 20.4 Transformation Check-In
```
TEXT: "12-week progress check-in"
IMAGE: Before/after photos side-by-side
ADDITIONAL TEXT: "Started at 195 lbs, now 175 lbs
Body fat from 22% to 14%
Bench from 135 to 185
Can see abs finally!
Feeling incredible"
```

---

## 📊 Data Extraction Expectations

### 21. **What the System Should Extract**

#### 21.1 From Meal Inputs
```
REQUIRED:
- meal_name (string)
- meal_type (breakfast/lunch/dinner/snack)

OPTIONAL:
- calories (number)
- protein_g (number)
- carbs_g (number)
- fat_g (number)
- fiber_g (number)
- foods (array of {name, quantity})
- estimated (boolean - was nutrition estimated?)
- notes (string)
```

#### 21.2 From Activity Inputs
```
REQUIRED:
- activity_name (string)
- activity_type (running/cycling/walking/swimming/sport)

OPTIONAL:
- duration_minutes (number)
- distance_km (number)
- pace (string, e.g., "6:00/km")
- calories_burned (number)
- heart_rate_avg (number)
- rpe (number 1-10)
- mood (string)
- energy_level (string)
- notes (string)
```

#### 21.3 From Workout Inputs
```
REQUIRED:
- workout_name (string)
- workout_type (strength/cardio/flexibility)

OPTIONAL:
- exercises (array of {name, sets, reps, weight_lbs})
- duration_minutes (number)
- rpe (number 1-10)
- difficulty_rating (number 1-10)
- workout_rating (number 1-10)
- mood (string)
- energy_level (string)
- notes (string)
```

#### 21.4 From Measurement Inputs
```
OPTIONAL (at least one required):
- weight_lbs (number)
- body_fat_pct (number)
- measurements (object with body part dimensions)
  - chest_in (number)
  - waist_in (number)
  - hips_in (number)
  - arms_in (number)
  - thighs_in (number)
- notes (string)
```

#### 21.5 From Note Inputs
```
REQUIRED:
- content (string)

OPTIONAL:
- title (string)
- category (string: reflection/goal/plan/observation)
- tags (array of strings)
```

---

## 🎯 Intent Detection Patterns

### 22. **Implicit vs Explicit Intent**

#### 22.1 Explicit Meal Intent
```
- "I ate..."
- "Had for lunch..."
- "Breakfast was..."
- "Consumed..."
- "Meal:"
```

#### 22.2 Implicit Meal Intent
```
- "Chicken and rice" (no verb, but clearly food)
- "500 calories" (number with calorie unit)
- Photo of food
```

#### 22.3 Explicit Workout Intent
```
- "Lifted..."
- "Workout:"
- "Trained..."
- "Exercise:"
- "Gym session:"
```

#### 22.4 Implicit Workout Intent
```
- "4x8 bench" (sets x reps format)
- "Squats 225" (exercise + weight)
- Photo of weights/gym
```

#### 22.5 Explicit Activity Intent
```
- "Ran..."
- "Walked..."
- "Cycled..."
- "Swam..."
- "Played..."
```

#### 22.6 Implicit Activity Intent
```
- "5 miles" (distance alone)
- "45 minutes cardio" (duration + activity type)
- Screenshot of Strava/fitness tracker
```

---

## 🔮 Future/Advanced Input Types

### 23. **Potential Future Enhancements**

#### 23.1 Barcode Scanning
```
- Scan food product barcode
- Auto-populate nutrition from database
```

#### 23.2 Recipe Import
```
- URL to recipe website
- Parse ingredients and nutrition
```

#### 23.3 Calendar Integration
```
- Import workouts from Google Calendar
- Import meal plans from scheduling apps
```

#### 23.4 Wearable Sync
```
- Auto-import from Apple Health
- Sync with Fitbit
- Connect to Garmin
- MyFitnessPal integration
```

#### 23.5 Bulk Import
```
- CSV upload of historical data
- Import from other fitness apps
- Batch photo upload
```

---

## 🎓 Summary: Input Type Matrix

| Input Type | Text | Voice | Image | PDF | Manual Type | Common Use Cases |
|------------|------|-------|-------|-----|-------------|------------------|
| **Meal** | ✅ | ✅ | ✅ | ✅ | ✅ | Food logging, nutrition tracking |
| **Activity** | ✅ | ✅ | ✅ | ❌ | ✅ | Cardio, running, cycling, sports |
| **Workout** | ✅ | ✅ | ✅ | ✅ | ✅ | Strength training, exercise logging |
| **Measurement** | ✅ | ✅ | ✅ | ✅ | ✅ | Weight, body fat, progress photos |
| **Note** | ✅ | ✅ | ❌ | ❌ | ✅ | Thoughts, goals, reflections |
| **Mixed** | ✅ | ✅ | ✅ | ✅ | ❌ | Complex entries spanning multiple types |

---

## 🏁 Conclusion

This document covers **every conceivable input type** a user might provide to the quick-entry-optimized system, including:

- ✅ Text variations (structured, casual, detailed, minimal)
- ✅ Voice/audio inputs (transcribed speech, uploaded audio files)
- ✅ Image uploads (meals, workouts, progress photos, screenshots)
- ✅ PDF documents (meal plans, workout programs, health records)
- ✅ Multimodal combinations (text + voice, text + image, all three)
- ✅ Manual type overrides (forcing classification)
- ✅ Numeric format variations (calories, macros, time, distance, weight, reps)
- ✅ Temporal context (meal times, workout timing, relative dates)
- ✅ Natural language patterns (casual, formal, questions, emotions)
- ✅ International variations (metric/imperial, date formats)
- ✅ Edge cases (ambiguity, minimal data, conflicts, slang)
- ✅ Metadata and additional context (notes, location, social)
- ✅ Correction patterns (user edits during confirmation)
- ✅ Null/empty inputs
- ✅ Complex real-world examples
- ✅ Data extraction expectations
- ✅ Intent detection patterns
- ✅ Future enhancement possibilities

**The system is designed to handle ALL of these input types intelligently, extract structured data, and save to the appropriate database tables after user confirmation.**
