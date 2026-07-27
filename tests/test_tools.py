from app.tools import *

print("\nOverall Persistency")
print(overall_persistency())

print("\nSWP Product")
print(product_persistency("SWP"))

print("\nSWAG Product")
print(product_persistency("SWAG"))

print("\nSavings LOB")
print(lob_persistency("SAVINGS"))

print("\nProtection LOB")
print(lob_persistency("PROTECTION"))

print("\nDuration 1")
print(duration_persistency(1))

print("\nDuration 2")
print(duration_persistency(2))