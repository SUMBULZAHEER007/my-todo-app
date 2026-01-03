# GitHub Branch Management Instructions

## How to Push Each Phase as Separate Branches

1. **Initialize your repository (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit with all phases"
   git remote add origin <your-repository-url>
   ```

2. **Create and push Phase 1 branch:**
   ```bash
   # Create a new branch for Phase 1
   git checkout -b phase-1-crud-database
   
   # Copy Phase_1 files to root (you may want to do this in a separate directory)
   # Or create the branch from the specific phase folder
   git add .
   git commit -m "Phase 1: Basic CRUD and Database functionality"
   git push -u origin phase-1-crud-database
   ```

3. **Create and push Phase 2 branch:**
   ```bash
   # Go back to main branch
   git checkout main
   
   # Create a new branch for Phase 2
   git checkout -b phase-2-ai-summary
   
   # Copy Phase_2 files to root (or work in separate directory)
   # Or create the branch from the specific phase folder
   git add .
   git commit -m "Phase 2: AI Summary functionality added"
   git push -u origin phase-2-ai-summary
   ```

4. **Create and push Phase 3 branch:**
   ```bash
   # Go back to main branch
   git checkout main
   
   # Create a new branch for Phase 3
   git checkout -b phase-3-task-categorization
   
   # Copy Phase_3 files to root (or work in separate directory)
   # Or create the branch from the specific phase folder
   git add .
   git commit -m "Phase 3: Task Categorization with AI"
   git push -u origin phase-3-task-categorization
   ```

5. **Create and push Phase 4 branch (final):**
   ```bash
   # Go back to main branch
   git checkout main
   
   # Create a new branch for Phase 4
   git checkout -b phase-4-complete-solution
   
   # Copy Phase_4 files to root (or work in separate directory)
   # Or create the branch from the specific phase folder
   git add .
   git commit -m "Phase 4: Complete AI-powered Todo App with RAG and Chat"
   git push -u origin phase-4-complete-solution
   ```

## Alternative Method (Recommended):
If you want to keep each phase in its own directory within the same repository:

1. Create the branches as above
2. In each branch, keep only the relevant phase files in the root
3. This way, each branch represents a complete, runnable phase

## For Judges:
- Each branch represents a complete, functional phase of the project
- Judges can checkout each branch to see the progression
- The branches are named to clearly indicate the phase: `phase-1-crud-database`, `phase-2-ai-summary`, `phase-3-task-categorization`, `phase-4-complete-solution`