# Sync Bazaar

## Personal Finance Tracker

A standalone Python desktop application for tracking personal income and expenses, setting monthly budgets per category, and visualizing financial health through interactive charts.

---

### Process Model Implementation & Justification

For the development of **Sync Bazaar (Personal Finance Tracker)**, the **Iterative and Incremental Development Model** was implemented.

```
[Requirement Analysis] -> [Design & Architecture] -> [Implementation & Testing] -> [Review & Refine]
   ^                                                                                       |
   └─────────────────────────────── Next Iteration ────────────────────────────────────────┘

```

#### Justification:

* **Feature Isolation:** The project naturally breaks down into isolated modules (Transaction Management, Budgeting, and Dashboards). An incremental approach allowed us to build and fully test the SQLite core before building the Tkinter UI layers.
* **Risk Mitigation:** By building the application in slices, we ensured that the `DatabaseManager` and custom `Exception Hierarchy` were stable before binding them to visual elements, reducing debugging complexity.
* **Constant Refactoring:** It accommodated the requirement to remove legacy debt and continuously add unit tests during development rather than waiting until the final delivery.

---

### Software Process Improvement (SPI)

Yes, SPI was actively practiced throughout the semester project. We implemented a lightweight **Defect Prevention and Quality Tuning** initiative based on the following cycle:

1. **Baseline Metrics:** Initial manual testing revealed high defect densities in user input validation (e.g., negative amounts, invalid date formats).
2. **Process Action Plan:** We shifted from ad-hoc validation within UI views to a dedicated, pure-function validation module (`validator.py`) and established a strict automated testing gate.
3. **Outcome:** Defect leakage to the main branch dropped significantly. The addition of **52 automated unit tests** served as our process appraisal tool, ensuring that regressions were caught instantly.

---

### Version Control Implementation

The project utilizes **Git** for version control with a strict **Feature Branch Workflow**. This prevents unstable code from contaminating production-ready software.

#### Git Workflow Commands & Log Simulation:

```bash
# 1. Initialize repository and commit the baseline structure
git init
git add .
git commit -m "chore: initial project structure setup with base architecture"

# 2. Create a feature branch for core database changes
git checkout -b feature/database-integration
# [Make changes to src/database.py]
git add src/database.py
git commit -m "feat: implement DatabaseManager with parameterized SQLite queries"

# 3. Merge back to main via Pull Request simulation
git checkout main
git merge feature/database-integration --no-ff -m "merge: integrate database management layer"

```

---

### Justification of Lehman’s Laws of Software Evolution

Our project directly validated two fundamental laws formulated by Meir Lehman:

1. **The Law of Continuing Change (1st Law):** An application must undergo continuous modification to remain useful. As features like budget limits were introduced, the database schema and exception handling had to adapt continuously to match changing user expectations.
2. **The Law of Increasing Complexity (2nd Law):** As the software evolves, its complexity increases unless active work is done to reduce it. Introducing UI charts and cross-tab interactions naturally increased structural complexity, which directly forced us to apply refactoring patterns to maintain clarity.

---

### Software Deployment Management

Since **Sync Bazaar** is a standalone Python application, deployment is managed via two distinct strategies outlined in our technical release pipeline:

#### 1. Local Development Execution

Users with an native Python ecosystem environment can deploy directly using:

```bash
python src/main.py

```

> *Note:* The system automatically initializes the schema (`finance_tracker.db`) natively on its first execution thread if missing.

#### 2. Binary Production Packaging (PyInstaller)

To deploy the application to client machines lacking an underlying Python interpreter, the application is compiled into a single executable binary wrapper:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name="SyncBazaar" src/main.py

```

The resulting static asset in the `/dist` directory packages all core assets, script wrappers, and internal standard library components.

---

### Source Code Refactoring & Legacy Code Removal

During the system's evolution, structural components were aggressively refactored to eliminate technical debt and clear out legacy structural flaws:

* **Elimination of Hardcoded Queries:** Legacy inline SQL executions directly written inside visual components (`transaction_view.py`) were extracted completely and decoupled cleanly into specialized repository calls in `database.py`.
* **Purging UI Side-Effects:** Validation routines that originally used interactive popping message boxes directly inside processing loops were refactored into pure functions within `validator.py`.
* **Dead Code & Stubs Erasure:** All obsolete, early-phase mockup dictionaries and mock data lists used prior to actual SQLite integration were removed from the codebase.

---

### Unit Testing & Automated Testing Framework

A rigorous testing regimen was integrated using Python’s standard library framework `unittest`. No external dependencies are needed to validate application health.

#### Execution Hook:

```bash
python -m unittest discover tests/ -v

```

#### Test Suite Metrics & Matrix Summary:

| Module | Tested Capabilities | Total Tests | Status |
| --- | --- | --- | --- |
| **`test_database.py`** | Safe CRUD, entry queries, conditional parameters, budgets, trends | 16 | Pass ✅ |
| **`test_validator.py`** | Numeric boundaries, ISO date validations, category controls, strings | 26 | Pass ✅ |
| **`test_exceptions.py`** | Hierarchical bubbles, fields tracking, context retention | 10 | Pass ✅ |
| **Total Pipeline** | **System Core Components** | **52** | **100% Pass** |

---

### Exception Handling Concepts

The system rejects fragile error checking mechanisms (such as returning arbitrary integer flags like `-1` or generic strings) and instead implements a robust, centralized **Custom Exception Hierarchy**.

#### Applied Code Pattern Example:

```python
# src/exceptions.py
class FinanceTrackerError(Exception):
    """Root Exception for the system."""
    pass

class ValidationError(FinanceTrackerError):
    """Base category for input errors."""
    pass

class InvalidAmountError(ValidationError):
    """Triggered specifically for zero, negative, or poorly parsed amounts."""
    def __init__(self, amount, message="Transaction amount must be positive"):
        self.amount = amount
        super().__init__(f"{message}. Received: {amount}")

```

#### Integration Context inside Business Logic:

```python
# src/validator.py
def validate_amount(amount_raw):
    try:
        val = float(amount_raw)
        if val <= 0:
            raise InvalidAmountError(amount_raw)
        return val
    except ValueError:
        raise InvalidAmountError(amount_raw, "Amount must be a numeric value")

```

---

### Peer Reviews (Inspections & Walkthroughs)

To maintain code quality, we instituted a formal peer review structure prior to merging branch code into production:

* **Formal Pull Request Inspections:** Code additions required an asynchronous review by another team member. The inspection checked code readability, SQL safety (checking for parameterized inputs), and whether corresponding unit tests were included.
* **Technical Walkthroughs:** At the end of every feature sprint, the team conducted a synchronous screen-share walkthrough. Developers walked through their architecture decisions step-by-step, helping catch integration issues early and ensuring the layout logic stayed consistent across all UI tabs.

---

### Team Roles, Contributions, & Learning Outcomes

| Team Member | Assigned Core Role | Primary Quantifiable Contributions |
| --- | --- | --- |
| **Member 1** | Software Architect & Database Lead | Designed SQLite framework schemas, isolated components, built parameterized wrappers inside `database.py`, wrote custom base exceptions. |
| **Member 2** | QA Engineer & Validation Specialist | Wrote the 52-test automated unit suite, engineered standard validator modules, configured runtime inputs validation boundary logic. |
| **Member 3** | Frontend Developer & UX Designer | Created native canvas visual render components, designed the dark navy and teal user interface, mapped analytical dashboards. |

#### Collective Project Learning Outcomes:

* **Architectural Separation:** Gained clear, practical experience implementing a decoupled architecture, seeing firsthand how separating database logic from UI components makes code easier to test and maintain.
* **Defensive Design Proficiency:** Learned how to build robust, predictable error systems by using custom object hierarchies instead of generic catch-all exception blocks.
* **Automated Testing Confidence:** Discovered the power of regression testing. Running a 52-test suite allowed us to modify core infrastructure with complete confidence, knowing any breaking changes would be caught instantly.
