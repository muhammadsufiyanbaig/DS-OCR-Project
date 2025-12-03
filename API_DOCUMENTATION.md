# DS-OCR-Project API Documentation

## Overview

**Title:** Hello World API  
**Version:** 1.0.0  
**Base URL:** `http://127.0.0.1:4444`

This API provides endpoints for managing bank account applications with OCR-based data extraction capabilities.

---

## Table of Contents

1. [Health Check](#health-check)
2. [Account Applications](#account-applications)
   - [Create Application](#create-application)
   - [Get All Applications](#get-all-applications)
   - [Get Application by ID](#get-application-by-id)
   - [Update Application](#update-application)
   - [Delete Application](#delete-application)
3. [Search Endpoints](#search-endpoints)
   - [Search by CNIC](#search-by-cnic)
   - [Search by Account Type](#search-by-account-type)
   - [Search by City](#search-by-city)
   - [Search by Account Number](#search-by-account-number)
   - [Search by IBAN](#search-by-iban)
4. [Utility Endpoints](#utility-endpoints)
   - [Get Applications Count](#get-applications-count)
   - [Get Paginated Applications](#get-paginated-applications)
5. [Data Models](#data-models)
6. [Validation Rules](#validation-rules)
7. [Error Responses](#error-responses)

---

## Health Check

### GET `/`

Returns API status and version information.

**Response:**
```json
{
  "message": "Hello World!",
  "status": "API is running",
  "version": "1.0.0"
}
```

---

## Account Applications

### Create Application

#### POST `/account-applications`

Creates a new account application. The `account_no` and `iban` are auto-generated.

**Request Body:** `AccountApplicationCreate`

```json
{
  "title_of_account": "JOHN DOE",
  "name": "JOHN DOE",
  "name_on_card": "JOHN DOE",
  "cnic_no": "12345-1234567-1",
  "fathers_husbands_name": "JAMES DOE",
  "mothers_name": "JANE DOE",
  "marital_status": "SINGLE",
  "gender": "MALE",
  "nationality": "PAKISTANI",
  "place_of_birth": "KARACHI",
  "date_of_birth": "1990-01-15",
  "cnic_expiry_date": "2030-01-15",
  "house_no_block_street": "HOUSE 123, BLOCK A, STREET 5",
  "area_location": "GULSHAN",
  "city": "KARACHI",
  "postal_code": "75300",
  "occupation": "SERVICE_PRIVATE",
  "purpose_of_account": "SALARY",
  "source_of_income": "EMPLOYMENT",
  "expected_monthly_turnover_dr": 50000,
  "expected_monthly_turnover_cr": 60000,
  "residential_status": "HOUSE_OWNED",
  "residing_since": "2015-01-01",
  "next_of_kin_name": "JANE DOE",
  "next_of_kin_relation": "S/O",
  "next_of_kin_cnic": "12345-1234567-2",
  "next_of_kin_relationship": "MOTHER",
  "next_of_kin_contact_no": "03001234567",
  "next_of_kin_address": "HOUSE 456, BLOCK B",
  "next_of_kin_email": "jane.doe@email.com",
  "internet_banking": true,
  "mobile_banking": true,
  "check_book": true,
  "sms_alerts": true,
  "card_type_gold": true,
  "card_type_classic": false,
  "zakat_deduction": false
}
```

**Response:** `200 OK` - Returns created `AccountApplication` object with auto-generated `id`, `account_no`, and `iban`.

---

### Get All Applications

#### GET `/account-applications`

Retrieves all account applications.

**Response:** `200 OK` - Array of `AccountApplication` objects.

```json
[
  {
    "id": 1,
    "account_no": "123456789012",
    "iban": "PK123456789012345678",
    "title_of_account": "JOHN DOE",
    "name": "JOHN DOE",
    "cnic_no": "12345-1234567-1",
    ...
  }
]
```

---

### Get Application by ID

#### GET `/account-applications/{application_id}`

Retrieves a specific account application by its ID.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `application_id` | integer | Yes | Unique application identifier |

**Response:** `200 OK` - `AccountApplication` object

**Error Response:** `404 Not Found` - Application not found

---

### Update Application

#### PUT `/account-applications/{application_id}`

Updates an existing account application.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `application_id` | integer | Yes | Unique application identifier |

**Request Body:** `AccountApplication` object with updated fields.

**Response:** `200 OK` - Updated `AccountApplication` object

**Error Response:** `404 Not Found` - Application not found

---

### Delete Application

#### DELETE `/account-applications/{application_id}`

Deletes an account application by its ID.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `application_id` | integer | Yes | Unique application identifier |

**Response:** `200 OK` - Deletion confirmation

**Error Response:** `404 Not Found` - Application not found

---

## Search Endpoints

### Search by CNIC

#### GET `/account-applications/search/cnic/{cnic_no}`

Search for an account application by CNIC number.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cnic_no` | string | Yes | CNIC number (format: `12345-1234567-1`) |

**Response:** `200 OK` - `AccountApplication` object

**Error Response:** `404 Not Found` - Account application not found

---

### Search by Account Type

#### GET `/account-applications/search/account-type/{account_type}`

Search for account applications by account type.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `account_type` | string | Yes | Account type: `CURRENT`, `SAVINGS`, or `AHU_LAT` |

**Response:** `200 OK` - Array of `AccountApplication` objects

---

### Search by City

#### GET `/account-applications/search/city/{city}`

Search for account applications by city.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `city` | string | Yes | City name (in uppercase) |

**Response:** `200 OK` - Array of `AccountApplication` objects

---

### Search by Account Number

#### GET `/account-applications/search/account-number/{account_no}`

Search for an account application by account number.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `account_no` | string | Yes | 12-digit account number |

**Response:** `200 OK` - `AccountApplication` object

**Error Response:** `404 Not Found` - Account application not found

---

### Search by IBAN

#### GET `/account-applications/search/iban/{iban}`

Search for an account application by IBAN.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `iban` | string | Yes | IBAN (format: `PK` + 18 digits) |

**Response:** `200 OK` - `AccountApplication` object

**Error Response:** `404 Not Found` - Account application not found

---

## Utility Endpoints

### Get Applications Count

#### GET `/account-applications/count`

Get the total count of all account applications.

**Response:** `200 OK`
```json
{
  "total_applications": 150
}
```

---

### Get Paginated Applications

#### GET `/account-applications/paginated`

Get paginated list of account applications.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `skip` | integer | No | 0 | Number of records to skip |
| `limit` | integer | No | 10 | Maximum number of records to return |

**Example:** `/account-applications/paginated?skip=10&limit=20`

**Response:** `200 OK` - Array of `AccountApplication` objects

---

## Data Models

### AccountApplicationCreate

Schema for creating new applications (without auto-generated fields).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title_of_account` | string | **Yes** | Account title (BLOCK LETTERS) |
| `name` | string | **Yes** | Name as per CNIC (BLOCK LETTERS) |
| `cnic_no` | string | **Yes** | CNIC number (format: `12345-1234567-1`) |
| `name_on_card` | string | No | Name for card (must match `name`) |
| `fathers_husbands_name` | string | No | Father's/Husband's name |
| `mothers_name` | string | No | Mother's name |
| `marital_status` | MaritalStatus | No | Marital status |
| `gender` | Gender | No | Gender |
| `nationality` | string | No | Nationality |
| `place_of_birth` | string | No | Place of birth |
| `date_of_birth` | string | No | Date of birth (YYYY-MM-DD) |
| `cnic_expiry_date` | string | No | CNIC expiry date |
| `house_no_block_street` | string | No | House address details |
| `area_location` | string | No | Area/Location |
| `city` | string | No | City name |
| `postal_code` | string | No | Postal code (5 digits) |
| `occupation` | Occupation | No | Occupation type |
| `occupation_other` | string | No | Other occupation details |
| `purpose_of_account` | string | No | Purpose of account |
| `source_of_income` | string | No | Source of income |
| `expected_monthly_turnover_dr` | float | No | Expected debit turnover (Rs M) |
| `expected_monthly_turnover_cr` | float | No | Expected credit turnover (Rs M) |
| `residential_status` | ResidentialStatus | No | Residential status |
| `residential_status_other` | string | No | Other residential details |
| `residing_since` | string | No | Residing since date |
| `next_of_kin_name` | string | Conditional* | Next of kin name |
| `next_of_kin_relation` | string | Conditional* | Relation (S/W/D/O) |
| `next_of_kin_cnic` | string | Conditional* | Next of kin CNIC |
| `next_of_kin_relationship` | string | No | Relationship type |
| `next_of_kin_contact_no` | string | No | Contact number |
| `next_of_kin_address` | string | No | Address |
| `next_of_kin_email` | string | No | Email address |
| `internet_banking` | boolean | No | Enable internet banking |
| `mobile_banking` | boolean | No | Enable mobile banking |
| `check_book` | boolean | No | Request check book |
| `sms_alerts` | boolean | No | Enable SMS alerts |
| `card_type_gold` | boolean | No | Request Gold card |
| `card_type_classic` | boolean | No | Request Classic card |
| `zakat_deduction` | boolean | No | Enable Zakat deduction |

> *Conditional: If any next of kin field is provided, `name`, `relation`, and `cnic` become required.

---

### AccountApplication

Full schema including auto-generated fields (used for responses and updates).

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier (auto-generated) |
| `account_no` | string | 12-digit account number (auto-generated) |
| `iban` | string | IBAN (PK + 18 digits, auto-generated) |
| `date` | string | Application date |
| `branch_city` | string | Branch city |
| `branch_code` | string | Branch code |
| `sbp_code` | string | SBP code |
| `account_type` | AccountType | Account type |
| + All fields from AccountApplicationCreate | | |

---

### Enumerations

#### AccountType
| Value | Description |
|-------|-------------|
| `CURRENT` | Current Account |
| `SAVINGS` | Savings Account |
| `AHU_LAT` | Ahu Lat Account |

#### MaritalStatus
| Value | Description |
|-------|-------------|
| `SINGLE` | Single |
| `MARRIED` | Married |
| `DIVORCED` | Divorced |
| `WIDOWED` | Widowed |

#### Gender
| Value | Description |
|-------|-------------|
| `MALE` | Male |
| `FEMALE` | Female |
| `OTHER` | Other |

#### Occupation
| Value | Description |
|-------|-------------|
| `SERVICE_GOVT` | Government Service |
| `SERVICE_PRIVATE` | Private Service |
| `FARMER` | Farmer |
| `HOUSE_WIFE` | House Wife |
| `STUDENT` | Student |
| `OTHER` | Other |

#### ResidentialStatus
| Value | Description |
|-------|-------------|
| `HOUSE_OWNED` | Owned House |
| `RENTAL` | Rental |
| `FAMILY` | Family House |
| `OTHER` | Other |

---

## Validation Rules

### General Rules

1. **BLOCK LETTERS:** All text fields must be in uppercase
   - Applies to: `name`, `title_of_account`, `fathers_husbands_name`, `mothers_name`, `nationality`, `place_of_birth`, `house_no_block_street`, `area_location`, `city`, `purpose_of_account`, `source_of_income`, `next_of_kin_name`, `next_of_kin_address`, `occupation_other`, `residential_status_other`, `name_on_card`

2. **Name Consistency:** `title_of_account`, `name`, and `name_on_card` must be identical

### Field-Specific Validations

| Field | Validation Rule |
|-------|-----------------|
| `cnic_no` | Format: `12345-1234567-1` (5 digits - 7 digits - 1 digit) |
| `next_of_kin_cnic` | Same format as CNIC |
| `date_of_birth` | Date format: `YYYY-MM-DD` |
| `cnic_expiry_date` | Date format: `YYYY-MM-DD` |
| `postal_code` | 5-digit numeric code |
| `next_of_kin_contact_no` | Valid phone number format |
| `next_of_kin_email` | Valid email format |
| `account_no` | 12-digit numeric (auto-generated) |
| `iban` | PK + 18 digits (auto-generated) |

### Next of Kin Validation

If **any** next of kin field is provided, the following fields become **required**:
- `next_of_kin_name`
- `next_of_kin_relation`
- `next_of_kin_cnic`

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Request successful |
| `404 Not Found` | Resource not found |
| `422 Unprocessable Entity` | Validation error |
| `500 Internal Server Error` | Server error |

### Validation Error Example

```json
{
  "detail": [
    {
      "loc": ["body", "cnic_no"],
      "msg": "CNIC must be in format: 12345-1234567-1",
      "type": "value_error"
    }
  ]
}
```

---

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/account-applications` | Create new application |
| `GET` | `/account-applications` | Get all applications |
| `GET` | `/account-applications/{id}` | Get application by ID |
| `PUT` | `/account-applications/{id}` | Update application |
| `DELETE` | `/account-applications/{id}` | Delete application |
| `GET` | `/account-applications/search/cnic/{cnic}` | Search by CNIC |
| `GET` | `/account-applications/search/account-type/{type}` | Search by account type |
| `GET` | `/account-applications/search/city/{city}` | Search by city |
| `GET` | `/account-applications/search/account-number/{no}` | Search by account number |
| `GET` | `/account-applications/search/iban/{iban}` | Search by IBAN |
| `GET` | `/account-applications/count` | Get total count |
| `GET` | `/account-applications/paginated` | Get paginated list |

---

## Running the API

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The API will be available at `http://127.0.0.1:4444`

### Interactive Documentation

- **Swagger UI:** `http://127.0.0.1:4444/docs`
- **ReDoc:** `http://127.0.0.1:4444/redoc`
