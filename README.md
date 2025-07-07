# **Building Multi-Agent Systems**

<iframe width="100%" height="400px" src="https://www.youtube.com/embed/n5vYcVVIurg?si=WlYtyrPx-UI8eGk3" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Multi-agent systems are fascinating. I once asked myself: what can multiple agents accomplish that a single agent cannot? I was wrong. 
!!! quote ""
    
    Anthropic's research shows that a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on their internal research evaluation. 

<div align="center">
  <img src="main.png" alt="Multi-Agent System" width="85%">
</div>

Multi-agent architectures are everywhere likely the deep research features from ChatGPT, Gemini, Perplexity and Grok all leverage multi-agent approaches under the hood.



!!! info "Code & Implementation"
    For this implementation, I leveraged the **OpenAI Agents SDK**.

    The complete source code and implementation details are available on GitHub: **[gauravreddy08/poogle](https://github.com/gauravreddy08/poogle)**

### **Step One: Multi means many**

> Multi means many, but more importantly, it means specialized.

A common pitfall when building multi-agent systems is expecting each agent to be a generalist. While LLMs are capable generalists, they excel when focused on a single, well-defined task.

In building my multi-agent search system, I divided the work into three precisely defined roles:

1. **Lead Agent**: The orchestrator responsible for overall search direction, task delegation, and shared memory management
2. **Search Agent**: A granular, single-purpose agent focused solely on web searches and communicating results through multiple search queries
3. **Answer Agent**: Synthesizes the final response using the initial query and curated shared memory context

> This granular delegation ensures each agent masters its domain rather than juggling multiple responsibilities.

### **Step Two: Think Like an Agent**

> To build effective agents, you must inhabit their perspective.

When designing the lead agent, I thought as an orchestrator would. What would I need?

<div align="center">
  <img src="lead-agent.png" alt="Thinking Like an Agent" width="70%">
</div>

- **Deliberation capability**: A mechanism to ponder and delegate tasks effectively achieved through reasoning abilities and tools to spawn multiple search agents
- **Quality control**: Search agents might return irrelevant data. Imagine searching for "perplexity loss function" and receiving results about Perplexity the company. Without filtering, this noise could derail the entire system. I built selective storage mechanisms so the lead agent curates what enters shared memory
- **Iterative exploration**: Search isn't single-shot. Humans build upon previous context, adjusting their trajectory as they learn. My lead agent can also spawn multiple search agents in loops until it finds what it needs. Sometimes it gets curious and explores tangentially (though I do set thresholds)


### **Step Three: Tokens Are Expensive (Optimization)**

> Multi-agent systems consume tokens voraciously. 

My approach: minimize the search model's output. Each search result gets a unique ID. When the research agent identifies useful results, it stores only the ID reference, Python code handles the actual storage. This eliminated redundant token generation where the research agent would otherwise regenerate large result chunks.

<div align="center">
  <img src="context-optimization.gif" alt="Optimization" width="100%">
</div>

> It's like using library call numbers instead of photocopying entire books, you get the same access with a fraction of the overhead.

#### **Some interesing traces:**

> Taken directly from OpenAI's Trace Logs.


??? quote "When is GTA VI releasing? What can I expect?"
    ```
    User asks:
    "When is GTA VI releasing? What can I expect?"

    Research Agent begins task planning and delegation...

    ├── Step 1: Sub-task: Find release date
    │   ├── Research Agent launches Search Agent
    │   │   → Query: "GTA VI release date"
    │   └── Search Agent returns result:
    │       → "GTA VI is officially set to release on May 26, 2026..."

    ├── Step 2: Sub-task: Find expected features
    │   ├── Research Agent launches another Search Agent
    │   │   → Query: "GTA VI expected features and gameplay elements"
    │   └── Search Agent returns result:
    │       → "Expected features include multiple cities (Vice City), multiple protagonists, improved AI..."

    ├── Step 3: Store findings in memory
    │   ├── Research Agent stores release date info
    │   │   → add_to_memory({ id: "01abf311-bce9..." })
    │   └── Research Agent stores gameplay features info
    │       → add_to_memory({ id: "ca011f09-6e7e..." })

    └── Step 4: Transfer to Answer Agent
        └── Research Agent hands off task
            → transfer_to_answer_agent()

    Answer Agent receives memory and generates final response for the user.
    ```

??? quote "What's the current status of Texas floods?"
    ```
    User asks:
    "What's the current status of Texas floods?"

    Answer Agent begins...

    ├── Step 1: Sub-task: Retrieve current info
    │   ├── Answer Agent launches Search Agent
    │   │   → Query: "Texas floods current status July 2025"
    │   └── Search Agent returns result:
    │       → "Severe flooding ongoing into July 2025; 79 dead, major damage in Kerr County..."

    ├── Step 2: Transfer to Answer Agent (self-triggered, final stage)
    │   └── Answer Agent prepares final user response
    │       → Extracts summary from search results:
    │          - 79 confirmed deaths
    │          - 27 children missing from Camp Mystic
    │          - Governor declared disaster + federal aid
    │          - 400+ first responders deployed
    │          - Massive river rise and displacement

    Final output: Concise report delivered to user.
    ```

??? quote "What is Big Beautiful Bill? Why is Elon against it?"
    ```
    User asks:
    "What is Big Beautiful Bill? Why is Elon against it?"

    Research Agent begins task planning and delegation...

    ├── Step 1: Sub-task: Why is Elon Musk against the bill?
    │   ├── Research Agent launches Search Agent
    │   │   → Query: "Why is Elon Musk against big beautiful bill?"
    │   └── Search Agent returns result:
    │       → Musk calls it “utterly insane and destructive,”
    │         criticizes cuts to EV tax credits, and suggests forming a new party.

    ├── Step 2: Sub-task: What is the Big Beautiful Bill?
    │   ├── Research Agent launches another Search Agent
    │   │   → Query: "What is the One Big Beautiful Bill proposed by Trump?"
    │   └── Search Agent returns result:
    │       → Bill includes:
    │           - Major tax cuts
    │           - Medicaid restrictions
    │           - Border wall funding
    │           - Elimination of clean energy incentives
    │           - $5T debt ceiling raise and $1.5T in cuts

    ├── Step 3: Store findings in memory
    │   ├── Research Agent stores Elon Musk’s response
    │   │   → add_to_memory({ id: "289e0869-c6cf..." })
    │   └── Research Agent stores bill details
    │       → add_to_memory({ id: "500606cd-69f9..." })

    └── Step 4: Transfer to Answer Agent
        └── Research Agent hands off task
            → transfer_to_answer_agent()

    Answer Agent receives memory and generates final response for the user.
    ```

#### **Looking Forward: Asynchronous Communication**

Current multi-agent systems lack true asynchronous execution. Real-world interactions are inherently asynchronous. Knowing *what* to say is only half the equation; knowing *when* to say it is equally crucial. That's the challenge I'm tackling next: teaching agents not just what to communicate, but when to break their silence.



???+ tip "Bonus: Poogle Questions | Starring Squid Game’s Lee Jung-jae"
    
    <iframe width="100%" height="400" src="https://www.youtube.com/embed/7x0lu6ZscAg?si=Hn5f5rWwDcWnSIvZ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

