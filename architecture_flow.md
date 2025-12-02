# DocuMinds Multi-Agent System Architecture Flow Diagram

## Overall Architecture Diagram

```mermaid
graph TB
    Start([Document Upload]) --> Router[Router Agent<br/>Complexity Assessment]
    Router --> SimplePath[Simple Processing Path]
    Router --> ComplexPath[Complex Processing Path]

    SimplePath --> Extractor[Extractor Agent<br/>Data Extraction]
    Extractor --> Summarizer[Summarizer Agent<br/>Content Summary]
    Summarizer --> Output[Generate Output]

    ComplexPath --> Orchestrator[Orchestrator Agent<br/>Workflow Planning]
    Orchestrator --> Extractor2[Extractor Agent<br/>Deep Analysis]
    Extractor2 --> Analyzer[Analyzer Agent<br/>Content Analysis]
    Analyzer --> Validator[Validator Agent<br/>Quality Check]
    Validator --> Summarizer2[Summarizer Agent<br/>Insight Generation]
    Summarizer2 --> Output2[Generate Output]

    Output --> Memory[Save to Federated Memory]
    Output2 --> Memory2[Save to Federated Memory]

    Memory --> End([Complete])
    Memory2 --> End2([Complete])

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style End2 fill:#FFB6C1
    style Router fill:#FFE66D
    style Orchestrator fill:#4ECDC4
```

## Multi-Agent Interaction Architecture

```mermaid
graph LR
    subgraph "External API Layer"
        API[OpenAI GPT-4 API]
    end

    subgraph "Control Layer"
        Router[Router Agent<br/>Document Classification]
        Orchestrator[Orchestrator Agent<br/>Workflow Management]
        Memory[Federated Memory<br/>Knowledge Base]
    end

    subgraph "Processing Agent Layer"
        Extractor[Extractor Agent<br/>Data Extraction]
        Analyzer[Analyzer Agent<br/>Content Analysis]
        Summarizer[Summarizer Agent<br/>Insight Generation]
        Validator[Validator Agent<br/>Quality Assurance]
    end

    subgraph "Storage Layer"
        Redis[Redis Cache]
        Postgres[PostgreSQL Database]
    end

    Router --> Orchestrator
    Router --> Memory
    Orchestrator --> Extractor
    Orchestrator --> Analyzer
    Orchestrator --> Summarizer
    Orchestrator --> Validator

    Extractor --> API
    Analyzer --> API
    Summarizer --> API
    Validator --> API

    API -.Return Analysis.-> Extractor
    API -.Return Analysis.-> Analyzer
    API -.Return Analysis.-> Summarizer
    API -.Return Analysis.-> Validator

    Memory --> Redis
    Memory --> Postgres

    style Router fill:#FFE66D
    style API fill:#FF6B6B
    style Orchestrator fill:#4ECDC4
```
## Simple Document Processing Flow

```mermaid
sequenceDiagram
    participant User as User
    participant API as FastAPI Server
    participant Router as Router Agent
    participant Extractor as Extractor Agent
    participant Summarizer as Summarizer Agent
    participant Memory as Federated Memory
    participant GPT as OpenAI API

    User->>API: Upload Document
    API->>Router: Send Document Data
    
    rect rgb(240, 240, 240)
        Note over Router: Complexity Assessment
        Router->>Router: Analyze document type
        Router->>Router: Calculate complexity score
        Router->>Router: Choose processing path
    end

    Router->>Extractor: Route to Simple Path
    Extractor->>GPT: Request data extraction
    GPT-->>Extractor: Return extracted data
    Extractor->>Summarizer: Send extracted data

    Summarizer->>GPT: Request summary generation
    GPT-->>Summarizer: Return generated summary
    Summarizer->>Memory: Store processing results
    Memory-->>API: Confirm storage

    API-->>User: Return final output
```

## Complex Document Processing Flow


```mermaid
sequenceDiagram
    participant User as User
    participant API as FastAPI Server
    participant Router as Router Agent
    participant Orchestrator as Orchestrator Agent
    participant Extractor as Extractor Agent
    participant Analyzer as Analyzer Agent
    participant Validator as Validator Agent
    participant Summarizer as Summarizer Agent
    participant Memory as Federated Memory
    participant GPT as OpenAI API

    User->>API: Upload Complex Document
    API->>Router: Send Document Data
    
    rect rgb(255, 250, 205)
        Note over Router: High Complexity Detected
        Router->>Router: Score complexity > 0.7
        Router->>Orchestrator: Route to complex path
    end

    Orchestrator->>Orchestrator: Create workflow plan
    Orchestrator->>Extractor: Execute extraction step

    Extractor->>GPT: Request deep extraction
    GPT-->>Extractor: Return structured data
    Extractor->>Memory: Store intermediate results
    Extractor->>Analyzer: Pass extracted data

    rect rgb(230, 230, 250)
        Note over Analyzer: Content Analysis Phase
        Analyzer->>Memory: Retrieve relevant memories
        Analyzer->>GPT: Request analysis
        GPT-->>Analyzer: Return analysis results
        Analyzer->>Validator: Pass analysis
    end

    Validator->>GPT: Validate accuracy
    GPT-->>Validator: Return validation score
    Validator->>Summarizer: Pass validated data

    Summarizer->>Memory: Retrieve insights
    Summarizer->>GPT: Generate final summary
    GPT-->>Summarizer: Return comprehensive summary
    Summarizer->>Memory: Store final results

    Memory-->>API: Return complete output
    API-->>User: Send processed document
```
## Single Agent Decision Flow


```mermaid
graph TB
    Start([Receive Task]) --> LoadContext[Load Context & History]
    LoadContext --> BuildPrompt[Build Specialized Prompt]

    BuildPrompt --> AgentType{Agent Type}

    AgentType -->|Extractor| ExtractorPrompt[Extractor Context<br/>- Document structure<br/>- Data fields<br/>- Format requirements]
    AgentType -->|Analyzer| AnalyzerPrompt[Analyzer Context<br/>- Content patterns<br/>- Compliance rules<br/>- Risk indicators]
    AgentType -->|Summarizer| SummarizerPrompt[Summarizer Context<br/>- Key insights<br/>- Audience type<br/>- Summary length]
    AgentType -->|Validator| ValidatorPrompt[Validator Context<br/>- Accuracy metrics<br/>- Consistency checks<br/>- Quality standards]

    ExtractorPrompt --> CallAPI[Call OpenAI API]
    AnalyzerPrompt --> CallAPI
    SummarizerPrompt --> CallAPI
    ValidatorPrompt --> CallAPI

    CallAPI --> ParseResponse[Parse AI Response]
    ParseResponse --> ExtractDecision[Extract Decision/Output]

    ExtractDecision --> ValidateOutput{Validate Output}
    ValidateOutput -->|Valid| StoreMemory[Update Memory]
    ValidateOutput -->|Invalid| Retry[Retry with Context]
    Retry --> CallAPI

    StoreMemory --> ReturnOutput[Return Output]
    ReturnOutput --> End([Task Complete])

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CallAPI fill:#FF6B6B
    style StoreMemory fill:#4ECDC4
```
## Federated Memory System Flow


```mermaid
graph TB
    Start([Agent Decision]) --> Classify[Classify Information]

    Classify --> ExtractFact[Extract Key Facts]
    ExtractFact --> Categorize{Categorize by Type}

    Categorize -->|Structured Data| StructuredPath[Structured Data<br/>- Fields & Values<br/>- Relationships<br/>- Metadata]
    Categorize -->|Insights| InsightsPath[Business Insights<br/>- Patterns<br/>- Anomalies<br/>- Recommendations]
    Categorize -->|Context| ContextPath[Contextual Info<br/>- Document type<br/>- Processing history<br/>- Quality metrics]

    StructuredPath --> IndexAgent[Agent-Specific Indexing]
    InsightsPath --> IndexAgent
    ContextPath --> IndexAgent

    IndexAgent --> BuildPerspectives[Build Memory Perspectives]
    BuildPerspectives --> StoreRedis[Store in Redis]
    StoreRedis --> IndexPostgres[Index in PostgreSQL]

    IndexPostgres --> AgentQuery{Agent Query?}
    AgentQuery -->|Yes| RetrievePerspectives[Retrieve Relevant Perspectives]
    AgentQuery -->|No| Done[Storage Complete]

    RetrievePerspectives --> FilterRelevance[Filter by Relevance]
    FilterRelevance --> RankImportance[Rank by Importance]
    RankImportance --> ReturnMemory[Return Memory]

    ReturnMemory --> EnhanceDecision[Enhance Agent Decision]

    style Start fill:#FFE66D
    style EnhanceDecision fill:#4ECDC4
    style StoreRedis fill:#FF6B6B
```
## Core Class Relationship Diagram



```mermaid
classDiagram
    class BaseAgent {
        #agent_id: str
        #agent_type: str
        #created_at: datetime
        #interaction_chain: list
        +log_interaction(): void
        +process(task_data, context): dict
        +get_audit_trail(): list
    }

    class RouterAgent {
        +complexity_threshold: float
        +document_types: dict
        +assess_complexity(document): float
        +route_document(document): dict
    }

    class OrchestratorAgent {
        -federated_memory: FederatedMemory
        -agents: dict
        +create_workflow_plan(routing_result, document): list
        +execute_workflow(plan, document): dict
        +_compile_final_output(context): dict
    }

    class ExtractorAgent {
        +extract_structured_data(document): dict
        +identify_key_fields(content): list
        +validate_extraction(data): bool
    }

    class AnalyzerAgent {
        +analyze_content(extracted_data): dict
        +detect_compliance_issues(data): list
        +identify_risks(content): list
    }

    class SummarizerAgent {
        +generate_summary(analysis_results): dict
        +extract_key_insights(data): list
        +create_executive_summary(content): str
    }

    class ValidatorAgent {
        +validate_accuracy(output): dict
        +check_consistency(data): bool
        +calculate_quality_score(results): float
    }

    class FederatedMemory {
        -redis_client: Redis
        -perspectives: dict
        +store(fact, metadata, perspectives): void
        +retrieve_for_agent(agent_type, query, limit): list
        +_calculate_relevance(query, fact, agent_type): float
    }

    class FastAPI {
        -router_agent: RouterAgent
        -orchestrator_agent: OrchestratorAgent
        +process_document(document): dict
        +health_check(): dict
        +get_agent_audit(agent_type): dict
    }

    BaseAgent <|-- RouterAgent
    BaseAgent <|-- OrchestratorAgent
    BaseAgent <|-- ExtractorAgent
    BaseAgent <|-- AnalyzerAgent
    BaseAgent <|-- SummarizerAgent
    BaseAgent <|-- ValidatorAgent

    OrchestratorAgent --> FederatedMemory
    OrchestratorAgent --> ExtractorAgent
    OrchestratorAgent --> AnalyzerAgent
    OrchestratorAgent --> SummarizerAgent
    OrchestratorAgent --> ValidatorAgent

    FastAPI --> RouterAgent
    FastAPI --> OrchestratorAgent
```
## Data Flow Architecture




```mermaid
graph LR
    subgraph "Input Sources"
        Upload[File Upload]
        API[API Request]
        Batch[Batch Processing]
    end

    subgraph "Processing Pipeline"
        Router[Router Agent]
        Simple[Simple Workflow]
        Complex[Complex Workflow]
        Memory[Federated Memory]
    end

    subgraph "Output Channels"
        Response[API Response]
        Export[File Export]
        Database[Data Storage]
        Insights[Insight Dashboard]
    end

    Upload --> Router
    API --> Router
    Batch --> Router

    Router --> Simple
    Router --> Complex

    Simple --> Memory
    Complex --> Memory

    Memory --> Response
    Memory --> Export
    Memory --> Database
    Memory --> Insights

    style Upload fill:#E8F5E9
    style API fill:#E3F2FD
    style Response fill:#FFF3E0
    style Insights fill:#F3E5F5
```
