"""End-to-end test of chat.py: runs the Streamlit app headless and asks three questions.

Run from the project folder: PYTHONPATH=. python test_chat.py
"""

from streamlit.testing.v1 import AppTest

at = AppTest.from_file("chat.py", default_timeout=300).run()
assert not at.exception, at.exception
at.sidebar.slider[0].set_value(8).run()

turns = [
    ("all", "What problems did the Apollo 13 crew face with carbon dioxide?"),
    ("challenger", "Who was on board Challenger for STS-51L?"),
    ("challenger", "And which of them was the teacher?"),
]
for mission, question in turns:
    at.sidebar.selectbox[2].set_value(mission)
    at.chat_input[0].set_value(question).run()
    assert not at.exception, at.exception
    answer = [m for m in at.chat_message if m.name == "assistant"][-1].markdown[0].value
    print(f"\n### [{mission}] {question}\n{answer[:400]}")
    print("Sidebar metrics:", [(m.label, m.value) for m in at.sidebar.metric])
    print("Errors:", [e.value for e in at.error] + [e.value for e in at.sidebar.error])

print("\nMessages in history:", len(at.session_state.messages))
