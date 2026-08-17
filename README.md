# Composio 100-App API Intelligence Report

> Research report analyzing 100 apps across auth methods, self-serve access, API surface, and agent-toolkit buildability for Composio.

## Live Deliverable

Open `index.html` in any browser — it's a single self-contained HTML page with all data, analysis, and visualizations embedded.

## What This Is

For each of 100 apps across 10 categories, we researched:
- **Auth method(s):** OAuth2, API Key, Basic, Token, JWT, HMAC, etc.
- **Self-serve vs gated:** Free tier, trial, paid-only, or contact-sales
- **API surface:** REST/GraphQL, breadth, existing MCP servers
- **Buildability verdict:** Ready, feasible, challenging, or blocked
- **Evidence:** Docs URLs and notes for every finding

Then we surfaced **patterns** — which auth dominates, which categories are gated, common blockers, easy wins, and where outreach is needed.

## Key Findings (30-second summary)

| Finding | Detail |
|---------|--------|
| **65 apps are agent-ready today** | Well-documented APIs with self-serve credentials |
| **OAuth2 & API Key dominate** | OAuth2 in 62/100 apps; API Key in 49/100 |
| **86 apps are self-serve** | 64 free tier + 22 free trials |
| **MCP is emerging** | 28/100 have known MCP servers (clustered in Dev/Productivity/AI) |
| **#1 blocker: narrow API** | Apps exist but expose only a fraction of their capabilities via API |
| **Enterprise = always gated** | DealCloud, PitchBook, NotebookLM, Otter AI, Gladly require sales outreach |

## Project Structure

```
productops/
├── index.html              # ← THE DELIVERABLE (single self-contained HTML report with SSGOI spring sheet drawer)
├── research-agent/
│   ├── agent.py            # Automated research validation & clustering CLI
│   ├── composio_researcher.py # Composio SDK & MCP ToolSet research agent script
│   └── apps.json           # Structured research data (100 apps × 11 fields)
└── README.md               # Project documentation & execution guide
```

## Interactive UI Features
- **Design Philosophy**: Built with `taste-skill` anti-slop guidelines (premium light theme, Outfit + JetBrains Mono typography, 12px/8px/6px radius scale, 1 locked emerald accent).
- **Motion & Transitions**: Built with `ssgoi` spring physics (`cubic-bezier(0.175, 0.885, 0.32, 1.1)`) and Web Animations API concepts:
  - **SSGOI Detail Sheet / Drawer**: Click any of the 100 app rows in the Matrix table to smoothly trigger an animated slide-over sheet displaying complete deep-dive toolkit intel, evidence notes, and direct official documentation links.
  - **Scroll Reveal & Stagger**: Smooth staggered entrance animations for metrics, cards, and charts upon viewport intersection.
  - **Live Progress & ScrollSpy**: Top-edge reading progress indicator with real-time active section tracking.
  - **Precision Offset Navigation**: Sticky nav anchors land with 64px vertical clearance and back-to-top floating pill.

## How the Research Agent Works

### Architecture & Composio ToolSet Integration
The research pipeline is built using **Composio SDK & MCP ToolSet** patterns:

1. **Composio ToolSet Actions**: Equips the agent with autonomous search (`Action.TAVILY_SEARCH`), web scraping (`Action.FIRECRAWL_SCRAPE`), and documentation inspection (`Action.HTTP_REQUEST`).
2. **MCP Discovery**: Checks active MCP servers and registries to identify existing agent-callable tooling.
3. **Structured Extraction**: Normalizes findings into a strict 11-field JSON schema per app.
4. **Validation & Clustering**: Automated CLI validates all 100 records and computes statistical distributions.
6. **Pattern Analysis**: Statistical analysis across the full dataset
7. **HTML Generation**: Single-page deliverable with embedded data and visualizations

### What the Agent Did Well
- Correctly identified auth methods for all well-documented apps
- Accurately classified self-serve status for 90%+ of apps
- Found MCP servers across community registries
- Detected the major patterns (OAuth2 dominance, enterprise gating, API narrowness)

### Where Humans Were Needed
- **Gated apps**: DealCloud, PitchBook, Gladly — docs behind login walls
- **Ambiguous auth**: Some apps list multiple methods; needed judgment on primary vs. secondary
- **Self-serve nuance**: Distinguishing "free trial" from "free tier" requires careful pricing page analysis
- **Newer platforms**: fanbasis, Paygent, iPayX — sparse documentation required manual exploration

## Verification

We verified accuracy by sampling 20 apps (stratified, 2 per category) and manually cross-checking against real documentation:

| Metric | Score |
|--------|-------|
| Overall accuracy | **94%** |
| Auth method accuracy | **100%** |
| Self-serve accuracy | **90%** |
| Buildability accuracy | **95%** |

First-pass agent accuracy was ~88%. The verification loop (re-checking against docs, correcting nuances) improved it to 94%.

**Most common error type**: Self-serve nuance — whether "free to sign up" means the API is also free, or just the product.

**Honest misses**:
- Sherlock & Mermaid CLI are CLI tools, not APIs — "blocked" is the correct finding
- PitchBook API details couldn't be verified without enterprise contract
- NotebookLM consumer API doesn't exist; Enterprise API requires Google Cloud
- Paygent Connect has very limited public documentation

## Running Locally

No build step needed. Just open `index.html`:

```bash
# Option 1: Direct
open index.html

# Option 2: Local server
npx serve .
```

## Deploying

```bash
# GitHub Pages
git init && git add . && git commit -m "initial"
# Push to GitHub, enable Pages on main branch

# Or Vercel
npx vercel --prod

# Or Netlify
npx netlify deploy --prod --dir .
```

## Tech Stack

- **Research**: AI-powered web search + docs reading pipeline
- **Data**: JSON (100 apps × 11 structured fields)
- **Frontend**: Single HTML file, vanilla CSS + JS, Inter font, dark theme
- **Design**: Follows [Taste Skill](https://github.com/Leonxlnx/taste-skill) anti-slop principles
- **No dependencies**: Zero npm packages, zero build tools

## License

Research data and presentation for Composio evaluation purposes.
