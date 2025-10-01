# Feature Design: Summarization Service

## Overview
The Summarization Service generates automated summaries of user fitness data at various time intervals (daily, weekly, monthly, quarterly). It aggregates workout data, nutrition logs, and progress metrics to provide users with actionable insights.

## Purpose
- Generate comprehensive activity summaries
- Aggregate user data across multiple dimensions
- Support multiple time periods (weekly, monthly, quarterly)
- Enable trend analysis and progress tracking
- Provide data for AI coaching context
- Run as scheduled background job

## Requirements

### Functional Requirements
1. **Weekly Summaries**: Generate every day for past 7 days
2. **Monthly Summaries**: Generate on 1st of month for previous month
3. **Quarterly Summaries**: Generate on first day of quarter
4. **Data Aggregation**: Combine workouts, nutrition, activities, weight
5. **Batch Processing**: Process all users efficiently
6. **Idempotency**: Safe to run multiple times
7. **Error Handling**: Continue processing on individual user errors

### Non-Functional Requirements
1. **Performance**: Process 1000 users in < 5 minutes
2. **Reliability**: Graceful error handling, retry failed users
3. **Observability**: Log progress and errors
4. **Scalability**: Support growing user base
5. **Data Quality**: Accurate calculations and aggregations

## Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────┐
│          Cron Job Trigger (Daily)                   │
│          /api/v1/background/summarize               │
└────────────────────┬────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────┐
│         SummarizationService                        │
│  ┌──────────────────────────────────────────────┐  │
│  │  generate_all_summaries()                    │  │
│  │    ├─ Get all users from profiles            │  │
│  │    ├─ For each user:                         │  │
│  │    │   └─ generate_user_summaries()          │  │
│  │    └─ Return aggregate results               │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  generate_user_summaries(user_id)            │  │
│  │    ├─ Check if summaries needed              │  │
│  │    ├─ Generate weekly (always)               │  │
│  │    ├─ Generate monthly (if 1st of month)     │  │
│  │    └─ Generate quarterly (if 1st of quarter) │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  generate_weekly_summary(user_id)            │  │
│  │    ├─ Fetch last 7 days data                 │  │
│  │    ├─ Aggregate workouts                     │  │
│  │    ├─ Aggregate nutrition                    │  │
│  │    ├─ Calculate metrics                      │  │
│  │    └─ Save to summaries table                │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────┐
│         Supabase: summaries table                   │
│  - id, user_id, period_type, period_start           │
│  - period_end, data (JSONB), created_at             │
└─────────────────────────────────────────────────────┘
```

## Interface Definition

### SummarizationService Class

```python
class SummarizationService:
    """
    Service for generating user activity summaries.

    Generates weekly, monthly, and quarterly summaries by aggregating
    user workout, nutrition, and activity data.
    """

    def __init__(self):
        """Initialize with Supabase client."""
        self.supabase = get_service_client()

    async def generate_all_summaries(self) -> Dict[str, Any]:
        """
        Generate summaries for all users.

        Returns:
            Dict with results: {processed, errors, summaries_created}
        """

    async def generate_user_summaries(self, user_id: str) -> int:
        """
        Generate all applicable summaries for a user.

        Args:
            user_id: User UUID

        Returns:
            int: Number of summaries created

        Raises:
            ValueError: If user_id is invalid
        """

    async def generate_weekly_summary(
        self,
        user_id: str,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Generate weekly summary (last 7 days).

        Args:
            user_id: User UUID
            end_date: End date for summary (default: today)

        Returns:
            Summary data dictionary
        """

    async def generate_monthly_summary(
        self,
        user_id: str,
        month: Optional[int] = None,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate monthly summary.

        Args:
            user_id: User UUID
            month: Month (1-12, default: previous month)
            year: Year (default: current year or previous if month=12)

        Returns:
            Summary data dictionary
        """

    async def generate_quarterly_summary(
        self,
        user_id: str,
        quarter: Optional[int] = None,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate quarterly summary.

        Args:
            user_id: User UUID
            quarter: Quarter (1-4, default: previous quarter)
            year: Year (default: current year or previous)

        Returns:
            Summary data dictionary
        """

    def _is_first_day_of_month(self, date: date) -> bool:
        """Check if date is first day of month."""

    def _is_first_day_of_quarter(self, date: date) -> bool:
        """Check if date is first day of quarter."""

    def _get_quarter(self, date: date) -> int:
        """Get quarter (1-4) for a date."""
```

## Data Models

### Summary Data Structure

```python
class SummaryPeriodType(str, Enum):
    """Summary period types."""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"

class WorkoutStats(BaseModel):
    """Workout statistics."""
    total_workouts: int
    total_duration_minutes: int
    total_calories: int
    workout_types: Dict[str, int]  # type -> count
    avg_duration_minutes: float

class NutritionStats(BaseModel):
    """Nutrition statistics."""
    total_meals_logged: int
    avg_calories_per_day: float
    avg_protein_g_per_day: float
    avg_carbs_g_per_day: float
    avg_fat_g_per_day: float
    days_logged: int

class ActivityStats(BaseModel):
    """Activity statistics (Strava, Garmin)."""
    total_activities: int
    total_distance_miles: float
    total_elevation_feet: float
    activity_types: Dict[str, int]  # type -> count

class SummaryData(BaseModel):
    """Complete summary data."""
    period_type: SummaryPeriodType
    period_start: date
    period_end: date
    workouts: WorkoutStats
    nutrition: NutritionStats
    activities: ActivityStats
    weight_change_lbs: Optional[float] = None
    notes: List[str] = []
```

### Database Schema

```sql
-- Summaries table
CREATE TABLE summaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id),
    period_type TEXT NOT NULL CHECK (period_type IN ('weekly', 'monthly', 'quarterly')),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, period_type, period_start)
);

-- Indexes
CREATE INDEX idx_summaries_user_id ON summaries(user_id);
CREATE INDEX idx_summaries_period ON summaries(user_id, period_type, period_start DESC);
```

## Usage Examples

### Cron Job Endpoint

```python
from fastapi import APIRouter, Depends
from app.api.middleware.auth import verify_cron_secret
from app.services.summarization_service import SummarizationService

router = APIRouter()

@router.post("/background/summarize")
async def run_summarization(_: None = Depends(verify_cron_secret)):
    """Run daily summarization for all users."""
    service = SummarizationService()
    result = await service.generate_all_summaries()

    return {
        "success": True,
        "message": "Summarization complete",
        "results": result,
        "timestamp": datetime.now().isoformat()
    }
```

### Manual Summary Generation

```python
from app.services.summarization_service import SummarizationService

# Generate for specific user
service = SummarizationService()
summaries_created = await service.generate_user_summaries("user-uuid")

# Generate specific period
weekly_summary = await service.generate_weekly_summary("user-uuid")
monthly_summary = await service.generate_monthly_summary("user-uuid")
```

### Fetching Summaries

```python
# Get user's recent summaries
summaries = supabase.table("summaries")\
    .select("*")\
    .eq("user_id", user_id)\
    .order("period_start", desc=True)\
    .limit(10)\
    .execute()
```

## Data Aggregation Logic

### Weekly Summary

```python
# Date range: last 7 days (including today)
end_date = datetime.now().date()
start_date = end_date - timedelta(days=6)

# Fetch workouts
workouts = supabase.table("workouts")\
    .select("*")\
    .eq("user_id", user_id)\
    .gte("date", start_date)\
    .lte("date", end_date)\
    .execute()

# Calculate stats
total_workouts = len(workouts.data)
total_duration = sum(w["duration_minutes"] for w in workouts.data)
workout_types = Counter(w["type"] for w in workouts.data)

# Similar for nutrition, activities, weight
```

### Monthly Summary

```python
# Date range: entire previous month
today = datetime.now().date()
if today.day == 1:
    # First day of month - summarize previous month
    last_month = today.replace(day=1) - timedelta(days=1)
    start_date = last_month.replace(day=1)
    end_date = last_month
else:
    # Not first day - no monthly summary generated
    return None
```

### Quarterly Summary

```python
# Date range: previous quarter
quarters = {
    1: (1, 3),   # Q1: Jan-Mar
    2: (4, 6),   # Q2: Apr-Jun
    3: (7, 9),   # Q3: Jul-Sep
    4: (10, 12)  # Q4: Oct-Dec
}

current_quarter = (datetime.now().month - 1) // 3 + 1
if _is_first_day_of_quarter(datetime.now().date()):
    # Generate previous quarter summary
    prev_quarter = current_quarter - 1 if current_quarter > 1 else 4
    # Calculate start/end dates
```

## Error Handling

### Individual User Errors

```python
async def generate_all_summaries(self):
    results = {"processed": 0, "errors": 0, "summaries_created": 0}

    users = self.supabase.table("profiles").select("id").execute()

    for user in users.data:
        try:
            count = await self.generate_user_summaries(user["id"])
            results["processed"] += 1
            results["summaries_created"] += count
        except Exception as e:
            logger.error(f"Error processing user {user['id']}: {e}")
            results["errors"] += 1
            # Continue with next user

    return results
```

### Database Errors

```python
try:
    self.supabase.table("summaries").insert(summary_data).execute()
except Exception as e:
    if "duplicate key" in str(e).lower():
        # Summary already exists - update instead
        self.supabase.table("summaries")\
            .update(summary_data)\
            .eq("user_id", user_id)\
            .eq("period_type", period_type)\
            .eq("period_start", start_date)\
            .execute()
    else:
        raise
```

## Performance Considerations

### Batch Processing

```python
# Process users in batches to avoid memory issues
BATCH_SIZE = 100

users = self.supabase.table("profiles").select("id").execute()
user_ids = [u["id"] for u in users.data]

for i in range(0, len(user_ids), BATCH_SIZE):
    batch = user_ids[i:i + BATCH_SIZE]
    for user_id in batch:
        await self.generate_user_summaries(user_id)
```

### Query Optimization

```python
# Fetch all data for a user in single queries
# Instead of: multiple queries per workout/meal
workouts = supabase.table("workouts")\
    .select("*")\
    .eq("user_id", user_id)\
    .gte("date", start_date)\
    .lte("date", end_date)\
    .execute()

meals = supabase.table("meals")\
    .select("*")\
    .eq("user_id", user_id)\
    .gte("date", start_date)\
    .lte("date", end_date)\
    .execute()

# Process in memory
```

### Caching

```python
# Cache user data that doesn't change
@lru_cache(maxsize=1000)
def _get_user_profile(user_id: str) -> Dict:
    return self.supabase.table("profiles")\
        .select("*")\
        .eq("id", user_id)\
        .single()\
        .execute()
```

## Testing Strategy

### Unit Tests
1. Test weekly summary generation
2. Test monthly summary generation
3. Test quarterly summary generation
4. Test batch processing (all users)
5. Test date range calculations
6. Test data aggregation logic
7. Test error handling
8. Test idempotency (duplicate summaries)

### Integration Tests
1. Test with real database (test environment)
2. Test full cron job flow
3. Test with missing data
4. Test with large datasets

### Edge Cases
1. User with no data
2. User with only one workout
3. Month/quarter transitions
4. Leap years
5. Duplicate summary prevention

## Security Considerations

1. **Service Role Only**: Use service client (bypasses RLS)
2. **Cron Secret**: Require authentication for endpoint
3. **Data Validation**: Validate all user data before aggregation
4. **Error Logging**: Don't log sensitive user data

## Success Criteria

✅ Weekly summaries generated daily
✅ Monthly summaries on 1st of month
✅ Quarterly summaries on quarter start
✅ All users processed efficiently
✅ Errors don't stop batch processing
✅ Duplicate summaries handled
✅ 80%+ test coverage
✅ < 5 minutes for 1000 users

## Dependencies

- `app.services.supabase_service`: Database access
- `datetime`, `timedelta`: Date calculations
- `collections.Counter`: Data aggregation
- `typing`: Type hints

## Future Enhancements

1. **Async Processing**: Use Celery for parallel processing
2. **Custom Date Ranges**: Allow manual date range specification
3. **Comparison Data**: Compare to previous periods
4. **Goal Progress**: Track progress toward user goals
5. **AI Insights**: Generate AI-powered insights
6. **Email Summaries**: Send summaries to users
7. **Export**: Export summaries to PDF/CSV

## References

- [PYTHON_BACKEND_MIGRATION_PLAN.md](../../PYTHON_BACKEND_MIGRATION_PLAN.md): Original design
- [Supabase RPC Functions](https://supabase.com/docs/guides/database/functions): For complex queries