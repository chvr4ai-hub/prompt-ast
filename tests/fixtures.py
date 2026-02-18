"""
Comprehensive test fixtures for heuristic parser.
Contains 20 real-world prompts across multiple domains with golden expected outputs.

Each fixture contains:
- description: human-readable test intent
- domain: stable category used by coverage assertions
- prompt: input prompt text
- expected_ast: golden output from the heuristic parser
"""

from __future__ import annotations

FIXTURES = [
    # Software Engineering (4 prompts)
    {
        "description": "Code review request with explicit sections",
        "domain": "software",
        "prompt": """Context: We have a Python API endpoint that handles user authentication.
Task: Review the security implications of storing passwords in plain text.
Constraints:
- Focus on security best practices
- Suggest concrete improvements
Output: Provide a bullet-point list""",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": "We have a Python API endpoint that handles user authentication.",
            "task": "Review the security implications of storing passwords in plain text.",
            "constraints": [
                "Focus on security best practices",
                "Suggest concrete improvements",
                "Provide a bullet-point list",
            ],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Architecture design with markdown headers",
        "domain": "software",
        "prompt": """## Context
We're building a microservices architecture for an e-commerce platform.

## Task
Design a scalable order processing service.

## Constraints
- Must handle 10k orders/minute
- Use event-driven architecture
- Be concise""",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": "We're building a microservices architecture for an e-commerce platform.",
            "task": "Design a scalable order processing service.",
            "constraints": [
                "Must handle 10k orders/minute",
                "Use event-driven architecture",
                "Be concise",
            ],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Debugging request with vague task (should detect ambiguity)",
        "domain": "software",
        "prompt": "Help me fix this bug.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "Help me fix this bug.",
            "constraints": [],
            "assumptions": [],
            "ambiguities": [
                "Task is too vague - missing details about what bug, what code, what symptoms"
            ],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "API design with role and constraints",
        "domain": "software",
        "prompt": "Act as a senior API architect. Design a REST API for a blog platform. Use JSON. Be detailed.",
        "expected_ast": {
            "version": "0.1",
            "role": "senior API architect",
            "context": None,
            "task": "Design a REST API for a blog platform.",
            "constraints": ["Be detailed"],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": "json", "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    # Data Analysis (3 prompts)
    {
        "description": "Data cleaning with audience specification",
        "domain": "data",
        "prompt": "Explain how to clean messy CSV data for beginners. Use step-by-step instructions.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "Explain how to clean messy CSV data for beginners.",
            "constraints": ["Use step-by-step instructions", "For beginners"],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Visualization request with output format",
        "domain": "data",
        "prompt": "Create a visualization strategy for sales data. Output as YAML with sections: Data Sources, Chart Types, Tools.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "Create a visualization strategy for sales data.",
            "constraints": [],
            "assumptions": [],
            "ambiguities": ["Missing context about sales data structure and volume"],
            "output_spec": {
                "format": "yaml",
                "structure": ["Data Sources", "Chart Types", "Tools"],
                "language": None,
            },
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Statistical analysis with numbered sections",
        "domain": "data",
        "prompt": """1. Context: Dataset with 10k customer records
2. Task: Perform correlation analysis between age and purchase frequency
3. Output: Statistical report in markdown""",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": "Dataset with 10k customer records",
            "task": "Perform correlation analysis between age and purchase frequency",
            "constraints": [],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": "markdown", "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    # Content Creation (3 prompts)
    {
        "description": "Blog writing with word limit",
        "domain": "content",
        "prompt": "Write a blog post about AI ethics in 500 words. Use a professional tone.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "Write a blog post about AI ethics in 500 words.",
            "constraints": ["500 words", "Professional tone"],
            "assumptions": [],
            "ambiguities": ["Missing target audience specification"],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Social media content with casual tone",
        "domain": "content",
        "prompt": "You are a social media manager. Create 3 tweet ideas about sustainable living. Be casual and engaging.",
        "expected_ast": {
            "version": "0.1",
            "role": "social media manager",
            "context": None,
            "task": "Create 3 tweet ideas about sustainable living.",
            "constraints": ["Casual tone", "Engaging"],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Technical documentation",
        "domain": "content",
        "prompt": "Document the installation process for our CLI tool. Use bullet points. Include troubleshooting steps.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "Document the installation process for our CLI tool.",
            "constraints": ["Use bullet points", "Include troubleshooting steps"],
            "assumptions": [],
            "ambiguities": [
                "Missing context about which CLI tool and target platforms"
            ],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    # Education (2 prompts)
    {
        "description": "Lesson planning",
        "domain": "education",
        "prompt": "As a high school teacher, create a lesson plan for teaching photosynthesis. Make it interactive and engaging.",
        "expected_ast": {
            "version": "0.1",
            "role": "high school teacher",
            "context": None,
            "task": "create a lesson plan for teaching photosynthesis.",
            "constraints": ["Interactive", "Engaging"],
            "assumptions": [],
            "ambiguities": ["Missing class duration and student prior knowledge level"],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Concept explanation with ELI5",
        "domain": "education",
        "prompt": "Explain quantum entanglement like I'm 5. Keep it under 100 words.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "Explain quantum entanglement like I'm 5.",
            "constraints": ["Explain like I'm 5", "Under 100 words"],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    # Business (2 prompts)
    {
        "description": "Strategy with background context",
        "domain": "business",
        "prompt": """Background: Our SaaS startup has 1000 users but low retention.
Goal: Develop a customer retention strategy.
Requirements: Focus on product improvements and communication.""",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": "Our SaaS startup has 1000 users but low retention.",
            "task": "Develop a customer retention strategy.",
            "constraints": ["Focus on product improvements and communication."],
            "assumptions": [],
            "ambiguities": ["Missing specific retention metrics and churn reasons"],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Process optimization",
        "domain": "business",
        "prompt": "Analyze our customer onboarding process and suggest improvements. Output as a table with: Current Step, Issue, Proposed Solution.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "Analyze our customer onboarding process and suggest improvements.",
            "constraints": [],
            "assumptions": [],
            "ambiguities": ["Missing details about current onboarding process"],
            "output_spec": {
                "format": "table",
                "structure": ["Current Step", "Issue", "Proposed Solution"],
                "language": None,
            },
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    # Creative (2 prompts)
    {
        "description": "Storytelling",
        "domain": "creative",
        "prompt": "Write a short story about a time traveler. Set in Victorian London. Keep it under 300 words.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "Write a short story about a time traveler.",
            "constraints": ["Set in Victorian London", "Under 300 words"],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Brainstorming",
        "domain": "creative",
        "prompt": "Brainstorm 10 unique product names for an eco-friendly water bottle. Be creative and catchy.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "Brainstorm 10 unique product names for an eco-friendly water bottle.",
            "constraints": ["Creative", "Catchy"],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    # Research (2 prompts)
    {
        "description": "Literature review",
        "domain": "research",
        "prompt": """Context: Researching machine learning in healthcare
Task: Summarize recent papers on ML for disease diagnosis
Constraints: Focus on 2023-2024 publications, include methodology overview
Result: Structured summary in JSON""",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": "Researching machine learning in healthcare",
            "task": "Summarize recent papers on ML for disease diagnosis",
            "constraints": [
                "Focus on 2023-2024 publications, include methodology overview"
            ],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": "json", "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Hypothesis formation",
        "domain": "research",
        "prompt": "What are potential research questions about social media's impact on teen mental health? List 5 testable hypotheses.",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "What are potential research questions about social media's impact on teen mental health?",
            "constraints": ["List 5 testable hypotheses"],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    # General (2 prompts)
    {
        "description": "Simple Q&A",
        "domain": "general",
        "prompt": "What is the capital of France?",
        "expected_ast": {
            "version": "0.1",
            "role": None,
            "context": None,
            "task": "What is the capital of France?",
            "constraints": [],
            "assumptions": [],
            "ambiguities": [],
            "output_spec": {"format": None, "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
    {
        "description": "Complex multi-part request",
        "domain": "general",
        "prompt": """Act as a technical consultant.

Context: Client has a legacy monolith written in Java 8.

Task: Provide a migration roadmap to microservices.

Constraints:
- Minimize downtime
- Budget: $100k
- Timeline: 6 months
- No code examples needed

Output: YAML with phases and milestones""",
        "expected_ast": {
            "version": "0.1",
            "role": "technical consultant",
            "context": "Client has a legacy monolith written in Java 8.",
            "task": "Provide a migration roadmap to microservices.",
            "constraints": [
                "Minimize downtime",
                "Budget: $100k",
                "Timeline: 6 months",
                "No code examples needed",
            ],
            "assumptions": [],
            "ambiguities": ["Missing details about monolith size and complexity"],
            "output_spec": {"format": "yaml", "structure": [], "language": None},
            "metadata": {"extracted_by": "heuristic", "confidence": 0.55},
        },
    },
]
