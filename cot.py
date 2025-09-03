# # chain of thought prompting example

# from openai import OpenAI
# import json

# client = OpenAI(
#     api_key="AIzaSyCaOYBSU1HVdM3702BljkRuFXxBApuk68s",
#     base_url="https://generativelanguage.googleapis.com/v1beta/",
# )


# SYSTEM_PROMPTS = """
# You are an expert AI assistant specialized in user queries using chain of thought prompting. You work on START, PLAN and OUTPUT steps.
# You need to first PLAN what needs to be done. The PLAN can multiple steps.
# Once the PLAN is ready, you will START executing the plan step by step.

# Rules:
# - Stricltly follow the output in json format.
# - Only run one step at a time.
# - The sequence of steps should be START(when user gives an input), PLAN (That can be multiple steps) and OUTPUT (Final output displayed to user).

# Output format:
# {"step": "START" | "PLAN" | "OUTPUT",  "content": "string"}

# Example 1:
# START: What is 2+3*5/10?
# PLAN: {
#     "step": "PLAN",
#     "content": "seems like user is interested in Math problem."
# }
# PLAN: {
#     "step": "PLAN",
#     "content": "looking to the problem, we ahould be using the BODMAS rule to solve this."
# }
# PLAN: {
#     "step": "PLAN",
#     "content": "Yes The BODMAS rule is applicable here."
# }
# PLAN: {
#     "step": "PLAN",
#     "content": "first we must multiply 3*5 which is 15."
# }
# PLAN: {
#     "step": "PLAN",
#     "content": "Now the new equation is 2+15/10."
# }
# PLAN: {
#     "step": "PLAN",
#     "content": "Now we must divide 15/10 which is 1.5."
# }
# PLAN: {
#     "step": "PLAN",
#     "content": "Now the new equation is 2+1.5 is finally 3.5 as answer."
# }
# OUTPUT: {
#     "step": "OUTPUT",
#     "content": "The final answer is 3.5."
#     }


# """

# response = client.chat.completions.create(
#     model="gemini-1.5-flash",
#     response_format={"type": "json_object"},
#     messages=[
#         {
#             "role": "system",
#             "content": SYSTEM_PROMPTS,
#         },
#         {
#             "role": "user",
#             "content": "Hey, can you write a js program to add numbers?",
#         }
#     ],
# )

# print(response.choices[0].message.content)


from openai import OpenAI
import json

client = OpenAI(
    api_key="AIzaSyCaOYBSU1HVdM3702BljkRuFXxBApuk68s",
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

SYSTEM_PROMPTS = """
You are an expert AI assistant specialized in user queries using chain of thought prompting. 

Rules:
1. Always begin with START when the user gives input.
2. After START, produce one or more PLAN steps that explain reasoning in small steps.
3. Only after all PLAN steps, give OUTPUT.
4. Never skip START or jump directly to OUTPUT.
5. Each response must be exactly one JSON object in this format:
   {"step": "START" | "PLAN" | "OUTPUT", "content": "..."}
6. If the previous step was START, the next must be PLAN.
7. If the previous step was PLAN, the next must be PLAN or OUTPUT.
"""


def run_step(messages):
    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=messages,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


user_query = input("👉 Enter your query: ")

messages = [
    {"role": "system", "content": SYSTEM_PROMPTS},
    {"role": "user", "content": user_query},
]

prev_step = None

while True:
    step = run_step(messages)
    print(step)

    messages.append({"role": "assistant", "content": json.dumps(step)})
    current = step["step"]

    if current == "START":
        print("🔥 STARTING THE PLAN...")
    elif current == "PLAN":
        print("📝 PLANNING...")
    elif current == "OUTPUT":
        print("✅ FINAL OUTPUT...")
        break
    else:
        print("⚠️ Unexpected step, retrying...")

    prev_step = current
