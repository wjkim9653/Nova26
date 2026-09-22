"""OpenAI Compatible Chat API Client 모듈"""

import os

class OpenAIChatLLM:
    def __init__(self):
        from openai import OpenAI
        self.model = os.getenv("NOVA_MODEL", "gpt-5.6-luna")
        self.client = OpenAI()

    def complete(self, messages, stop=None):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        text = resp.choices[0].message.content or ""
        return self._truncate_at_stop(text, stop)  # stop token이 지정된 경우, 그 토큰에서 문자열을 잘라서 반환 (GPT 5 계열 모델은 호출 인자로 stop 지정을 허용하지 않으므로 호출 후 사후 로직으로 처리)

    @staticmethod
    def _truncate_at_stop(text, stop):
        """response text에서 stop 문자열이 처음 나오는 지점 앞까지만 반환함 (Chat API의 stop 기능 모사)"""
        if not stop:
            return text
        cut_idx = len(text)
        for s in stop:
            idx = text.find(s)  # stop 문자열이 처음 나오는 index
            if idx != -1:  # stop 문자열이 존재하면 cut을 그 index로 갱신
                cut_idx = min(cut_idx, idx)  # 다른 stop 문자열이 먼저 나올 수 있으므로, 가장 먼저 나오는 stop 문자열의 index를 cut_idx로 설정
        return text[:cut_idx]
    