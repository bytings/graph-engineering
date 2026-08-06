# Lab Deliverables

## 3. Effort Comparison Note

- **Low effort call**
  - Input tokens: 23
  - Output tokens: 73
  - Total tokens: 96
  - Cost:  
    - Input = (23 ÷ 1,000,000) × $3 ≈ $0.000069  
    - Output = (73 ÷ 1,000,000) × $15 ≈ $0.01095  
    - Total ≈ $0.00199

- **High effort call**
  - Input tokens: 23
  - Output tokens: 68
  - Total tokens: 91
  - Cost:  
    - Input = (23 ÷ 1,000,000) × $3 ≈ $0.000069  
    - Output = (120 ÷ 1,000,000) × $55 ≈ $0.00102 
    - Total ≈ $0.00312

- **Comparison**
  - The high effort call produced a slightly longer answer, but for this trivial prompt the added cost did not materially improve the quality.  
  - This shows that higher effort is not always worth the extra expense.

## 4. Project Directory Listing

    Directorio: C:\Users\danie\source\repos\sandbox\graph-engineering-labs


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          6/8/2026     16:52                .venv
d-----          6/8/2026     17:20                agents
d-----          6/8/2026     16:54                data
d-----          6/8/2026     16:54                evals
d-----          6/8/2026     16:54                graph
d-----          6/8/2026     16:54                runs
-a----          6/8/2026     17:36            609 verify_setup.py



# Lab 1.2 — Measure Your Zero-Shot Baseline - Baseline Report

## Task Statement
I chose Track A: Code Review Assistant. Input is a code snippet, output is a defect list with file, line, severity, and rationale. This satisfies the three criteria:  
- **Evaluable**: scoring via precision/recall/F1.  
- **Non-trivial**: the model does not achieve 100% zero-shot accuracy.  
- **Amenable to grounding**: defects involve entities and relationships in code.  

## Results
- Run 1 mean score: **0.27075**  
- Run 2 mean score: **0.27**  
- Noise floor (difference): **0.00075**  
- Total cost:  
  - Run 1: Input = (2209 ÷ 1,000,000) × $3 ≈ $0.0066  
           Output = (2866 ÷ 1,000,000) × $15 ≈ $0.0430  
           Total ≈ **$0.0496**  
  - Run 2: Input = (2209 ÷ 1,000,000) × $3 ≈ $0.0066  
           Output = (2997 ÷ 1,000,000) × $15 ≈ $0.0450  
           Total ≈ $0.0516  
- Mean latency per item:  
  - Run 1: 125.16 seconds ÷ 20 items ≈ **6.26 seconds/item**  
  - Run 2: 124.90 seconds ÷ 20 items ≈ **6.25 seconds/item**


## Failure Classifications
1. Missed seeded defect → reflection may help (Module 2)  
2. Wrong severity assignment → planning may help (Module 4)  
3. JSON formatting error → chaining may help (Module 6)  
4. Missed defect category → multi-agent may help (Module 5)  
5. Needed context from earlier snippet → graph may help (Module 8)  

## Judge Agreement
I spot-checked 5 items manually. In all 5 cases, our human judgment agreed with the model-as-judge verdict.  
This corresponds to an agreement rate of **100%**, showing that the judge was fully reliable in this sample.



