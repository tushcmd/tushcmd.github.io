"""Site content."""

SITE = {
    "name": "Muturi David",
    "handle": "Tush",
    "url": "https://tushdev.co",
    "email": "muturidavid854@gmail.com",
    "role": "Full-stack and mobile engineer // Product Engineer",
    "description": "Muturi David (Tush) is a full-stack web and mobile engineer in Kenya.",
    "bio_points": [
        "Full-stack and mobile engineer based in Kenya.",
        "About three years of professional work in JavaScript and Python.",
        "Building products for businesses running on M-Pesa.",
        "Exploring Rust for systems programming.",
    ],
    "location": "Kenya",
    "exploring": "Rust / Systems",
}

# (label, href, icon file name in static/icons/)
LINKS = [
    ("GitHub", "https://github.com/tushcmd", "github"),
    ("LinkedIn", "https://linkedin.com/in/tushdev", "linkedin"),
    ("X", "https://x.com/0xtush", "x"),
    ("Email", "mailto:muturidavid854@gmail.com", "mail"),
    ("Resume", "/assets/Muturi_David_Resume.pdf", "file"),
]

# Hero portrait backdrop: "tile" (the blue from the original art), "tint" (follows the theme accent) or "clear" (no tile).
AVATAR_STYLE = "tile"

NAV = [
    ("Projects", "/projects/"),
    ("Writing", "/writing/"),
    ("Stack", "/stack/"),
    # ("Now", "/now/"),
]

WORK = [
    {
        "name": "Solo, FNewsteer",
        "href": "https://tushcmd.github.io/fns-fe/",
        "current": True,
        "when": "Mar 2026 - now",
        "points": [
            "Trading loss-prevention app built around forex news blackout windows.",
            "One Python backend feeds a web dashboard, a Chrome extension, a mobile app and an MCP server for Claude Desktop.",
        ],
    },
    {
        "name": "Frontend Engineer, MicroRootsKe",
        "when": "ERP",
        "points": [
            "Interface for an ERP that runs AI-assisted microgreens production.",
            "Next.js, Tailwind CSS and shadcn/ui.",
        ],
    },
    {
        "name": "Software Engineering Intern, COSEKE Kenya",
        "when": "Aug 2025 - Feb 2026",
        "points": [
            "Built and maintained React dashboards for an enterprise document management SaaS.",
            "Worked with designers and backend engineers on responsive, accessible interfaces.",
            "Integrated REST APIs and tuned performance.",
        ],
    },
    {
        "name": "Software Engineering Fellow and Resident, Headstarter",
        "when": "Jul 2024 - Mar 2025",
        "points": [
            "Shipped an AI churn prediction model, an image generation tool and a SaaS learning platform.",
            "Used React, Next.js, Firebase, OpenAI and AWS, with CI/CD in agile teams.",
        ],
    },
]

# Entries with a slug get a case study page at /projects/<slug>/
PROJECTS = [
    {
        "name": "FNewsteer",
        "slug": "fnewsteer",
        "when": "Web / Mobile / API",
        "points": [
            "Warns traders before high-impact news and keeps them out of blackout windows.",
            "Android home screen widget and push alerts.",
        ],
        "stack": ["FastAPI", "Next.js", "Expo", "FastMCP"],
        "links": [("Live", "https://tushcmd.github.io/fns-fe/"), ("Code", "https://github.com/tushcmd/fnewsteer")],
        "featured": True,
    },
    {
        "name": "Kenya Import Duty Calculator",
        "slug": "import-duty-calc",
        "when": "Public tool",
        "points": [
            "Estimates import duty on vehicles, motorcycles and machinery from the KRA CRSP schedules.",
            "Matches KRA's own template to six decimal places.",
        ],
        "stack": ["FastAPI", "SQLite", "Next.js"],
        "links": [("Live", "https://import-duty-calc.vercel.app/"), ("Code", "https://github.com/tushcmd/import-duty-calc")],
        "featured": True,
    },
    # {
    #     "name": "MukWamb Capital",
    #     "when": "Fintech",
    #     "points": [
    #         "Loan management for Kenyan microfinance, with admin and borrower portals.",
    #         "M-Pesa STK Push, paybill reconciliation and OTP sign-in by SMS.",
    #     ],
    #     "stack": ["Next.js", "PostgreSQL", "Drizzle", "Daraja"],
    #     "links": [],
    #     "featured": True,
    # },
    {
        "name": "MicroRootsKe ERP",
        "when": "Frontend",
        "points": ["Interface for an ERP that runs AI-assisted microgreens production."],
        "stack": ["Next.js", "Tailwind CSS", "shadcn/ui"],
        "links": [],
    },
    {
        "name": "Flashcards SaaS",
        "when": "~50 users in week one",
        "points": [
            "GPT-4 flashcard generation with Stripe subscriptions.",
            "Real-time CRUD on Firestore.",
        ],
        "stack": ["Next.js", "Clerk", "Firebase", "Stripe"],
        "links": [],
    },
    {
        "name": "AI Customer Support Chat Bot",
        "when": "AI",
        "points": [
            "Support chatbot with authentication and feedback.",
            "PostgreSQL and Prisma backend serving concurrent sessions at 99.9% uptime.",
        ],
        "stack": ["Next.js", "Prisma", "PostgreSQL", "OpenAI"],
        "links": [],
    },
    # {
    #     "name": "Rilla Voice",
    #     "when": "Hackathon finalist",
    #     "points": [
    #         "Led the frontend for a team of five.",
    #         "Transcript viewer with comments and LLM-written summaries.",
    #     ],
    #     "stack": ["React", "TypeScript", "AWS Lambda", "DynamoDB"],
    #     "links": [],
    # },
    {
        "name": "Credit Card Fraud Detection",
        "when": "Machine learning",
        "points": [
            "Flags fraudulent transactions in a simulated set of 1,000 customers and 800 merchants.",
            "Handles class imbalance and feature selection.",
        ],
        "stack": ["Python", "scikit-learn", "Pandas"],
        "links": [ ("Code", "https://github.com/tushcmd/fraud-detection")],
    },
    {
        "name": "Brain Tumor Classification",
        "when": "Computer vision",
        "points": [
            "Custom-trained neural network that classifies 1,000 MRI scans into three conditions.",
            "Drafts a report in under 200 ms.",
        ],
        "stack": ["Python", "Keras", "Neural networks"],
        "links": [("Code", "https://github.com/tushcmd/brain-tumor-classification")],
    },
]

STACK = [
    ("Languages", "JavaScript, TypeScript, Python, SQL. Learning Rust."),
    ("Frontend", "React, Next.js (App Router), React Native, Expo, NativeWind, Tailwind CSS, shadcn/ui"),
    ("Backend", "Node.js, Express, FastAPI, SQLAlchemy, Drizzle, Prisma, BetterAuth, Clerk"),
    ("Data", "PostgreSQL, Neon, SQLite, MongoDB, Firebase Firestore"),
    ("Infrastructure", "Docker, GitHub Actions, GHCR, Render,  Cloudflare (DNS, R2), AWS (Lambda, S3, DynamoDB)"),
    ("Payments, messaging", "M-Pesa Daraja, Stripe"),
    ("AI and ML", "OpenAI API, FastMCP, Keras, scikit-learn, Pandas"),
    ("Tooling", "Git, GitHub, Bash, Figma, uv"),
]

LEARNING = [
    "Rust for systems programming",
    # "C and ARM assembly",
    "RHCSA (EX200, RHEL 9), with a homelab on Rocky Linux and AlmaLinux",
    "Computer architecture and networking",
]

# NOW = {
#     "updated": "October 2026",
#     "items": [
#         ("Building", "FNewsteer: the mobile app, the Chrome extension and the MCP server that sit on one shared backend."),
#         ("Shipping", "The frontend for the MicroRootsKe ERP with Next.js, Tailwind CSS and shadcn/ui."),
#         ("Learning", "Rust for systems programming, and RHCSA preparation in a Linux homelab."),
#         ("Writing", "Notes on shipping AI features, support bots and dashboard design."),
#     ],
# }