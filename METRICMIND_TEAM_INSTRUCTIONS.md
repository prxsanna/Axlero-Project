# MetricMind — Team Development Instructions

## 1. Project Overview

**MetricMind** is an AI-powered business/analytics assistant designed to take business data and help users understand what is happening in their metrics.

The project should move beyond simply displaying numbers. The goal is to build a system that can:

1. Accept business/metric data.
2. Process and analyze the data.
3. Use an LLM to understand the data and user questions.
4. Generate useful explanations and insights.
5. Eventually provide actionable recommendations based on the available metrics.

### Current Development Direction

The immediate focus is to make the existing AI code more structured and move it toward a **LangChain + Llama 3 based architecture**, while also evaluating whether an external/online database would actually add value to the project.

Do **not** introduce a new technology just because it is available. Every addition should have a clear purpose and should improve the final MetricMind system.

---

# 2. General Instructions for Everyone

Before writing new code:

- Pull the latest `prasanna` branch.
- Read the existing code before changing it.
- Do not unnecessarily rewrite working code.
- Keep your changes related to your assigned task.
- Reuse existing functions where possible.
- Do not commit API keys, passwords, tokens, `.env` files, or other secrets.
- Add comments only where the logic needs explanation.
- Test your code locally before pushing.
- Make sure your code does not break another person's work.
- If you change an existing function, explain the change in your GitHub commit.

### Important

**Do not create duplicate files/functions for the same purpose.**

Before adding a new module, check whether the project already has something that performs the same job.

---

# 3. Nanditha — LangChain + Llama 3

## Main Task

Study and implement the transition from the current Gemini-based AI code toward:

**LangChain + Llama 3**

### Step 1 — Understand the Existing Code

First identify:

- Where Gemini is initialized.
- Where the prompt is created.
- Where the user input is sent to the model.
- Where the model response is received.
- How the response is currently returned to the rest of the application.

Do not immediately delete the Gemini implementation.

Understand the current flow first.

### Step 2 — Learn the Required Concepts

Understand at least:

- What LangChain is.
- What an LLM wrapper is.
- What a prompt template is.
- What a chain is.
- How LangChain sends prompts to an LLM.
- What Llama 3 is.
- How Llama 3 can be accessed in the chosen environment/provider.
- How the model response can be passed back into MetricMind.

### Step 3 — Convert the Existing Gemini Flow

The target architecture should be conceptually similar to:

    User Question
          ↓
    MetricMind Application
          ↓
    Prompt Template
          ↓
    LangChain
          ↓
    Llama 3
          ↓
    Generated Response
          ↓
    MetricMind Output

Keep the interface between the AI layer and the rest of the application simple.

For example, the rest of the project should ideally be able to call one function such as:

    generate_insight(user_input, data)

The internal implementation can then use LangChain + Llama 3.

### Step 4 — Do Not Hard-Code Secrets

Use environment variables.

Example:

    LLM_API_KEY=your_key_here

Never put the real key inside Python code or GitHub.

### Step 5 — Test

Test with:

- A simple general question.
- A question about sample metric data.
- A question requiring an explanation.
- An invalid/empty input.

Document what works and what still needs improvement.

### Expected Output

Nanditha should commit:

- Updated AI/LLM code.
- Required dependency changes.
- `.env.example` if needed.
- A short explanation/documentation of the new LangChain + Llama 3 flow.

---

# 4. Trisha — Database Investigation

## Main Task

Investigate whether changing/adding the database is actually useful for MetricMind.

### Important Decision Rule

**Do NOT change the database simply because an online database is available.**

Changing the database can affect:

- Existing code.
- Data models.
- Connections.
- Queries.
- Configuration.
- Testing.
- Other team members' code.

It may also mean that the project needs to be started/configured again from the beginning in several areas.

Therefore, only recommend a database change if the online database provides a **real benefit to MetricMind**.

### Investigate

Compare the current database/storage approach with a suitable online/cloud database option.

Check:

- Is the current database sufficient?
- Does MetricMind actually need persistent cloud storage?
- Will multiple users need access to the same data?
- Will the AI need a larger/more realistic dataset?
- Does an online database make querying easier?
- Does it improve deployment?
- Does it introduce unnecessary complexity?
- Can the current database support the final demonstration?

### Final Recommendation

Give one of these conclusions:

**A. Keep the current database**

if changing it does not provide meaningful value.

OR

**B. Change to an online database**

only if there is a clear project benefit.

If recommending a change, explain:

1. Why it is needed.
2. What database should be used.
3. What parts of the project need to change.
4. What existing code will be affected.
5. Whether the team needs to restart/reconfigure the project.
6. How the migration should be done safely.

### Expected Output

Trisha should commit a short document such as:

    DATABASE_EVALUATION.md

It should contain:

- Current database.
- Proposed database.
- Advantages.
- Disadvantages.
- Migration impact.
- Final recommendation.

**Do not migrate the actual project database until the team agrees that the change is worthwhile.**

---

# 5. Coding Standard for The Assigned Work

Use a structure similar to:

    project/
    │
    ├── app/
    │   ├── ...
    │
    ├── ai/
    │   ├── ...
    │
    ├── database/
    │   ├── ...
    │
    ├── requirements.txt
    ├── .env.example
    └── README.md

The exact folder structure should follow the existing project. Do not reorganize the entire repository unnecessarily.

### Python

Use clear function names:

    generate_insight()
    load_data()
    analyze_metrics()
    create_prompt()

Avoid unclear names such as:

    abc()
    test1()
    newcode()
    finalfinal.py

---

# 6. How to Continue Existing Code

Before modifying a file:

### 1. Pull latest code

    git checkout prasanna
    git pull origin prasanna

### 2. Check what changed

    git status
    git log --oneline -5

### 3. Open and understand the relevant files

Find the existing implementation first.

### 4. Make the smallest necessary change

Do not modify unrelated code.

### 5. Run the application

Make sure the project still starts.

### 6. Test your assigned functionality

Do not push untested code.

---

# 7. GitHub Commands — GitHub Posting

## If the repository is already initialized

After completing your work:

    git status

    git add .

    git status

    git commit -m "Complete assigned MetricMind tasks"

    git push origin <your-branch-name>

Replace `<your-branch-name>` with your actual branch.

For example:

    git push origin nanditha

or:

    git push origin trisha

---

# 8. Recommended Commit Messages

Use specific commit messages instead of:

    update
    changes
    final
    done

Examples:

    git commit -m "Integrate LangChain with Llama 3"

    git commit -m "Add database evaluation for MetricMind"

    git commit -m "Update AI insight generation"

    git commit -m "Add environment configuration example"

---

# 9. Before Pushing — Checklist

Run:

    git status

Then verify:

- [ ] My assigned task is complete.
- [ ] Code runs without errors.
- [ ] I tested the new functionality.
- [ ] I did not commit API keys or `.env`.
- [ ] I did not modify unrelated files.
- [ ] My commit message explains the change.
- [ ] I pushed to my own branch.
- [ ] I informed the team what I completed.

---

# 10. Important Team Rule

Because the project deadline is close, prioritize:

**Working → Tested → Integrated**

over:

**Complicated → Experimental → Unfinished**

Do not add technologies, databases, frameworks, or features unless they contribute directly to the final MetricMind project.

The objective is to have a **working, explainable, demonstrable MetricMind system**, not just a collection of technologies.

---

# 11. Team Development Goal

By the end of assigned work:

### Nanditha

    Existing Gemini AI flow
            ↓
    LangChain integration
            ↓
    Llama 3 integration
            ↓
    Tested MetricMind response

### Trisha

    Current database
            ↓
    Evaluate online database
            ↓
    Compare benefits/costs
            ↓
    Final recommendation

### Whole Team

    Pull latest code
          ↓
    Complete assigned work
          ↓
    Test
          ↓
    Commit
          ↓
    Push to GitHub
          ↓
    Inform team
          ↓
    Integrate everything into MetricMind

---

# 12. Do Not Forget

If something is unclear, **do not randomly change the architecture**.

First check:

1. Existing implementation.
2. Existing dependencies.
3. Other team members' changes.
4. Whether the proposed change is actually necessary.

Then discuss the change with the team before making a large modification.
