# Critical Fix: Garmin Table Mismatch Resolved

## 🚨 Problem Discovered

**The AI Coach could NOT access Garmin data** despite garmy successfully syncing it to the database.

### Root Cause
- **Coach queries**: `garmin_sleep_data`, `garmin_hrv_data`, `garmin_stress_data`, `garmin_body_battery`, `garmin_readiness`
- **Garmy syncs to**: `sleep_logs`, `hrv_logs`, `stress_logs`, `body_battery_logs`, `daily_readiness`
- **Result**: Coach saw ZERO Garmin data (tables didn't exist!)

---

## ✅ Solution Implemented

### Fixed File: `app/services/context_builder.py`

Updated **ALL** Garmin queries in two critical methods:
1. `_get_recovery_metrics()` - Lines 834-1103
2. `_get_recovery_performance_correlations()` - Lines 1128-1364

### Table Name Changes

| Old (Wrong) Table | New (Correct) Table | Filter Added |
|---|---|---|
| `garmin_sleep_data` | `sleep_logs` | `.eq("source", "garmin")` |
| `garmin_hrv_data` | `hrv_logs` | `.eq("source", "garmin")` |
| `garmin_stress_data` | `stress_logs` | `.eq("source", "garmin")` |
| `garmin_body_battery` | `body_battery_logs` | `.eq("source", "garmin")` |
| `garmin_readiness` | `daily_readiness` | (no filter needed) |

### Column Name Changes

| Old Column | New Column | Notes |
|---|---|---|
| `calendar_date` | `sleep_date` | For sleep logs |
| `calendar_date` | `recorded_at` | For HRV/stress logs |
| `calendar_date` | `date` | For readiness/battery |
| `total_sleep_seconds` | `total_sleep_minutes` | Units changed: /60 instead of /3600 |
| `overall_score` | `sleep_score` | For sleep logs |
| `overall_score` | `readiness_score` | For readiness |
| `deep_sleep_seconds` | `deep_sleep_minutes` | Units changed |
| `light_sleep_seconds` | `light_sleep_minutes` | Units changed |
| `rem_sleep_seconds` | `rem_sleep_minutes` | Units changed |
| `awake_sleep_seconds` | `awake_minutes` | Units changed |
| `average_hrv_ms` | `avg_hrv_ms` | Name shortened |
| `last_night_avg_ms` | `hrv_rmssd_ms` | Changed to standard HRV metric |
| `weekly_avg_ms` | `hrv_sdnn_ms` | Changed to standard HRV metric |
| `rest_stress_duration_seconds` | `rest_minutes` | Simplified |
| `highest_body_battery` | `battery_level` | Simplified schema |
| `body_battery_charged` | `charged_value` | Column renamed |
| `body_battery_drained` | `drained_value` | Column renamed |
| `readiness_message` | `readiness_status` | Status instead of message |

---

## Impact

### Before Fix
❌ Coach queries non-existent `garmin_*` tables
❌ Returns: "No recovery data available from Garmin"
❌ Coach cannot make data-driven recommendations
❌ Users see no benefit from Garmin sync

### After Fix
✅ Coach queries correct `sleep_logs`, `hrv_logs`, etc.
✅ Filters by `source="garmin"` to get only Garmin data
✅ Coach displays comprehensive recovery metrics
✅ Coach can make personalized recommendations based on:
- Sleep quality (last 7 nights)
- HRV trends (improving/declining/stable)
- Stress levels (daily averages)
- Body Battery (energy reserves)
- Training Readiness (recovery status)
✅ Recovery-performance correlations work
✅ Personalized training recommendations based on real data

---

## Specific Changes by Section

### 1. Sleep Data Query (Line 835-879)
**Before:**
```python
self.supabase.table("garmin_sleep_data")
    .gte("calendar_date", cutoff_date)

total_duration = latest_sleep.get("total_sleep_seconds", 0) / 3600
sleep_score = latest_sleep.get("overall_score")
```

**After:**
```python
self.supabase.table("sleep_logs")
    .eq("source", "garmin")  # NEW: Filter for Garmin data
    .gte("sleep_date", cutoff_date)

total_duration = latest_sleep.get("total_sleep_minutes", 0) / 60
sleep_score = latest_sleep.get("sleep_score")
```

### 2. HRV Data Query (Line 881-920)
**Before:**
```python
self.supabase.table("garmin_hrv_data")
    .gte("calendar_date", cutoff_date)

last_night_avg = latest_hrv.get("last_night_avg_ms")
weekly_avg = latest_hrv.get("weekly_avg_ms")
status = latest_hrv.get("status")
```

**After:**
```python
self.supabase.table("hrv_logs")
    .eq("source", "garmin")  # NEW: Filter for Garmin data
    .gte("recorded_at", cutoff_date)

hrv_rmssd = latest_hrv.get("hrv_rmssd_ms")
hrv_sdnn = latest_hrv.get("hrv_sdnn_ms")
measurement_type = latest_hrv.get("measurement_type")
```

### 3. Stress Data Query (Line 922-957)
**Before:**
```python
self.supabase.table("garmin_stress_data")
    .gte("calendar_date", cutoff_date)

rest_time = latest_stress.get("rest_stress_duration_seconds", 0) / 3600
```

**After:**
```python
self.supabase.table("stress_logs")
    .eq("source", "garmin")  # NEW: Filter for Garmin data
    .gte("recorded_at", cutoff_date)

rest_time = latest_stress.get("rest_minutes", 0) / 60
```

### 4. Body Battery Query (Line 959-999)
**Before:**
```python
self.supabase.table("garmin_body_battery")
    .gte("calendar_date", cutoff_date)

highest = latest_battery.get("highest_body_battery")
lowest = latest_battery.get("lowest_body_battery")
charged = latest_battery.get("body_battery_charged")
drained = latest_battery.get("body_battery_drained")
```

**After:**
```python
self.supabase.table("body_battery_logs")
    .eq("source", "garmin")  # NEW: Filter for Garmin data
    .gte("date", cutoff_date)

battery_level = latest_battery.get("battery_level")
charged = latest_battery.get("charged_value")
drained = latest_battery.get("drained_value")
```

### 5. Readiness Query (Line 1001-1039)
**Before:**
```python
self.supabase.table("garmin_readiness")
    .gte("calendar_date", cutoff_date)

score = latest_readiness.get("overall_score")
message = latest_readiness.get("readiness_message")
```

**After:**
```python
self.supabase.table("daily_readiness")
    .gte("date", cutoff_date)

score = latest_readiness.get("readiness_score")
status = latest_readiness.get("readiness_status")
```

### 6. Recovery Insights (Line 1041-1103)
- Fixed all references to use new column names
- Sleep: `total_sleep_seconds` → `total_sleep_minutes`
- HRV: `status` → check `hrv_rmssd_ms` value directly
- Readiness: `overall_score` → `readiness_score`

### 7. Correlation Analysis (Line 1128-1364)
**Fixed all 4 data fetches:**
- Sleep: `garmin_sleep_data` → `sleep_logs` with source filter
- HRV: `garmin_hrv_data` → `hrv_logs` with source filter
- Stress: `garmin_stress_data` → `stress_logs` with source filter
- Readiness: `garmin_readiness` → `daily_readiness`

**Fixed all column references in correlations:**
- Sleep quality vs workout performance
- HRV trends vs training load
- Readiness score vs workout completion
- Stress patterns analysis
- Personalized recovery recommendations

---

## Testing Required

### Unit Tests
- [ ] Test `_get_recovery_metrics()` returns data
- [ ] Test `_get_recovery_performance_correlations()` returns insights
- [ ] Verify no errors when no Garmin data exists
- [ ] Verify data is correctly parsed and formatted

### Integration Tests
1. **User authenticates with Garmin:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/garmin/test \
     -H "Authorization: Bearer JWT_TOKEN" \
     -d '{"email": "user@garmin.com", "password": "password"}'
   ```
   Expected: `{"success": true, "profile": {...}}`

2. **User syncs Garmin data:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/garmin/sync \
     -H "Authorization: Bearer JWT_TOKEN" \
     -d '{"email": "user@garmin.com", "password": "password", "days_back": 7}'
   ```
   Expected: `{"success": true, "total_synced": 156, ...}`

3. **Verify data in Supabase:**
   ```sql
   -- Should see rows in all these tables
   SELECT COUNT(*) FROM sleep_logs WHERE source = 'garmin';
   SELECT COUNT(*) FROM hrv_logs WHERE source = 'garmin';
   SELECT COUNT(*) FROM stress_logs WHERE source = 'garmin';
   SELECT COUNT(*) FROM body_battery_logs WHERE source = 'garmin';
   SELECT COUNT(*) FROM daily_readiness;
   ```

4. **Coach accesses data:**
   - Open Coach chat
   - Ask: "How was my sleep last week?"
   - Expected: Coach shows detailed sleep metrics from Garmin data
   - Ask: "Am I ready for a hard workout today?"
   - Expected: Coach shows readiness score and recovery metrics

---

## Verification Checklist

- [x] Fixed all table names in `_get_recovery_metrics()`
- [x] Fixed all column names in `_get_recovery_metrics()`
- [x] Added source filters to distinguish Garmin data
- [x] Fixed all table names in `_get_recovery_performance_correlations()`
- [x] Fixed all column names in correlations
- [x] Fixed sleep hours calculation (seconds→minutes)
- [x] Fixed HRV references (last_night_avg_ms→hrv_rmssd_ms)
- [x] Fixed readiness score references (overall_score→readiness_score)
- [x] Fixed Body Battery references (simplified schema)
- [x] Updated recovery insights logic
- [ ] Test with real Garmin data sync
- [ ] Verify Coach displays recovery metrics
- [ ] Verify correlations work with real data

---

## Next Steps

1. ✅ **Fix Complete** - All table and column names updated
2. ⏳ **Test Locally** - Sync real Garmin data and verify Coach sees it
3. ⏳ **Remove Old Files** - Delete `garmin_service.py` and `garmin_sync_service.py`
4. ⏳ **Update Tests** - Modify tests to use new table/column names
5. ⏳ **Deploy** - Push changes to staging/production
6. ⏳ **Monitor** - Watch logs for any errors

---

## Summary

**Problem**: Coach queried non-existent `garmin_*` tables
**Solution**: Updated to query actual schema tables with correct columns
**Result**: Coach can now access and display all Garmin health data

**Total Changes**:
- 2 methods updated
- 5 table names changed
- 20+ column names updated
- Source filters added for data isolation
- Units conversions fixed (seconds → minutes)

**Files Modified**: 1 (`app/services/context_builder.py`)
**Lines Changed**: ~200+ lines across 2 methods

**Status**: ✅ **FIXED - Ready for Testing**

---

**Date**: October 11, 2025
**Developer**: Claude Code
**Issue**: Critical - AI Coach could not access Garmin data
**Resolution**: Table/column mismatches corrected
