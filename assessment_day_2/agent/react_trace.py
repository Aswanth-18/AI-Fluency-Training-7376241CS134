from agent import agent
from config import banner


QUESTION = (
    "Which is cheaper: buying a Laptop and Monitor with a 10% discount, "
    "or buying a Laptop, Monitor and Keyboard with a 15% discount? "
    "By how much?"
)


if __name__ == "__main__":

    banner("ASSESSMENT DAY 2 - REACT TRACE")

    print("\nQUESTION:")
    print(QUESTION)

    print("\n--- AGENT ACTIONS AND OBSERVATIONS ---")

    answer = agent(
        QUESTION,
        max_steps=8
    )

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(answer)