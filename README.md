# 🧠 Nexus: Deep Research & Content Architect

> **An autonomous deep-agent that thinks, plans, researches in parallel, and adapts to you.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/Architecture-Map%20Reduce-orange)
![State](https://img.shields.io/badge/State-Pydantic%20Typed-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**Nexus** is a production-grade Deep Agent built with **LangGraph** and **LangChain**. Unlike standard chatbots, Nexus employs a **Map-Reduce architecture** to perform parallelized research, maintains **long-term memory** of user preferences, and includes a **Human-in-the-Loop** workflow for quality assurance.

---

## 🏗️ Architecture

Nexus operates on a cyclic state graph designed for complex reasoning tasks.

```mermaid
graph TD
    User(User Request) --> Planner
    Planner -->|Generates Research Plan| MapNode{Distribute}
    
    subgraph Parallel Research [Map-Reduce Layer]
        MapNode -->|Thread 1| Worker1[Search Worker 1]
        MapNode -->|Thread 2| Worker2[Search Worker 2]
        MapNode -->|Thread 3| Worker3[Search Worker 3]
    end
    
    Worker1 --> Reducer[Writer Node]
    Worker2 --> Reducer
    Worker3 --> Reducer
    
    Reducer -->|Draft Content| Human{Human Review}
    Human -->|Feedback / Critique| Reducer
    Human -->|Approve| End((Final Output))