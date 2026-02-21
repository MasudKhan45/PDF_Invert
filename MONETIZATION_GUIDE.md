# Monetization Setup Guide

This guide walks you through setting up monetization for your PDF Inverter application using Google AdSense (for ads) and Stripe (for premium subscriptions).

## Part 1: Google AdSense Setup

### Step 1: Create AdSense Account

1. **Go to Google AdSense**: Visit [https://www.google.com/adsense](https://www.google.com/adsense)
2. **Sign up** with your Google account
3. **Enter your website URL**: Use your Hostinger domain (e.g., `https://yourpdfdomain.com`)
4. **Fill in payment details**: Required for receiving earnings

### Step 2: Get Approval

1. **Add AdSense code to your site**: Google will provide a verification code
2. **Wait for approval**: Usually takes 24-48 hours (can take up to 2 weeks)
3. **Requirements**:
   - Original, quality content
   - Easy navigation
   - Privacy policy page (we'll add this)
   - About page (optional but recommended)

### Step 3: Create Ad Units

Once approved:

1. **Login to AdSense Dashboard**
2. **Navigate to Ads → By ad unit**
3. **Create 3 ad units**:

   **Ad Unit 1: Top Banner**
   - Type: Display ad
   - Size: Responsive
   - Name: "PDF_Inverter_Top_Banner"
   
   **Ad Unit 2: Sidebar**
   - Type: Display ad  
   - Size: Responsive
   - Name: "PDF_Inverter_Sidebar"
   
   **Ad Unit 3: Bottom Banner**
   - Type: Display ad
   - Size: Responsive
   - Name: "PDF_Inverter_Bottom"

4. **Copy the ad code** for each unit
5. **Update `templates/index.html`**: Replace placeholder `YOUR_ADSENSE_CLIENT_ID` with your actual client ID (format: `ca-pub-XXXXXXXXXX`)

### Step 4: Add Privacy Policy

**Required for AdSense compliance**

Create a Privacy Policy page:
- Use a generator: [https://www.freeprivacypolicy.com/](https://www.freeprivacypolicy.com/)
- Include: Cookie usage, Google AdSense data collection
- Add link to footer of your site

---

## Part 2: Stripe Setup for Premium Subscriptions

### Step 1: Create Stripe Account

1. **Go to Stripe**: Visit [https://stripe.com](https://stripe.com)
2. **Sign up** for a Stripe account
3. **Complete account verification**:
   - Business details
   - Bank account info (for payouts)
   - Identity verification

### Step 2: Get API Keys

1. **Login to Stripe Dashboard**
2. **Navigate to Developers → API keys**
3. **Copy your keys**:
   - **Publishable key**: Starts with `pk_test_` (test mode) or `pk_live_` (production)
   - **Secret key**: Starts with `sk_test_` (test mode) or `sk_live_` (production)

4. **Create a `.env` file** in your project root:

```bash
# Stripe Keys (TEST MODE - use for development)
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE

# Stripe Keys (LIVE MODE - use in production)
# STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_KEY_HERE
# STRIPE_SECRET_KEY=sk_live_YOUR_KEY_HERE

# App Config
FLASK_SECRET_KEY=your-random-secret-key-here
```

### Step 3: Create Products in Stripe

1. **Navigate to Products** in Stripe Dashboard
2. **Create products** for each pricing tier:

   **Product 1: Lifetime Ad-Free**
   - Name: "PDF Inverter - Ad-Free (Lifetime)"
   - Description: "One-time payment for lifetime ad-free access"
   - Pricing: One-time payment of $4.99
   - Copy the **Price ID** (starts with `price_`)

   **Product 2: Monthly Subscription** (Optional)
   - Name: "PDF Inverter - Premium Monthly"  
   - Description: "Monthly subscription for ad-free experience"
   - Pricing: Recurring monthly at $1.99
   - Copy the **Price ID**

   **Product 3: Yearly Subscription** (Optional)
   - Name: "PDF Inverter - Premium Yearly"
   - Description: "Yearly subscription - Save 37%"
   - Pricing: Recurring yearly at $14.99
   - Copy the **Price ID**

3. **Add Price IDs to `.env`**:
```bash
STRIPE_LIFETIME_PRICE_ID=price_XXXXXXXXXX
STRIPE_MONTHLY_PRICE_ID=price_XXXXXXXXXX
STRIPE_YEARLY_PRICE_ID=price_XXXXXXXXXX
```

### Step 4: Configure Webhooks (Production Only)

**For production deployment:**

1. **Navigate to Developers → Webhooks** in Stripe
2. **Add endpoint**: `https://yourdomain.com/stripe-webhook`
3. **Select events to listen to**:
   - `checkout.session.completed`
   - `customer.subscription.deleted` (if using subscriptions)
   - `invoice.payment_failed` (if using subscriptions)
4. **Copy the signing secret**: Starts with `whsec_`
5. **Add to `.env`**:
```bash
STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET_HERE
```

---

## Part 3: Configuration

### Update `config.py`

The application reads from environment variables. Make sure your `.env` file is properly configured (see Stripe setup above).

### Security Notes

⚠️ **IMPORTANT**:
- **Never commit `.env` to git** (already in `.gitignore`)
- **Keep secret keys secure**
- **Use test keys during development**
- **Switch to live keys only in production**

---

## Part 4: Testing

### Test AdSense (After Approval)

1. **Start your app**: `python app.py`
2. **Open**: `http://localhost:5000`
3. **Verify ads appear** (may show blank in localhost - that's normal)
4. **Deploy to production** to see real ads
5. **Check AdSense dashboard** for impressions/revenue

### Test Stripe Payments

1. **Use test mode keys** in `.env`
2. **Click "Go Premium"** button on your site
3. **Use Stripe test cards**:
   - Success: `4242 4242 4242 4242`
   - Decline: `4000 0000 0000 0002`
   - Any future expiry date, any CVC
4. **Verify** ads disappear after successful payment
5. **Check Stripe Dashboard** for test payments

---

## Part 5: Going Live

### Before Production:

✅ **AdSense Checklist**:
- [ ] Account approved
- [ ] Ad units created
- [ ] Privacy policy page added
- [ ] Ads showing correctly on staging

✅ **Stripe Checklist**:
- [ ] Account fully verified
- [ ] Products created
- [ ] Webhook configured
- [ ] Tested with test cards
- [ ] Switched to live API keys

### Launch Steps:

1. **Update `.env` with live keys**
2. **Deploy to Hostinger**
3. **Test a real small payment** ($0.50 if possible)
4. **Monitor Stripe Dashboard** for payments
5. **Monitor AdSense Dashboard** for ad performance

---

## Revenue Optimization Tips

### AdSense Best Practices

- **Don't click your own ads** (violates ToS, can get banned)
- **Optimize ad placement** for visibility without being intrusive
- **Monitor CTR** (Click-Through Rate) in dashboard
- **Test different ad sizes** to maximize revenue
- **Wait 2-3 months** for consistent revenue data

### Pricing Strategy

- **Start with one-time payment** ($4.99) - simpler
- **Add subscriptions later** if you get recurring traffic
- **Consider**: Limited free uses (5 PDFs/day) to increase conversions
- **A/B test pricing**: Try $2.99, $4.99, $9.99 to find sweet spot

---

## Troubleshooting

### AdSense Issues

**Ads not showing:**
- Check if account is approved
- Verify ad code is correct
- Check browser console for errors
- AdSense may take 20 minutes to activate new units

**Low earnings:**
- Normal at first - need traffic
- Optimize for relevant keywords (PDF, invert, dark mode)
- Drive traffic through SEO, social media

### Stripe Issues

**Payment fails:**
- Check API keys are correct
- Verify webhook signature (production)
- Check Stripe logs for errors
- Ensure HTTPS in production (required)

---

## Support & Resources

- **AdSense Help**: [https://support.google.com/adsense](https://support.google.com/adsense)
- **Stripe Docs**: [https://stripe.com/docs](https://stripe.com/docs)
- **Payment Testing**: [https://stripe.com/docs/testing](https://stripe.com/docs/testing)

**Good luck with monetization! 🚀💰**
