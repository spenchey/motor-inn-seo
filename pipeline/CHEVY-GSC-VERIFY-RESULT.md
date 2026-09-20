# Chevrolet Google Search Console verification result

- Recorded: 2026-09-20 17:56 CDT (America/Chicago).
- Property: https://www.motorinnofcarroll.com/
- Account: spencer.heywood@motorinnmail.com.
- Outcome: **FAILED — incorrect HTML meta tag; ownership remains unverified.**
- Method: Google Search Console HTML tag verification, performed with computer control in Chrome.
- DealerOn case: 01919856.

## Verification performed

Opened the property URL in Chrome. Search Console showed “Oops, you don't have access to this property.” Selected **VERIFY YOUR OWNERSHIP**, expanded **HTML tag**, read the required token, and clicked that method's **VERIFY** button.

The required tag displayed by Search Console was:

```html
<meta name="google-site-verification" content="wuEnGcwCntRpyJ3Twx52YW9beweA6zGwhAeON_TVOVI" />
```

## Exact Google Search Console result

> Ownership verification failed
>
> Verification method:
> HTML tag
>
> Failure reason:
> Your meta tag is incorrect. Are you using a meta tag for a different site or user account?
>
> Found meta tag:

```text
pZSUgoqsI65kNZ_U1uzC74rYka8L50FlLAdB20ZPZRM
n-yUnBZDHaOarQJ9FX8XkBJLLjhIaERP24CK2lQrS2w
6Pu_nZHW3mOmPOWlXpakVF6LjJWQd9OxucfKgqwI9Ck
1pQWe-y2GWPSQnOuUUsAom7aU-A-AV39zFvJ2_x-rH8
wuEnGcwCntRpyJ3Twx52YW9beweA6zGwhAeON_TVOV
```

> Please fix your implementation and reverify, or use another verification method.

## Required correction

Google's result confirms that the installed token is missing its final uppercase `I`: found `TVOV`, required `TVOVI`. Correct this tag in the homepage `<head>` while preserving the other existing verification tags, then retry HTML tag verification after the correction is live.

A short local reply draft for DealerOn Gmail thread `1a0b525811343bf6` is saved in [chevy-tag-fix-draft.md](chevy-tag-fix-draft.md). **The email has not been sent.** No website changes or password entry occurred during this verification attempt.
