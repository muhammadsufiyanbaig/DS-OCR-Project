# Frontend Changes Required - Account Application API Update

## Overview
This document outlines the changes needed on the frontend after the backend API updates for the account application system.

---

## 🔴 Breaking Changes

### 1. Card Type Fields Replaced
**OLD (Remove these):**
```javascript
card_type_gold: boolean
card_type_classic: boolean
```

**NEW (Add these):**
```javascript
card_type: "CLASSIC" | "GOLD" | "TITANIUM" | "PLATINUM" | "SIGNATURE" | "INFINITE" | null
card_network: "VISA" | "MASTERCARD" | null
```

### 2. Account Type is Now Required
The `account_type` field is now **required** when creating a new application.

```javascript
account_type: "CURRENT" | "SAVINGS" | "AHU_LAT"  // Required field
```

### 3. Next of Kin - New Flag System
**OLD:** Kin fields were individually optional
**NEW:** Use `has_next_of_kin` flag to control kin section

```javascript
has_next_of_kin: boolean  // If true, kin details are required
```

---

## 🆕 New Enums & Values

### Account Type (Required)
```typescript
enum AccountType {
  CURRENT = "CURRENT",
  SAVINGS = "SAVINGS",
  AHU_LAT = "AHU_LAT"
}
```

### Card Type (Choose ONE)
```typescript
enum CardType {
  CLASSIC = "CLASSIC",
  GOLD = "GOLD",
  TITANIUM = "TITANIUM",
  PLATINUM = "PLATINUM",
  SIGNATURE = "SIGNATURE",
  INFINITE = "INFINITE"
}
```

### Card Network (Choose ONE)
```typescript
enum CardNetwork {
  VISA = "VISA",
  MASTERCARD = "MASTERCARD"
}
```

### Occupation (Expanded Options)
```typescript
enum Occupation {
  SERVICE_GOVT = "SERVICE_GOVT",
  SERVICE_PRIVATE = "SERVICE_PRIVATE",
  BUSINESS = "BUSINESS",
  SELF_EMPLOYED = "SELF_EMPLOYED",
  FARMER = "FARMER",
  HOUSE_WIFE = "HOUSE_WIFE",
  STUDENT = "STUDENT",
  RETIRED = "RETIRED",
  DOCTOR = "DOCTOR",
  ENGINEER = "ENGINEER",
  TEACHER = "TEACHER",
  LAWYER = "LAWYER",
  ACCOUNTANT = "ACCOUNTANT",
  IT_PROFESSIONAL = "IT_PROFESSIONAL",
  BANKER = "BANKER",
  UNEMPLOYED = "UNEMPLOYED",
  OTHER = "OTHER"
}
```

### Marital Status
```typescript
enum MaritalStatus {
  SINGLE = "SINGLE",
  MARRIED = "MARRIED",
  DIVORCED = "DIVORCED",
  WIDOWED = "WIDOWED"
}
```

### Gender
```typescript
enum Gender {
  MALE = "MALE",
  FEMALE = "FEMALE",
  OTHER = "OTHER"
}
```

### Residential Status
```typescript
enum ResidentialStatus {
  HOUSE_OWNED = "HOUSE_OWNED",
  RENTAL = "RENTAL",
  FAMILY = "FAMILY",
  OTHER = "OTHER"
}
```

---

## 📝 Updated Form Fields

### Required Fields
| Field | Type | Description |
|-------|------|-------------|
| `account_type` | enum | CURRENT, SAVINGS, or AHU_LAT |
| `title_of_account` | string | Account title (UPPERCASE) |
| `name` | string | Full name as per CNIC (UPPERCASE) |
| `cnic_no` | string | Format: XXXXX-XXXXXXX-X |

### Card Selection Section (Replace old checkboxes)
```jsx
// OLD UI (Remove)
<Checkbox name="card_type_gold" label="Gold Card" />
<Checkbox name="card_type_classic" label="Classic Card" />

// NEW UI (Add)
<Select name="card_type" label="Card Type">
  <Option value="">No Card</Option>
  <Option value="CLASSIC">Classic</Option>
  <Option value="GOLD">Gold</Option>
  <Option value="TITANIUM">Titanium</Option>
  <Option value="PLATINUM">Platinum</Option>
  <Option value="SIGNATURE">Signature</Option>
  <Option value="INFINITE">Infinite</Option>
</Select>

<RadioGroup name="card_network" label="Card Network">
  <Radio value="VISA">VISA</Radio>
  <Radio value="MASTERCARD">Mastercard</Radio>
</RadioGroup>
```

### Account Type Section (New Required Field)
```jsx
<Select name="account_type" label="Account Type" required>
  <Option value="CURRENT">Current Account</Option>
  <Option value="SAVINGS">Savings Account</Option>
  <Option value="AHU_LAT">Ahu Lat Account</Option>
</Select>
```

### Next of Kin Section (Updated Logic)
```jsx
<Checkbox 
  name="has_next_of_kin" 
  label="Add Next of Kin Information" 
  onChange={(checked) => setShowKinFields(checked)}
/>

{has_next_of_kin && (
  <>
    <Input name="next_of_kin_name" label="Name" required />
    <Input name="next_of_kin_relation" label="Relation (S/O, D/O, W/O)" required />
    <Input name="next_of_kin_cnic" label="CNIC" required />
    <Input name="next_of_kin_relationship" label="Relationship" />
    <Input name="next_of_kin_contact_no" label="Contact Number" />
    <Input name="next_of_kin_address" label="Address" />
    <Input name="next_of_kin_email" label="Email" />
  </>
)}
```

### Occupation Dropdown (Expanded)
```jsx
<Select name="occupation" label="Occupation">
  <Option value="">Select Occupation</Option>
  <Option value="SERVICE_GOVT">Government Service</Option>
  <Option value="SERVICE_PRIVATE">Private Service</Option>
  <Option value="BUSINESS">Business</Option>
  <Option value="SELF_EMPLOYED">Self Employed</Option>
  <Option value="FARMER">Farmer</Option>
  <Option value="HOUSE_WIFE">House Wife</Option>
  <Option value="STUDENT">Student</Option>
  <Option value="RETIRED">Retired</Option>
  <Option value="DOCTOR">Doctor</Option>
  <Option value="ENGINEER">Engineer</Option>
  <Option value="TEACHER">Teacher</Option>
  <Option value="LAWYER">Lawyer</Option>
  <Option value="ACCOUNTANT">Accountant</Option>
  <Option value="IT_PROFESSIONAL">IT Professional</Option>
  <Option value="BANKER">Banker</Option>
  <Option value="UNEMPLOYED">Unemployed</Option>
  <Option value="OTHER">Other</Option>
</Select>
```

---

## 📤 API Request Body Examples

### Minimal Request (Required Fields Only)
```json
{
  "account_type": "SAVINGS",
  "title_of_account": "JOHN DOE",
  "name": "JOHN DOE",
  "cnic_no": "42101-1234567-8",
  "has_next_of_kin": false
}
```

### Full Request (With All Optional Fields)
```json
{
  "account_type": "SAVINGS",
  "title_of_account": "MUHAMMAD ALI",
  "name": "MUHAMMAD ALI",
  "name_on_card": "MUHAMMAD ALI",
  "cnic_no": "42101-1234567-8",
  "fathers_husbands_name": "AHMED ALI",
  "mothers_name": "FATIMA ALI",
  "marital_status": "MARRIED",
  "gender": "MALE",
  "nationality": "PAKISTANI",
  "place_of_birth": "KARACHI",
  "date_of_birth": "01-01-1990",
  "cnic_expiry_date": "01-01-2030",
  "house_no_block_street": "HOUSE 123, BLOCK A, STREET 5",
  "area_location": "GULSHAN-E-IQBAL",
  "city": "KARACHI",
  "postal_code": "75300",
  "occupation": "IT_PROFESSIONAL",
  "occupation_other": null,
  "purpose_of_account": "SALARY",
  "source_of_income": "EMPLOYMENT",
  "expected_monthly_turnover_dr": 100000,
  "expected_monthly_turnover_cr": 150000,
  "residential_status": "HOUSE_OWNED",
  "residential_status_other": null,
  "residing_since": "2015",
  "has_next_of_kin": true,
  "next_of_kin_name": "AHMED ALI",
  "next_of_kin_relation": "S/O",
  "next_of_kin_cnic": "42101-9876543-2",
  "next_of_kin_relationship": "FATHER",
  "next_of_kin_contact_no": "0300-1234567",
  "next_of_kin_address": "SAME AS ABOVE",
  "next_of_kin_email": "ahmed@example.com",
  "internet_banking": true,
  "mobile_banking": true,
  "check_book": true,
  "sms_alerts": true,
  "card_type": "GOLD",
  "card_network": "VISA",
  "zakat_deduction": false
}
```

---

## 📥 API Response Changes

The response now includes:
- `has_next_of_kin` (boolean)
- `card_type` (string or null)
- `card_network` (string or null)
- Removed: `card_type_gold`, `card_type_classic`

---

## ✅ TypeScript Interface

```typescript
interface AccountApplicationCreate {
  // Required
  account_type: 'CURRENT' | 'SAVINGS' | 'AHU_LAT';
  title_of_account: string;
  name: string;
  cnic_no: string;
  
  // Optional Personal Info
  name_on_card?: string;
  fathers_husbands_name?: string;
  mothers_name?: string;
  marital_status?: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED';
  gender?: 'MALE' | 'FEMALE' | 'OTHER';
  nationality?: string;
  place_of_birth?: string;
  date_of_birth?: string;  // Format: DD-MM-YYYY
  cnic_expiry_date?: string;  // Format: DD-MM-YYYY
  
  // Address
  house_no_block_street?: string;
  area_location?: string;
  city?: string;
  postal_code?: string;
  
  // Occupation
  occupation?: 'SERVICE_GOVT' | 'SERVICE_PRIVATE' | 'BUSINESS' | 'SELF_EMPLOYED' | 
               'FARMER' | 'HOUSE_WIFE' | 'STUDENT' | 'RETIRED' | 'DOCTOR' | 
               'ENGINEER' | 'TEACHER' | 'LAWYER' | 'ACCOUNTANT' | 
               'IT_PROFESSIONAL' | 'BANKER' | 'UNEMPLOYED' | 'OTHER';
  occupation_other?: string;
  
  // Financial
  purpose_of_account?: string;
  source_of_income?: string;
  expected_monthly_turnover_dr?: number;
  expected_monthly_turnover_cr?: number;
  
  // Residential
  residential_status?: 'HOUSE_OWNED' | 'RENTAL' | 'FAMILY' | 'OTHER';
  residential_status_other?: string;
  residing_since?: string;
  
  // Next of Kin (Optional Section)
  has_next_of_kin: boolean;
  next_of_kin_name?: string;      // Required if has_next_of_kin = true
  next_of_kin_relation?: string;  // Required if has_next_of_kin = true
  next_of_kin_cnic?: string;      // Required if has_next_of_kin = true
  next_of_kin_relationship?: string;
  next_of_kin_contact_no?: string;
  next_of_kin_address?: string;
  next_of_kin_email?: string;
  
  // Services
  internet_banking: boolean;
  mobile_banking: boolean;
  check_book: boolean;
  sms_alerts: boolean;
  
  // Card Selection (Single Choice)
  card_type?: 'CLASSIC' | 'GOLD' | 'TITANIUM' | 'PLATINUM' | 'SIGNATURE' | 'INFINITE';
  card_network?: 'VISA' | 'MASTERCARD';
  
  // Zakat
  zakat_deduction: boolean;
}
```

---

## 🔄 Migration Checklist

- [ ] Remove `card_type_gold` and `card_type_classic` checkboxes
- [ ] Add `card_type` dropdown (single selection)
- [ ] Add `card_network` radio buttons (VISA/Mastercard)
- [ ] Add `account_type` dropdown (required field)
- [ ] Add `has_next_of_kin` checkbox to toggle kin section
- [ ] Update occupation dropdown with new options
- [ ] Update form validation for required fields
- [ ] Update TypeScript interfaces/types
- [ ] Test form submission with new payload structure
- [ ] Update any display components showing card type info

---

## 📞 API Endpoints (No Changes)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/account-applications` | Create new application |
| GET | `/account-applications` | Get all applications |
| GET | `/account-applications/{id}` | Get by ID |
| PUT | `/account-applications/{id}` | Update application |
| DELETE | `/account-applications/{id}` | Delete application |
| GET | `/account-applications/count` | Get total count |
| GET | `/account-applications/paginated?skip=0&limit=10` | Paginated list |
| GET | `/account-applications/search/cnic/{cnic}` | Search by CNIC |
| GET | `/account-applications/search/account-type/{type}` | Search by account type |
| GET | `/account-applications/search/city/{city}` | Search by city |
| GET | `/account-applications/search/account-number/{account_no}` | Search by account number |
| GET | `/account-applications/search/iban/{iban}` | Search by IBAN |

---

## ⚠️ Validation Rules (Unchanged)

1. **UPPERCASE**: All text fields must be in BLOCK LETTERS
2. **CNIC Format**: `XXXXX-XXXXXXX-X` (with dashes)
3. **Date Format**: `DD-MM-YYYY`
4. **Name Consistency**: `title_of_account`, `name`, and `name_on_card` must be identical
5. **Kin Required Fields**: When `has_next_of_kin = true`, these are required:
   - `next_of_kin_name`
   - `next_of_kin_relation`
   - `next_of_kin_cnic`
