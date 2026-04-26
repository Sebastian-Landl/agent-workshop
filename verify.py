from datetime import datetime
import math

now = datetime.now()
# now = datetime(2025, 12, 19, 0, 26, 25, 560333)
print(f"Current datetime: {now}")

print("\nEquation with placeholders:")
print(
    "(sin(<current_month>) + 17890047.323211) * (86608.432254 + <current_hour>) / <current_year> + <current_day> * 998877.11223344"
)

print("\nEquation with values:")
print(
    f"(sin({now.month}) + 17890047.323211) * (86608.432254 + {now.hour}) / {now.year} + {now.day} * 998877.11223344"
)

# (sin(<current_month>)+17890047.323211)*(86608.432254+<current_hour>)/<current_year>+<current_day>*998877.11223344
result = (math.sin(now.month) + 17890047.323211) * (
    86608.432254 + now.hour
) / now.year + now.day * 998877.11223344
print(f"Correct result: {result}")

print("\nStep-by-step calculation:")
step1 = math.sin(now.month)
print(f"Step 1: sin({now.month}) = {step1}")

step2 = step1 + 17890047.323211
print(f"Step 2: {step1} + 17890047.323211 = {step2}")

step3 = 86608.432254 + now.hour
print(f"Step 3: 86608.432254 + {now.hour} = {step3}")

step4 = step2 * step3
print(f"Step 4: {step2} * {step3} = {step4}")

step5 = step4 / now.year
print(f"Step 5: {step4} / {now.year} = {step5}")

step6 = now.day * 998877.11223344
print(f"Step 6: {now.day} * 998877.11223344 = {step6}")

step7 = step5 + step6
print(f"Step 7: {step5} + {step6} = {step7}")

print(f"\nFinal result: {step7}")
