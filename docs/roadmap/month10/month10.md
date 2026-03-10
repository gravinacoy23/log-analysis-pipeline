# Month 10 — Introduction to TensorFlow

## Primary Goal

Build a simple neural network using TensorFlow. Understand the
fundamentals — not to become a deep learning researcher, but to
understand how neural networks work and how to use them in a pipeline.

---

# Technical Focus

## Neural Network Fundamentals

- What a neuron is
- Layers — input, hidden, output
- Activation functions — ReLU, sigmoid, softmax
- Forward pass — how predictions are made
- Why neural networks can learn non-linear relationships

## Loss Functions

- What a loss function measures
- Binary cross-entropy for binary classification
- Categorical cross-entropy for multiclass
- Mean squared error for regression
- How loss guides training

## Gradients and Backpropagation (Conceptual)

- What a gradient is
- How backpropagation adjusts weights
- Learning rate — too high vs too low
- No need to implement from scratch — understand the concept

## Simple Feedforward Network with TensorFlow

- `tf.keras.Sequential`
- Dense layers
- Compile: optimizer, loss, metrics
- Fit: epochs, batch size, validation split
- Evaluate on test set

## Model Serialization

- Saving a TensorFlow model with `.save()`
- Loading and running inference
- SavedModel format vs H5

---

# ML Objective

Using the same log classification task from Month 8:

**Task: Predict log level (INFO / WARNING / ERROR) from cpu, mem, response_time, service**

Build a feedforward neural network and compare results with logistic
regression from Month 8. The goal is not to beat the classical model —
it is to understand the process.

---

# Project Structure (Additions This Month)

```
log-analysis-pipeline/
│
├── src/
│   └── models/
│       └── neural_net.py         ← new this month
│
├── output/
│   └── models/
│       └── neural_net_v1/        ← SavedModel format
│
├── docs/
│   └── tensorflow_experiment.md  ← new this month
```

---

# Comparison Deliverable

At the end of Month 10 write a documented comparison:

```
docs/model_comparison.md
```

Compare logistic regression (Month 8) vs neural network (Month 10):
- Training time
- Accuracy, precision, recall, F1
- Complexity vs performance tradeoff
- Which would you use in production and why

---

# Portfolio Finalization

Month 10 closes the roadmap. The final week is dedicated to:

- Reviewing the entire codebase
- Cleaning up any technical debt
- Ensuring the README covers the full project
- Ensuring all documentation is current
- Final commit that marks the project as complete

---

# Deliverables

By the end of Month 10 you must have:

- TensorFlow model trained on log data
- Model saved in SavedModel format
- Training process documented
- Comparison with classical ML documented
- Portfolio-ready repository
- Final clean commit

---

# Strategic Outcome

After completing this roadmap you will have:

- A real data pipeline built from scratch
- Experience with the full ML lifecycle
- Cloud deployment skills (AWS)
- A professional Git portfolio
- The foundation to grow into Data Engineering or ML Engineering

The next step after this roadmap is specialization — going deeper into
one of these areas depending on what you enjoy most and where the
opportunities are.
