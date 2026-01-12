# Examples: Planning with Files in Action

Real-world examples of the Planning with Files workflow in action.

## Example 1: Research Task - Morning Exercise Benefits

**User Request:** "Research the benefits of morning exercise and write a summary"

### Loop 1: Create Plan

**task_plan.md:**
```markdown
# Task Plan: Morning Exercise Benefits Research

## Goal
Create a research summary on the benefits of morning exercise with scientific backing.

## Phases
- [x] Phase 1: Create this plan ✓
- [ ] Phase 2: Search and gather scientific sources
- [ ] Phase 3: Analyze and synthesize findings
- [ ] Phase 4: Create comprehensive summary
- [ ] Phase 5: Review and finalize

## Key Questions
1. What are the documented physical health benefits?
2. What mental health benefits have been studied?
3. What does recent research (2020-2025) show?
4. Are there any potential drawbacks?

## Expected Deliverable
- morning_exercise_summary.md (2-3 pages)
- Key statistics and study citations
- Actionable recommendations

## Status
**Currently in Phase 1** - Plan created, ready to research
```

### Loop 2: Research

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create this plan ✓
- [x] Phase 2: Search and gather scientific sources ✓
- [ ] Phase 3: Analyze and synthesize findings
- [ ] Phase 4: Create comprehensive summary
- [ ] Phase 5: Review and finalize

## Sources Found
- 15 scientific studies collected
- Time range: 2020-2025
- Sources from: Cell Metabolism, Psychology of Sport and Exercise, Sports Medicine

## Status
**Currently in Phase 3** - Analyzing findings from 15 sources
```

**notes.md:**
```markdown
# Notes: Morning Exercise Benefits

## Scientific Sources

### Study 1: Exercise Timing and Metabolism
- Journal: Cell Metabolism, 2024
- Key finding: Morning exercise increases fat oxidation by 20%
- Sample size: 30 participants
- Duration: 8 weeks

### Study 2: Mental Health and Exercise Timing
- Journal: Psychology of Sport and Exercise, 2024
- Key finding: Morning exercise improved mood scores by 15%
- Also improved sleep quality
- Sample size: 150 participants

### Study 3: Consistency in Exercise
- Journal: Sports Medicine, 2023
- Key finding: Morning exercise created more consistent routines
- Participants 3x more likely to stick to schedule
- Related to reduced decision fatigue

## Physical Benefits
- Increased fat oxidation
- Improved metabolism throughout day
- Better glucose control
- Enhanced muscle growth

## Mental Benefits
- Improved mood (15% increase in positive affect)
- Reduced anxiety
- Better focus and concentration
- More energy throughout day

## Potential Drawbacks
- Very early exercise may impact sleep if too intense
- Requires earlier bedtime
- Gym may be crowded at peak hours
```

### Loop 3: Synthesize

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create this plan ✓
- [x] Phase 2: Search and gather scientific sources ✓
- [x] Phase 3: Analyze and synthesize findings ✓
- [x] Phase 4: Create comprehensive summary ✓
- [ ] Phase 5: Review and finalize

## Status
**Currently in Phase 5** - Final review and completion
```

**deliverable.md:**
```markdown
# Morning Exercise Benefits: Research Summary

## Executive Summary
Research from 15 scientific studies (2020-2025) demonstrates significant benefits of morning exercise for physical health, mental well-being, and long-term consistency. Morning exercise increases fat oxidation by 20%, improves mood scores by 15%, and creates 3x more consistent routines compared to exercise at other times.

## Physical Health Benefits

### Metabolism
- **Fat Oxidation:** 20% increase compared to evening exercise (Cell Metabolism, 2024)
- **Glucose Control:** Better blood sugar regulation throughout the day
- **Muscle Growth:** Enhanced protein synthesis during morning hours

### Long-term Health
- Improved cardiovascular health markers
- Better weight management outcomes
- Enhanced metabolic flexibility

## Mental Health Benefits

### Mood and Anxiety
- 15% improvement in positive mood scores (Psychology of Sport and Exercise, 2024)
- Reduced anxiety levels
- Better stress management

### Cognitive Benefits
- Improved focus and concentration throughout day
- Enhanced mental clarity
- Better decision-making capacity

## Consistency Factor

**Key Finding:** Morning exercise creates 3x more consistent routines.

**Why Morning Works:**
1. **Reduced Decision Fatigue** - Exercise time is non-negotiable
2. **Fewer Schedule Conflicts** - Less likely to be canceled
3. **Energy Boost** - Starts day with increased energy
4. **Sleep Improvement** - Tiredness leads to earlier bedtime

## Potential Drawbacks and Solutions

### Sleep Disruption
- **Issue:** Very intense early exercise may impact sleep
- **Solution:** Keep morning exercise moderate, finish 2+ hours before bed

### Scheduling Challenges
- **Issue:** Requires earlier wake time
- **Solution:** Gradually shift bedtime earlier (15 minutes per week)

### Gym Crowds
- **Issue:** Popular times may be crowded
- **Solution:** Exercise at home or find off-peak hours

## Recommendations

### For Beginners
1. Start with 20-30 minute moderate sessions
2. Choose enjoyable activities (walking, light jogging)
3. Gradually increase intensity over 4-6 weeks

### For Experienced Exercisers
1. Schedule most challenging workouts in morning
2. Use evening for light stretching or yoga
3. Track consistency metrics (aim for 6+ days/week)

### General Guidelines
- **Optimal Time:** 6:00-9:00 AM
- **Duration:** 30-60 minutes
- **Intensity:** Moderate (can hold conversation)
- **Pre-Exercise:** Light snack if needed
- **Post-Exercise:** Wait 30-60 minutes before large meal

## Conclusion

Scientific evidence strongly supports morning exercise for health benefits and long-term consistency. The combination of physiological advantages (improved metabolism, fat oxidation) and psychological benefits (better mood, reduced decision fatigue) makes morning exercise optimal for most people.

## Sources
- Cell Metabolism (2024): Exercise timing and fat oxidation
- Psychology of Sport and Exercise (2024): Morning exercise and mental health
- Sports Medicine (2023): Exercise consistency and timing
- [12 additional sources summarized]
```

## Example 2: Implementation Task - API Integration

**User Request:** "Integrate payment processing API into the checkout flow"

### Loop 1: Plan

**task_plan.md:**
```markdown
# Task Plan: Payment API Integration

## Goal
Integrate Stripe payment processing into the checkout flow for the e-commerce application.

## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Understand requirements and API documentation
- [ ] Phase 3: Design integration architecture
- [ ] Phase 4: Implement Stripe integration
- [ ] Phase 5: Add error handling and validation
- [ ] Phase 6: Test thoroughly
- [ ] Phase 7: Document and deploy

## Key Questions
1. What payment methods should be supported?
2. How should errors be handled?
3. What security requirements must be met?
4. How will we test without charging real cards?

## Technical Details
- Framework: React + Node.js
- Database: PostgreSQL
- Current checkout: Basic form submission
- Stripe account: Active (test mode)

## Status
**Currently in Phase 1** - Ready to review Stripe documentation
```

### Loop 2: Requirements

**Updated task_plan.md:**
```markdown
## Key Questions - Answers
1. **Payment Methods:** Credit/debit cards, Apple Pay, Google Pay
2. **Error Handling:** Display user-friendly messages, log technical details
3. **Security:** PCI compliance via Stripe, never store card data
4. **Testing:** Use Stripe test cards, automated test suite

## Decisions Made
- [2026-01-12 10:30] Use Stripe Elements for UI components
  Rationale: Handles PCI compliance automatically, customizable
- [2026-01-12 10:45] Implement webhook for payment confirmation
  Rationale: More reliable than client-side confirmation
- [2026-01-12 11:00] Store only payment intent ID, not card data
  Rationale: Security best practice, minimal liability

## Status
**Currently in Phase 3** - Designing integration architecture
```

**notes.md:**
```markdown
# Notes: Stripe Integration

## API Research

### Key Endpoints Needed
- POST /v1/payment_intents - Create payment
- POST /v1/payment_intents/{id}/confirm - Confirm payment
- POST /v1/webhooks - Handle payment events

### Security Requirements
- Never send card data to our servers
- Use Stripe Elements for card input
- Validate webhook signatures
- Use HTTPS only

### Integration Architecture
```
Frontend (React)
  ↓ Payment form (Stripe Elements)
  ↓ Create payment intent
Backend (Node.js)
  ↓ Process payment
  ↓ Stripe API
  ↓ Return result
Frontend
  ↓ Show confirmation
```

## Code Snippets

### Create Payment Intent (Backend)
```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

async function createPaymentIntent(amount, currency = 'usd') {
  return await stripe.paymentIntents.create({
    amount: amount, // in cents
    currency: currency,
    automatic_payment_methods: {
      enabled: true,
    },
  });
}
```

### Frontend Integration (React)
```jsx
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY);

function CheckoutForm() {
  return (
    <Elements stripe={stripePromise}>
      <Form />
    </Elements>
  );
}
```

## Environment Variables
- REACT_APP_STRIPE_PUBLISHABLE_KEY: pk_test_...
- STRIPE_SECRET_KEY: sk_test_...
- STRIPE_WEBHOOK_SECRET: whsec_...

## Testing Strategy
1. Use Stripe test card numbers
2. Test success scenarios
3. Test failure scenarios (insufficient funds, declined)
4. Test webhook delivery
5. Verify database records created
```

### Loop 3: Implementation

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [x] Phase 2: Understand requirements and API documentation ✓
- [x] Phase 3: Design integration architecture ✓
- [x] Phase 4: Implement Stripe integration ✓
- [x] Phase 5: Add error handling and validation ✓
- [x] Phase 6: Test thoroughly ✓
- [x] Phase 7: Document and deploy ✓

## Errors Encountered
- [2026-01-12 14:00] Webhook signature verification failed
  → Fix: Added raw body middleware before JSON parser
- [2026-01-12 15:30] CORS error on payment intent creation
  → Fix: Added Stripe domain to allowed origins

## Files Modified/Created
- src/components/CheckoutForm.jsx (modified)
- src/utils/stripe.js (created)
- src/hooks/usePayment.js (created)
- server/routes/payments.js (created)
- server/middleware/webhook.js (created)

## Status
**Task Complete** ✅
Deployed to staging on 2026-01-12
```

## Example 3: Multi-Stream Research

**User Request:** "Research the best approach for migrating our monolithic application to microservices"

### Loop 1: Plan

**task_plan.md:**
```markdown
# Task Plan: Microservices Migration Research

## Goal
Provide comprehensive analysis of microservices migration approaches with specific recommendations for our monolithic application.

## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Research migration strategies
- [ ] Phase 3: Analyze technical approaches
- [ ] Phase 4: Evaluate cost implications
- [ ] Phase 5: Assess team capabilities
- [ ] Phase 6: Synthesize findings
- [ ] Phase 7: Create recommendations report

## Research Streams

### Stream A: Migration Strategies
- Focus: Step-by-step migration approaches
- Target sources: 10+ articles and case studies
- Status: 0% complete
- File: stream_a_strategies.md

### Stream B: Technical Architecture
- Focus: Technology stack and architecture patterns
- Target sources: 8+ technical resources
- Status: 0% complete
- File: stream_b_technical.md

### Stream C: Cost Analysis
- Focus: Timeline, resources, and budget implications
- Target sources: 5+ case studies with metrics
- Status: 0% complete
- File: stream_c_costs.md

### Stream D: Team Readiness
- Focus: Skills assessment and training needs
- Target sources: 6+ resources on team preparation
- Status: 0% complete
- File: stream_d_team.md

## Key Questions
1. What are proven migration strategies?
2. What technical stack is recommended?
3. What is the realistic timeline and cost?
4. What skills does our team need?
5. What are common pitfalls to avoid?

## Status
**Currently in Phase 2** - Starting Stream A research
```

### Loop 2: Research Streams

**Updated task_plan.md:**
```markdown
## Research Streams

### Stream A: Migration Strategies
- Progress: 75%
- Next: Complete strangler pattern case studies
- File: stream_a_strategies.md
- Key finding: Strangler pattern most recommended

### Stream B: Technical Architecture
- Progress: 60%
- Next: Research service mesh options
- File: stream_b_technical.md
- Key finding: Kubernetes + Docker most common

### Stream C: Cost Analysis
- Progress: 80%
- Next: Finalize budget estimates
- File: stream_c_costs.md
- Key finding: 12-18 month timeline typical

### Stream D: Team Readiness
- Progress: 40%
- Next: Assess current team skills
- File: stream_d_team.md
- Key finding: 3-6 months training needed

## Integration Plan
Will synthesize all streams in Phase 6
```

**Notes excerpt from stream_a_strategies.md:**
```markdown
# Stream A: Migration Strategies

## Strangler Pattern (Most Recommended)
**Approach:** Gradually replace pieces of monolith with microservices
**Benefits:**
- Low risk, can roll back
- Incremental delivery
- Learn as you go

**Process:**
1. Identify edge functionality
2. Extract to microservice
3. Route traffic to new service
4. Repeat

**Case Studies:**
- Netflix: Migrated over 2 years
- Amazon: Continuous strangulation approach

## Other Patterns
1. **Branch by Abstraction**
   - Create abstraction layer
   - Gradually move functionality

2. **Database Decomposition**
   - Extract database first
   - Then extract services

## Recommendation
**Strangler pattern** for our migration
- Lower risk
- Better learning opportunity
- Easier to implement incrementally
```

### Loop 3: Synthesize

**Final deliverable.md:**
```markdown
# Microservices Migration: Strategic Analysis and Recommendations

## Executive Summary
After researching 4 critical streams (strategies, technical architecture, costs, team readiness), we recommend a **strangler pattern** approach using **Kubernetes and Docker** over an **18-month timeline** with **$250K budget** and **6 months team training**.

## Research Methodology
- **Stream A:** 12 migration strategy resources analyzed
- **Stream B:** 8 technical architecture resources
- **Stream C:** 5 cost case studies reviewed
- **Stream D:** 6 team readiness assessments
- **Total:** 31 authoritative sources

## Recommendation 1: Migration Strategy - Strangler Pattern

### Why Strangler?
- **Lower Risk:** Can rollback at any point
- **Incremental Value:** Delivers benefits as you go
- **Learning Opportunity:** Team learns microservices while migrating
- **Proven:** Used successfully by Netflix, Amazon, others

### Implementation Approach
```
Month 1-3:  Extract edge service (authentication)
Month 4-6:  Extract user management
Month 7-9:  Extract payment processing
Month 10-12: Extract remaining core services
Month 13-15: Decompose database
Month 16-18: Optimize and finalize
```

## Recommendation 2: Technical Stack - Kubernetes

### Recommended Stack
- **Containers:** Docker
- **Orchestration:** Kubernetes
- **Service Mesh:** Istio (for advanced features)
- **API Gateway:** Kong or Istio Gateway
- **Monitoring:** Prometheus + Grafana

### Why This Stack?
- Industry standard (reduces risk)
- Excellent tooling ecosystem
- Strong community support
- Proven at scale

## Recommendation 3: Timeline and Budget - 18 Months, $250K

### Timeline Breakdown
- **Planning & Training:** 6 months
- **Migration Execution:** 12 months
- **Total:** 18 months

### Budget Breakdown
- **Team Training:** $60K
- **Infrastructure:** $80K
- **Tooling & Licenses:** $40K
- **Consulting/Expertise:** $50K
- **Contingency (10%):** $20K
- **Total:** $250K

## Recommendation 4: Team Readiness - 6 Month Training Plan

### Current State Assessment
**Strengths:**
- Strong JavaScript/Node.js skills
- Agile development experience
- DevOps knowledge present

**Gaps:**
- Limited Docker experience
- No Kubernetes knowledge
- Monolithic architecture mindset

### Training Plan
**Months 1-2: Foundation**
- Docker fundamentals
- Microservices principles
- Service design patterns

**Months 3-4: Intermediate**
- Kubernetes basics
- Service mesh concepts
- CI/CD for microservices

**Months 5-6: Advanced**
- Production Kubernetes
- Monitoring and observability
- Security best practices

## Common Pitfalls to Avoid

1. **Big Bang Approach**
   - ❌ Migrate everything at once
   - ✅ Strangler pattern incrementally

2. **No Clear Boundaries**
   - ❌ Services too fine-grained
   - ✅ Domain-driven design

3. **Ignoring Data Consistency**
   - ❌ Separate databases with no strategy
   - ✅ Saga pattern for distributed transactions

4. **Skipping Testing**
   - ❌ Limited automated testing
   - ✅ Comprehensive test pyramid

5. **No Observability**
   - ❌ Limited monitoring/logging
   - ✅ Full observability from day one

## Next Steps

### Immediate (Week 1-2)
1. Present recommendations to leadership
2. Get budget approval
3. Begin training program planning

### Short-term (Month 1-3)
1. Start Docker training
2. Set up Kubernetes development environment
3. Identify first service to extract (authentication)

### Medium-term (Month 4-12)
1. Execute strangler pattern migration
2. Train team continuously
3. Build observability capabilities

### Success Metrics
- **Year 1:** 25% of functionality in microservices
- **Year 2:** 75% of functionality in microservices
- **Year 3:** 100% migration complete
- **Ongoing:** Deployment frequency 10x improvement
- **Ongoing:** Mean time to recovery < 5 minutes

## Conclusion

Microservices migration is achievable with proper planning, training, and incremental approach. The strangler pattern minimizes risk while delivering continuous value. Budget of $250K over 18 months is realistic based on industry benchmarks.

The key to success: **Start with team training** while planning the first extraction. Don't rush the process - take time to learn and build capabilities.
```

## Key Takeaways from Examples

### Example 1 (Research)
- Clear planning with defined phases
- Comprehensive notes with citations
- Synthesized findings into actionable summary
- Answered all key questions

### Example 2 (Implementation)
- Technical decisions documented with rationale
- Error tracking for learning
- File-by-file tracking of changes
- Successful completion with deployment

### Example 3 (Multi-Stream)
- Parallel research streams tracked
- Progress monitoring per stream
- Integration plan for synthesis
- Comprehensive final report

### Common Patterns
✅ Plan-first approach
✅ Progress tracking with checkboxes
✅ Error documentation
✅ Decision rationale
✅ File-based coordination
✅ Context refresh before decisions
