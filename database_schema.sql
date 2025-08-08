-- Christopher's AI Coaching Business - Billing System Database Schema
-- Comprehensive schema for automated billing, subscriptions, and revenue management

-- Core customer and subscription tables
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(255),
    billing_address JSONB,
    shipping_address JSONB,
    payment_methods JSONB[], -- Array of payment method details
    customer_type VARCHAR(50) DEFAULT 'individual', -- individual, business, enterprise
    lifecycle_stage VARCHAR(50) DEFAULT 'prospect', -- prospect, trial, active, churned, won_back
    acquisition_source VARCHAR(100),
    referral_code VARCHAR(50),
    tax_exempt BOOLEAN DEFAULT FALSE,
    tax_ids JSONB, -- VAT numbers, tax IDs for different regions
    preferred_currency VARCHAR(3) DEFAULT 'USD',
    preferred_language VARCHAR(5) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',
    stripe_customer_id VARCHAR(255) UNIQUE,
    paypal_customer_id VARCHAR(255),
    total_lifetime_value DECIMAL(12,2) DEFAULT 0.00,
    predicted_ltv DECIMAL(12,2),
    churn_risk_score DECIMAL(3,2), -- 0.00 to 1.00
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subscription plans and pricing
CREATE TABLE subscription_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    plan_type VARCHAR(50) NOT NULL, -- coaching, course, community, enterprise
    billing_model VARCHAR(50) NOT NULL, -- recurring, one_time, usage_based
    base_price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    billing_interval VARCHAR(20) NOT NULL, -- monthly, quarterly, annually, one_time
    trial_period_days INTEGER DEFAULT 0,
    setup_fee DECIMAL(10,2) DEFAULT 0.00,
    features JSONB, -- Plan features and limits
    max_participants INTEGER,
    access_duration_days INTEGER, -- For courses, NULL for ongoing access
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer subscriptions
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id),
    plan_id UUID NOT NULL REFERENCES subscription_plans(id),
    stripe_subscription_id VARCHAR(255) UNIQUE,
    paypal_subscription_id VARCHAR(255),
    status VARCHAR(50) NOT NULL, -- active, trialing, past_due, canceled, unpaid
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    trial_start TIMESTAMP,
    trial_end TIMESTAMP,
    cancel_at TIMESTAMP,
    canceled_at TIMESTAMP,
    ended_at TIMESTAMP,
    billing_cycle_anchor TIMESTAMP,
    proration_behavior VARCHAR(50) DEFAULT 'create_prorations',
    collection_method VARCHAR(50) DEFAULT 'charge_automatically',
    quantity INTEGER DEFAULT 1,
    unit_amount DECIMAL(10,2) NOT NULL,
    discount_id UUID REFERENCES discounts(id),
    tax_percent DECIMAL(5,2) DEFAULT 0.00,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payment transactions and invoices
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id),
    subscription_id UUID REFERENCES subscriptions(id),
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    stripe_invoice_id VARCHAR(255) UNIQUE,
    status VARCHAR(50) NOT NULL, -- draft, open, paid, void, uncollectible
    amount_due DECIMAL(12,2) NOT NULL,
    amount_paid DECIMAL(12,2) DEFAULT 0.00,
    amount_remaining DECIMAL(12,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    total DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    description TEXT,
    invoice_pdf_url VARCHAR(500),
    hosted_invoice_url VARCHAR(500),
    payment_intent_id VARCHAR(255),
    due_date TIMESTAMP,
    paid_at TIMESTAMP,
    next_payment_attempt TIMESTAMP,
    attempt_count INTEGER DEFAULT 0,
    billing_reason VARCHAR(100), -- subscription_cycle, subscription_create, manual, etc.
    collection_method VARCHAR(50) DEFAULT 'charge_automatically',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Individual invoice line items
CREATE TABLE invoice_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID NOT NULL REFERENCES invoices(id),
    subscription_id UUID REFERENCES subscriptions(id),
    plan_id UUID REFERENCES subscription_plans(id),
    description TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    unit_amount DECIMAL(10,2) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    tax_rate DECIMAL(5,2) DEFAULT 0.00,
    period_start TIMESTAMP,
    period_end TIMESTAMP,
    proration BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payment transactions
CREATE TABLE payment_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id),
    invoice_id UUID REFERENCES invoices(id),
    subscription_id UUID REFERENCES subscriptions(id),
    payment_intent_id VARCHAR(255) NOT NULL,
    stripe_charge_id VARCHAR(255),
    paypal_transaction_id VARCHAR(255),
    amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    payment_method_type VARCHAR(50), -- card, bank_transfer, paypal, etc.
    payment_method_details JSONB,
    status VARCHAR(50) NOT NULL, -- pending, succeeded, failed, canceled
    failure_code VARCHAR(100),
    failure_message TEXT,
    receipt_url VARCHAR(500),
    refunded_amount DECIMAL(12,2) DEFAULT 0.00,
    dispute_status VARCHAR(50),
    processing_fee DECIMAL(8,2) DEFAULT 0.00,
    net_amount DECIMAL(12,2),
    gateway VARCHAR(50) NOT NULL, -- stripe, paypal, etc.
    gateway_response JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Discounts and promotional pricing
CREATE TABLE discounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(100) UNIQUE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- percentage, fixed_amount, free_trial
    value DECIMAL(10,2) NOT NULL, -- Percentage (0-100) or fixed amount
    currency VARCHAR(3),
    applies_to VARCHAR(50) DEFAULT 'all', -- all, specific_plans, first_payment
    applicable_plans UUID[], -- Array of plan IDs if applies_to = 'specific_plans'
    max_redemptions INTEGER,
    redemptions_count INTEGER DEFAULT 0,
    duration VARCHAR(50) DEFAULT 'once', -- once, repeating, forever
    duration_in_months INTEGER,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dunning management for failed payments
CREATE TABLE dunning_campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id),
    subscription_id UUID REFERENCES subscriptions(id),
    invoice_id UUID REFERENCES invoices(id),
    campaign_type VARCHAR(50) NOT NULL, -- failed_payment, expiring_card, voluntary_churn
    status VARCHAR(50) NOT NULL, -- active, paused, completed, failed
    current_step INTEGER DEFAULT 1,
    total_steps INTEGER NOT NULL,
    next_action_at TIMESTAMP,
    success_rate DECIMAL(5,2),
    recovery_amount DECIMAL(12,2),
    campaign_config JSONB, -- Step configurations, timing, etc.
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Individual dunning actions and communications
CREATE TABLE dunning_actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES dunning_campaigns(id),
    step_number INTEGER NOT NULL,
    action_type VARCHAR(50) NOT NULL, -- email, sms, phone_call, payment_retry
    status VARCHAR(50) NOT NULL, -- scheduled, sent, delivered, failed, clicked
    scheduled_at TIMESTAMP NOT NULL,
    executed_at TIMESTAMP,
    message_template VARCHAR(255),
    message_content TEXT,
    response_data JSONB,
    success BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Revenue analytics and reporting
CREATE TABLE revenue_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_date DATE NOT NULL,
    metric_type VARCHAR(50) NOT NULL, -- daily, weekly, monthly
    mrr DECIMAL(12,2), -- Monthly Recurring Revenue
    arr DECIMAL(12,2), -- Annual Recurring Revenue
    new_mrr DECIMAL(12,2),
    expansion_mrr DECIMAL(12,2),
    contraction_mrr DECIMAL(12,2),
    churn_mrr DECIMAL(12,2),
    net_new_mrr DECIMAL(12,2),
    active_customers INTEGER,
    new_customers INTEGER,
    churned_customers INTEGER,
    total_revenue DECIMAL(12,2),
    one_time_revenue DECIMAL(12,2),
    refunds DECIMAL(12,2),
    gross_revenue DECIMAL(12,2),
    payment_volume DECIMAL(12,2),
    successful_payments INTEGER,
    failed_payments INTEGER,
    payment_success_rate DECIMAL(5,2),
    avg_revenue_per_customer DECIMAL(10,2),
    customer_ltv DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(metric_date, metric_type)
);

-- Tax rates and compliance
CREATE TABLE tax_rates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction VARCHAR(100) NOT NULL,
    tax_type VARCHAR(50) NOT NULL, -- vat, gst, sales_tax, etc.
    rate DECIMAL(5,4) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    valid_from DATE NOT NULL,
    valid_until DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Webhook events and processing
CREATE TABLE webhook_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(50) NOT NULL, -- stripe, paypal, etc.
    event_id VARCHAR(255) UNIQUE NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    api_version VARCHAR(20),
    data JSONB NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for optimal query performance
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_stripe_id ON customers(stripe_customer_id);
CREATE INDEX idx_customers_lifecycle ON customers(lifecycle_stage);
CREATE INDEX idx_customers_churn_risk ON customers(churn_risk_score DESC);

CREATE INDEX idx_subscriptions_customer ON subscriptions(customer_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_subscriptions_period ON subscriptions(current_period_end);

CREATE INDEX idx_invoices_customer ON invoices(customer_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_due_date ON invoices(due_date);
CREATE INDEX idx_invoices_stripe_id ON invoices(stripe_invoice_id);

CREATE INDEX idx_payments_customer ON payment_transactions(customer_id);
CREATE INDEX idx_payments_status ON payment_transactions(status);
CREATE INDEX idx_payments_created ON payment_transactions(created_at);

CREATE INDEX idx_revenue_metrics_date ON revenue_metrics(metric_date);
CREATE INDEX idx_revenue_metrics_type ON revenue_metrics(metric_type);

CREATE INDEX idx_webhook_processed ON webhook_events(processed, created_at);

-- Triggers for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payment_transactions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();