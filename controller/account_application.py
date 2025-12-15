from sqlmodel import Session
from fastapi import HTTPException
from model import AccountApplicationCreate, AccountType
from db.schemas import AccountApplication
from typing import List, Optional
from utils.validations import generate_account_number, generate_iban


def create_account_application(application_create: AccountApplicationCreate, session: Session) -> AccountApplication:
    """Create a new account application using model SQL query"""
    print("API called with data:", application_create.model_dump())
    try:
        # Get data and convert enums to their string values
        data = application_create.model_dump()
        
        # Convert enum fields to string values
        if data.get('marital_status'):
            data['marital_status'] = data['marital_status'].value if hasattr(data['marital_status'], 'value') else data['marital_status']
        if data.get('gender'):
            data['gender'] = data['gender'].value if hasattr(data['gender'], 'value') else data['gender']
        if data.get('occupation'):
            data['occupation'] = data['occupation'].value if hasattr(data['occupation'], 'value') else data['occupation']
        if data.get('residential_status'):
            data['residential_status'] = data['residential_status'].value if hasattr(data['residential_status'], 'value') else data['residential_status']
        if data.get('account_type'):
            data['account_type'] = data['account_type'].value if hasattr(data['account_type'], 'value') else data['account_type']
        if data.get('card_type'):
            data['card_type'] = data['card_type'].value if hasattr(data['card_type'], 'value') else data['card_type']
        if data.get('card_network'):
            data['card_network'] = data['card_network'].value if hasattr(data['card_network'], 'value') else data['card_network']
        
        # Convert to full AccountApplication model
        application_data = AccountApplication(**data)

        # Generate account number and IBAN
        application_data.account_no = generate_account_number()
        application_data.iban = generate_iban()

        return AccountApplication.create(session, application_data)
    except Exception as e:
        print(f"Error creating application: {e}")
        import traceback
        traceback.print_exc()
        raise


def get_account_applications(session: Session) -> List[AccountApplication]:
    """Retrieve all account applications using model SQL query"""
    return AccountApplication.get_all(session)


def get_account_application_by_id(application_id: int, session: Session) -> AccountApplication:
    """Retrieve a specific account application by ID using model SQL query"""
    application = AccountApplication.get_by_id(session, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Account application not found")
    return application


def update_account_application(application_id: int, updated_application: AccountApplication, session: Session) -> AccountApplication:
    """Update an existing account application using model SQL query"""
    update_data = updated_application.model_dump(exclude_unset=True, exclude={'id'})
    application = AccountApplication.update_by_id(session, application_id, update_data)
    if not application:
        raise HTTPException(status_code=404, detail="Account application not found")
    return application


def delete_account_application(application_id: int, session: Session) -> dict:
    """Delete an account application by ID using model SQL query"""
    success = AccountApplication.delete_by_id(session, application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account application not found")
    return {"message": "Account application deleted successfully"}


# Additional business logic methods using model SQL queries
def get_application_by_cnic(cnic_no: str, session: Session) -> Optional[AccountApplication]:
    """Get account application by CNIC number"""
    return AccountApplication.get_by_cnic(session, cnic_no)


def get_applications_by_account_type(account_type: str, session: Session) -> List[AccountApplication]:
    """Get account applications by account type"""
    try:
        acc_type = AccountType(account_type.upper())
        return AccountApplication.get_by_account_type(session, acc_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid account type")


def get_applications_by_city(city: str, session: Session) -> List[AccountApplication]:
    """Get account applications by city"""
    return AccountApplication.get_by_city(session, city.upper())


def get_total_applications_count(session: Session) -> int:
    """Get total count of account applications"""
    return AccountApplication.count_total(session)


def get_paginated_applications(skip: int = 0, limit: int = 10, session: Session = None) -> List[AccountApplication]:
    """Get paginated account applications"""
    return AccountApplication.get_paginated(session, skip, limit)


def get_application_by_account_number(account_no: str, session: Session) -> Optional[AccountApplication]:
    """Get account application by account number"""
    return AccountApplication.get_by_account_number(session, account_no)


def get_application_by_iban(iban: str, session: Session) -> Optional[AccountApplication]:
    """Get account application by IBAN"""
    return AccountApplication.get_by_iban(session, iban)


# Analytics Functions
def get_analytics_by_account_type(session: Session) -> dict:
    """Get count of applications grouped by account type"""
    data = AccountApplication.count_by_account_type(session)
    total = sum(data.values())
    return {
        "total": total,
        "breakdown": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_analytics_by_city(session: Session) -> dict:
    """Get count of applications grouped by city"""
    data = AccountApplication.count_by_city(session)
    total = sum(data.values())
    return {
        "total": total,
        "breakdown": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_analytics_by_gender(session: Session) -> dict:
    """Get count of applications grouped by gender"""
    data = AccountApplication.count_by_gender(session)
    total = sum(data.values())
    return {
        "total": total,
        "breakdown": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_analytics_by_occupation(session: Session) -> dict:
    """Get count of applications grouped by occupation"""
    data = AccountApplication.count_by_occupation(session)
    total = sum(data.values())
    return {
        "total": total,
        "breakdown": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_analytics_by_card_type(session: Session) -> dict:
    """Get count of applications grouped by card type"""
    data = AccountApplication.count_by_card_type(session)
    total = sum(data.values())
    return {
        "total": total,
        "breakdown": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_analytics_by_card_network(session: Session) -> dict:
    """Get count of applications grouped by card network"""
    data = AccountApplication.count_by_card_network(session)
    total = sum(data.values())
    return {
        "total": total,
        "breakdown": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_analytics_by_marital_status(session: Session) -> dict:
    """Get count of applications grouped by marital status"""
    data = AccountApplication.count_by_marital_status(session)
    total = sum(data.values())
    return {
        "total": total,
        "breakdown": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_analytics_by_residential_status(session: Session) -> dict:
    """Get count of applications grouped by residential status"""
    data = AccountApplication.count_by_residential_status(session)
    total = sum(data.values())
    return {
        "total": total,
        "breakdown": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_services_analytics(session: Session) -> dict:
    """Get analytics for services (internet banking, mobile banking, etc.)"""
    data = AccountApplication.get_services_stats(session)
    total = AccountApplication.count_total(session)
    return {
        "total_applications": total,
        "services": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_kin_analytics(session: Session) -> dict:
    """Get analytics for next of kin"""
    data = AccountApplication.get_kin_stats(session)
    total = sum(data.values())
    return {
        "total": total,
        "breakdown": data,
        "percentages": {k: round((v / total) * 100, 2) if total > 0 else 0 for k, v in data.items()}
    }


def get_dashboard_summary(session: Session) -> dict:
    """Get comprehensive dashboard summary with all analytics"""
    total = AccountApplication.count_total(session)
    
    return {
        "total_applications": total,
        "account_types": AccountApplication.count_by_account_type(session),
        "gender_distribution": AccountApplication.count_by_gender(session),
        "card_types": AccountApplication.count_by_card_type(session),
        "card_networks": AccountApplication.count_by_card_network(session),
        "top_cities": dict(list(AccountApplication.count_by_city(session).items())[:10]),
        "services_adoption": AccountApplication.get_services_stats(session),
        "kin_stats": AccountApplication.get_kin_stats(session)
    }


# ==================== ADVANCED ANALYTICS FUNCTIONS ====================

def get_financial_insights(session: Session) -> dict:
    """Get comprehensive financial analytics with insights"""
    stats = AccountApplication.get_financial_stats(session)
    total = AccountApplication.count_total(session)
    
    # Calculate insights
    avg_net_flow = stats["credit_turnover"]["average"] - stats["debit_turnover"]["average"]
    
    return {
        "summary": stats,
        "insights": {
            "average_net_monthly_flow": round(avg_net_flow, 2),
            "flow_direction": "POSITIVE" if avg_net_flow > 0 else "NEGATIVE",
            "total_expected_monthly_deposits": stats["credit_turnover"]["total"],
            "total_expected_monthly_withdrawals": stats["debit_turnover"]["total"],
            "highest_single_deposit_expectation": stats["credit_turnover"]["maximum"],
            "total_applications_analyzed": total
        }
    }


def get_gender_account_cross_analysis(session: Session) -> dict:
    """Cross-tabulation analysis: Gender vs Account Type with insights"""
    data = AccountApplication.get_cross_analysis_gender_account(session)
    
    # Calculate insights
    insights = {}
    for gender, accounts in data.items():
        total_for_gender = sum(accounts.values())
        preferred_account = max(accounts, key=accounts.get) if accounts else None
        insights[gender] = {
            "total": total_for_gender,
            "preferred_account_type": preferred_account,
            "account_distribution": accounts
        }
    
    return {
        "cross_tabulation": data,
        "gender_insights": insights
    }


def get_occupation_card_cross_analysis(session: Session) -> dict:
    """Cross-tabulation analysis: Occupation vs Card Type with insights"""
    data = AccountApplication.get_cross_analysis_occupation_card(session)
    
    # Calculate premium card adoption by occupation
    premium_cards = ['PLATINUM', 'SIGNATURE', 'INFINITE']
    premium_adoption = {}
    
    for occupation, cards in data.items():
        total = sum(cards.values())
        premium_count = sum(cards.get(card, 0) for card in premium_cards)
        premium_adoption[occupation] = {
            "total_customers": total,
            "premium_card_holders": premium_count,
            "premium_adoption_rate": round((premium_count / total) * 100, 2) if total > 0 else 0
        }
    
    # Sort by premium adoption rate
    sorted_adoption = dict(sorted(premium_adoption.items(), 
                                   key=lambda x: x[1]["premium_adoption_rate"], 
                                   reverse=True))
    
    return {
        "cross_tabulation": data,
        "premium_card_adoption_by_occupation": sorted_adoption,
        "top_premium_adopters": list(sorted_adoption.keys())[:5]
    }


def get_city_performance_analytics(session: Session) -> dict:
    """Comprehensive city-wise performance with rankings"""
    city_data = AccountApplication.get_city_performance(session)
    
    if not city_data:
        return {"cities": [], "insights": {}}
    
    # Calculate rankings
    by_volume = sorted(city_data, key=lambda x: x["total_applications"], reverse=True)
    by_value = sorted(city_data, key=lambda x: x["total_monthly_credit"], reverse=True)
    by_avg_value = sorted(city_data, key=lambda x: x["avg_monthly_credit"], reverse=True)
    
    return {
        "city_performance": city_data,
        "rankings": {
            "by_application_volume": [c["city"] for c in by_volume[:10]],
            "by_total_credit_value": [c["city"] for c in by_value[:10]],
            "by_average_customer_value": [c["city"] for c in by_avg_value[:10]]
        },
        "insights": {
            "highest_volume_city": by_volume[0]["city"] if by_volume else None,
            "highest_value_city": by_value[0]["city"] if by_value else None,
            "highest_avg_customer_value_city": by_avg_value[0]["city"] if by_avg_value else None,
            "total_cities": len(city_data)
        }
    }


def get_occupation_income_analysis(session: Session) -> dict:
    """Analyze income patterns by occupation"""
    data = AccountApplication.get_avg_turnover_by_occupation(session)
    
    if not data:
        return {"occupations": [], "insights": {}}
    
    # Calculate insights
    highest_earning = data[0] if data else None
    lowest_earning = data[-1] if data else None
    
    # Calculate income tiers
    income_tiers = {"high": [], "medium": [], "low": []}
    for occ in data:
        if occ["avg_credit"] >= 300000:
            income_tiers["high"].append(occ["occupation"])
        elif occ["avg_credit"] >= 100000:
            income_tiers["medium"].append(occ["occupation"])
        else:
            income_tiers["low"].append(occ["occupation"])
    
    return {
        "occupation_income_data": data,
        "income_tiers": income_tiers,
        "insights": {
            "highest_earning_occupation": highest_earning["occupation"] if highest_earning else None,
            "highest_avg_income": highest_earning["avg_credit"] if highest_earning else 0,
            "lowest_earning_occupation": lowest_earning["occupation"] if lowest_earning else None,
            "lowest_avg_income": lowest_earning["avg_credit"] if lowest_earning else 0
        }
    }


def get_premium_customer_analysis(session: Session) -> dict:
    """In-depth analysis of premium card holders"""
    data = AccountApplication.get_premium_card_demographics(session)
    
    # Calculate premium vs non-premium comparison
    income_difference = data["avg_monthly_credit_premium"] - data["avg_monthly_credit_non_premium"]
    income_multiplier = (data["avg_monthly_credit_premium"] / data["avg_monthly_credit_non_premium"] 
                         if data["avg_monthly_credit_non_premium"] > 0 else 0)
    
    return {
        "premium_demographics": data,
        "insights": {
            "income_difference": round(income_difference, 2),
            "income_multiplier": round(income_multiplier, 2),
            "premium_customer_profile": {
                "top_occupation": max(data["occupation_distribution"], 
                                      key=data["occupation_distribution"].get) if data["occupation_distribution"] else None,
                "top_city": max(data["top_cities"], 
                               key=data["top_cities"].get) if data["top_cities"] else None,
                "dominant_gender": max(data["gender_distribution"], 
                                       key=data["gender_distribution"].get) if data["gender_distribution"] else None
            }
        }
    }


def get_digital_banking_insights(session: Session) -> dict:
    """Comprehensive digital banking adoption analysis"""
    data = AccountApplication.get_digital_adoption_analysis(session)
    
    # Calculate digital maturity score
    digital_score = (data["full_digital_customers"] / data["total_customers"]) * 100 if data["total_customers"] > 0 else 0
    
    # Determine digital maturity level
    if digital_score >= 70:
        maturity_level = "ADVANCED"
    elif digital_score >= 40:
        maturity_level = "GROWING"
    else:
        maturity_level = "DEVELOPING"
    
    return {
        "adoption_data": data,
        "insights": {
            "digital_maturity_score": round(digital_score, 2),
            "digital_maturity_level": maturity_level,
            "non_digital_opportunity": data["no_digital"],
            "recommendation": "Focus on converting internet-only users to full digital" 
                            if data["internet_only"] > data["mobile_only"] 
                            else "Promote internet banking to mobile-only users"
        }
    }


def get_high_value_customer_insights(session: Session, threshold: float = 500000) -> dict:
    """Identify and analyze high-value customers with actionable insights"""
    data = AccountApplication.get_high_value_customers(session, threshold)
    
    return {
        "high_value_analysis": data,
        "insights": {
            "total_high_value": data["total_high_value_customers"],
            "market_concentration": f"{data['percentage_of_total']}% of customers are high-value",
            "recommended_focus_city": list(data["top_cities"].keys())[0] if data["top_cities"] else None,
            "recommended_target_occupation": list(data["top_occupations"].keys())[0] if data["top_occupations"] else None,
            "preferred_products": {
                "card_type": max(data["preferred_card_types"], 
                               key=data["preferred_card_types"].get) if data["preferred_card_types"] else None,
                "account_type": max(data["account_type_preference"], 
                                   key=data["account_type_preference"].get) if data["account_type_preference"] else None
            }
        }
    }


def get_profile_completeness_analytics(session: Session) -> dict:
    """Analyze profile completeness with improvement recommendations"""
    data = AccountApplication.get_profile_completeness(session)
    
    # Identify weakest areas
    completion_rates = data["field_completion_rates"]
    sorted_fields = sorted(completion_rates.items(), key=lambda x: x[1])
    
    return {
        "completeness_data": data,
        "insights": {
            "overall_health": "GOOD" if data["average_completeness_percentage"] >= 70 else 
                             "MODERATE" if data["average_completeness_percentage"] >= 50 else "NEEDS_IMPROVEMENT",
            "weakest_fields": [f[0] for f in sorted_fields[:3]],
            "strongest_fields": [f[0] for f in sorted_fields[-3:]],
            "improvement_priority": sorted_fields[0][0] if sorted_fields else None,
            "fully_complete_rate": round((data["fully_complete_profiles"] / data["total_applications"]) * 100, 2) 
                                   if data["total_applications"] > 0 else 0
        }
    }


def get_customer_segmentation(session: Session) -> dict:
    """Customer segmentation with actionable insights"""
    data = AccountApplication.get_customer_segments(session)
    
    # Find largest and smallest segments
    segments = data["segments"]
    sorted_segments = sorted(segments.items(), key=lambda x: x[1]["count"], reverse=True)
    
    # Generate recommendations for each segment
    segment_recommendations = {
        "premium_digital_natives": "Offer exclusive digital-first experiences and premium rewards",
        "high_value_traditional": "Focus on relationship banking and personalized in-branch services",
        "young_professionals": "Promote career-linked products and financial planning tools",
        "business_owners": "Cross-sell business banking products and merchant services",
        "value_seekers": "Educate on digital benefits and offer upgrade incentives",
        "fully_engaged": "Maintain loyalty with rewards and referral programs"
    }
    
    return {
        "segmentation_data": data,
        "insights": {
            "largest_segment": sorted_segments[0][0] if sorted_segments else None,
            "smallest_segment": sorted_segments[-1][0] if sorted_segments else None,
            "growth_opportunity": sorted_segments[-1][0] if sorted_segments else None
        },
        "segment_recommendations": segment_recommendations
    }


def get_executive_summary(session: Session) -> dict:
    """Generate executive summary with key business metrics and insights"""
    total = AccountApplication.count_total(session)
    financial = AccountApplication.get_financial_stats(session)
    digital = AccountApplication.get_digital_adoption_analysis(session)
    services = AccountApplication.get_services_stats(session)
    segments = AccountApplication.get_customer_segments(session)
    completeness = AccountApplication.get_profile_completeness(session)
    
    # Key metrics
    digital_adoption = round((digital["full_digital_customers"] / total) * 100, 2) if total > 0 else 0
    service_engagement = round(sum(services.values()) / (total * 5) * 100, 2) if total > 0 else 0
    
    # Find top segment
    top_segment = max(segments["segments"].items(), key=lambda x: x[1]["count"])[0] if segments["segments"] else None
    
    return {
        "key_metrics": {
            "total_customers": total,
            "total_expected_monthly_deposits": financial["credit_turnover"]["total"],
            "average_customer_value": financial["credit_turnover"]["average"],
            "digital_adoption_rate": digital_adoption,
            "service_engagement_score": service_engagement,
            "profile_completeness": completeness["average_completeness_percentage"]
        },
        "health_indicators": {
            "digital_maturity": "HIGH" if digital_adoption >= 60 else "MEDIUM" if digital_adoption >= 30 else "LOW",
            "data_quality": "HIGH" if completeness["average_completeness_percentage"] >= 70 else 
                           "MEDIUM" if completeness["average_completeness_percentage"] >= 50 else "LOW",
            "customer_engagement": "HIGH" if service_engagement >= 60 else 
                                  "MEDIUM" if service_engagement >= 40 else "LOW"
        },
        "top_insights": [
            f"Digital banking adoption is at {digital_adoption}%",
            f"Average customer expects Rs. {financial['credit_turnover']['average']:,.0f} monthly credit",
            f"Top customer segment: {top_segment}",
            f"Profile completeness average: {completeness['average_completeness_percentage']}%"
        ],
        "recommendations": [
            "Focus on converting non-digital users to mobile banking",
            "Target high-value customers for premium card upgrades",
            "Improve profile completeness through incentivized data collection"
        ]
    }