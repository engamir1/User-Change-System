# Social Housing Exchange System - نظام تبادل الإسكان الاجتماعي ✅

## Current Goal
Build a smart matching system for citizens to exchange apartments based on floor and direction preferences.

---

## Phase 1: Database + Citizen Registration Form ✅
- [x] Create citizen data model with all required fields (national_id, name, building, floor, direction, phone, wish_floor, wish_direction)
- [x] Build registration form page for submitting exchange requests
- [x] Add form validation (required fields, number validation)
- [x] Add dropdown/select fields for wish_floor (أعلى/أسفل/أى) and wish_direction (بحرى/قبلى/شرقى/غربى/أى)
- [x] Display success message after registration

---

## Phase 2: Smart Matching Algorithm ✅
- [x] Implement match_requests() function with scoring logic
- [x] Check floor compatibility (أعلى/أسفل/أى)
- [x] Check direction compatibility (بحرى/قبلى/أى)
- [x] Implement reverse matching check (both sides must want compatible floors)
- [x] Calculate match score based on floor proximity and direction match
- [x] Sort results by highest score first

---

## Phase 3: Match Results Display Page ✅
- [x] Create search page with citizen selector dropdown and "ابحث عن شريك تبديل" button
- [x] Display matched citizens sorted by compatibility percentage
- [x] Show citizen details: name, floor, direction, contact info
- [x] Display match percentage/score for each result
- [x] Add styling for match results cards with color-coded scores

---

## Notes
- Using Arabic text throughout the interface
- Floor options: أعلى (higher), أسفل (lower), أى (any)
- Direction options: بحرى (north), قبلى (south), شرقى (east), غربى (west), أى (any)
- Matching is bidirectional - both parties must want compatible exchanges
- Tested with multiple scenarios - all working correctly!
- Avatar images generated using Dicebear API based on citizen names
- Color-coded scores: Green (>80%), Yellow (>60%), Red (otherwise)
