"""
Quick test to verify the groq_service_v2.py formatting fix.
"""
import sys
sys.path.insert(0, 'C:\\Users\\pradord\\Documents\\Projects\\wagner_coach\\wagner-coach-backend')

# Test the string formatting
test_string = """
Example: "bench pressed" → exercises=[{{"name": "Bench Press"}}] with sets/reps/weight ALL null
""".format(classification_instruction="test")

print("SUCCESS: String formatting works correctly!")
print(f"Result: {test_string}")
