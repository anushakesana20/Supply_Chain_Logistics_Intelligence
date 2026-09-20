from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --------------------------------------------------
# 1. Load Hugging Face AI Model
# --------------------------------------------------

MODEL_NAME = "google/flan-t5-small"

print("Loading AI model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("AI model loaded successfully.")


# --------------------------------------------------
# 2. Validated Project Information
# --------------------------------------------------

PROJECT_CONTEXT = """
Supply Chain Logistics Intelligence System:

Total Sales: 36,784,735.01
Total Profit: 3,966,902.97
Total Orders: 65,752
Total Customers: 20,652
Total Products: 118
Late Delivery Rate: 54.83%
On-Time Rate: 45.17%

Machine Learning:
Random Forest was used for late-delivery prediction.
Accuracy: 68.73%
Baseline Accuracy: 54.83%

Demand Forecasting:
Selected forecasting baseline: Naive Baseline.
Forecast MAE: 131,973.37
Forecast RMSE: 191,232.60

Inventory limitation:
Actual inventory quantities are not available in the dataset.
Inventory recommendations are demand-based only.

Supplier limitation:
The dataset does not contain a proper supplier field.
Supplier performance cannot be calculated reliably.
"""


# --------------------------------------------------
# 3. GenAI Assistant
# --------------------------------------------------

def ask_assistant(question):

    question_lower = question.lower()

    # ----------------------------------------------
    # Validated answers
    # ----------------------------------------------

    if "late delivery rate" in question_lower:
        return (
            "The late delivery rate is 54.83%. "
            "This means about 55% of the delivery records "
            "were identified as having late-delivery risk."
        )

    if "total sales" in question_lower:
        return (
            "Total sales are ₹36,784,735.01."
        )

    if "total profit" in question_lower:
        return (
            "Total profit is ₹3,966,902.97."
        )

    if "orders" in question_lower:
        return (
            "The dataset contains 65,752 unique orders."
        )

    if "customers" in question_lower:
        return (
            "The dataset contains 20,652 unique customers."
        )

    if "products" in question_lower:
        return (
            "The dataset contains 118 unique products."
        )

    if "accuracy" in question_lower:
        return (
            "The Random Forest late-delivery prediction model "
            "achieved 68.73% accuracy, compared with a "
            "54.83% majority-class baseline."
        )

    if "forecast" in question_lower:
        return (
            "The selected demand forecasting baseline was "
            "the Naive Baseline. Its evaluation MAE was "
            "131,973.37 and RMSE was 191,232.60."
        )

    if "inventory" in question_lower:
        return (
            "Actual inventory quantities are not available "
            "in the dataset. Therefore, inventory recommendations "
            "are based on demand indicators."
        )

    if "supplier" in question_lower:
        return (
            "The dataset does not contain a proper supplier field, "
            "so supplier performance cannot be calculated reliably."
        )

    if "on time" in question_lower or "on-time" in question_lower:
        return (
            "The on-time rate is 45.17%."
        )

    # ----------------------------------------------
    # Use FLAN-T5 for other questions
    # ----------------------------------------------

    prompt = f"""
You are a Supply Chain Analytics Assistant.

Use ONLY the validated information below.
Do not invent numerical values.

{PROJECT_CONTEXT}

Question:
{question}

Give a short, simple business explanation.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=80
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer


# --------------------------------------------------
# 4. Run the Assistant
# --------------------------------------------------

if __name__ == "__main__":

    question = input("Ask a supply-chain question: ")

    answer = ask_assistant(question)

    print("\nAI Assistant:")
    print(answer)