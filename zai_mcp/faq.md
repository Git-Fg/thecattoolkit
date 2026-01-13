# FAQs

## GLM Coding Plan Details

**Q: How much usage quota does the plan provide?**

**A:** Subscribe once, unlock unmatched usage and unbeatable value.

* **Lite Plan**: Up to \~120 prompts every 5 hours — about 3× the usage quota of the Claude Pro plan.
* **Pro Plan**: Up to \~600 prompts every 5 hours — about 3× the usage quota of the Claude Max (5x) plan.
* **Max Plan**: Up to \~2400 prompts every 5 hours — about 3× the usage quota of the Claude Max (20x) plan.

In terms of token consumption, each prompt typically allows 15–20 model calls, giving a total monthly allowance of tens of billions of tokens — all at only \~1% of standard API pricing, making it extremely cost-effective.

> The above figures are estimates. Actual usage may vary depending on project complexity, codebase size, and whether auto-accept features are enabled.

***

**Q: Which models are supported? How can I switch between them?**

**A:** This plan is powered by Z.ai’s latest flagship models **GLM-4.7**, **GLM-4.6**, **GLM-4.5** and **GLM-4.5-Air**. Switching works as follows.

<Check>
  Mapping between Claude Code internal model environment variables and GLM models, with the default configuration as follows:

  * `ANTHROPIC_DEFAULT_OPUS_MODEL`: `GLM-4.7`
  * `ANTHROPIC_DEFAULT_SONNET_MODEL`: `GLM-4.7`
  * `ANTHROPIC_DEFAULT_HAIKU_MODEL`: `GLM-4.5-Air` If adjustments are needed, you can directly modify the configuration file (for example, \~/.claude/settings.json in Claude Code) to switch to GLM-4.5 or other models.
</Check>

***

**Q: Which coding tools are supported?**

**A:** The pack currently supports [**Claude Code, Roo Code, Kilo Code, Cline, OpenCode, Crush, Goose**](/devpack/tool/goose)]\(/devpack/tool/crush)]\(/devpack/tool/opencode)]\(/devpack/tool/cline)]\(/devpack/tool/kilo)]\(/devpack/tool/roo)]\(/devpack/tool/claude), and more. Please refer to our tool guide for step-by-step setup. All supported coding tools share the same usage quota under your subscription.

***

**Q: Can I use my GLM Coding Plan quota in non-AI coding tools?**

**A:**  No. The GLM Coding Plan quota is **only** intended to be used within coding/IDE tools designated or recognized by [Z.ai](http://Z.ai) (such as Claude Code, Kilo Code, etc.) for personal code-assistance scenarios in your local IDE or terminal.

If you want to integrate GLM models into your own applications, websites, bots, SaaS products or other systems via API, please use [Z.ai](http://Z.ai)’s enterprise-grade API / MaaS services and follow the corresponding terms and pricing.

***

**Q: Can the plan only be used within supported coding tools?**

**A:** Yes. API calls are billed separately and do not use the Coding Plan quota.

***

**Q: What happens when my plan quota runs out? Will the system consume my account balance?**

**A:** No. GLM-4.7 calls made in supported coding tools will **only** use your Coding Plan quota.

* Once the quota is used up, you’ll need to wait until the next **5-hour cycle** for it to refresh. The system will not deduct from your account balance.
* Users subscribed to the Coding Plan can only make calls via the plan’s quota in supported tools. API calls outside the plan are not available.

***

## MCP Call

**Q：Which plan supports Vision Understanding, Web Search and Web Reader MCP tools?**

**A：** All plans support these MCP tools, but the Lite plan includes only a limited quota for trial purposes.

***

**Q：What is the quota of Vision Understanding, Web Search and Web Reader MCP in the plan?**

**A：** The MCP quotas for the Lite, Pro and Max plans are as follows:

* **Lite Plan**:  Include a total of 100 web searches and web readers per month, along with the 5-hour maximum prompt resource pool of the package for vision understanding.
* **Pro Plan**: Include a total of 1,000 web searches and web readers per month, along with the 5-hour maximum prompt resource pool of the package for vision understanding.
* **Max Plan**: Include a total of 4,000 web searches and web readers per month, along with the 5-hour maximum prompt resource pool of the package for vision understanding.

***

**Q：Besides using the GLM Coding Plan resource package, can I use other methods to call these three MCP tools for Vision Understanding, Web Search and Web Reader?**

**A：** Other than the resource package, we currently do not provide any other access solutions for calling these three MCP tools. If you use other similar MCP tools and incur billing issues during their use, such issues are not within the scope of this package.

***

## Subscription Management

**Q: Will my subscription renew automatically?**

**A:** Yes. Your subscription will automatically renew at the end of each billing cycle, and the fee will be charged to your saved payment method.

***

**Q: How are subscription fees deducted?**

**A:** The system deducts fees in the following order:

1. Credits balance will be used first.
2. If insufficient, cash balance will be used;.
3. If still insufficient, the remaining amount will be charged from your linked payment method (e.g., bank card or PayPal).

<Tip>
  Please note that a small minimum applies when charging your credit card. If the remaining amount is less, we will round up the deduction to meet this minimum.
</Tip>

***

**Q: How can I cancel my subscription?**

**A:** You can cancel your subscription on the subscription management page. Please make sure to cancel at least 24 hours before your next billing date to avoid auto-renewal. After cancellation, your current plan remains valid until it expires.

***

**Q: Can I get a refund?**

**A:** Subscription payments are generally non-refundable. You can still use the service until the end of your billing cycle. For special cases, please contact customer support.

***

## Upgrade your Plan

**Q: How can I upgrade my plan?**

**A:** Go to your subscription page, choose “Upgrade,” and the change will take effect once the price difference is paid. Steps are as follows:

1. Go to your [subscription page](https://z.ai/subscribe?utm_source=zai\&utm_medium=index\&utm_term=glm-coding-plan\&utm_campaign=Platform_Ops&_channel_track_key=6lShUDnv).
2. Click “Subscribe” and select your desired plan.
3. Confirm the change.
4. The new plan will take effect after the current billing cycle ends.

***

**Q: How can I downgrade my plan?**

**A:** On the subsciption page, select your desired plan. The change will take effect after the current billing cycle ends. You can also cancel your current subscription and re-subscribe to the desired plan after the billing cycle ends. Steps are as follows:

1. Go to your [subscription page](https://z.ai/subscribe?utm_source=zai\&utm_medium=index\&utm_term=glm-coding-plan\&utm_campaign=Platform_Ops&_channel_track_key=6lShUDnv).
2. Click “Subscribe” and select your desired plan.
3. Confirm the change.
4. The new plan will take effect after the current billing cycle ends.

***

**Q: How can I change my billing cycle?**

**A:** On the subsciption page, select your desired plan. The change will take effect after the current billing cycle ends. You can also cancel your current subscription and re-subscribe to the desired plan after the billing cycle ends. Steps are as follows:

1. Go to your [subscription page](https://z.ai/subscribe?utm_source=zai\&utm_medium=index\&utm_term=glm-coding-plan\&utm_campaign=Platform_Ops&_channel_track_key=6lShUDnv).
2. Click “Subscribe” and select your desired billing cycle.
3. Confirm the change.
4. The new cycle will take effect after the current billing period ends.

***

## 'Invite Friends, Get Credits'

**Q: Where can I view the credits I earned?**

**A:** You can view your credit rewards in the \[Invite Friends, Earn Credits pop-up - Your Credit Rewards] or check the details under \[Billing - Transaction History].

***

**Q: Where can I use my credits? Can I withdraw them?**

**A:** Credits can be used on \[Z.ai platform] to offset various purchases, including subscriptions like GLM Coding Plan, resource packs, feature extensions, and API calls.

<Tip>
  Credits are promotional benefits and cannot be withdrawn, transferred, or refunded.
</Tip>

***

**Q: How is a successful invitation defined? What does my friend need to do?**

**A:** A successful invitation must meet all of the following:

1. The referred friend shall access the campaign page through the inviter's unique referral link or code.
2. Your friend is a new user (has never paid for a subscription).
3. They complete their first GLM Coding Plan subscription payment within 72 hours.
4. The order is not refunded within 24 hours.

***

**Q: When will I receive the credits after inviting a friend?**

**A:** Credits are usually issued within 24-48 hours after your friend’s payment is confirmed and the order passes review. Check \[Finance - Transaction History]. If not received after 72 hours, contact support.

***

**Q: What does "friend’s actual payment amount" mean? How are credits calculated if a coupon is used?**

**A:** "Actual payment amount" refers to the final cash amount your friend paid for their first order.

For example: If a plan costs 100 USD, and your friend gets a 50% first-order discount, an extra 10% off from your referral, and uses 5 USD in credits, the final actual payment is 40 USD. Your credits will be calculated based on 40 USD (e.g., 10% of 40 USD = 4 USD). Credit calculation does not include any coupons, discounts, point deductions, or refunded amounts.

***

**Q: Why didn’t I receive credits after referring a friend?**

**A:** Common reasons include:

1. Your friend didn’t register using your exclusive link/code.
2. Your friend completed payment after 72 hours.
3. Your friend was not a new subscribing user.
4. The order was refunded.
5. The system detected unusual activity (e.g., bulk registrations, fraud).

**If none of these apply, please contact customer support with your account and your friend’s registration information.**


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.z.ai/llms.txt