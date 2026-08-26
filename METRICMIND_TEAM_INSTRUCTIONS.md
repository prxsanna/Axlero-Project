# MetricMind — Team Development Instructions

## 1. Project Overview

MetricMind is an AI-powered business analytics and insight system.

The goal of MetricMind is to take business/financial data, understand important business metrics, and allow an AI system to provide meaningful explanations and insights to the user.

The project should not simply display numbers.

The intended flow is:

    Business Data
          ↓
    PostgreSQL Database
          ↓
    Cube.dev Semantic Layer
          ↓
    Business Metrics
          ↓
    FastAPI
          ↓
    LangChain
          ↓
    Llama 3
          ↓
    AI-generated Insights
          ↓
    MetricMind User


## 2. Overall Team Goal

Everyone should understand:

- Their assigned component.
- Why the component is required.
- How the component works.
- How it connects to MetricMind.
- How their work connects to the other team members' work.
- What changes are required to integrate everything.

The objective is not just to write code.

Everyone should be able to explain their implementation during the project demonstration.


## 3. Current Team Responsibilities

| Team Member | Main Responsibility |
|-------------|---------------------|
| Nanditha | LangChain + Llama 3 |
| Trisha | PostgreSQL + Databricks + Online Datasets |
| Sooraj + Amal | Cube.dev Semantic Layer |


# 4. Nanditha — LangChain + Llama 3

## Main Objective

Understand the existing Gemini-based AI implementation and work toward converting the AI layer to:

    LangChain + Llama 3

The goal is to understand how the existing AI system works before modifying it.


## Task 1 — Explain LangChain

Nanditha should understand and be able to explain:

- What LangChain is.
- Why LangChain can be useful for MetricMind.
- What an LLM wrapper is.
- What prompts are.
- What prompt templates are.
- What chains are.
- How LangChain communicates with an LLM.
- How LangChain can fit into the MetricMind backend.

The explanation should be simple enough for the entire team to understand.


## Task 2 — Explain Llama 3

Understand:

- What Llama 3 is.
- Why Llama 3 can be used as the LLM for MetricMind.
- How Llama 3 differs from Gemini in the current implementation.
- How Llama 3 can be accessed.
- Whether the chosen Llama 3 setup is cloud-based or offline/local.


## Task 3 — Cloud vs Offline Llama

Compare:

### Cloud Llama

Advantages:

- Easier setup.
- No need to run the model locally.
- Lower local hardware requirements.

Disadvantages:

- Requires network access.
- May require an API/provider.
- May introduce usage limitations or costs.


### Offline/Local Llama

Advantages:

- Can run locally.
- Greater control over the environment.
- No external API required after setup.

Disadvantages:

- Requires sufficient hardware.
- Can be slower depending on the machine.
- Requires local model setup.

The team should understand which approach is practical for MetricMind.


## Task 4 — Study Existing Gemini Code

Before changing anything:

Find the existing:

    ai_agent.py

Understand:

- How Gemini is initialized.
- How the prompt is created.
- How user input is handled.
- How the database/metric information is passed to the model.
- How the Gemini response is generated.
- How the response is returned to the application.

Do NOT immediately delete the existing Gemini implementation.

First understand the current architecture.


## Task 5 — Convert Gemini → LangChain + Llama 3

The target architecture should be approximately:

    User Input
        ↓
    FastAPI
        ↓
    AI Agent
        ↓
    LangChain
        ↓
    Prompt Template
        ↓
    Llama 3
        ↓
    AI Response
        ↓
    FastAPI
        ↓
    User

The conversion should preserve the existing application's functionality wherever possible.

Avoid unnecessarily rewriting unrelated code.


## Task 6 — Controlled Intent Output

The AI should eventually be able to produce controlled/structured intent output.

For example, instead of returning completely free-form text:

    "The user seems to be asking about profit."

The system should be able to identify an intent in a controlled format.

Example concept:

    {
        "intent": "profit_analysis"
    }

The exact implementation should follow the existing project's architecture.

The important objective is:

    User Question
        ↓
    LLM
        ↓
    Controlled Intent
        ↓
    Appropriate Metric / Backend Logic


## Expected Output

Nanditha should provide:

- Explanation of LangChain.
- Explanation of Llama 3.
- Cloud vs offline comparison.
- Understanding of existing ai_agent.py.
- Gemini → LangChain + Llama 3 implementation/plan.
- Controlled intent output test.
- Required dependency/configuration changes.


# 5. Trisha — PostgreSQL + Databricks + Online Datasets

## Main Objective

Understand the existing PostgreSQL database and determine whether introducing Databricks or another online dataset/database would actually improve MetricMind.


## Task 1 — Understand PostgreSQL

Trisha should understand the current PostgreSQL database.

Specifically:

- Understand the 4 existing tables.
- Understand the purpose of each table.
- Understand the columns in each table.
- Understand the relationships between the tables.
- Understand how the backend currently accesses the database.
- Understand how the current data supports MetricMind.

The goal is to be able to explain the existing database structure to the team.


## Task 2 — Explain Columns and Relationships

For each table, document:

- Table name.
- Purpose.
- Important columns.
- Primary key if applicable.
- Foreign key if applicable.
- Relationship with other tables.
- Why the table is useful to MetricMind.

Do not change the database structure without discussing it with the team.


## Task 3 — Check Databricks Suitability

Investigate whether Databricks is actually useful for MetricMind.

Understand:

- What Databricks provides.
- Whether MetricMind needs its capabilities.
- Whether it would improve the project.
- Whether it would introduce unnecessary complexity.
- Whether it fits the current architecture.

Do not add Databricks simply because it is a popular technology.

The question is:

    Does Databricks provide real value to MetricMind?


## Task 4 — Find Suitable Existing Online Datasets

Search for existing online datasets that could potentially be useful for MetricMind.

The dataset should contain data that is actually relevant to the project's business/financial metrics.

Check:

- What data the dataset contains.
- Whether it has the required columns.
- Whether it supports useful business metrics.
- Whether it can be integrated into the existing project.
- Whether it provides more value than the current database.


# IMPORTANT DATABASE RULE

Changing the database is NOT a small change.

Changing the current database could require changes to:

- Backend code.
- Database connection.
- Queries.
- Models.
- Data processing.
- Semantic layer.
- Testing.
- Configuration.

It could potentially mean that significant parts of the backend work need to be started/reworked again.

Therefore:

## Do NOT recommend replacing the current database unless:

1. The online dataset is clearly useful.
2. It contains the required data for MetricMind.
3. It provides meaningful additional value.
4. The benefits justify the migration effort.
5. The team agrees that the change is worthwhile.

If these conditions are not satisfied:

    KEEP THE CURRENT DATABASE.


## Expected Output

Trisha should provide:

- Explanation of the existing PostgreSQL database.
- Explanation of the 4 tables.
- Columns and relationships.
- Databricks suitability analysis.
- Suitable online dataset investigation.
- Final recommendation.

The recommendation should clearly state:

    KEEP CURRENT DATABASE

or:

    CONSIDER DATABASE/DATASET CHANGE

with reasons.


# 6. Sooraj + Amal — Cube.dev

## Main Objective

Understand Cube.dev and investigate how it can become the semantic layer for MetricMind.

The main idea is:

    PostgreSQL
        ↓
    Cube.dev
        ↓
    Business Metrics
        ↓
    FastAPI / AI System


## Task 1 — Explain Cube.dev

Sooraj and Amal should understand:

- What Cube.dev is.
- What problem Cube.dev solves.
- Why a semantic layer is useful.
- Why MetricMind could benefit from Cube.dev.
- How Cube.dev works with databases.
- How Cube.dev can expose business metrics consistently.

The explanation should be simple enough for the entire team to understand.


## Task 2 — Understand Cube.dev as a Semantic Layer

Understand the purpose of a semantic layer.

Instead of allowing every part of the application to independently calculate:

    Revenue
    Cost
    Profit
    Margin

Cube.dev can define these metrics centrally.

This gives the project a consistent definition of important business metrics.

Conceptually:

    Raw Database Data
            ↓
       Cube.dev
            ↓
    Standardized Metrics
            ↓
    Application / AI


## Task 3 — Learn Cube.dev → PostgreSQL Connection

Understand how Cube.dev connects to the existing PostgreSQL database.

The intended flow is:

    PostgreSQL
         ↓
      Cube.dev
         ↓
    Semantic Models
         ↓
    Queries / Metrics

Before implementing anything, understand how the existing PostgreSQL schema maps to Cube.dev.


## Task 4 — Define Business Metrics

The following metrics should be investigated and defined in Cube.dev:

### Revenue

Understand how Revenue should be calculated using the existing database.


### Cost

Understand how Cost should be calculated.


### Profit

Conceptually:

    Profit = Revenue - Cost


### Margin

Conceptually:

    Margin = Profit / Revenue

The actual implementation must use the correct columns and tables from the existing PostgreSQL database.

Do not invent columns or data that do not exist.


## Task 5 — Plan Replacing the Python Semantic Layer

The project currently has Python-based semantic logic.

Sooraj and Amal should investigate how Cube.dev could replace or reduce the responsibility of that Python semantic layer.

Current concept:

    PostgreSQL
        ↓
    Python Semantic Layer
        ↓
    FastAPI / AI

Possible future concept:

    PostgreSQL
        ↓
    Cube.dev
        ↓
    FastAPI / AI

Do not immediately delete the Python semantic layer.

First:

1. Understand what it currently does.
2. Identify which parts Cube.dev can replace.
3. Identify which parts still need Python.
4. Determine whether the replacement is actually beneficial.
5. Plan the migration.
6. Discuss the plan with the team.


## Task 6 — Cube.dev + FastAPI

Investigate how FastAPI can communicate with Cube.dev.

The intended concept is:

    User Request
        ↓
    FastAPI
        ↓
    Cube.dev
        ↓
    Metric Result
        ↓
    FastAPI
        ↓
    AI / User

Understand:

- How FastAPI would query Cube.dev.
- What information needs to be sent.
- What response Cube.dev returns.
- How the response can be passed to the AI layer.


## Task 7 — Cube.dev + LangChain

Investigate how the Cube.dev metric layer can work with LangChain.

The intended architecture is:

    User Question
          ↓
    LangChain + Llama 3
          ↓
    Identify Required Metric
          ↓
    FastAPI
          ↓
    Cube.dev
          ↓
    PostgreSQL
          ↓
    Metric Result
          ↓
    LangChain / Llama 3
          ↓
    Explanation / Insight

For example:

    User:
    "What is our profit?"

The system should eventually be capable of determining that it needs:

    Profit

Then retrieve the metric through the semantic layer.

The exact implementation will be decided after the team understands the integration.


## Expected Output

Sooraj and Amal should provide:

- Explanation of Cube.dev.
- Explanation of semantic layers.
- Cube.dev → PostgreSQL understanding.
- Revenue definition.
- Cost definition.
- Profit definition.
- Margin definition.
- Existing Python semantic layer analysis.
- Plan for replacing/moving semantic logic to Cube.dev.
- Cube.dev + FastAPI integration plan.
- Cube.dev + LangChain integration plan.


# 7. Overall MetricMind Architecture

The intended architecture should be understood as:

                    USER
                     |
                     v
                  FastAPI
                     |
                     v
              LangChain + Llama 3
                     |
                     | Determine intent /
                     | required metric
                     v
                Cube.dev
              Semantic Layer
                     |
                     v
                PostgreSQL
                     |
                     v
             Metric Calculation
                     |
                     v
                Cube.dev
                     |
                     v
              FastAPI / AI
                     |
                     v
             MetricMind Insight

This is the architecture the team should investigate.

It does NOT mean every component must be implemented immediately.

Each team member should first understand their component and how the components connect.


# 8. Integration Between Team Members

The three workstreams are connected.


## Trisha

Responsible for understanding:

    PostgreSQL
        ↓
    Existing Data

She determines what data actually exists and whether an external dataset/database is useful.


## Sooraj + Amal

Responsible for:

    PostgreSQL
        ↓
    Cube.dev
        ↓
    Revenue / Cost / Profit / Margin

Their work depends on understanding the PostgreSQL tables and columns.


## Nanditha

Responsible for:

    LangChain
        ↓
    Llama 3
        ↓
    Intent / AI reasoning

Her work eventually needs to interact with the metric layer.


## Combined System

The final system should conceptually become:

    PostgreSQL
         ↓
      Cube.dev
         ↓
    Business Metrics
         ↓
       FastAPI
         ↑
         |
    LangChain + Llama 3
         ↑
         |
       User


# 9. Coding Rules

Before modifying existing code:

1. Pull the latest branch.
2. Check the current implementation.
3. Understand the existing code.
4. Identify exactly what needs to change.
5. Make the smallest necessary change.
6. Test the change.
7. Commit only completed work.


# 10. Do Not Rewrite Working Code Unnecessarily

Do NOT:

- Delete working code without understanding it.
- Rewrite the entire backend.
- Replace the database without justification.
- Remove the Python semantic layer immediately.
- Add libraries just because they are available.
- Add technologies that do not provide project value.
- Commit unfinished experiments as final implementation.


# 11. Environment Variables

Never commit:

- API keys.
- Passwords.
- Database credentials.
- Tokens.
- .env files containing secrets.

Use:

    .env

locally.

If configuration needs to be documented, use:

    .env.example

Example:

    LLM_API_KEY=your_key_here
    DATABASE_URL=your_database_url_here

Never put real credentials in the example file.


# 12. Testing

Every completed task must be tested.


## Nanditha

Test:

- Basic LLM request.
- Metric-related question.
- Controlled intent output.
- Invalid/empty input.
- LangChain + Llama 3 connection.


## Trisha

Test/verify:

- PostgreSQL tables.
- Table relationships.
- Required columns.
- Dataset compatibility.
- Databricks suitability.


## Sooraj + Amal

Test/verify:

- Cube.dev connection to PostgreSQL.
- Revenue.
- Cost.
- Profit.
- Margin.
- Metric queries.
- Connection/response flow.


# 13. GitHub Workflow

Everyone should work on their own branch.

Before starting work:

    git status
    git branch
    git pull origin <your-branch-name>

If the repository setup requires switching branches:

    git checkout <your-branch-name>


# 14. Before Committing

Run:

    git status

Check that only the files you intended to change are listed.

Then:

    git diff

Review your changes.


# 15. Add Your Changes

For a specific file:

    git add filename.py

For multiple specific files:

    git add file1.py file2.py

If all your changes are completed and safe:

    git add .

Then check:

    git status


# 16. Commit

Use a meaningful commit message.

Examples:

    git commit -m "Integrate LangChain with Llama 3"

    git commit -m "Document PostgreSQL and dataset evaluation"

    git commit -m "Add Cube.dev metric definitions"

Avoid messages such as:

    update
    changes
    final
    done
    stuff


# 17. Push to GitHub

If your branch is prasanna:

    git push origin prasanna

If your branch is nanditha:

    git push origin nanditha

If your branch is trisha:

    git push origin trisha

If your branch is sooraj:

    git push origin sooraj

If your branch is amal:

    git push origin amal

Always replace the branch name with your actual branch.


# 18. Complete GitHub Workflow

The standard workflow is:

    git status

    git branch

    git pull origin <your-branch-name>

    # Make your changes

    git status

    git diff

    git add .

    git status

    git commit -m "Describe your completed work"

    git push origin <your-branch-name>


# 19. Before Pushing — Checklist

Each team member should confirm:

- [ ] I understand my assigned component.
- [ ] I read the existing code before changing it.
- [ ] I completed my assigned work.
- [ ] I tested my changes.
- [ ] I did not modify unrelated code.
- [ ] I did not commit API keys or passwords.
- [ ] I checked git status.
- [ ] I reviewed my changes.
- [ ] My commit message is meaningful.
- [ ] I pushed to my own branch.
- [ ] I informed the team about what I completed.


# 20. Important Project Rules

## Rule 1 — Working Code Comes First

A simple working implementation is better than an advanced unfinished implementation.


## Rule 2 — Do Not Add Technology Without Purpose

Every technology must answer:

    Why does MetricMind need this?

If there is no clear answer, do not add it.


## Rule 3 — Database Changes Require Justification

Do not replace the current PostgreSQL database unless the new dataset/database clearly improves MetricMind.

Remember:

    Database change
          ↓
    Backend changes
          ↓
    Query changes
          ↓
    Semantic layer changes
          ↓
    Testing again

Therefore, database migration should only happen when it provides real value.


## Rule 4 — Do Not Remove Existing Components Too Early

Before replacing:

    Gemini
    Python Semantic Layer
    PostgreSQL

the team must understand:

- What the existing component does.
- What the replacement provides.
- What functionality may be lost.
- What code needs to change.
- Whether the replacement actually improves MetricMind.


# 21. Final Team Objective

The final MetricMind system should aim toward:

                    USER
                      |
                      v
                   FastAPI
                      |
                      v
             LangChain + Llama 3
                      |
                      v
              Intent / Question
                      |
                      v
                  Cube.dev
               Semantic Layer
                      |
                      v
                 PostgreSQL
                      |
                      v
          Revenue / Cost / Profit
                 / Margin
                      |
                      v
                 FastAPI
                      |
                      v
             LLM Explanation
                      |
                      v
              MetricMind Insight

The exact architecture may change as the team investigates the components.

The important requirement is that every architectural change must have a clear reason.


# 22. Final Responsibility Summary

## Nanditha

    LangChain
        +
    Llama 3
        +
    Existing Gemini ai_agent.py
        +
    Gemini → LangChain + Llama 3
        +
    Controlled Intent Output


## Trisha

    PostgreSQL
        +
    4 Existing Tables
        +
    Columns & Relationships
        +
    Databricks Evaluation
        +
    Online Dataset Investigation
        +
    Final Database Recommendation

Remember:

Only recommend changing the current database if the alternative clearly provides the required data and adds real value.


## Sooraj + Amal

    Cube.dev
        +
    Semantic Layer
        +
    Cube.dev → PostgreSQL
        +
    Revenue
        +
    Cost
        +
    Profit
        +
    Margin
        +
    Python Semantic Layer Replacement Plan
        +
    Cube.dev + FastAPI
        +
    Cube.dev + LangChain


# 23. Final Goal

The goal is for the whole team to understand:

    What am I building?
            ↓
    Why is it needed?
            ↓
    How does it work?
            ↓
    How does it connect to MetricMind?
            ↓
    How does my component connect
    to the other components?

Everyone should be able to explain their component clearly and demonstrate how it contributes to the final MetricMind system.

Build only what is necessary, test everything, and integrate carefully.
