"""
ReAct Loop 모듈
Thought / Action을 모델이 생성하며, 코드는 Tool을 실행해 Observation을 반환함
"""
import re
from .tools import TOOLS


# 에이전트가 생성하는 Thought / Action을 파싱하는 정규식
ACTION_RE = re.compile(r"Action:\s*([A-Za-z_]\w*)\s*\[(.*?)\]", re.DOTALL)
# group 1: ([A-Za-z_]\w*) -> tool name
# group 2: (.*?) -> tool parameter (non-greedy match; 최소매칭 -> 첫 번째 ]에서 멈춤)


def build_system_prompt():
    tool_lines = [f"- {name}[input]: {spec['description']}" for name, spec in TOOLS.items()]
    tools_block = "\n".join(tool_lines)
    return (
        "당신은 ReAct 방식으로 동작하는 의료 보조 에이전트입니다. \n"
        "사용자가 질문하면, 먼저 Thought를 생성하고, 필요하면 Action을 실행하여 Observation을 얻은 후, 최종 답변을 생성합니다. \n"
        "사용할 수 있는 Tool은 다음과 같습니다:\n\n"

        f"{tools_block}\n"
        "Finish[answer]: 최종 답변을 반환하고 종료합니다. \n\n"

        "매 단계마다 아래 두 줄만 출력하세요:\n"
        "Thought: 무엇을 왜 하는지에 대한 추론\n"
        "Action: Tool[parameter]\n\n"

        "규칙: 한 번에 Thought 1개 + Action 1개만 출력해야 하며, Observation은 Action이 실제로 실행되는 시스템에서 제공합니다.\n"
        "정보를 다 얻으면 Action: Finish[answer] 로 끝내세요."
    )

def run_react(question, llm, max_steps=8, verbose=True):
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": f"Question: {question}"},
    ]
    for step in range(1, max_steps + 1):
        text = llm.complete(messages, stop=["Observation:"]).strip()  # 모델이 Observation을 환각으로 생성하지 못 하게 끊음. ReAct Loop의 안정적 동작을 위한 트릭이라고 함...
        if verbose:
            print(f"\n[Step {step}]\n{text}")

        matches = list(ACTION_RE.finditer(text))  # Action: Tool[parameter] 형태를 모두 찾아서 matches에 저장. RE.finditer()는 match object iterator를 반환
        if not matches:  # 출력 형식 지켜지지 않았으므로 재요청
            messages.append({"role": "assistant", "content": text})  # Thought + Action 기록을 그대로 assistant message로 추가 -> 다음 step에서 모델이 다시 제대로 Thought + Action을 생성하도록 유도
            messages.append({"role": "user", "content": "형식 오류. 'Action: Tool[parameter]' 형태로 출력하세요."})  # 사용자 메시지: 형식 오류 안내
            continue

        action, arg = matches[-1].group(1), matches[-1].group(2).strip()  # 마지막 Action만 사용 (중간에 여러 Action이 나올 수 있으므로)
        if action == "Finish":  # 최종 답변 생성된 경우
            if verbose:
                print(f"\n=== 최종 답변 ===\n{arg}")
            return arg  # 최종 답변 반환

        if action in TOOLS:  # 정의된 Tool인 경우
            try:
                observation = str(TOOLS[action]["func"](arg))  # Tool 실행
            except Exception as e:
                observation = f"오류: {type(e).__name__}: {e}"
        else:  # 정의되지 않은 Tool인 경우
            observation = f"오류: '{action}'은(는) 정의되지 않은 Tool 호출. 사용 가능한 Tool은 다음과 같음: {', '.join(TOOLS)}"

        if verbose:
            print(f"Observation: {observation}")
        messages.append({"role": "assistant", "content": text})  # Thought + Action 기록을 그대로 assistant message로 추가
        messages.append({"role": "user", "content": f"Observation: {observation}"})  # Observation 기록을 user message로 추가 -> 다음 step에서 모델이 Observation을 참고하여 Thought + Action 생성

    return " 최대 단계 수 초과: 최종 답변 없음. ReAct Loop 종료."