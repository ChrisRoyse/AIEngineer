# Christopher's AI Coaching Business - Billing System API Documentation

## API Overview

The Christopher's AI Coaching Billing System provides a comprehensive RESTful API for managing customers, subscriptions, payments, and revenue analytics. The API is designed for high performance, security, and scalability.

**Base URL**: `https://billing.christopherai.coach/api/v1`

**Authentication**: Bearer Token (JWT) or API Key
**Rate Limiting**: 1000 requests per minute per API key
**Response Format**: JSON
**API Version**: v1.0

## Authentication

### API Key Authentication

```http
Authorization: Bearer your-api-key-here
Content-Type: application/json
```

### JWT Token Authentication

```http
Authorization: JWT your-jwt-token-here
Content-Type: application/json
```

## Customer Management API

### Create Customer

Create a new customer in the billing system.

```http
POST /customers
```

**Request Body:**
```json
{
  "email": "customer@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-555-123-4567",
  "company": "Example Corp",
  "billing_address": {
    "line1": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "postal_code": "94105",
    "country": "US"
  },
  "payment_method_id": "pm_1234567890",
  "metadata": {
    "acquisition_source": "website",
    "referral_code": "FRIEND2023"
  }
}
```

**Response (201 Created):**
```json
{
  "customer_id": "cus_abc123def456",
  "stripe_customer_id": "cus_stripe_xyz789",
  "email": "customer@example.com",
  "lifecycle_stage": "prospect",
  "created_at": "2024-01-15T10:30:00Z",
  "payment_methods": [
    {
      "id": "pm_1234567890",
      "type": "card",
      "last4": "4242",
      "exp_month": 12,
      "exp_year": 2025
    }
  ]
}
```

### Get Customer

Retrieve customer information and subscription details.

```http
GET /customers/{customer_id}
```

**Response (200 OK):**
```json
{
  "customer_id": "cus_abc123def456",
  "email": "customer@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-555-123-4567",
  "lifecycle_stage": "active",
  "total_lifetime_value": 15000.00,
  "churn_risk_score": 0.15,
  "subscriptions": [
    {
      "subscription_id": "sub_def456ghi789",
      "plan_name": "Elite 1:1 Coaching",
      "status": "active",
      "current_period_start": "2024-01-01T00:00:00Z",
      "current_period_end": "2024-02-01T00:00:00Z",
      "amount": 5000.00,
      "currency": "USD"
    }
  ],
  "payment_methods": [
    {
      "id": "pm_1234567890",
      "type": "card",
      "last4": "4242",
      "exp_month": 12,
      "exp_year": 2025,
      "is_default": true
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "last_activity_at": "2024-01-20T14:45:00Z"
}
```

### Update Customer

Update customer information and preferences.

```http
PUT /customers/{customer_id}
```

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "phone": "+1-555-987-6543",
  "billing_address": {
    "line1": "456 Oak Ave",
    "city": "Los Angeles", 
    "state": "CA",
    "postal_code": "90210",
    "country": "US"
  },
  "preferred_currency": "USD",
  "metadata": {
    "updated_source": "customer_portal"
  }
}
```

### List Customers

Retrieve paginated list of customers with filtering options.

```http
GET /customers?page=1&limit=50&lifecycle_stage=active&sort=created_at:desc
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `limit` (int): Items per page (default: 50, max: 100)
- `lifecycle_stage` (string): Filter by lifecycle stage
- `created_after` (ISO date): Filter customers created after date
- `sort` (string): Sort field and direction (e.g., "created_at:desc")

**Response (200 OK):**
```json
{
  "customers": [
    {
      "customer_id": "cus_abc123def456",
      "email": "customer@example.com",
      "name": "John Doe",
      "lifecycle_stage": "active",
      "total_lifetime_value": 15000.00,
      "current_mrr": 5000.00,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 247,
    "pages": 5,
    "has_next": true,
    "has_previous": false
  }
}
```

## Subscription Management API

### Create Subscription

Create a new subscription for a customer.

```http
POST /subscriptions
```

**Request Body:**
```json
{
  "customer_id": "cus_abc123def456",
  "plan_id": "elite_coaching",
  "payment_method_id": "pm_1234567890",
  "trial_period_days": 7,
  "proration_behavior": "create_prorations",
  "metadata": {
    "campaign_source": "email_campaign_jan2024",
    "sales_rep": "sarah_jones"
  },
  "discount_code": "NEWCLIENT20",
  "billing_cycle_anchor": "2024-02-01T00:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "subscription_id": "sub_def456ghi789",
  "stripe_subscription_id": "sub_stripe_123abc",
  "customer_id": "cus_abc123def456",
  "plan_id": "elite_coaching",
  "status": "trialing",
  "current_period_start": "2024-01-15T10:30:00Z",
  "current_period_end": "2024-02-15T10:30:00Z",
  "trial_start": "2024-01-15T10:30:00Z",
  "trial_end": "2024-01-22T10:30:00Z",
  "amount": 5000.00,
  "currency": "USD",
  "discount_applied": {
    "code": "NEWCLIENT20",
    "type": "percentage",
    "value": 20,
    "amount_off": 1000.00
  },
  "client_secret": "pi_client_secret_for_payment_confirmation"
}
```

### Get Subscription

Retrieve detailed subscription information.

```http
GET /subscriptions/{subscription_id}
```

**Response (200 OK):**
```json
{
  "subscription_id": "sub_def456ghi789",
  "customer_id": "cus_abc123def456",
  "plan": {
    "id": "elite_coaching",
    "name": "Elite 1:1 Coaching",
    "price": 5000.00,
    "currency": "USD",
    "interval": "monthly",
    "trial_days": 7
  },
  "status": "active",
  "current_period_start": "2024-02-01T00:00:00Z",
  "current_period_end": "2024-03-01T00:00:00Z",
  "billing_cycle_anchor": "2024-02-01T00:00:00Z",
  "quantity": 1,
  "discount": null,
  "tax_percent": 8.75,
  "latest_invoice": {
    "invoice_id": "in_789xyz123",
    "amount_due": 5000.00,
    "status": "paid",
    "paid_at": "2024-02-01T00:05:00Z"
  },
  "upcoming_invoice": {
    "amount_due": 5000.00,
    "period_start": "2024-03-01T00:00:00Z",
    "period_end": "2024-04-01T00:00:00Z"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Subscription

Modify existing subscription (plan changes, quantities, etc.).

```http
PUT /subscriptions/{subscription_id}
```

**Request Body:**
```json
{
  "plan_id": "group_coaching",
  "quantity": 2,
  "proration_behavior": "create_prorations",
  "billing_cycle_anchor": "unchanged",
  "metadata": {
    "change_reason": "customer_downgrade",
    "processed_by": "support_team"
  }
}
```

### Cancel Subscription

Cancel a subscription with optional cancellation options.

```http
DELETE /subscriptions/{subscription_id}
```

**Request Body:**
```json
{
  "cancel_at_period_end": true,
  "cancellation_reason": "customer_request",
  "feedback": "Switching to competitor",
  "offer_retention": true,
  "metadata": {
    "cancelled_by": "customer_portal"
  }
}
```

**Response (200 OK):**
```json
{
  "subscription_id": "sub_def456ghi789",
  "status": "active",
  "cancel_at_period_end": true,
  "cancel_at": "2024-03-01T00:00:00Z",
  "retention_offers": [
    {
      "type": "discount",
      "discount_percent": 25,
      "duration_months": 3,
      "offer_expires": "2024-01-22T00:00:00Z"
    },
    {
      "type": "pause_subscription",
      "max_pause_months": 2,
      "offer_expires": "2024-01-22T00:00:00Z"
    }
  ],
  "cancelled_at": "2024-01-20T15:30:00Z"
}
```

### Pause/Resume Subscription

Temporarily pause or resume a subscription.

```http
POST /subscriptions/{subscription_id}/pause
```

**Request Body:**
```json
{
  "pause_until": "2024-06-01T00:00:00Z",
  "reason": "temporary_financial_hardship",
  "maintain_access": false,
  "automatic_resume": true
}
```

## Payment Management API

### Process Payment

Process a one-time payment or retry failed payment.

```http
POST /payments
```

**Request Body:**
```json
{
  "customer_id": "cus_abc123def456",
  "amount": 997.00,
  "currency": "USD",
  "payment_method_id": "pm_1234567890",
  "description": "Self-Paced AI Course",
  "metadata": {
    "product_id": "course_ai_fundamentals",
    "order_id": "ord_789xyz"
  },
  "receipt_email": "customer@example.com",
  "statement_descriptor": "CHRISTOPHER AI"
}
```

**Response (200 OK):**
```json
{
  "payment_id": "pay_abc123def456",
  "stripe_payment_intent_id": "pi_stripe_789xyz",
  "amount": 997.00,
  "currency": "USD",
  "status": "succeeded",
  "payment_method": {
    "type": "card",
    "last4": "4242",
    "exp_month": 12,
    "exp_year": 2025
  },
  "receipt_url": "https://pay.stripe.com/receipts/...",
  "processing_fee": 29.21,
  "net_amount": 967.79,
  "processed_at": "2024-01-20T16:45:00Z"
}
```

### Get Payment

Retrieve payment transaction details.

```http
GET /payments/{payment_id}
```

### Refund Payment

Process full or partial refund.

```http
POST /payments/{payment_id}/refund
```

**Request Body:**
```json
{
  "amount": 997.00,
  "reason": "requested_by_customer",
  "refund_application_fee": true,
  "metadata": {
    "refund_reason": "course_not_completed",
    "processed_by": "support_team"
  }
}
```

## Invoice Management API

### List Invoices

Retrieve customer invoices with filtering.

```http
GET /customers/{customer_id}/invoices?status=paid&limit=25
```

**Response (200 OK):**
```json
{
  "invoices": [
    {
      "invoice_id": "in_789xyz123",
      "invoice_number": "INV-2024-001234",
      "customer_id": "cus_abc123def456",
      "subscription_id": "sub_def456ghi789",
      "status": "paid",
      "amount_due": 5000.00,
      "amount_paid": 5000.00,
      "tax_amount": 437.50,
      "total": 5437.50,
      "currency": "USD",
      "due_date": "2024-02-01T00:00:00Z",
      "paid_at": "2024-02-01T00:05:00Z",
      "invoice_pdf_url": "https://pay.stripe.com/invoice/...",
      "hosted_invoice_url": "https://invoice.stripe.com/i/...",
      "line_items": [
        {
          "description": "Elite 1:1 Coaching (Feb 1 - Mar 1, 2024)",
          "quantity": 1,
          "unit_amount": 5000.00,
          "amount": 5000.00,
          "period": {
            "start": "2024-02-01T00:00:00Z",
            "end": "2024-03-01T00:00:00Z"
          }
        }
      ],
      "created_at": "2024-01-31T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 25,
    "total": 12,
    "has_next": false
  }
}
```

### Send Invoice Reminder

Send manual invoice reminder to customer.

```http
POST /invoices/{invoice_id}/remind
```

**Request Body:**
```json
{
  "message_type": "gentle_reminder",
  "custom_message": "Hi John, just a friendly reminder about your upcoming coaching session payment.",
  "send_via": ["email", "sms"]
}
```

## Dunning Management API

### Get Dunning Campaigns

Retrieve active dunning campaigns.

```http
GET /dunning/campaigns?status=active&customer_id=cus_abc123def456
```

**Response (200 OK):**
```json
{
  "campaigns": [
    {
      "campaign_id": "dun_abc123def456",
      "customer_id": "cus_abc123def456",
      "subscription_id": "sub_def456ghi789",
      "campaign_type": "failed_payment",
      "status": "active",
      "current_step": 3,
      "total_steps": 5,
      "success_probability": 0.68,
      "amount_at_risk": 5000.00,
      "next_action_at": "2024-01-22T10:00:00Z",
      "actions_taken": [
        {
          "step": 1,
          "action_type": "payment_retry",
          "executed_at": "2024-01-20T10:00:00Z",
          "success": false
        },
        {
          "step": 2,
          "action_type": "email",
          "executed_at": "2024-01-21T10:00:00Z",
          "success": true,
          "engagement": {
            "opened": true,
            "clicked": false
          }
        }
      ],
      "created_at": "2024-01-20T10:00:00Z"
    }
  ]
}
```

### Manually Trigger Dunning Action

Manually execute a specific dunning action.

```http
POST /dunning/campaigns/{campaign_id}/actions
```

**Request Body:**
```json
{
  "action_type": "email",
  "template": "payment_urgent_personal",
  "personalization": {
    "agent_name": "Sarah Johnson",
    "custom_message": "I wanted to personally reach out about your account."
  },
  "schedule_at": "2024-01-22T14:00:00Z"
}
```

### Get Dunning Analytics

Retrieve dunning campaign performance metrics.

```http
GET /dunning/analytics?period_days=30
```

**Response (200 OK):**
```json
{
  "period": {
    "start_date": "2023-12-21",
    "end_date": "2024-01-20",
    "days": 30
  },
  "overall_metrics": {
    "total_campaigns": 45,
    "successful_recoveries": 32,
    "recovery_rate_percent": 71.11,
    "total_recovered": 156000.00,
    "avg_recovery_amount": 4875.00,
    "avg_resolution_hours": 48.5
  },
  "by_campaign_type": [
    {
      "type": "failed_payment",
      "recovery_rate": 68.75,
      "total_recovered": 142000.00,
      "campaigns": 32
    },
    {
      "type": "card_expiring",
      "recovery_rate": 85.71,
      "total_recovered": 12000.00,
      "campaigns": 7
    }
  ],
  "step_effectiveness": [
    {
      "step": 1,
      "action_type": "payment_retry",
      "success_rate": 25.5
    },
    {
      "step": 2,
      "action_type": "email",
      "success_rate": 15.2
    },
    {
      "step": 3,
      "action_type": "sms",
      "success_rate": 12.8
    }
  ]
}
```

## Revenue Analytics API

### Get Revenue Metrics

Retrieve comprehensive revenue analytics.

```http
GET /analytics/revenue?period_days=30&include_forecast=true
```

**Response (200 OK):**
```json
{
  "period": {
    "start_date": "2023-12-21T00:00:00Z",
    "end_date": "2024-01-20T00:00:00Z",
    "days": 30
  },
  "core_metrics": {
    "mrr": 485000.00,
    "arr": 5820000.00,
    "new_mrr": 65000.00,
    "expansion_mrr": 12000.00,
    "contraction_mrr": 8000.00,
    "churn_mrr": 15000.00,
    "net_new_mrr": 54000.00,
    "active_customers": 127,
    "new_customers": 13,
    "churned_customers": 3,
    "total_revenue": 512000.00,
    "payment_success_rate": 96.8,
    "avg_revenue_per_customer": 3818.90,
    "customer_ltv": 28500.00
  },
  "growth_rates": {
    "mrr_growth_rate": 12.5,
    "customer_growth_rate": 11.3,
    "revenue_growth_rate": 15.2
  },
  "cohort_analysis": {
    "monthly_cohorts": [
      {
        "month": "2024-01",
        "size": 13,
        "avg_ltv": 31200.00,
        "retention_rate": 92.3
      },
      {
        "month": "2023-12", 
        "size": 11,
        "avg_ltv": 28900.00,
        "retention_rate": 90.9
      }
    ]
  },
  "forecasts": {
    "mrr_forecast": {
      "30_days": 521000.00,
      "60_days": 558000.00,
      "90_days": 597000.00,
      "confidence_interval": {
        "low": 567000.00,
        "high": 627000.00
      }
    },
    "customer_forecast": {
      "30_days": 135,
      "60_days": 144,
      "90_days": 153
    }
  }
}
```

### Get Customer Segmentation

Analyze customer segments and their performance.

```http
GET /analytics/customer-segments
```

**Response (200 OK):**
```json
{
  "segments": [
    {
      "segment_name": "VIP Customers",
      "criteria": {
        "min_ltv": 50000,
        "subscription_value": ">= 3000"
      },
      "customer_count": 23,
      "avg_ltv": 75300.00,
      "total_mrr": 185000.00,
      "churn_rate": 2.1,
      "characteristics": [
        "High engagement with coaching sessions",
        "Multiple subscription add-ons",
        "Strong payment history",
        "Low churn risk"
      ]
    },
    {
      "segment_name": "Growth Customers",
      "criteria": {
        "ltv_range": "10000-50000",
        "subscription_value": "1000-3000"
      },
      "customer_count": 67,
      "avg_ltv": 28400.00,
      "total_mrr": 245000.00,
      "churn_rate": 5.8,
      "characteristics": [
        "Steady engagement",
        "Occasional plan upgrades",
        "Good payment reliability",
        "Medium churn risk"
      ]
    },
    {
      "segment_name": "Trial Converters",
      "criteria": {
        "ltv_range": "0-10000",
        "lifecycle_stage": "trial"
      },
      "customer_count": 37,
      "avg_ltv": 3200.00,
      "total_mrr": 55000.00,
      "churn_rate": 15.2,
      "characteristics": [
        "Early in customer journey",
        "Testing coaching value",
        "Price sensitivity",
        "Higher churn risk"
      ]
    }
  ],
  "recommendations": [
    {
      "segment": "VIP Customers",
      "action": "Implement premium support tier",
      "expected_impact": "Reduce churn by 50%, increase referrals"
    },
    {
      "segment": "Trial Converters", 
      "action": "Enhanced onboarding program",
      "expected_impact": "Improve trial-to-paid conversion by 25%"
    }
  ]
}
```

### Executive Revenue Report

Generate comprehensive executive-level revenue report.

```http
GET /analytics/executive-report?period_days=30
```

**Response (200 OK):**
```json
{
  "report_title": "Executive Revenue Report - 30 Day Period",
  "report_period": {
    "current": {
      "start": "2023-12-21",
      "end": "2024-01-20"
    },
    "previous": {
      "start": "2023-11-21", 
      "end": "2023-12-21"
    }
  },
  "executive_summary": {
    "key_highlights": [
      "MRR grew 12.5% to $485K, exceeding target by $35K",
      "Payment recovery rate improved to 71%, saving $156K in revenue",
      "Customer LTV increased 8.3% due to improved retention",
      "Elite coaching tier showing strong demand with 89% occupancy"
    ],
    "concerns": [
      "Trial-to-paid conversion down 3.2% from previous period",
      "Higher churn in community access tier (18.5%)"
    ],
    "recommendations": [
      "Implement enhanced trial onboarding program",
      "Review community access pricing and value proposition",
      "Expand elite coaching capacity due to high demand"
    ]
  },
  "key_performance_indicators": {
    "revenue_health": "excellent",
    "customer_growth": "strong", 
    "payment_performance": "excellent",
    "churn_risk": "low"
  },
  "period_comparisons": {
    "mrr_change": 12.5,
    "customer_change": 11.3,
    "ltv_change": 8.3,
    "churn_change": -2.1,
    "recovery_rate_change": 4.8
  }
}
```

## Webhook Events API

### List Webhook Events

Retrieve webhook event logs for debugging.

```http
GET /webhooks/events?source=stripe&processed=true&limit=50
```

**Response (200 OK):**
```json
{
  "events": [
    {
      "event_id": "evt_stripe_abc123",
      "source": "stripe", 
      "event_type": "invoice.payment_succeeded",
      "processed": true,
      "processed_at": "2024-01-20T16:45:32Z",
      "retry_count": 0,
      "data": {
        "object": "invoice",
        "id": "in_stripe_def456",
        "amount_paid": 500000,
        "customer": "cus_stripe_ghi789"
      },
      "created_at": "2024-01-20T16:45:30Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 1247,
    "has_next": true
  }
}
```

### Retry Webhook Event

Manually retry failed webhook processing.

```http
POST /webhooks/events/{event_id}/retry
```

## API Error Responses

### Standard Error Format

All API errors follow a consistent format:

```json
{
  "error": {
    "type": "validation_error",
    "code": "INVALID_EMAIL_FORMAT",
    "message": "The email address format is invalid",
    "details": {
      "field": "email",
      "value": "invalid-email",
      "expected_format": "Valid email address"
    },
    "request_id": "req_abc123def456",
    "timestamp": "2024-01-20T16:45:00Z"
  }
}
```

### Common Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `VALIDATION_ERROR` | Request validation failed |
| 400 | `PAYMENT_FAILED` | Payment processing failed |
| 401 | `AUTHENTICATION_REQUIRED` | API key required |
| 401 | `INVALID_API_KEY` | API key is invalid |
| 403 | `INSUFFICIENT_PERMISSIONS` | API key lacks required permissions |
| 404 | `RESOURCE_NOT_FOUND` | Requested resource doesn't exist |
| 409 | `RESOURCE_CONFLICT` | Resource already exists |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error occurred |
| 502 | `STRIPE_ERROR` | Stripe API error |
| 503 | `SERVICE_UNAVAILABLE` | Service temporarily unavailable |

## Rate Limiting

The API implements rate limiting to ensure service availability:

- **Standard Rate**: 1000 requests per minute per API key
- **Burst Rate**: 100 requests per 10 seconds
- **Premium Rate**: 5000 requests per minute (for premium accounts)

Rate limit headers are included in all responses:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1640995200
X-RateLimit-Type: standard
```

## Pagination

List endpoints use cursor-based pagination:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 247,
    "pages": 5,
    "has_next": true,
    "has_previous": false,
    "next_cursor": "cus_abc123def456",
    "previous_cursor": null
  }
}
```

## Webhooks (Outgoing)

The billing system can send webhooks to your application for important events:

### Webhook Events

| Event Type | Description |
|------------|-------------|
| `customer.created` | New customer registered |
| `subscription.activated` | Subscription became active |
| `payment.succeeded` | Payment processed successfully |
| `payment.failed` | Payment failed |
| `subscription.cancelled` | Subscription was cancelled |
| `dunning.recovery_succeeded` | Failed payment recovered |
| `invoice.overdue` | Invoice is overdue |

### Webhook Payload Example

```json
{
  "id": "evt_webhook_abc123",
  "type": "payment.succeeded",
  "created": 1640995200,
  "data": {
    "object": {
      "payment_id": "pay_abc123def456",
      "customer_id": "cus_abc123def456", 
      "amount": 5000.00,
      "currency": "USD",
      "status": "succeeded"
    }
  },
  "api_version": "v1.0"
}
```

### Webhook Security

Webhooks are secured using HMAC-SHA256 signatures:

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)
```

## SDK Examples

### Python SDK Usage

```python
import christopher_billing

# Initialize client
client = christopher_billing.Client(api_key="your-api-key")

# Create customer
customer = client.customers.create(
    email="customer@example.com",
    name="John Doe",
    payment_method_id="pm_1234567890"
)

# Create subscription
subscription = client.subscriptions.create(
    customer_id=customer.id,
    plan_id="elite_coaching",
    trial_period_days=7
)

# Get revenue metrics
metrics = client.analytics.revenue_metrics(period_days=30)
print(f"Current MRR: ${metrics.mrr:,.2f}")
```

### JavaScript SDK Usage

```javascript
const ChristopherBilling = require('@christopher/billing');

const client = new ChristopherBilling({
  apiKey: 'your-api-key'
});

// Create customer and subscription
const customer = await client.customers.create({
  email: 'customer@example.com',
  name: 'John Doe',
  paymentMethodId: 'pm_1234567890'
});

const subscription = await client.subscriptions.create({
  customerId: customer.id,
  planId: 'elite_coaching',
  trialPeriodDays: 7
});

console.log(`Subscription created: ${subscription.id}`);
```

## Testing

### Test Environment

**Base URL**: `https://billing-test.christopherai.coach/api/v1`

Use test API keys for the test environment:
- Test Secret Key: `sk_test_...`
- Test Publishable Key: `pk_test_...`

### Test Data

The test environment includes sample data:

- Test customers with various lifecycle stages
- Sample subscriptions and payment history
- Mock webhook events for testing integrations

### Test Cards (Stripe Test Mode)

| Card Number | Description |
|-------------|-------------|
| 4242424242424242 | Succeeds |
| 4000000000000002 | Declined |
| 4000000000000119 | Processing error |
| 4000000000000341 | Attach fails |

This comprehensive API documentation provides all the information needed to integrate with Christopher's AI Coaching Billing System. The API is designed for reliability, security, and ease of use, enabling seamless billing automation and revenue optimization.