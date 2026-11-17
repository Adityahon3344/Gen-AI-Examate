from app.tools import check_scheme_eligibility


# Test 1: All demonstration rules pass
result1 = check_scheme_eligibility(
    land_holding="7/12 holder",
    land_size_acres=2.0,
    caste_category="OBC",
    received_same_component_last_10_years=False,
    already_has_tractor=False
)

print("\nTEST 1 - Eligible Farmer")
print(result1)


# Test 2: Multiple demonstration rules fail
result2 = check_scheme_eligibility(
    land_holding="Not registered",
    land_size_acres=0.2,
    caste_category="OPEN",
    received_same_component_last_10_years=True,
    already_has_tractor=True
)

print("\nTEST 2 - Not Eligible Farmer")
print(result2)
