# Expert Panel: SEO Strategy (Eric Siu, github.com/ericosiu/ai-marketing-skills)
# GATE: any SEO plan, page-factory batch, or major content change scores >=90/100
# across all 10 experts before it reaches Spencer's approval queue. Under 90: rewrite
# weak parts, rescore, max 3 rounds; log every score delta in brain/LOG.md.

## The 10 Experts
1. **Technical SEO Specialist** — site architecture, crawlability, CWV, structured data
2. **Content Strategist** — clusters, gaps, SERP intent alignment
3. **Conversion Rate Optimizer** — does it connect to revenue, not traffic?
4. **Revenue Attribution Expert** — dollar outcomes tied to the recommendation?
5. **Competitive Analyst** — competitor moves, gaps (use brain/competitor-read-*.md)
6. **AI/AEO Specialist** — AI Overviews, ChatGPT citations, Perplexity accounted?
7. **Data Scientist** — statistically sound? real trend or noise? (n-sizes, windows)
8. **Growth Hacker** — fastest path to measurable results?
9. **Operations Expert** — feasible with current resources (DealerOn dependency? approvals?)
10. **ROI Calculator** — passes 4:1? expected return stated w/ assumptions?

## Scoring criteria (each expert scores /100 on these)
- Data backing: real data cited (GSC/GA4/DFS pulls), never projections alone
- Actionable specificity: exact next steps, no 'optimize content' vagueness
- ROI estimate quality: realistic, assumptions stated
- Risk assessment: honest failure modes
- Feasibility: executable with CURRENT resources (1 agent, DealerOn gate, Spencer approval)
- Alignment: serves Motor Inn goals (leads > traffic; Carrolls 51401 focus; no 50501 drift)

## Motor Inn scoring protocol
1. Run the plan/page through all 10 experts (LLM pass, 1 message per expert for
   independence; aggregate mean + min. Floor rule: if ANY expert <80, rewrite that
   dimension regardless of mean).
2. Under-90 mean => revise + rescore, max 3 rounds. Log every round: expert, score, change.
3. Final package to Spencer shows: final scores, per-expert one-line verdict, changes made.
4. Panels are cheap: run on the llama (GLM-5.3-Flash) batch, ~10 x 200 tokens.
