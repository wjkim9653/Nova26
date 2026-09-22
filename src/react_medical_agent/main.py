import argparse
from .react import run_react
from .llm import OpenAIChatLLM

DEFAULT_Q = "환자 P002의 체온을 섭씨로 알려줘."

def main():
    parser = argparse.ArgumentParser(description="Simple ReAct Medical Agent")
    parser.add_argument("-q", "--question", default=DEFAULT_Q, help="질문 (기본값: %(default)s)")
    parser.add_argument("--max_steps", type=int, default=8, help="ReAct Loop 최대 반복 횟수 (기본값: %(default)s)")
    args = parser.parse_args()

    llm = OpenAIChatLLM()  # OpenAI Chat LLM 초기화
    print(f"Question: {args.question}\n" + "=" * 50)
    answer = run_react(args.question, llm, max_steps=args.max_steps)
    print("\n" + "=" * 50 + f"\nAnswer: {answer}")


if __name__ == "__main__":
    main()