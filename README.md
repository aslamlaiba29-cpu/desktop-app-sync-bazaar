# Sync Bazaar

An interactive, multi-vendor e-commerce platform that allows local vendors to set up virtual stalls, list inventories, and interact directly with consumers. The application streamlines retail pipelines, tracks inventory fluctuations dynamically, and manages real-time transaction ordering with structured automated invoice generation.

---

### Process Model Implementation & Justification

The **Iterative and Incremental Development Model** was implemented for Sync Bazaar. This framework broke down the system's expansive multi-vendor scope into manageable software iterations.

#### Justification

* **System Modularization:** E-commerce systems have distinct core engines (e.g., identity access, inventory control, payment checks). Developing progressively allowed the team to secure base data states before rolling out public-facing storefront interfaces.
* **Continuous Integration Risk Reduction:** Introducing code in mini-milestones prevented late-stage integration bottlenecks. The structural stability of multi-vendor registration routines was validated early, ensuring smooth downstream data piping.
* **Continuous Refactoring and QA:** This cyclic process aligned directly with our goal to progressively eliminate legacy dependencies, introduce custom exception blocks, and expand code testing metrics during active development.

---

### Software Process Improvement (SPI)

Active Software Process Improvement (SPI) guidelines were followed throughout the semester timeline to catch and address workflow bottlenecks.

* **The Problem:** Early code assemblies revealed a high density of processing defects within shared shopping cart calculations and pricing updates across concurrent user sessions.
* **The Process Shift:** The team shifted from a localized verification approach to a structured pipeline strategy. Validation routines were decoupled into isolated pure scripts, and strict structural walkthrough gates were mandated before branch integration.
* **The SPI Metrics:** Defect leakage to the production codebase dropped significantly. The addition of **58 automated test cases** served as our continuous measurement mechanism, providing immediate feedback on engineering quality.

---

### Version Control Implementation

The project relies on **Git** for version control, using a strict **Feature Branch Workflow** to isolate volatile code from stable production assets.

```bash
# Initialize project workspace and commit system baseline
git init
git add .
git commit -m "chore: scaffold base multi-vendor repository structure"

# Construct a protective branch for isolated core integration
git checkout -b feature/vendor-inventory-api
# [Engineer implementation files within /src]
git add src/inventory_manager.py
git commit -m "feat: design database wrapper for parameterized vendor inventory updates"

# Safe integration with the production trunk via manual merge control
git checkout main
git merge feature/vendor-inventory-api --no-ff -m "merge: integrate vendor inventory tracking subsystem"

```

---

### Justification of Lehman’s Laws of Software Evolution

The continuous lifecycle management of the platform directly confirmed two fundamental laws of software dynamics:

1. **The Law of Continuing Change (1st Law):** An e-commerce environment must evolve continuously or become obsolete. Adapting to shifting design objectives—such as shifting from static platform operations to handling variable vendor platform discount variables—forced ongoing changes to core database structures.
2. **The Law of Increasing Complexity (2nd Law):** As a software application evolves, its internal architecture grows more intricate unless active structural maintenance is performed. Introducing multi-tenant cart states naturally increased logic complexity, requiring dedicated code refactoring to keep the system clean and maintainable.

---

### Software Deployment Management

Sync Bazaar uses a multi-tier deployment management approach to cater to both local development needs and target execution environments.

#### 1. Runtime Application Execution

Developers can launch the platform application locally within native Python environments using standard interpreter commands:

```bash
python src/main.py

```

> *Note:* An automated schema checking sequence verifies database state connectivity on initialization, generating data repositories dynamically if no prior backend trace is found.

#### 2. Standalone Binary Packaging (PyInstaller Production Pipeline)

To distribute production-ready client binaries without requiring an underlying Python installation, the application is packaged using PyInstaller configuration routines:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name="SyncBazaarStorefront" src/main.py

```

This compilation routine aggregates core assets, script dependencies, and underlying standard libraries into a single executable located inside the local `/dist` target path.

---

### Source Code Refactoring & Legacy Code Removal

During development, the codebase was heavily refactored to optimize runtime performance and clear out old technical debt:

* **Separation of Concerns (SoC):** Database access logic was extracted out of visual interface elements and moved into dedicated repositories, decoupling UI components from underlying data structures.
* **Elimination of Mock Subsystems:** Early development arrays, hardcoded product tables, and static testing arrays were replaced entirely with dynamic database models.
* **Removal of UI Validation Side-Effects:** Legacy processing logic that directly generated error windows mid-calculation was refactored into modular, testable validation functions.

---

### Unit Testing & Automated Testing Framework

Comprehensive test coverage was built using Python's native standard library `unittest` framework, keeping the system free from heavy external dependencies.

#### Execution Hook

```bash
python -m unittest discover tests/ -v

```

#### Test Suite Metrics & Matrix Summary

| Target Subsystem | Checked Components | Executed Scenarios | Status Flag |
| --- | --- | --- | --- |
| **`test_database.py`** | Multi-vendor isolation tables, catalog queries, transactional state safety | 18 | Fully Functional ✅ |
| **`test_validator.py`** | Numeric boundary inputs, inventory range validation, user email patterns | 28 | Fully Functional ✅ |
| **`test_exceptions.py`** | Exception bubbling layers, fields integrity tracking, recovery states | 12 | Fully Functional ✅ |
| **Complete System Metrics** | **Unified System Processing Engines** | **58 Total Tests** | **100% Passing** |

---

### Exception Handling Concepts

Sync Bazaar implements a specialized **Custom Exception Hierarchy** that provides structured, graceful error recovery instead of relying on generic runtime alerts.

#### Exception Engine Blueprint

```python
# src/exceptions.py
class SyncBazaarError(Exception):
    """Root error exception wrapper for all custom platform issues."""
    pass

class InventoryException(SyncBazaarError):
    """Base exception layer managing product stock operational processing."""
    pass

class InsufficientStockError(InventoryException):
    """Triggered dynamically when a purchase request exceeds available vendor stock levels."""
    def __init__(self, SKU, requested, available):
        self.SKU = SKU
        self.requested = requested
        self.available = available
        super().__init__(f"Stock Shortage for Item [{SKU}]. Requested: {requested}, Available: {available}")

```

#### Code Implementation Sample

```python
# src/inventory_manager.py
def process_stock_deduction(SKU, count_to_deduct):
    current_stock = fetch_current_inventory_level(SKU)
    if count_to_deduct > current_stock:
        raise InsufficientStockError(SKU, count_to_deduct, current_stock)
    update_inventory_record(SKU, current_stock - count_to_deduct)

```

---

### Peer Reviews (Inspections & Walkthroughs)

To maintain clean code standards across the engineering lifecycle, the team implemented a multi-stage review process before any code reached production:

* **Asynchronous Pull Request Inspections:** Merging code into the main branch required approval from another developer. Code was evaluated for SQL injection risks (checking for parameterized inputs), proper separation of concerns, and full unit test coverage.
* **Synchronous Technical Walkthroughs:** At the end of every feature milestone, the team conducted screen-share walkthroughs. Developers traced the execution path of new features step-by-step, helping the entire team understand system dependencies and maintain a consistent UI and logic architecture across all modules.

---

### Team Roles, Contributions, & Learning Outcomes

| Engineering Peer | Designated System Role | Tangible Primary Project Contributions |
| --- | --- | --- |
| **Team Member 1** | Lead Software Architect & Database Engineer | Modeled multi-tenant database schemas, engineered transaction processing layers, built secure SQL interfaces, and created core custom exception classes. |
| **Team Member 2** | Quality Assurance Lead & Systems Analyst | Developed the 58-test automated execution suite, wrote input validators, configured testing environments, and managed code regression gates. |
| **Team Member 3** | Frontend Interface & User Experience Engineer | Developed custom rendering canvas engines, created the responsive dark theme storefront dashboard, and mapped dynamic analytical charts. |

#### Collective Project Learning Outcomes

* **Decoupled Architecture Design:** Gained practical experience implementing clean separation of concerns, seeing firsthand how isolating data layers from the presentation layer makes code easier to test and maintain.
* **Defensive Programming Excellence:** Learned to design resilient error handling systems by using custom exception hierarchies to make system failures predictable and easily traceable.
* **Continuous Integration Reliability:** Realized the value of automated testing pipelines. Running a 58-test validation suite gave the team the confidence to refactor core system engines without worrying about introducing silent regressions.
