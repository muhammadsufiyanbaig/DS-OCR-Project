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

## 📊 NEW: Analytics API Endpoints

### Dashboard Summary
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/dashboard` | Get comprehensive dashboard with all key metrics |

### Basic Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/account-types` | Breakdown by account type (CURRENT, SAVINGS, AHU_LAT) |
| GET | `/analytics/cities` | Breakdown by city |
| GET | `/analytics/gender` | Breakdown by gender (MALE, FEMALE, OTHER) |
| GET | `/analytics/occupation` | Breakdown by occupation |
| GET | `/analytics/card-types` | Breakdown by card type (CLASSIC, GOLD, etc.) |
| GET | `/analytics/card-networks` | Breakdown by card network (VISA, MASTERCARD) |
| GET | `/analytics/marital-status` | Breakdown by marital status |
| GET | `/analytics/residential-status` | Breakdown by residential status |
| GET | `/analytics/services` | Services adoption stats |
| GET | `/analytics/next-of-kin` | With/without kin information stats |

### 🚀 Advanced Analytics (NEW!)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/executive-summary` | Executive report with key metrics, health indicators & recommendations |
| GET | `/analytics/financial-insights` | Financial analysis: avg/min/max turnovers, net cash flow |
| GET | `/analytics/cross-analysis/gender-account` | Cross-tabulation: Gender vs Account Type preferences |
| GET | `/analytics/cross-analysis/occupation-card` | Cross-tabulation: Occupation vs Card Type with premium adoption |
| GET | `/analytics/city-performance` | City rankings by volume, value, and average customer worth |
| GET | `/analytics/occupation-income` | Income patterns by occupation with tier classification |
| GET | `/analytics/premium-customers` | Demographics of PLATINUM/SIGNATURE/INFINITE card holders |
| GET | `/analytics/digital-banking` | Digital adoption analysis with maturity scoring |
| GET | `/analytics/high-value-customers?threshold=500000` | High-value customer analysis (configurable threshold) |
| GET | `/analytics/profile-completeness` | Data quality analysis with field completion rates |
| GET | `/analytics/customer-segments` | Behavioral segmentation with targeted recommendations |

---

## 📈 Analytics Response Examples

### Dashboard Summary Response
**GET** `/analytics/dashboard`
```json
{
  "total_applications": 150,
  "account_types": {
    "SAVINGS": 80,
    "CURRENT": 50,
    "AHU_LAT": 20
  },
  "gender_distribution": {
    "MALE": 90,
    "FEMALE": 55,
    "OTHER": 5
  },
  "card_types": {
    "GOLD": 45,
    "CLASSIC": 40,
    "PLATINUM": 30,
    "TITANIUM": 20,
    "NO_CARD": 15
  },
  "card_networks": {
    "VISA": 80,
    "MASTERCARD": 55,
    "NO_CARD": 15
  },
  "top_cities": {
    "KARACHI": 50,
    "LAHORE": 35,
    "ISLAMABAD": 25,
    "RAWALPINDI": 15,
    "FAISALABAD": 10
  },
  "services_adoption": {
    "internet_banking": 120,
    "mobile_banking": 110,
    "check_book": 90,
    "sms_alerts": 130,
    "zakat_deduction": 45
  },
  "kin_stats": {
    "with_next_of_kin": 100,
    "without_next_of_kin": 50
  }
}
```

### Individual Analytics Response
**GET** `/analytics/account-types`
```json
{
  "total": 150,
  "breakdown": {
    "SAVINGS": 80,
    "CURRENT": 50,
    "AHU_LAT": 20
  },
  "percentages": {
    "SAVINGS": 53.33,
    "CURRENT": 33.33,
    "AHU_LAT": 13.33
  }
}
```

### Services Analytics Response
**GET** `/analytics/services`
```json
{
  "total_applications": 150,
  "services": {
    "internet_banking": 120,
    "mobile_banking": 110,
    "check_book": 90,
    "sms_alerts": 130,
    "zakat_deduction": 45
  },
  "percentages": {
    "internet_banking": 80.0,
    "mobile_banking": 73.33,
    "check_book": 60.0,
    "sms_alerts": 86.67,
    "zakat_deduction": 30.0
  }
}
```

---

## 🚀 Advanced Analytics Response Examples

### Executive Summary (For Decision Makers)
**GET** `/analytics/executive-summary`
```json
{
  "key_metrics": {
    "total_customers": 150,
    "total_expected_monthly_deposits": 45000000,
    "average_customer_value": 300000,
    "digital_adoption_rate": 65.5,
    "service_engagement_score": 72.3,
    "profile_completeness": 78.5
  },
  "health_indicators": {
    "digital_maturity": "HIGH",
    "data_quality": "HIGH",
    "customer_engagement": "HIGH"
  },
  "top_insights": [
    "Digital banking adoption is at 65.5%",
    "Average customer expects Rs. 300,000 monthly credit",
    "Top customer segment: premium_digital_natives",
    "Profile completeness average: 78.5%"
  ],
  "recommendations": [
    "Focus on converting non-digital users to mobile banking",
    "Target high-value customers for premium card upgrades",
    "Improve profile completeness through incentivized data collection"
  ]
}
```

### Financial Insights
**GET** `/analytics/financial-insights`
```json
{
  "summary": {
    "debit_turnover": {
      "average": 150000,
      "minimum": 10000,
      "maximum": 1000000,
      "total": 22500000
    },
    "credit_turnover": {
      "average": 250000,
      "minimum": 20000,
      "maximum": 2000000,
      "total": 37500000
    }
  },
  "insights": {
    "average_net_monthly_flow": 100000,
    "flow_direction": "POSITIVE",
    "total_expected_monthly_deposits": 37500000,
    "total_expected_monthly_withdrawals": 22500000,
    "highest_single_deposit_expectation": 2000000,
    "total_applications_analyzed": 150
  }
}
```

### Cross-Analysis: Occupation vs Card Type
**GET** `/analytics/cross-analysis/occupation-card`
```json
{
  "cross_tabulation": {
    "IT_PROFESSIONAL": {"GOLD": 15, "PLATINUM": 10, "CLASSIC": 5},
    "DOCTOR": {"PLATINUM": 12, "SIGNATURE": 8, "GOLD": 5},
    "BUSINESS": {"INFINITE": 5, "PLATINUM": 8, "GOLD": 7}
  },
  "premium_card_adoption_by_occupation": {
    "DOCTOR": {
      "total_customers": 25,
      "premium_card_holders": 20,
      "premium_adoption_rate": 80.0
    },
    "BUSINESS": {
      "total_customers": 20,
      "premium_card_holders": 13,
      "premium_adoption_rate": 65.0
    }
  },
  "top_premium_adopters": ["DOCTOR", "BUSINESS", "LAWYER", "IT_PROFESSIONAL", "BANKER"]
}
```

### City Performance Analysis
**GET** `/analytics/city-performance`
```json
{
  "city_performance": [
    {
      "city": "KARACHI",
      "total_applications": 50,
      "avg_monthly_credit": 350000,
      "total_monthly_credit": 17500000
    },
    {
      "city": "LAHORE",
      "total_applications": 35,
      "avg_monthly_credit": 280000,
      "total_monthly_credit": 9800000
    }
  ],
  "rankings": {
    "by_application_volume": ["KARACHI", "LAHORE", "ISLAMABAD"],
    "by_total_credit_value": ["KARACHI", "LAHORE", "ISLAMABAD"],
    "by_average_customer_value": ["ISLAMABAD", "KARACHI", "LAHORE"]
  },
  "insights": {
    "highest_volume_city": "KARACHI",
    "highest_value_city": "KARACHI",
    "highest_avg_customer_value_city": "ISLAMABAD",
    "total_cities": 12
  }
}
```

### Customer Segmentation
**GET** `/analytics/customer-segments`
```json
{
  "segmentation_data": {
    "total_customers": 150,
    "segments": {
      "premium_digital_natives": {"count": 25, "percentage": 16.67},
      "high_value_traditional": {"count": 10, "percentage": 6.67},
      "young_professionals": {"count": 45, "percentage": 30.0},
      "business_owners": {"count": 20, "percentage": 13.33},
      "value_seekers": {"count": 30, "percentage": 20.0},
      "fully_engaged": {"count": 35, "percentage": 23.33}
    }
  },
  "insights": {
    "largest_segment": "young_professionals",
    "smallest_segment": "high_value_traditional",
    "growth_opportunity": "high_value_traditional"
  },
  "segment_recommendations": {
    "premium_digital_natives": "Offer exclusive digital-first experiences and premium rewards",
    "high_value_traditional": "Focus on relationship banking and personalized in-branch services",
    "young_professionals": "Promote career-linked products and financial planning tools",
    "business_owners": "Cross-sell business banking products and merchant services",
    "value_seekers": "Educate on digital benefits and offer upgrade incentives",
    "fully_engaged": "Maintain loyalty with rewards and referral programs"
  }
}
```

### High-Value Customer Analysis
**GET** `/analytics/high-value-customers?threshold=500000`
```json
{
  "high_value_analysis": {
    "threshold": 500000,
    "total_high_value_customers": 25,
    "percentage_of_total": 16.67,
    "preferred_card_types": {"PLATINUM": 10, "SIGNATURE": 8, "INFINITE": 5, "GOLD": 2},
    "top_occupations": {"BUSINESS": 8, "DOCTOR": 6, "LAWYER": 5, "IT_PROFESSIONAL": 4, "BANKER": 2},
    "top_cities": {"KARACHI": 10, "ISLAMABAD": 7, "LAHORE": 5},
    "account_type_preference": {"CURRENT": 15, "SAVINGS": 10}
  },
  "insights": {
    "total_high_value": 25,
    "market_concentration": "16.67% of customers are high-value",
    "recommended_focus_city": "KARACHI",
    "recommended_target_occupation": "BUSINESS",
    "preferred_products": {
      "card_type": "PLATINUM",
      "account_type": "CURRENT"
    }
  }
}
```

### Digital Banking Adoption
**GET** `/analytics/digital-banking`
```json
{
  "adoption_data": {
    "total_customers": 150,
    "full_digital_customers": 95,
    "internet_only": 15,
    "mobile_only": 10,
    "no_digital": 30,
    "digital_adoption_rate": 63.33,
    "any_digital_rate": 80.0,
    "digital_by_account_type": {"SAVINGS": 70, "CURRENT": 45, "AHU_LAT": 5}
  },
  "insights": {
    "digital_maturity_score": 63.33,
    "digital_maturity_level": "GROWING",
    "non_digital_opportunity": 30,
    "recommendation": "Focus on converting internet-only users to full digital"
  }
}
```

### Profile Completeness Analysis
**GET** `/analytics/profile-completeness`
```json
{
  "completeness_data": {
    "total_applications": 150,
    "average_completeness_percentage": 72.5,
    "fully_complete_profiles": 25,
    "above_80_percent": 65,
    "below_50_percent": 15,
    "field_completion_rates": {
      "fathers_husbands_name": 85.5,
      "mothers_name": 45.2,
      "date_of_birth": 92.3,
      "nationality": 88.7,
      "place_of_birth": 78.4,
      "address_complete": 82.1,
      "occupation": 95.6,
      "financial_info": 68.9,
      "residential_status": 72.3,
      "next_of_kin": 55.4,
      "card_selected": 78.9
    }
  },
  "insights": {
    "overall_health": "GOOD",
    "weakest_fields": ["mothers_name", "next_of_kin", "financial_info"],
    "strongest_fields": ["occupation", "date_of_birth", "nationality"],
    "improvement_priority": "mothers_name",
    "fully_complete_rate": 16.67
  }
}
```

---

## 🎨 Frontend Dashboard Implementation Ideas

### Summary Cards
```jsx
// Example: Display key metrics as cards
<div className="dashboard-cards">
  <Card title="Total Applications" value={data.total_applications} />
  <Card title="Savings Accounts" value={data.account_types.SAVINGS} />
  <Card title="Current Accounts" value={data.account_types.CURRENT} />
  <Card title="Active Cards" value={totalCards} />
</div>
```

### Charts Integration
```jsx
// Pie Chart for Account Types
<PieChart data={[
  { name: 'Savings', value: data.account_types.SAVINGS },
  { name: 'Current', value: data.account_types.CURRENT },
  { name: 'Ahu Lat', value: data.account_types.AHU_LAT }
]} />

// Bar Chart for Top Cities
<BarChart data={Object.entries(data.top_cities).map(([city, count]) => ({
  city,
  count
}))} />

// Doughnut Chart for Card Networks
<DoughnutChart data={[
  { name: 'VISA', value: data.card_networks.VISA },
  { name: 'Mastercard', value: data.card_networks.MASTERCARD }
]} />
```

### Services Adoption Progress Bars
```jsx
<div className="services-stats">
  <ProgressBar 
    label="Internet Banking" 
    value={data.percentages.internet_banking} 
  />
  <ProgressBar 
    label="Mobile Banking" 
    value={data.percentages.mobile_banking} 
  />
  <ProgressBar 
    label="SMS Alerts" 
    value={data.percentages.sms_alerts} 
  />
  <ProgressBar 
    label="Check Book" 
    value={data.percentages.check_book} 
  />
</div>
```

---

## 📱 TypeScript Interfaces for Analytics

```typescript
// Basic Analytics
interface AnalyticsBreakdown {
  total: number;
  breakdown: Record<string, number>;
  percentages: Record<string, number>;
}

interface ServicesAnalytics {
  total_applications: number;
  services: {
    internet_banking: number;
    mobile_banking: number;
    check_book: number;
    sms_alerts: number;
    zakat_deduction: number;
  };
  percentages: Record<string, number>;
}

interface DashboardSummary {
  total_applications: number;
  account_types: Record<string, number>;
  gender_distribution: Record<string, number>;
  card_types: Record<string, number>;
  card_networks: Record<string, number>;
  top_cities: Record<string, number>;
  services_adoption: ServicesAnalytics['services'];
  kin_stats: {
    with_next_of_kin: number;
    without_next_of_kin: number;
  };
}

// Advanced Analytics Interfaces
interface ExecutiveSummary {
  key_metrics: {
    total_customers: number;
    total_expected_monthly_deposits: number;
    average_customer_value: number;
    digital_adoption_rate: number;
    service_engagement_score: number;
    profile_completeness: number;
  };
  health_indicators: {
    digital_maturity: 'HIGH' | 'MEDIUM' | 'LOW';
    data_quality: 'HIGH' | 'MEDIUM' | 'LOW';
    customer_engagement: 'HIGH' | 'MEDIUM' | 'LOW';
  };
  top_insights: string[];
  recommendations: string[];
}

interface FinancialInsights {
  summary: {
    debit_turnover: {
      average: number;
      minimum: number;
      maximum: number;
      total: number;
    };
    credit_turnover: {
      average: number;
      minimum: number;
      maximum: number;
      total: number;
    };
  };
  insights: {
    average_net_monthly_flow: number;
    flow_direction: 'POSITIVE' | 'NEGATIVE';
    total_expected_monthly_deposits: number;
    total_expected_monthly_withdrawals: number;
    highest_single_deposit_expectation: number;
    total_applications_analyzed: number;
  };
}

interface CityPerformance {
  city_performance: Array<{
    city: string;
    total_applications: number;
    avg_monthly_credit: number;
    total_monthly_credit: number;
  }>;
  rankings: {
    by_application_volume: string[];
    by_total_credit_value: string[];
    by_average_customer_value: string[];
  };
  insights: {
    highest_volume_city: string | null;
    highest_value_city: string | null;
    highest_avg_customer_value_city: string | null;
    total_cities: number;
  };
}

interface CustomerSegmentation {
  segmentation_data: {
    total_customers: number;
    segments: Record<string, {
      count: number;
      percentage: number;
    }>;
  };
  insights: {
    largest_segment: string | null;
    smallest_segment: string | null;
    growth_opportunity: string | null;
  };
  segment_recommendations: Record<string, string>;
}

interface HighValueCustomerAnalysis {
  high_value_analysis: {
    threshold: number;
    total_high_value_customers: number;
    percentage_of_total: number;
    preferred_card_types: Record<string, number>;
    top_occupations: Record<string, number>;
    top_cities: Record<string, number>;
    account_type_preference: Record<string, number>;
  };
  insights: {
    total_high_value: number;
    market_concentration: string;
    recommended_focus_city: string | null;
    recommended_target_occupation: string | null;
    preferred_products: {
      card_type: string | null;
      account_type: string | null;
    };
  };
}

interface DigitalBankingInsights {
  adoption_data: {
    total_customers: number;
    full_digital_customers: number;
    internet_only: number;
    mobile_only: number;
    no_digital: number;
    digital_adoption_rate: number;
    any_digital_rate: number;
    digital_by_account_type: Record<string, number>;
  };
  insights: {
    digital_maturity_score: number;
    digital_maturity_level: 'ADVANCED' | 'GROWING' | 'DEVELOPING';
    non_digital_opportunity: number;
    recommendation: string;
  };
}

interface ProfileCompletenessAnalysis {
  completeness_data: {
    total_applications: number;
    average_completeness_percentage: number;
    fully_complete_profiles: number;
    above_80_percent: number;
    below_50_percent: number;
    field_completion_rates: Record<string, number>;
  };
  insights: {
    overall_health: 'GOOD' | 'MODERATE' | 'NEEDS_IMPROVEMENT';
    weakest_fields: string[];
    strongest_fields: string[];
    improvement_priority: string | null;
    fully_complete_rate: number;
  };
}

interface CrossAnalysisOccupationCard {
  cross_tabulation: Record<string, Record<string, number>>;
  premium_card_adoption_by_occupation: Record<string, {
    total_customers: number;
    premium_card_holders: number;
    premium_adoption_rate: number;
  }>;
  top_premium_adopters: string[];
}
```

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
